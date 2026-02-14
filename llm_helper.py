"""
LLM Helper for Sheet-Editor AI Agent
Generates structured JSON commands from natural language requests
"""

import json
import re
import requests
from typing import Dict, List, Optional, Any

class LLMHelper:
    """Interface to LLM API providers (Groq or OpenAI)"""
    
    def __init__(self, api_key: str, provider: str = "groq", model: str = None):
        """
        Initialize LLM helper
        
        Args:
            api_key: API key (Groq or OpenAI)
            provider: "groq" or "openai"
            model: Model name (auto-selected if None)
        """
        self.api_key = api_key
        self.provider = provider
        
        # Auto-select model based on provider
        if model is None:
            model = "openai/gpt-oss-20b" if provider == "groq" else "gpt-4o-mini"
        
        self.model = model
        
        if provider == "groq":
            try:
                from groq import Groq
                self.client = Groq(api_key=api_key)
            except ImportError:
                raise ImportError("Groq SDK not installed. Run: pip install groq")
        elif provider == "openai":
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=api_key)
            except ImportError:
                raise ImportError("OpenAI SDK not installed. Run: pip install openai")
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def _call_api(self, prompt: str, system: str = "") -> str:
        """Make API call to configured provider (Groq or OpenAI)"""
        try:
            # Ensure strings are properly encoded (remove problematic characters)
            prompt = prompt.encode('ascii', 'ignore').decode('ascii')
            system = system.encode('ascii', 'ignore').decode('ascii')
            
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,  # Low temperature for deterministic commands
                max_tokens=1000
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return json.dumps({"error": f"API Error: {str(e)}"})
    
    def generate_command(self, user_request: str, df_context: dict, conversation_history: list = None) -> dict:
        """
        Generate structured command from natural language request
        
        Args:
            user_request: User's natural language instruction
            df_context: DataFrame metadata (columns, shape, preview)
            conversation_history: Recent chat history for context
            
        Returns:
            dict: Structured command or insight response
        """
        system = """You are a data manipulation assistant. Given a user request and DataFrame context,
output a STRUCTURED COMMAND in JSON format.

CRITICAL RULES:
1. Output ONLY valid JSON - no explanations before or after
2. Use action names from the supported list below
3. Include all required parameters
4. Add "reasoning" field explaining the command
5. For INSIGHTS/QUESTIONS (not operations), use action "insight" instead
6. For MULTI-STEP requests, return an ARRAY of commands to execute in sequence

MULTI-STEP HANDLING:
- If user asks for ONE thing: return single command object
- If user asks for MULTIPLE things: return array of command objects
- Execute commands in logical order (e.g., rename before using new name)

COMMAND vs INSIGHT:
- "Remove row 3" -> COMMAND (modifies data)
- "How many rows?" -> INSIGHT (just answers question)
- "Change column A to 7" -> COMMAND (modifies data)
- "What's the sum of revenue?" -> INSIGHT (just answers question)

Supported COMMAND actions:

**Row Operations:**
- delete_row: {"row_index": int} - 1-indexed
- delete_rows: {"row_indices": [int, int, ...]} - 1-indexed
- delete_rows_condition: {"column": str, "operator": str, "value": any}
- keep_rows_condition: {"column": str, "operator": str, "value": any}
- insert_row: {"row_index": int, "values": [...]}
- sort_rows: {"column": str, "ascending": bool}
- remove_duplicates: {"subset_columns": [str] or null}

**Column Operations:**
- delete_column: {"column_name": str}
- rename_column: {"old_name": str, "new_name": str}
- add_constant_column: {"column_name": str, "value": any}
- add_empty_column: {"column_name": str}
- reorder_columns: {"new_order": [str, ...]}
- duplicate_column: {"source": str, "target": str}
- merge_columns: {"columns": [str, ...], "separator": str, "target": str}

**Cell/Value Operations:**
- replace_text: {"column": str, "old_value": str, "new_value": str}
- replace_conditional: {"column": str, "condition": {"operator": str, "value": any}, "new_value": any}
- set_column_value: {"column": str, "value": any}
- fill_na: {"column": str, "value": any}
- trim_whitespace: {"column": str or null}  # null = all columns
- change_case: {"column": str, "case_type": "upper"/"lower"/"title"}
- assign_sequence: {"column": str, "sequence_type": "number"/"uppercase"/"lowercase", "start": int}  # start only for numbers

**Date/Time Operations:**
- reformat_date: {"column": str, "old_format": str, "new_format": str}
- extract_date_part: {"column": str, "part": "year"/"month"/"day", "target_column": str}
- convert_to_datetime: {"column": str}
- calculate_duration: {"start_col": str, "end_col": str, "target_col": str, "unit": "days"/"hours"}

**Numeric Operations:**
- multiply_column: {"column": str, "factor": float}
- add_to_column: {"column": str, "value": float}
- round_column: {"column": str, "decimals": int}
- normalize_column: {"column": str, "method": "minmax"/"zscore"}
- create_ratio: {"numerator_col": str, "denominator_col": str, "target": str}

**Filtering:**
- keep_rows_condition: {"column": str, "operator": str, "value": any}  # Filter to KEEP matching rows
- delete_rows_condition: {"column": str, "operator": str, "value": any} # Filter to REMOVE matching rows
- convert_type: {"column": str, "target_type": "int"/"float"/"str"/"boolean"}

**Aggregation (returns insights, doesn't modify data):**
- group_aggregate: {"group_by": [str...], "agg_column": str, "agg_func": "sum"/"mean"/"count"/"min"/"max"}
- count_by_category: {"column": str}
- unique_counts: {"column": str or null}  # null = all columns
- summary_stats: {"column": str}

Operators: "==", "!=", "<", ">", "<=", ">=", "contains", "startswith", "endswith"

OUTPUT FORMAT for SINGLE COMMAND:
{
  "action": "delete_row",
  "parameters": {"row_index": 3},
  "reasoning": "User requested to remove 3rd row"
}

OUTPUT FORMAT for MULTI-STEP:
[
  {
    "action": "rename_column",
    "parameters": {"old_name": "Col1", "new_name": "Quarter"},
    "reasoning": "Step 1: Rename first column"
  },
  {
    "action": "add_constant_column",
    "parameters": {"column_name": "Value", "value": 8},
    "reasoning": "Step 2: Add new column with value 8"
  }
]

OUTPUT FORMAT for INSIGHTS:
{
  "action": "insight",
  "response": "The DataFrame has 1000 rows and 5 columns",
  "reasoning": "User asked a question about the data"
}

EXAMPLES:
User: "Remove third row"
Output: {"action": "delete_row", "parameters": {"row_index": 3}, "reasoning": "Delete row at index 3"}

User: "How many rows?"
Output: {"action": "insight", "response": "1000 rows", "reasoning": "User asked for row count"}

User: "Rename Col1 to ID and add a Status column with value Active"
Output: [
  {"action": "rename_column", "parameters": {"old_name": "Col1", "new_name": "ID"}, "reasoning": "Rename first column"},
  {"action": "add_constant_column", "parameters": {"column_name": "Status", "value": "Active"}, "reasoning": "Add Status column"}
]

User: "What's the total revenue by country?"
Output: {"action": "group_aggregate", "parameters": {"group_by": ["country"], "agg_column": "revenue", "agg_func": "sum"}, "reasoning": "User wants aggregated revenue by country"}

User: "Change first column values to 7"
Output: {"action": "set_column_value", "parameters": {"column": "<first column name>", "value": 7}, "reasoning": "Set all values in first column to 7"}
"""
        
        # Format conversation history if provided
        history_context = ""
        if conversation_history and len(conversation_history) > 0:
            recent_history = conversation_history[-6:]
            history_lines = []
            for msg in recent_history:
                role = "User" if msg["role"] == "user" else "Assistant"
                content = msg["content"][:150]
                history_lines.append(f"{role}: {content}")
            
            if history_lines:
                history_context = f"""
RECENT CONVERSATION:
{chr(10).join(history_lines)}
"""
        
        prompt = f"""
{history_context}

DATAFRAME CONTEXT:
Columns: {df_context.get('columns', [])}
Shape: {df_context.get('shape', 'unknown')} (rows, columns)
Preview (first 3 rows):
{df_context.get('preview', 'N/A')}

USER REQUEST:
"{user_request}"

Generate the JSON command or insight response:
"""
        
        response = self._call_api(prompt, system)
        
        # Parse JSON response
        try:
            # Clean response (remove markdown if present)
            cleaned = response.strip()
            if cleaned.startswith('```'):
                cleaned = re.sub(r'^```json\s*', '', cleaned)
                cleaned = re.sub(r'^```\s*', '', cleaned)
                cleaned = re.sub(r'\s*```$', '', cleaned)
            
            parsed = json.loads(cleaned)
            
            # Handle different response types:
            # 1. Single command object: {"action": "...", ...}
            # 2. Array of commands: [{"action": "..."}, {"action": "..."}]
            # 3. Nested array (LLM quirk): [[{"action": "..."}]]
            
            if isinstance(parsed, list):
                # If it's an array of commands, return as-is
                if len(parsed) > 0:
                    # Check if it's a nested array (unwrap it)
                    if isinstance(parsed[0], list):
                        return parsed[0]
                    return parsed
                else:
                    return {
                        "action": "error",
                        "error": "LLM returned empty array"
                    }
            
            # Single command object
            return parsed
        except json.JSONDecodeError:
            # Try to extract JSON from response
            try:
                # Try to match array first
                array_match = re.search(r'(\[.*\])', response, re.DOTALL)
                if array_match:
                    parsed = json.loads(array_match.group(1))
                    if isinstance(parsed, list) and len(parsed) > 0:
                        return parsed
                
                # Fall back to object match
                match = re.search(r'(\{.*\})', response, re.DOTALL)
                if match:
                    parsed = json.loads(match.group(1))
                    return parsed
            except:
                pass
            
            return {
                "action": "error",
                "error": "Failed to parse LLM response",
                "raw_response": response
            }
    
    def answer_insight(self, question: str, df_context: dict, df_stats: dict = None) -> str:
        """
        Answer analytical questions about the data
        
        Args:
            question: User's question
            df_context: DataFrame metadata
            df_stats: Optional statistics (describe(), value_counts(), etc.)
            
        Returns:
            str: Natural language answer
        """
        system = """You are a data analyst assistant. Answer questions about DataFrames concisely and accurately.

RULES:
1. Base answers ONLY on provided context and statistics
2. Be concise - 1-2 sentences
3. Include specific numbers when available
4. Don't hallucinate insights not in the data
"""
        
        stats_text = ""
        if df_stats:
            stats_text = f"\n\nSTATISTICS:\n{json.dumps(df_stats, indent=2, default=str)}"
        
        prompt = f"""
DATAFRAME:
Columns: {df_context.get('columns', [])}
Shape: {df_context.get('shape', 'unknown')}
Data types: {df_context.get('dtypes', {})}
{stats_text}

QUESTION: {question}

Answer concisely:
"""
        
        return self._call_api(prompt, system)
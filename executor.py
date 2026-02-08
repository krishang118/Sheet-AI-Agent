"""
Command executor for Sheet-Editor AI Agent
Routes commands to appropriate operation modules
"""

import pandas as pd
from typing import Dict, Any, List, Optional
from operations import row_ops, column_ops, cell_ops, date_ops, numeric_ops, type_ops, aggregation_ops

class ExecutionError(Exception):
    """Custom exception for execution errors"""
    pass

class Executor:
    """Executes structured commands on DataFrames"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize executor with DataFrame
        
        Args:
            df: Initial DataFrame
        """
        self.df = df.copy()
        self.history: List[Dict[str, Any]] = []
        self.df_history: List[pd.DataFrame] = [df.copy()]
        
    def execute(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a command
        
        Args:
            command: Structured command from LLM
            
        Returns:
            dict: Execution result with status and message
        """
        action = command.get("action")
        parameters = command.get("parameters", {})
        reasoning = command.get("reasoning", "")
        
        if not action:
            raise ExecutionError("No action specified in command")
        
        # Handle special actions
        if action == "error":
            return {
                "status": "error",
                "message": command.get("error", "Unknown error"),
                "raw_response": command.get("raw_response", "")
            }
        
        if action == "insight":
            return {
                "status": "insight",
                "response": command.get("response", ""),
                "reasoning": reasoning
            }
        
        # Execute operation
        try:
            # Save current state before execution
            self.df_history.append(self.df.copy())
            
            # Route to appropriate operation
            if action in ["delete_row", "delete_rows", "delete_rows_condition", "keep_rows_condition",
                         "insert_row", "sort_rows", "remove_duplicates"]:
                self.df = self._execute_row_op(action, parameters)
                
            elif action in ["delete_column", "rename_column", "add_constant_column", "add_empty_column",
                           "reorder_columns", "duplicate_column", "merge_columns"]:
                self.df = self._execute_column_op(action, parameters)
                
            elif action in ["replace_text", "replace_conditional", "set_column_value", 
                           "fill_na", "trim_whitespace", "change_case"]:
                self.df = self._execute_cell_op(action, parameters)
                
            elif action in ["reformat_date", "extract_date_part", "convert_to_datetime", "calculate_duration"]:
                self.df = self._execute_date_op(action, parameters)
                
            elif action in ["multiply_column", "add_to_column", "round_column", 
                           "normalize_column", "create_ratio"]:
                self.df = self._execute_numeric_op(action, parameters)
                
            elif action == "convert_type":
                self.df = self._execute_type_op(action, parameters)
            
            elif action in ["group_aggregate", "count_by_category", "unique_counts", "summary_stats"]:
                # Aggregation operations return insights, not DataFrame modifications
                insight_result = self._execute_aggregation_op(action, parameters)
                return {
                    "status": "insight",
                    "response": insight_result.get("response", ""),
                    "reasoning": reasoning,
                    "data": insight_result.get("data", {})
                }
                
            else:
                raise ExecutionError(f"Unsupported action: {action}")
            
            # Log successful execution
            self.history.append({
                "action": action,
                "parameters": parameters,
                "reasoning": reasoning,
                "status": "success"
            })
            
            return {
                "status": "success",
                "message": f"Successfully executed: {action}",
                "action": action,
                "reasoning": reasoning,
                "new_shape": self.df.shape
            }
            
        except Exception as e:
            # Rollback on error
            if len(self.df_history) > 1:
                self.df = self.df_history.pop()
            
            return {
                "status": "error",
                "message": f"Execution failed: {str(e)}",
                "action": action,
                "error_detail": str(e)
            }
    
    def _execute_row_op(self, action: str, params: dict) -> pd.DataFrame:
        """Execute row operation"""
        if action == "delete_row":
            return row_ops.delete_row(self.df, **params)
        elif action == "delete_rows":
            return row_ops.delete_rows(self.df, **params)
        elif action == "delete_rows_condition":
            return row_ops.delete_rows_condition(self.df, **params)
        elif action == "keep_rows_condition":
            return row_ops.keep_rows_condition(self.df, **params)
        elif action == "insert_row":
            return row_ops.insert_row(self.df, **params)
        elif action == "sort_rows":
            return row_ops.sort_rows(self.df, **params)
        elif action == "remove_duplicates":
            return row_ops.remove_duplicates(self.df, **params)
        else:
            raise ExecutionError(f"Unknown row operation: {action}")
    
    def _execute_column_op(self, action: str, params: dict) -> pd.DataFrame:
        """Execute column operation"""
        if action == "delete_column":
            return column_ops.delete_column(self.df, **params)
        elif action == "rename_column":
            return column_ops.rename_column(self.df, **params)
        elif action == "add_constant_column":
            return column_ops.add_constant_column(self.df, **params)
        elif action == "add_empty_column":
            return column_ops.add_empty_column(self.df, **params)
        elif action == "reorder_columns":
            return column_ops.reorder_columns(self.df, **params)
        elif action == "duplicate_column":
            return column_ops.duplicate_column(self.df, **params)
        elif action == "merge_columns":
            return column_ops.merge_columns(self.df, **params)
        else:
            raise ExecutionError(f"Unknown column operation: {action}")
    
    def _execute_cell_op(self, action: str, params: dict) -> pd.DataFrame:
        """Execute cell operation"""
        if action == "replace_text":
            return cell_ops.replace_text(self.df, **params)
        elif action == "replace_conditional":
            return cell_ops.replace_conditional(self.df, **params)
        elif action == "set_column_value":
            return cell_ops.set_column_value(self.df, **params)
        elif action == "fill_na":
            return cell_ops.fill_na(self.df, **params)
        elif action == "trim_whitespace":
            return cell_ops.trim_whitespace(self.df, **params)
        elif action == "change_case":
            return cell_ops.change_case(self.df, **params)
        else:
            raise ExecutionError(f"Unknown cell operation: {action}")
    
    def _execute_date_op(self, action: str, params: dict) -> pd.DataFrame:
        """Execute date operation"""
        if action == "reformat_date":
            return date_ops.reformat_date(self.df, **params)
        elif action == "extract_date_part":
            return date_ops.extract_date_part(self.df, **params)
        elif action == "convert_to_datetime":
            return date_ops.convert_to_datetime(self.df, **params)
        elif action == "calculate_duration":
            return date_ops.calculate_duration(self.df, **params)
        else:
            raise ExecutionError(f"Unknown date operation: {action}")
    
    def _execute_numeric_op(self, action: str, params: dict) -> pd.DataFrame:
        """Execute numeric operation"""
        if action == "multiply_column":
            return numeric_ops.multiply_column(self.df, **params)
        elif action == "add_to_column":
            return numeric_ops.add_to_column(self.df, **params)
        elif action == "round_column":
            return numeric_ops.round_column(self.df, **params)
        elif action == "normalize_column":
            return numeric_ops.normalize_column(self.df, **params)
        elif action == "create_ratio":
            return numeric_ops.create_ratio(self.df, **params)
        else:
            raise ExecutionError(f"Unknown numeric operation: {action}")
    
    def _execute_type_op(self, action: str, params: dict) -> pd.DataFrame:
        """Execute type conversion"""
        return type_ops.convert_type(self.df, **params)
    
    def _execute_aggregation_op(self, action: str, params: dict) -> Dict[str, Any]:
        """Execute aggregation operation (returns insight)"""
        if action == "group_aggregate":
            return aggregation_ops.group_aggregate(self.df, **params)
        elif action == "count_by_category":
            return aggregation_ops.count_by_category(self.df, **params)
        elif action == "unique_counts":
            return aggregation_ops.unique_counts(self.df, **params)
        elif action == "summary_stats":
            return aggregation_ops.summary_stats(self.df, **params)
        else:
            raise ExecutionError(f"Unknown aggregation operation: {action}")
    
    def undo(self) -> bool:
        """
        Undo last operation
        
        Returns:
            bool: True if undo successful
        """
        if len(self.df_history) > 1:
            self.df_history.pop()  # Remove current
            self.df = self.df_history[-1].copy()  # Restore previous
            if len(self.history) > 0:
                self.history.pop()
            return True
        return False
    
    def get_dataframe(self) -> pd.DataFrame:
        """Get current DataFrame"""
        return self.df.copy()
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get execution history"""
        return self.history.copy()

"""
Cell/value operations for Sheet-Editor AI Agent
Category 3: All cell-level value manipulations
"""

import pandas as pd
from typing import Any, Optional, Dict


def replace_text(df: pd.DataFrame, column: str, old_value: str, new_value: str) -> pd.DataFrame:
    """
    Replace text globally in a column
    
    Args:
        df: DataFrame
        column: Column name
        old_value: Value to replace
        new_value: Replacement value
    
    Returns:
        Modified DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    df = df.copy()
    df[column] = df[column].replace(old_value, new_value)
    return df


def replace_conditional(df: pd.DataFrame, column: str, condition: Dict[str, Any], new_value: Any) -> pd.DataFrame:
    """
    Replace values conditionally
    
    Args:
        df: DataFrame
        column: Column name
        condition: {"operator": str, "value": any}
        new_value: Replacement value
    
    Returns:
        Modified DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    operator = condition.get("operator")
    cond_value = condition.get("value")
    
    df = df.copy()
    
    # Create mask
    if operator == "==":
        mask = df[column] == cond_value
    elif operator == "!=":
        mask = df[column] != cond_value
    elif operator == "<":
        mask = df[column] < cond_value
    elif operator == ">":
        mask = df[column] > cond_value
    elif operator == "<=":
        mask = df[column] <= cond_value
    elif operator == ">=":
        mask = df[column] >= cond_value
    else:
        raise ValueError(f"Unsupported operator: {operator}")
    
    # Replace where mask is True
    df.loc[mask, column] = new_value
    return df


def set_column_value(df: pd.DataFrame, column: str, value: Any) -> pd.DataFrame:
    """
    Set all values in a column to a constant
    
    Args:
        df: DataFrame
        column: Column name
        value: Value to set
    
    Returns:
        Modified DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    df = df.copy()
    df[column] = value
    return df


def fill_na(df: pd.DataFrame, column: str, value: Any) -> pd.DataFrame:
    """
    Fill NA/null values in a column
    
    Args:
        df: DataFrame
        column: Column name
        value: Fill value
    
    Returns:
        Modified DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    df = df.copy()
    df[column] = df[column].fillna(value)
    return df


def trim_whitespace(df: pd.DataFrame, column: Optional[str] = None) -> pd.DataFrame:
    """
    Trim whitespace from strings
    
    Args:
        df: DataFrame
        column: Column name (None = all string columns)
    
    Returns:
        Modified DataFrame
    """
    df = df.copy()
    
    if column:
        # Trim specific column
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found")
        
        if df[column].dtype == 'object':
            df[column] = df[column].str.strip()
    else:
        # Trim all object columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()
    
    return df


def change_case(df: pd.DataFrame, column: str, case_type: str) -> pd.DataFrame:
    """
    Change case of text values
    
    Args:
        df: DataFrame
        column: Column name
        case_type: "upper", "lower", or "title"
    
    Returns:
        Modified DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    if case_type not in ["upper", "lower", "title"]:
        raise ValueError(f"Invalid case_type: {case_type}")
    
    df = df.copy()
    
    if case_type == "upper":
        df[column] = df[column].astype(str).str.upper()
    elif case_type == "lower":
        df[column] = df[column].astype(str).str.lower()
    elif case_type == "title":
        df[column] = df[column].astype(str).str.title()
    return df


def assign_sequence(df: pd.DataFrame, column: str, sequence_type: str, start: int = 1) -> pd.DataFrame:
    """
    Assign sequential values to a column
    
    Args:
        df: DataFrame
        column: Column name
        sequence_type: Type of sequence - "number", "uppercase", "lowercase"
        start: Starting value for number sequences (default: 1)
    
    Returns:
        Modified DataFrame
    
    Examples:
        - sequence_type="number", start=1 → 1, 2, 3, 4, ...
        - sequence_type="uppercase" → A, B, C, D, ..., Z, AA, AB, ...
        - sequence_type="lowercase" → a, b, c, d, ..., z, aa, ab, ...
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    if sequence_type not in ["number", "uppercase", "lowercase"]:
        raise ValueError(f"Invalid sequence_type: {sequence_type}. Must be 'number', 'uppercase', or 'lowercase'")
    
    df = df.copy()
    num_rows = len(df)
    
    if sequence_type == "number":
        # Generate numeric sequence
        df[column] = range(start, start + num_rows)
    
    elif sequence_type == "uppercase":
        # Generate uppercase letter sequence (A, B, C, ..., Z, AA, AB, ...)
        def num_to_uppercase(n):
            result = ""
            while n >= 0:
                result = chr(65 + (n % 26)) + result
                n = n // 26 - 1
            return result
        
        df[column] = [num_to_uppercase(i) for i in range(num_rows)]
    
    elif sequence_type == "lowercase":
        # Generate lowercase letter sequence (a, b, c, ..., z, aa, ab, ...)
        def num_to_lowercase(n):
            result = ""
            while n >= 0:
                result = chr(97 + (n % 26)) + result
                n = n // 26 - 1
            return result
        
        df[column] = [num_to_lowercase(i) for i in range(num_rows)]
    
    return df

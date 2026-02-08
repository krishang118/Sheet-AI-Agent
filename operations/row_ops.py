"""
Row operations for Sheet-Editor AI Agent
Category 1: All row-level manipulations
"""

import pandas as pd
from typing import List, Any, Optional

def delete_row(df: pd.DataFrame, row_index: int) -> pd.DataFrame:
    """
    Delete row by index (1-indexed for user interface)
    
    Args:
        df: DataFrame
        row_index: Row number (1-indexed)
    
    Returns:
        Modified DataFrame
    """
    if row_index < 1 or row_index > len(df):
        raise ValueError(f"Row index {row_index} out of range (1-{len(df)})")
    
    # Convert to 0-indexed
    actual_index = row_index - 1
    return df.drop(df.index[actual_index]).reset_index(drop=True)

def delete_rows(df: pd.DataFrame, row_indices: List[int]) -> pd.DataFrame:
    """
    Delete multiple rows by indices (1-indexed)
    
    Args:
        df: DataFrame
        row_indices: List of row numbers (1-indexed)
    
    Returns:
        Modified DataFrame
    """
    # Validate indices
    for idx in row_indices:
        if idx < 1 or idx > len(df):
            raise ValueError(f"Row index {idx} out of range (1-{len(df)})")
    
    # Convert to 0-indexed
    actual_indices = [df.index[i - 1] for i in row_indices]
    return df.drop(actual_indices).reset_index(drop=True)

def delete_rows_condition(df: pd.DataFrame, column: str, operator: str, value: Any) -> pd.DataFrame:
    """
    Delete rows matching a condition
    
    Args:
        df: DataFrame
        column: Column name
        operator: Comparison operator (==, !=, <, >, <=, >=, contains, startswith, endswith)
        value: Comparison value
    
    Returns:
        Modified DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    # Create mask based on operator
    if operator == "==":
        mask = df[column] == value
    elif operator == "!=":
        mask = df[column] != value
    elif operator == "<":
        mask = df[column] < value
    elif operator == ">":
        mask = df[column] > value
    elif operator == "<=":
        mask = df[column] <= value
    elif operator == ">=":
        mask = df[column] >= value
    elif operator == "contains":
        mask = df[column].astype(str).str.contains(str(value), na=False)
    elif operator == "startswith":
        mask = df[column].astype(str).str.startswith(str(value), na=False)
    elif operator == "endswith":
        mask = df[column].astype(str).str.endswith(str(value), na=False)
    else:
        raise ValueError(f"Unsupported operator: {operator}")
    
    # Delete matching rows
    return df[~mask].reset_index(drop=True)

def keep_rows_condition(df: pd.DataFrame, column: str, operator: str, value: Any) -> pd.DataFrame:
    """
    Keep only rows matching a condition (delete others)
    
    Args:
        df: DataFrame
        column: Column name
        operator: Comparison operator
        value: Comparison value
    
    Returns:
        Modified DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    # Create mask (same as delete_rows_condition)
    if operator == "==":
        mask = df[column] == value
    elif operator == "!=":
        mask = df[column] != value
    elif operator == "<":
        mask = df[column] < value
    elif operator == ">":
        mask = df[column] > value
    elif operator == "<=":
        mask = df[column] <= value
    elif operator == ">=":
        mask = df[column] >= value
    elif operator == "contains":
        mask = df[column].astype(str).str.contains(str(value), na=False)
    elif operator == "startswith":
        mask = df[column].astype(str).str.startswith(str(value), na=False)
    elif operator == "endswith":
        mask = df[column].astype(str).str.endswith(str(value), na=False)
    else:
        raise ValueError(f"Unsupported operator: {operator}")
    
    # Keep matching rows
    return df[mask].reset_index(drop=True)

def insert_row(df: pd.DataFrame, row_index: int, values: List[Any]) -> pd.DataFrame:
    """
    Insert new row at specified index
    
    Args:
        df: DataFrame
        row_index: Position to insert (1-indexed)
        values: List of values for each column
    
    Returns:
        Modified DataFrame
    """
    if len(values) != len(df.columns):
        raise ValueError(f"Expected {len(df.columns)} values, got {len(values)}")
    
    if row_index < 1 or row_index > len(df) + 1:
        raise ValueError(f"Row index {row_index} out of range (1-{len(df)+1})")
    
    # Create new row as DataFrame
    new_row = pd.DataFrame([values], columns=df.columns)
    
    # Insert at position (0-indexed)
    actual_index = row_index - 1
    df_before = df.iloc[:actual_index]
    df_after = df.iloc[actual_index:]
    
    return pd.concat([df_before, new_row, df_after], ignore_index=True)

def sort_rows(df: pd.DataFrame, column: str, ascending: bool = True) -> pd.DataFrame:
    """
    Sort rows by column
    
    Args:
        df: DataFrame
        column: Column to sort by
        ascending: Sort direction
    
    Returns:
        Sorted DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    return df.sort_values(by=column, ascending=ascending).reset_index(drop=True)

def remove_duplicates(df: pd.DataFrame, subset_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Remove duplicate rows
    
    Args:
        df: DataFrame
        subset_columns: Columns to check for duplicates (None = all columns)
    
    Returns:
        DataFrame with duplicates removed
    """
    if subset_columns:
        # Validate columns exist
        for col in subset_columns:
            if col not in df.columns:
                raise ValueError(f"Column '{col}' not found")
    
    return df.drop_duplicates(subset=subset_columns, keep='first').reset_index(drop=True)

"""
Column operations for Sheet-Editor AI Agent
Category 2: All column-level manipulations
"""

import pandas as pd
from typing import List, Any

def delete_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Delete a column
    
    Args:
        df: DataFrame
        column_name: Name of column to delete
    
    Returns:
        Modified DataFrame
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found")
    
    return df.drop(columns=[column_name])


def rename_column(df: pd.DataFrame, old_name: str, new_name: str) -> pd.DataFrame:
    """
    Rename a column
    
    Args:
        df: DataFrame
        old_name: Current column name
        new_name: New column name
    
    Returns:
        Modified DataFrame
    """
    if old_name not in df.columns:
        raise ValueError(f"Column '{old_name}' not found")
    
    return df.rename(columns={old_name: new_name})


def add_constant_column(df: pd.DataFrame, column_name: str, value: Any) -> pd.DataFrame:
    """
    Add a new column with constant value
    
    Args:
        df: DataFrame
        column_name: Name of new column
        value: Constant value for all rows
    
    Returns:
        Modified DataFrame
    """
    if column_name in df.columns:
        raise ValueError(f"Column '{column_name}' already exists")
    
    df = df.copy()
    df[column_name] = value
    return df


def add_empty_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Add a new empty column (NA values)
    
    Args:
        df: DataFrame
        column_name: Name of new column
    
    Returns:
        Modified DataFrame
    """
    if column_name in df.columns:
        raise ValueError(f"Column '{column_name}' already exists")
    
    df = df.copy()
    df[column_name] = pd.NA
    return df


def reorder_columns(df: pd.DataFrame, new_order: List[str]) -> pd.DataFrame:
    """
    Reorder columns
    
    Args:
        df: DataFrame
        new_order: List of column names in desired order
    
    Returns:
        Reordered DataFrame
    """
    # Validate all columns exist
    for col in new_order:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found")
    
    # Check if all columns are included
    if set(new_order) != set(df.columns):
        missing = set(df.columns) - set(new_order)
        raise ValueError(f"Missing columns in new order: {missing}")
    
    return df[new_order]


def duplicate_column(df: pd.DataFrame, source: str, target: str) -> pd.DataFrame:
    """
    Duplicate a column
    
    Args:
        df: DataFrame
        source: Source column to copy
        target: Name of new column
    
    Returns:
        Modified DataFrame
    """
    if source not in df.columns:
        raise ValueError(f"Source column '{source}' not found")
    
    if target in df.columns:
        raise ValueError(f"Target column '{target}' already exists")
    
    df = df.copy()
    df[target] = df[source]
    return df


def merge_columns(df: pd.DataFrame, columns: List[str], separator: str, target: str) -> pd.DataFrame:
    """
    Merge multiple columns into one
    
    Args:
        df: DataFrame
        columns: List of columns to merge
        separator: Separator string
        target: Name of new merged column
    
    Returns:
        Modified DataFrame
    """
    # Validate columns
    for col in columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found")
    
    if target in df.columns:
        raise ValueError(f"Target column '{target}' already exists")
    
    df = df.copy()
    # Convert to string and merge
    df[target] = df[columns].astype(str).agg(separator.join, axis=1)
    return df

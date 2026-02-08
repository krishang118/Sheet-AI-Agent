"""
Numeric transformation operations for Sheet-Editor AI Agent
Category 5: Numeric manipulations and calculations
"""

import pandas as pd

def multiply_column(df: pd.DataFrame, column: str, factor: float) -> pd.DataFrame:
    """
    Multiply column by a factor
    
    Args:
        df: DataFrame
        column: Column name
        factor: Multiplication factor
    
    Returns:
        Modified DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    df = df.copy()
    df[column] = pd.to_numeric(df[column], errors='coerce') * factor
    return df

def add_to_column(df: pd.DataFrame, column: str, value: float) -> pd.DataFrame:
    """
    Add constant to column
    
    Args:
        df: DataFrame
        column: Column name
        value: Value to add
    
    Returns:
        Modified DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    df = df.copy()
    df[column] = pd.to_numeric(df[column], errors='coerce') + value
    return df


def round_column(df: pd.DataFrame, column: str, decimals: int) -> pd.DataFrame:
    """
    Round values in column
    
    Args:
        df: DataFrame
        column: Column name
        decimals: Number of decimal places
    
    Returns:
        Modified DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    df = df.copy()
    df[column] = pd.to_numeric(df[column], errors='coerce').round(decimals)
    return df


def normalize_column(df: pd.DataFrame, column: str, method: str = "minmax") -> pd.DataFrame:
    """
    Normalize column values
    
    Args:
        df: DataFrame
        column: Column name
        method: "minmax" (0-1) or "zscore" (standardize)
    
    Returns:
        Modified DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    if method not in ["minmax", "zscore"]:
        raise ValueError(f"Invalid method: {method}")
    
    df = df.copy()
    values = pd.to_numeric(df[column], errors='coerce')
    
    if method == "minmax":
        # Scale to [0, 1]
        min_val = values.min()
        max_val = values.max()
        if max_val > min_val:
            df[column] = (values - min_val) / (max_val - min_val)
        else:
            df[column] = 0
    elif method == "zscore":
        # Standardize (mean=0, std=1)
        mean_val = values.mean()
        std_val = values.std()
        if std_val > 0:
            df[column] = (values - mean_val) / std_val
        else:
            df[column] = 0
    
    return df

def create_ratio(df: pd.DataFrame, numerator_col: str, denominator_col: str, target: str) -> pd.DataFrame:
    """
    Create ratio column from two columns
    
    Args:
        df: DataFrame
        numerator_col: Numerator column
        denominator_col: Denominator column
        target: Name of new ratio column
    
    Returns:
        Modified DataFrame
    """
    if numerator_col not in df.columns:
        raise ValueError(f"Column '{numerator_col}' not found")
    if denominator_col not in df.columns:
        raise ValueError(f"Column '{denominator_col}' not found")
    
    df = df.copy()
    numerator = pd.to_numeric(df[numerator_col], errors='coerce')
    denominator = pd.to_numeric(df[denominator_col], errors='coerce')
    
    # Avoid division by zero
    df[target] = numerator / denominator.replace(0, pd.NA)
    return df

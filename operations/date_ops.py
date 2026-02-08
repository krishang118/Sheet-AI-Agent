"""
Date/time operations for Sheet-Editor AI Agent
Category 4: Date and time manipulations
"""

import pandas as pd
from typing import Optional

def reformat_date(df: pd.DataFrame, column: str, old_format: str, new_format: str) -> pd.DataFrame:
    """
    Reformat date column
    
    Args:
        df: DataFrame
        column: Column name
        old_format: Current format (e.g., "%d-%m-%Y")
        new_format: Target format (e.g., "%m/%d/%Y")
    
    Returns:
        Modified DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    df = df.copy()
    # Parse with old format then format to new format
    df[column] = pd.to_datetime(df[column], format=old_format).dt.strftime(new_format)
    return df


def extract_date_part(df: pd.DataFrame, column: str, part: str, target_column: str) -> pd.DataFrame:
    """
    Extract part of date (year/month/day)
    
    Args:
        df: DataFrame
        column: Source column
        part: "year", "month", or "day"
        target_column: Name of new column
    
    Returns:
        Modified DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    if part not in ["year", "month", "day"]:
        raise ValueError(f"Invalid part: {part}")
    
    df = df.copy()
    # Convert to datetime first
    dt = pd.to_datetime(df[column])
    
    if part == "year":
        df[target_column] = dt.dt.year
    elif part == "month":
        df[target_column] = dt.dt.month
    elif part == "day":
        df[target_column] = dt.dt.day
    
    return df


def convert_to_datetime(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Convert column to datetime type
    
    Args:
        df: DataFrame
        column: Column name
    
    Returns:
        Modified DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    df = df.copy()
    df[column] = pd.to_datetime(df[column], errors='coerce')
    return df


def calculate_duration(df: pd.DataFrame, start_col: str, end_col: str, 
                       target_col: str, unit: str = "days") -> pd.DataFrame:
    """
    Calculate duration between two date columns
    
    Args:
        df: DataFrame
        start_col: Start date column
        end_col: End date column
        target_col: Name of new column for duration
        unit: "days" or "hours"
    
    Returns:
        Modified DataFrame
    """
    if start_col not in df.columns:
        raise ValueError(f"Column '{start_col}' not found")
    if end_col not in df.columns:
        raise ValueError(f"Column '{end_col}' not found")
    
    df = df.copy()
    start = pd.to_datetime(df[start_col])
    end = pd.to_datetime(df[end_col])
    
    if unit == "days":
        df[target_col] = (end - start).dt.days
    elif unit == "hours":
        df[target_col] = (end - start).dt.total_seconds() / 3600
    else:
        raise ValueError(f"Unsupported unit: {unit}")
    
    return df

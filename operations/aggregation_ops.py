"""
Aggregation operations for Sheet-Editor AI Agent
Category 8: Aggregation and summary (returns insights, not modifications)
"""

import pandas as pd
from typing import List, Optional, Dict, Any


def group_aggregate(df: pd.DataFrame, group_by: List[str], agg_column: str, 
                   agg_func: str) -> Dict[str, Any]:
    """
    Group by columns and aggregate (returns insight, doesn't modify DataFrame)
    
    Args:
        df: DataFrame
        group_by: Columns to group by
        agg_column: Column to aggregate
        agg_func: Aggregation function ("sum", "mean", "count", "min", "max")
    
    Returns:
        Dict with insight response
    """
    # Validate columns
    for col in group_by:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found")
    
    if agg_column not in df.columns:
        raise ValueError(f"Column '{agg_column}' not found")
    
    # Validate function
    valid_funcs = ["sum", "mean", "count", "min", "max"]
    if agg_func not in valid_funcs:
        raise ValueError(f"Invalid function: {agg_func}. Use: {valid_funcs}")
    
    # Perform aggregation
    if agg_func == "sum":
        result = df.groupby(group_by)[agg_column].sum()
    elif agg_func == "mean":
        result = df.groupby(group_by)[agg_column].mean()
    elif agg_func == "count":
        result = df.groupby(group_by)[agg_column].count()
    elif agg_func == "min":
        result = df.groupby(group_by)[agg_column].min()
    elif agg_func == "max":
        result = df.groupby(group_by)[agg_column].max()
    
    # Format result as insight
    result_str = result.to_string()
    group_by_str = ", ".join(group_by)
    
    response = f"**{agg_func.capitalize()} of {agg_column} by {group_by_str}:**\n\n```\n{result_str}\n```"
    
    return {
        "action": "insight",
        "response": response,
        "data": result.to_dict()
    }


def count_by_category(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """
    Count occurrences per category (returns insight)
    
    Args:
        df: DataFrame
        column: Column to count
    
    Returns:
        Dict with insight response
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    # Get value counts
    counts = df[column].value_counts()
    
    # Format result
    result_str = counts.to_string()
    
    response = f"**Count by {column}:**\n\n```\n{result_str}\n```\n\nTotal: {len(df)} rows"
    
    return {
        "action": "insight",
        "response": response,
        "data": counts.to_dict()
    }


def unique_counts(df: pd.DataFrame, column: Optional[str] = None) -> Dict[str, Any]:
    """
    Count unique values (returns insight)
    
    Args:
        df: DataFrame
        column: Column name (None = all columns)
    
    Returns:
        Dict with insight response
    """
    if column:
        # Specific column
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found")
        
        unique_count = df[column].nunique()
        total_count = len(df[column])
        
        response = f"**Unique values in {column}:**\n- Unique: {unique_count}\n- Total: {total_count}\n- Percentage: {unique_count/total_count*100:.1f}%"
    else:
        # All columns
        unique_counts_dict = df.nunique().to_dict()
        result_str = "\n".join([f"- {col}: {count}" for col, count in unique_counts_dict.items()])
        
        response = f"**Unique values per column:**\n\n{result_str}"
    
    return {
        "action": "insight",
        "response": response
    }


def summary_stats(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """
    Get summary statistics for a column (returns insight)
    
    Args:
        df: DataFrame
        column: Column name
    
    Returns:
        Dict with insight response
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    # Get statistics
    col_data = pd.to_numeric(df[column], errors='coerce')
    
    stats = {
        "Count": col_data.count(),
        "Mean": col_data.mean(),
        "Median": col_data.median(),
        "Std Dev": col_data.std(),
        "Min": col_data.min(),
        "Max": col_data.max(),
        "25%": col_data.quantile(0.25),
        "75%": col_data.quantile(0.75)
    }
    
    # Format result
    result_str = "\n".join([f"- {k}: {v:.2f}" if isinstance(v, float) else f"- {k}: {v}" 
                           for k, v in stats.items()])
    
    response = f"**Summary statistics for {column}:**\n\n{result_str}"
    return {
        "action": "insight",
        "response": response,
        "data": stats
    }

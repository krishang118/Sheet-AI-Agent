"""
Type conversion operations for Sheet-Editor AI Agent
Category 7: Type casting and conversions
"""

import pandas as pd
def convert_type(df: pd.DataFrame, column: str, target_type: str) -> pd.DataFrame:
    """
    Convert column to different type
    
    Args:
        df: DataFrame
        column: Column name
        target_type: "int", "float", "str", "boolean"
    
    Returns:
        Modified DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    if target_type not in ["int", "float", "str", "boolean"]:
        raise ValueError(f"Invalid target_type: {target_type}")
    
    df = df.copy()
    
    if target_type == "int":
        df[column] = pd.to_numeric(df[column], errors='coerce').astype('Int64')  # Nullable int
    elif target_type == "float":
        df[column] = pd.to_numeric(df[column], errors='coerce')
    elif target_type == "str":
        df[column] = df[column].astype(str)
    elif target_type == "boolean":
        # Convert to boolean (0/False, 1/True)
        df[column] = df[column].astype(bool)
    
    return df

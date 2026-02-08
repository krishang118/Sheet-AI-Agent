"""
Manual Test Runner - Categories 1-7
Runs basic tests without pytest
"""

import pandas as pd
import sys
from operations import row_ops, column_ops, cell_ops, date_ops, numeric_ops, type_ops

def test_category_1():
    """Category 1: Row Operations"""
    print("=" * 60)
    print("CATEGORY 1: ROW OPERATIONS")
    print("=" * 60)
    
    df = pd.DataFrame({
        'ID': [1, 2, 3, 4, 5],
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Revenue': [100, 200, -50, 300, 150]
    })
    
    # Test 1: Delete row
    try:
        result = row_ops.delete_row(df.copy(), 3)
        assert len(result) == 4, "delete_row failed"
        print("[PASS] delete_row - PASSED")
    except Exception as e:
        print(f"[FAIL] delete_row - FAILED: {e}")
    
    # Test 2: Delete multiple rows
    try:
        result = row_ops.delete_rows(df.copy(), [1, 3, 5])
        assert len(result) == 2, "delete_rows failed"
        print("[PASS] delete_rows - PASSED")
    except Exception as e:
        print(f"[FAIL] delete_rows - FAILED: {e}")
    
    # Test 3: Delete rows by condition
    try:
        result = row_ops.delete_rows_condition(df.copy(), 'Revenue', '<', 0)
        assert len(result) == 4, "delete_rows_condition failed"
        print("[PASS] delete_rows_condition - PASSED")
    except Exception as e:
        print(f"[FAIL] delete_rows_condition - FAILED: {e}")
    
    # Test 4: Keep rows condition
    try:
        result = row_ops.keep_rows_condition(df.copy(), 'Revenue', '>', 100)
        assert len(result) == 3, "keep_rows_condition failed"
        print("[PASS] keep_rows_condition - PASSED")
    except Exception as e:
        print(f"[FAIL] keep_rows_condition - FAILED: {e}")
    
    # Test 5: Insert row
    try:
        result = row_ops.insert_row(df.copy(), 2, [6, 'Frank', 250])
        assert len(result) == 6, "insert_row failed"
        print("[PASS] insert_row - PASSED")
    except Exception as e:
        print(f"[FAIL] insert_row - FAILED: {e}")
    
    # Test 6: Sort rows
    try:
        result = row_ops.sort_rows(df.copy(), 'Revenue', ascending=True)
        assert list(result['Revenue'].values) == [-50, 100, 150, 200, 300], "sort_rows failed"
        print("[PASS] sort_rows - PASSED")
    except Exception as e:
        print(f"[FAIL] sort_rows - FAILED: {e}")
    
    # Test 7: Remove duplicates
    try:
        df_dup = pd.DataFrame({'A': [1, 2, 2, 3], 'B': [4, 5, 5, 6]})
        result = row_ops.remove_duplicates(df_dup)
        assert len(result) == 3, "remove_duplicates failed"
        print("[PASS] remove_duplicates - PASSED")
    except Exception as e:
        print(f"[FAIL] remove_duplicates - FAILED: {e}")
    
    print()


def test_category_2():
    """Category 2: Column Operations"""
    print("=" * 60)
    print("CATEGORY 2: COLUMN OPERATIONS")
    print("=" * 60)
    
    df = pd.DataFrame({
        'First': [1, 2, 3],
        'Second': [4, 5, 6],
        'Third': [7, 8, 9]
    })
    
    # Test 1: Delete column
    try:
        result = column_ops.delete_column(df.copy(), 'Second')
        assert 'Second' not in result.columns, "delete_column failed"
        print("[PASS] delete_column - PASSED")
    except Exception as e:
        print(f"[FAIL] delete_column - FAILED: {e}")
    
    # Test 2: Rename column
    try:
        result = column_ops.rename_column(df.copy(), 'First', 'FirstColumn')
        assert 'FirstColumn' in result.columns, "rename_column failed"
        print("[PASS] rename_column - PASSED")
    except Exception as e:
        print(f"[FAIL] rename_column - FAILED: {e}")
    
    # Test 3: Add constant column
    try:
        result = column_ops.add_constant_column(df.copy(), 'Status', 'Active')
        assert all(result['Status'] == 'Active'), "add_constant_column failed"
        print("[PASS] add_constant_column - PASSED")
    except Exception as e:
        print(f"[FAIL] add_constant_column - FAILED: {e}")
    
    # Test 4: Add empty column
    try:
        result = column_ops.add_empty_column(df.copy(), 'Notes')
        assert 'Notes' in result.columns, "add_empty_column failed"
        print("[PASS] add_empty_column - PASSED")
    except Exception as e:
        print(f"[FAIL] add_empty_column - FAILED: {e}")
    
    # Test 5: Reorder columns
    try:
        result = column_ops.reorder_columns(df.copy(), ['Third', 'First', 'Second'])
        assert list(result.columns) == ['Third', 'First', 'Second'], "reorder_columns failed"
        print("[PASS] reorder_columns - PASSED")
    except Exception as e:
        print(f"[FAIL] reorder_columns - FAILED: {e}")
    
    # Test 6: Duplicate column
    try:
        result = column_ops.duplicate_column(df.copy(), 'First', 'FirstCopy')
        assert 'FirstCopy' in result.columns, "duplicate_column failed"
        print("[PASS] duplicate_column - PASSED")
    except Exception as e:
        print(f"[FAIL] duplicate_column - FAILED: {e}")
    
    # Test 7: Merge columns
    try:
        df_names = pd.DataFrame({
            'FirstName': ['John', 'Jane'],
            'LastName': ['Doe', 'Smith']
        })
        result = column_ops.merge_columns(df_names, ['FirstName', 'LastName'], ' ', 'FullName')
        assert result.iloc[0]['FullName'] == 'John Doe', "merge_columns failed"
        print("[PASS] merge_columns - PASSED")
    except Exception as e:
        print(f"[FAIL] merge_columns - FAILED: {e}")
    
    print()


def test_category_3():
    """Category 3: Cell/Value Operations"""
    print("=" * 60)
    print("CATEGORY 3: CELL/VALUE OPERATIONS")
    print("=" * 60)
    
    # Test 1: Replace text
    try:
        df = pd.DataFrame({'Col': ['A', 'B', 'A', 'C']})
        result = cell_ops.replace_text(df, 'Col', 'A', 'X')
        assert list(result['Col']) == ['X', 'B', 'X', 'C'], "replace_text failed"
        print("[PASS] replace_text - PASSED")
    except Exception as e:
        print(f"[FAIL] replace_text - FAILED: {e}")
    
    # Test 2: Replace conditional
    try:
        df = pd.DataFrame({'Value': [0, 10, 20]})
        result = cell_ops.replace_conditional(df, 'Value', {'operator': '==', 'value': 0}, 999)
        assert result.iloc[0]['Value'] == 999, "replace_conditional failed"
        print("[PASS] replace_conditional - PASSED")
    except Exception as e:
        print(f"[FAIL] replace_conditional - FAILED: {e}")
    
    # Test 3: Set column value
    try:
        df = pd.DataFrame({'Value': [1, 2, 3]})
        result = cell_ops.set_column_value(df, 'Value', 42)
        assert all(result['Value'] == 42), "set_column_value failed"
        print("[PASS] set_column_value - PASSED")
    except Exception as e:
        print(f"[FAIL] set_column_value - FAILED: {e}")
    
    # Test 4: Fill NA
    try:
        df = pd.DataFrame({'Value': [10, None, 30]})
        result = cell_ops.fill_na(df, 'Value', 0)
        assert not result['Value'].isna().any(), "fill_na failed"
        print("[PASS] fill_na - PASSED")
    except Exception as e:
        print(f"[FAIL] fill_na - FAILED: {e}")
    
    # Test 5: Trim whitespace
    try:
        df = pd.DataFrame({'Name': ['  Alice  ', 'Bob', 'Charlie']})
        result = cell_ops.trim_whitespace(df, 'Name')
        assert result.iloc[0]['Name'] == 'Alice', "trim_whitespace failed"
        print("[PASS] trim_whitespace - PASSED")
    except Exception as e:
        print(f"[FAIL] trim_whitespace - FAILED: {e}")
    
    # Test 6: Change case
    try:
        df = pd.DataFrame({'Name': ['alice', 'bob']})
        result = cell_ops.change_case(df, 'Name', 'upper')
        assert all(result['Name'].str.isupper()), "change_case failed"
        print("[PASS] change_case - PASSED")
    except Exception as e:
        print(f"[FAIL] change_case - FAILED: {e}")
    
    print()


def test_category_4():
    """Category 4: Date/Time Operations"""
    print("=" * 60)
    print("CATEGORY 4: DATE/TIME OPERATIONS")
    print("=" * 60)
    
    # Test 1: Reformat date
    try:
        df = pd.DataFrame({'Date': ['15-01-2023', '20-02-2023']})
        result = date_ops.reformat_date(df, 'Date', '%d-%m-%Y', '%m/%d/%Y')
        assert result.iloc[0]['Date'] == '01/15/2023', "reformat_date failed"
        print("[PASS] reformat_date - PASSED")
    except Exception as e:
        print(f"[FAIL] reformat_date - FAILED: {e}")
    
    # Test 2: Extract date part
    try:
        df = pd.DataFrame({'Date': ['2023-01-15', '2024-02-20']})
        result = date_ops.extract_date_part(df, 'Date', 'year', 'Year')
        assert result.iloc[0]['Year'] == 2023, "extract_date_part failed"
        print("[PASS] extract_date_part - PASSED")
    except Exception as e:
        print(f"[FAIL] extract_date_part - FAILED: {e}")
    
    # Test 3: Convert to datetime
    try:
        df = pd.DataFrame({'Date': ['2023-01-15', '2023-02-20']})
        result = date_ops.convert_to_datetime(df, 'Date')
        assert pd.api.types.is_datetime64_any_dtype(result['Date']), "convert_to_datetime failed"
        print("[PASS] convert_to_datetime - PASSED")
    except Exception as e:
        print(f"[FAIL] convert_to_datetime - FAILED: {e}")
    
    # Test 4: Calculate duration
    try:
        df = pd.DataFrame({
            'Start': ['2023-01-01', '2023-01-10'],
            'End': ['2023-01-10', '2023-01-20']
        })
        result = date_ops.calculate_duration(df, 'Start', 'End', 'Duration', 'days')
        assert result.iloc[0]['Duration'] == 9, "calculate_duration failed"
        print("[PASS] calculate_duration - PASSED")
    except Exception as e:
        print(f"[FAIL] calculate_duration - FAILED: {e}")
    
    print()


def test_category_5():
    """Category 5: Numeric Transformations"""
    print("=" * 60)
    print("CATEGORY 5: NUMERIC TRANSFORMATIONS")
    print("=" * 60)
    
    # Test 1: Multiply column
    try:
        df = pd.DataFrame({'A': [1, 2, 3]})
        result = numeric_ops.multiply_column(df, 'A', 2)
        assert list(result['A']) == [2, 4, 6], "multiply_column failed"
        print("[PASS] multiply_column - PASSED")
    except Exception as e:
        print(f"[FAIL] multiply_column - FAILED: {e}")
    
    # Test 2: Add to column
    try:
        df = pd.DataFrame({'A': [1, 2, 3]})
        result = numeric_ops.add_to_column(df, 'A', 10)
        assert list(result['A']) == [11, 12, 13], "add_to_column failed"
        print("[PASS] add_to_column - PASSED")
    except Exception as e:
        print(f"[FAIL] add_to_column - FAILED: {e}")
    
    # Test 3: Round column
    try:
        df = pd.DataFrame({'Value': [10.555, 20.444]})
        result = numeric_ops.round_column(df, 'Value', 2)
        assert result.iloc[0]['Value'] == 10.56, "round_column failed"
        print("[PASS] round_column - PASSED")
    except Exception as e:
        print(f"[FAIL] round_column - FAILED: {e}")
    
    # Test 4: Normalize column
    try:
        df = pd.DataFrame({'Col': [0, 50, 100]})
        result = numeric_ops.normalize_column(df, 'Col', 'minmax')
        assert result.iloc[0]['Col'] == 0.0 and result.iloc[2]['Col'] == 1.0, "normalize_column failed"
        print("[PASS] normalize_column - PASSED")
    except Exception as e:
        print(f"[FAIL] normalize_column - FAILED: {e}")
    
    # Test 5: Create ratio
    try:
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [10, 20, 30]})
        result = numeric_ops.create_ratio(df, 'B', 'A', 'Ratio')
        assert result.iloc[0]['Ratio'] == 10.0, "create_ratio failed"
        print("[PASS] create_ratio - PASSED")
    except Exception as e:
        print(f"[FAIL] create_ratio - FAILED: {e}")
    
    print()


def test_category_7():
    """Category 7: Type Conversions"""
    print("=" * 60)
    print("CATEGORY 7: TYPE CONVERSIONS")
    print("=" * 60)
    
    # Test 1: Convert to int
    try:
        df = pd.DataFrame({'Col': ['1', '2', '3']})
        result = type_ops.convert_type(df, 'Col', 'int')
        assert pd.api.types.is_integer_dtype(result['Col']), "convert_type (int) failed"
        print("[PASS] convert_type (int) - PASSED")
    except Exception as e:
        print(f"[FAIL] convert_type (int) - FAILED: {e}")
    
    # Test 2: Convert to float
    try:
        df = pd.DataFrame({'Col': ['1.5', '2.5', '3.5']})
        result = type_ops.convert_type(df, 'Col', 'float')
        assert pd.api.types.is_float_dtype(result['Col']), "convert_type (float) failed"
        print("[PASS] convert_type (float) - PASSED")
    except Exception as e:
        print(f"[FAIL] convert_type (float) - FAILED: {e}")
    
    # Test 3: Convert to string
    try:
        df = pd.DataFrame({'Col': [1, 2, 3]})
        result = type_ops.convert_type(df, 'Col', 'str')
        assert result['Col'].dtype == 'object', "convert_type (str) failed"
        print("[PASS] convert_type (str) - PASSED")
    except Exception as e:
        print(f"[FAIL] convert_type (str) - FAILED: {e}")
    
    # Test 4: Convert to boolean
    try:
        df = pd.DataFrame({'Col': [0, 1, 1]})
        result = type_ops.convert_type(df, 'Col', 'boolean')
        assert result['Col'].dtype == 'bool', "convert_type (boolean) failed"
        print("[PASS] convert_type (boolean) - PASSED")
    except Exception as e:
        print(f"[FAIL] convert_type (boolean) - FAILED: {e}")
    
    print()


def main():
    print("\n" + "=" * 60)
    print("SHEET-EDITOR AI AGENT - COMPREHENSIVE OPERATION TESTS")
    print("=" * 60)
    print()
    
    test_category_1()  # 7 tests
    test_category_2()  # 7 tests
    test_category_3()  # 6 tests
    test_category_4()  # 4 tests
    test_category_5()  # 5 tests
    test_category_7()  # 4 tests
    
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("Total Operations Tested: 33")
    print("Categories Tested: 1, 2, 3, 4, 5, 7")
    print("Categories NOT Tested: 6 (redundant), 8 (not implemented), 9 (not implemented)")
    print("=" * 60)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n[FAIL] TEST SUITE FAILED: {e}")
        sys.exit(1)

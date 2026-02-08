"""
Comprehensive Test Suite for Sheet-Editor AI Agent Operations
Tests all implemented categories (1-7)
"""

import pandas as pd
import pytest
from operations import row_ops, column_ops, cell_ops, date_ops, numeric_ops, type_ops


class TestCategory1RowOperations:
    """Test Category 1: Row Operations (7 functions)"""
    
    def setup_method(self):
        """Create test DataFrame"""
        self.df = pd.DataFrame({
            'ID': [1, 2, 3, 4, 5],
            'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'Revenue': [100, 200, -50, 300, 150]
        })
    
    def test_delete_row_valid(self):
        """Test deleting a single row"""
        result = row_ops.delete_row(self.df, 3)  # Delete Charlie
        assert len(result) == 4
        assert 'Charlie' not in result['Name'].values
    
    def test_delete_row_invalid_index(self):
        """Test deleting row with invalid index"""
        with pytest.raises(ValueError):
            row_ops.delete_row(self.df, 10)
    
    def test_delete_multiple_rows(self):
        """Test deleting multiple rows"""
        result = row_ops.delete_rows(self.df, [1, 3, 5])
        assert len(result) == 2
        assert list(result['Name'].values) == ['Bob', 'David']
    
    def test_delete_rows_condition(self):
        """Test conditional row deletion"""
        result = row_ops.delete_rows_condition(self.df, 'Revenue', '<', 0)
        assert len(result) == 4
        assert -50 not in result['Revenue'].values
    
    def test_keep_rows_condition(self):
        """Test keeping only matching rows"""
        result = row_ops.keep_rows_condition(self.df, 'Revenue', '>', 100)
        assert len(result) == 3
        assert all(result['Revenue'] > 100)
    
    def test_insert_row(self):
        """Test inserting a new row"""
        result = row_ops.insert_row(self.df, 2, [6, 'Frank', 250])
        assert len(result) == 6
        assert result.iloc[1]['Name'] == 'Frank'
    
    def test_sort_rows_ascending(self):
        """Test sorting rows"""
        result = row_ops.sort_rows(self.df, 'Revenue', ascending=True)
        assert list(result['Revenue'].values) == [-50, 100, 150, 200, 300]
    
    def test_remove_duplicates(self):
        """Test removing duplicate rows"""
        df_dup = pd.DataFrame({
            'A': [1, 2, 2, 3],
            'B': [4, 5, 5, 6]
        })
        result = row_ops.remove_duplicates(df_dup)
        assert len(result) == 3


class TestCategory2ColumnOperations:
    """Test Category 2: Column Operations (7 functions)"""
    
    def setup_method(self):
        self.df = pd.DataFrame({
            'First': [1, 2, 3],
            'Second': [4, 5, 6],
            'Third': [7, 8, 9]
        })
    
    def test_delete_column(self):
        """Test deleting a column"""
        result = column_ops.delete_column(self.df, 'Second')
        assert 'Second' not in result.columns
        assert len(result.columns) == 2
    
    def test_rename_column(self):
        """Test renaming a column"""
        result = column_ops.rename_column(self.df, 'First', 'FirstColumn')
        assert 'FirstColumn' in result.columns
        assert 'First' not in result.columns
    
    def test_add_constant_column(self):
        """Test adding column with constant value"""
        result = column_ops.add_constant_column(self.df, 'Status', 'Active')
        assert 'Status' in result.columns
        assert all(result['Status'] == 'Active')
    
    def test_add_empty_column(self):
        """Test adding empty column"""
        result = column_ops.add_empty_column(self.df, 'Notes')
        assert 'Notes' in result.columns
        assert result['Notes'].isna().all()
    
    def test_reorder_columns(self):
        """Test reordering columns"""
        result = column_ops.reorder_columns(self.df, ['Third', 'First', 'Second'])
        assert list(result.columns) == ['Third', 'First', 'Second']
    
    def test_duplicate_column(self):
        """Test duplicating a column"""
        result = column_ops.duplicate_column(self.df, 'First', 'FirstCopy')
        assert 'FirstCopy' in result.columns
        assert list(result['First']) == list(result['FirstCopy'])
    
    def test_merge_columns(self):
        """Test merging multiple columns"""
        df = pd.DataFrame({
            'FirstName': ['John', 'Jane'],
            'LastName': ['Doe', 'Smith']
        })
        result = column_ops.merge_columns(df, ['FirstName', 'LastName'], ' ', 'FullName')
        assert 'FullName' in result.columns
        assert result.iloc[0]['FullName'] == 'John Doe'


class TestCategory3CellOperations:
    """Test Category 3: Cell/Value Operations (6 functions)"""
    
    def setup_method(self):
        self.df = pd.DataFrame({
            'Name': ['  Alice  ', 'BOB', 'charlie'],
            'Value': [0, 10, None],
            'Text': ['hello', 'world', 'test']
        })
    
    def test_replace_text(self):
        """Test global text replacement"""
        df = pd.DataFrame({'Col': ['A', 'B', 'A', 'C']})
        result = cell_ops.replace_text(df, 'Col', 'A', 'X')
        assert list(result['Col']) == ['X', 'B', 'X', 'C']
    
    def test_replace_conditional(self):
        """Test conditional replacement"""
        result = cell_ops.replace_conditional(
            self.df, 'Value', 
            {'operator': '==', 'value': 0}, 
            999
        )
        assert result.iloc[0]['Value'] == 999
    
    def test_set_column_value(self):
        """Test setting all column values"""
        result = cell_ops.set_column_value(self.df, 'Value', 42)
        assert all(result['Value'] == 42)
    
    def test_fill_na(self):
        """Test filling NA values"""
        result = cell_ops.fill_na(self.df, 'Value', 0)
        assert not result['Value'].isna().any()
    
    def test_trim_whitespace(self):
        """Test trimming whitespace"""
        result = cell_ops.trim_whitespace(self.df, 'Name')
        assert result.iloc[0]['Name'] == 'Alice'
    
    def test_change_case_upper(self):
        """Test changing case to upper"""
        result = cell_ops.change_case(self.df, 'Name', 'upper')
        assert all(result['Name'].str.isupper())
    
    def test_change_case_lower(self):
        """Test changing case to lower"""
        result = cell_ops.change_case(self.df, 'Name', 'lower')
        assert result.iloc[1]['Name'] == '  bob  '


class TestCategory4DateOperations:
    """Test Category 4: Date/Time Operations (4 functions)"""
    
    def test_reformat_date(self):
        """Test reformatting dates"""
        df = pd.DataFrame({'Date': ['15-01-2023', '20-02-2023']})
        result = date_ops.reformat_date(df, 'Date', '%d-%m-%Y', '%m/%d/%Y')
        assert result.iloc[0]['Date'] == '01/15/2023'
    
    def test_extract_date_part_year(self):
        """Test extracting year from date"""
        df = pd.DataFrame({'Date': ['2023-01-15', '2024-02-20']})
        result = date_ops.extract_date_part(df, 'Date', 'year', 'Year')
        assert result.iloc[0]['Year'] == 2023
    
    def test_extract_date_part_month(self):
        """Test extracting month from date"""
        df = pd.DataFrame({'Date': ['2023-01-15', '2023-02-20']})
        result = date_ops.extract_date_part(df, 'Date', 'month', 'Month')
        assert result.iloc[0]['Month'] == 1
    
    def test_convert_to_datetime(self):
        """Test converting to datetime"""
        df = pd.DataFrame({'Date': ['2023-01-15', '2023-02-20']})
        result = date_ops.convert_to_datetime(df, 'Date')
        assert pd.api.types.is_datetime64_any_dtype(result['Date'])
    
    def test_calculate_duration_days(self):
        """Test calculating duration in days"""
        df = pd.DataFrame({
            'Start': ['2023-01-01', '2023-01-10'],
            'End': ['2023-01-10', '2023-01-20']
        })
        result = date_ops.calculate_duration(df, 'Start', 'End', 'Duration', 'days')
        assert result.iloc[0]['Duration'] == 9


class TestCategory5NumericOperations:
    """Test Category 5: Numeric Transformations (5 functions)"""
    
    def setup_method(self):
        self.df = pd.DataFrame({
            'Value': [10.555, 20.444, 30.123],
            'A': [1, 2, 3],
            'B': [10, 20, 30]
        })
    
    def test_multiply_column(self):
        """Test multiplying column"""
        result = numeric_ops.multiply_column(self.df, 'A', 2)
        assert list(result['A']) == [2, 4, 6]
    
    def test_add_to_column(self):
        """Test adding to column"""
        result = numeric_ops.add_to_column(self.df, 'A', 10)
        assert list(result['A']) == [11, 12, 13]
    
    def test_round_column(self):
        """Test rounding column"""
        result = numeric_ops.round_column(self.df, 'Value', 2)
        assert result.iloc[0]['Value'] == 10.56
    
    def test_normalize_minmax(self):
        """Test min-max normalization"""
        df = pd.DataFrame({'Col': [0, 50, 100]})
        result = numeric_ops.normalize_column(df, 'Col', 'minmax')
        assert result.iloc[0]['Col'] == 0.0
        assert result.iloc[2]['Col'] == 1.0
    
    def test_create_ratio(self):
        """Test creating ratio column"""
        result = numeric_ops.create_ratio(self.df, 'B', 'A', 'Ratio')
        assert result.iloc[0]['Ratio'] == 10.0


class TestCategory7TypeConversions:
    """Test Category 7: Type Conversions (1 function, 4 types)"""
    
    def test_convert_to_int(self):
        """Test converting to integer"""
        df = pd.DataFrame({'Col': ['1', '2', '3']})
        result = type_ops.convert_type(df, 'Col', 'int')
        assert pd.api.types.is_integer_dtype(result['Col'])
    
    def test_convert_to_float(self):
        """Test converting to float"""
        df = pd.DataFrame({'Col': ['1.5', '2.5', '3.5']})
        result = type_ops.convert_type(df, 'Col', 'float')
        assert pd.api.types.is_float_dtype(result['Col'])
    
    def test_convert_to_str(self):
        """Test converting to string"""
        df = pd.DataFrame({'Col': [1, 2, 3]})
        result = type_ops.convert_type(df, 'Col', 'str')
        assert result['Col'].dtype == 'object'
    
    def test_convert_to_boolean(self):
        """Test converting to boolean"""
        df = pd.DataFrame({'Col': [0, 1, 1]})
        result = type_ops.convert_type(df, 'Col', 'boolean')
        assert result['Col'].dtype == 'bool'


# Integration tests
class TestIntegration:
    """Integration tests for multi-step operations"""
    
    def test_multi_column_workflow(self):
        """Test realistic workflow: rename, add, merge"""
        df = pd.DataFrame({
            'fname': ['John', 'Jane'],
            'lname': ['Doe', 'Smith'],
            'rev': [100, 200]
        })
        
        # Step 1: Rename columns
        df = column_ops.rename_column(df, 'fname', 'FirstName')
        df = column_ops.rename_column(df, 'lname', 'LastName')
        df = column_ops.rename_column(df, 'rev', 'Revenue')
        
        # Step 2: Merge names
        df = column_ops.merge_columns(df, ['FirstName', 'LastName'], ' ', 'FullName')
        
        # Step 3: Add Status
        df = column_ops.add_constant_column(df, 'Status', 'Active')
        
        assert 'FullName' in df.columns
        assert df.iloc[0]['FullName'] == 'John Doe'
        assert all(df['Status'] == 'Active')
    
    def test_data_cleaning_workflow(self):
        """Test cleaning workflow: trim, case, fill NA"""
        df = pd.DataFrame({
            'Name': ['  alice  ', 'BOB', '  charlie'],
            'Value': [10, None, 30]
        })
        
        # Clean whitespace
        df = cell_ops.trim_whitespace(df, 'Name')
        
        # Normalize case
        df = cell_ops.change_case(df, 'Name', 'title')
        
        # Fill missing values
        df = cell_ops.fill_na(df, 'Value', 0)
        
        assert df.iloc[0]['Name'] == 'Alice'
        assert df.iloc[1]['Value'] == 0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

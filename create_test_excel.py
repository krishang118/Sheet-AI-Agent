"""
Create a multi-sheet test Excel file for testing Sheet-AI-Agent
"""

import pandas as pd
from datetime import datetime, timedelta

# Sheet 1: Sales Data
sales_data = {
    'Date': [datetime(2024, 1, i).strftime('%Y-%m-%d') for i in range(1, 11)],
    'Product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Laptop', 
                'Mouse', 'Headphones', 'Keyboard', 'Monitor', 'Laptop'],
    'Quantity': [2, 15, 8, 3, 1, 20, 5, 10, 2, 3],
    'Price': [1200, 25, 75, 350, 1200, 25, 120, 75, 350, 1200],
    'Region': ['North', 'South', 'East', 'West', 'North', 
               'South', 'East', 'West', 'North', 'South']
}
df_sales = pd.DataFrame(sales_data)

# Sheet 2: Employee Data
employee_data = {
    'EmployeeID': ['E001', 'E002', 'E003', 'E004', 'E005', 'E006', 'E007', 'E008'],
    'Name': ['John Smith', 'Emma Wilson', 'Michael Brown', 'Sarah Davis', 
             'James Johnson', 'Lisa Anderson', 'David Taylor', 'Maria Garcia'],
    'Department': ['Sales', 'Engineering', 'HR', 'Sales', 'Engineering', 
                   'Marketing', 'Engineering', 'HR'],
    'Salary': [65000, 85000, 55000, 70000, 90000, 60000, 95000, 58000],
    'Start_Date': ['2020-01-15', '2019-03-22', '2021-06-10', '2020-11-05',
                   '2018-07-18', '2022-02-28', '2019-09-14', '2021-04-30']
}
df_employees = pd.DataFrame(employee_data)

# Sheet 3: Inventory
inventory_data = {
    'ItemCode': ['IT001', 'IT002', 'IT003', 'IT004', 'IT005', 'IT006'],
    'ItemName': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 'Webcam'],
    'Stock': [45, 150, 80, 30, 65, 42],
    'ReorderLevel': [20, 50, 30, 15, 25, 20],
    'UnitCost': [1000, 20, 60, 300, 100, 80]
}
df_inventory = pd.DataFrame(inventory_data)

# Sheet 4: Monthly Targets
targets_data = {
    'Month': ['January', 'February', 'March', 'April', 'May', 'June'],
    'Target': [50000, 55000, 60000, 58000, 62000, 65000],
    'Achieved': [48000, 57000, 59000, 61000, 63000, 66000],
    'Status': ['Missed', 'Achieved', 'Missed', 'Achieved', 'Achieved', 'Achieved']
}
df_targets = pd.DataFrame(targets_data)

# Create Excel file with multiple sheets
output_file = 'test_multi_sheet.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df_sales.to_excel(writer, sheet_name='Sales', index=False)
    df_employees.to_excel(writer, sheet_name='Employees', index=False)
    df_inventory.to_excel(writer, sheet_name='Inventory', index=False)
    df_targets.to_excel(writer, sheet_name='Monthly_Targets', index=False)

print(f"✅ Created {output_file} with 4 sheets:")
print(f"   1. Sales ({len(df_sales)} rows)")
print(f"   2. Employees ({len(df_employees)} rows)")
print(f"   3. Inventory ({len(df_inventory)} rows)")
print(f"   4. Monthly_Targets ({len(df_targets)} rows)")

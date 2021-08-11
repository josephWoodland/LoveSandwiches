import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from the user
    """
    while True:
        print('Please enter sales data from the last market.')
        print('Data should be six numbers, seperated by commas')
        print('Example : 10,20,30,30,40,10,\n')

        data_str = input('Enter your data here: ')
        sales_data = data_str.split(',')
        

        if validate_data(sales_data):
            print('Data is valid')
            break
    return sales_data

def validate_data(values):
    """
    Validates user data, checks for right values and if the right
    amount of values have been inputed
    """
    try:

        [int(value) for value in values]

        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values required, you provided {len(values)} '
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again \n')
        return False

    return True

def update_worksheet(data, sheet):
    """
    Update a worksheet, add new row with the current surplus data
    """
    print(f'Updating {sheet} worksheet.....\n')
    worksheet = SHEET.worksheet(sheet)
    worksheet.append_row(data)
    print('Surplus {sheet} updated successfully.\n')


def calculate_surplus_data(sales_row):
    """
    Compare the sales with the stock and calculate the surplus amounts

    The surplus is defind as the sales - stock
    - Postive surplus indicates waste
    - Negative surplus indicates extra made
    """
    print('Calculating surplus data....\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[len(stock) - 1]
    
    surplus_data = []

    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def get_last_5_entries_sales():
    """
    Collects the last 5 days worth of sales
    """
    sales = SHEET.worksheet('sales')
    # column = sales.col_values(3)
    
    columns = []

    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    pprint(columns)

    


def main():
    """
    Run all program function
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')

print('Welcome to love Sandwiches Data Automation')
# main()
get_last_5_entries_sales()
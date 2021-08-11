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
    print(f'{sheet} worksheet updated successfully.\n')


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

    columns = []

    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    Takes the last 5 days of sales data
    Over each array entry we calculate the stock levels by the average sale data then add 10%
    Returns array of guide of stock levels
    """
    print('Calculating stock data...\n')
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num)) 
    return new_stock_data

def get_stock_values(data):
    """
    Takes in the stock data array and retruns an object with the keys and values of each stock item
    """
    # Get the stock item names - the first row of the stock worksheet
    print ('Getting stock list...')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_items = stock[0]
    stock_list = zip(stock_items, data)
    stock_dict = dict(stock_list)
    print(stock_list)
    print(stock_dict)


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

sales_columns = get_last_5_entries_sales()
stock_data = calculate_stock_data(sales_columns)
update_worksheet(stock_data, 'stock')
get_stock_values(stock_data)

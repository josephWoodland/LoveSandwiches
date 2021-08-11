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

def update_sales_worksheet(data):
    """
    Update the sales worksheet, add new row with the current sales data
    """
    print('Updating sales worksheet.....\n')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print('Sales worksheet updated successfully.\n')

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
    pprint(f'Stock Row: {stock_row} \n Sales Row: {sales_row}')



def main():
    """
    Run all program function
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)

print('Welcome to love Sandwiches Data Automation')
main()
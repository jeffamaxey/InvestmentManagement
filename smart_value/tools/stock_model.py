import xlwings
import pathlib
import shutil
import os
from datetime import datetime
import pandas as pd
import re
import smart_value.stocks


def model_exist(ticker):
    """Creates a new model if it doesn't already exist"""

    stock_regex = re.compile(".*Stock_Valuation_v")

    # Relevant Paths
    cwd = pathlib.Path.cwd().resolve()
    template_folder_path = cwd / 'templates' / 'Listed_template'
    new_bool = False

    try:
        # Check if the template exists
        if pathlib.Path(template_folder_path).exists():
            path_list = [val_file_path for val_file_path in template_folder_path.iterdir()
                         if template_folder_path.is_dir() and val_file_path.is_file()]
            template_path_list = list(item for item in path_list if stock_regex.match(str(item)))
            if len(template_path_list) > 1 or len(template_path_list) == 0:
                raise FileNotFoundError("The template file error", "temp_file")
        else:
            raise FileNotFoundError("The stock_template folder doesn't exist", "temp_folder")
    except FileNotFoundError as err:
        if err.args[1] == "temp_folder":
            print("The stock_template folder doesn't exist")
        if err.args[1] == "temp_file":
            print("The template file error")
    else:
        # New model path
        model_name = ticker + "_" + os.path.basename(template_path_list[0])
        new_path = cwd / model_name
        if not pathlib.Path(new_path).exists():
            # Creates a new model file if not already exists in cwd
            print(f'Copying template to create {model_name}...')
            new_bool = True
            shutil.copy(template_path_list[0], new_path)

        return model_name, new_path, new_bool

def new_stock_model(ticker):
    """Creates a new model if it doesn't already exist, otherwise update the model"""

    path_tuple = model_exist(ticker)

    company = smart_value.stocks.Stock(ticker)
    company.load_data()  # uses yahoo finance data by default

    # update the new model
    print(f'Updating {path_tuple[0]}...')
    with xlwings.App(visible=False) as app:
        model_xl = xlwings.Book(path_tuple[1])
        update_dashboard(model_xl.sheets('Dashboard'), company, path_tuple[-1])
        update_data(model_xl.sheets('Data'), company)
        model_xl.save(path_tuple[0])
        model_xl.close()


def update_dashboard(dash_sheet, stock, new_bool):
    """Update the Dashboard sheet"""

    if new_bool:
        dash_sheet.range('C4').value = stock.name
        dash_sheet.range('C5').value = datetime.today().strftime('%Y-%m-%d')
    dash_sheet.range('C3').value = stock.security_code
    dash_sheet.range('H3').value = stock.exchange
    dash_sheet.range('H12').value = stock.report_currency
    dash_sheet.range('C6').value = stock.next_earnings
    if pd.to_datetime(dash_sheet.range('C5').value) > pd.to_datetime(dash_sheet.range('C6').value):
        stock.val_status = "Outdated"
    else:
        stock.val_status = ""
    dash_sheet.range('E6').value = stock.val_status
    dash_sheet.range('H4').value = stock.price[0]
    dash_sheet.range('I4').value = stock.price[1]
    dash_sheet.range('H5').value = stock.shares
    dash_sheet.range('H13').value = stock.fx_rate


def update_data(data_sheet, stock):
    """Update the Data sheet"""

    data_sheet.range('C3').value = stock.is_df.columns[0]  # last financial year
    if len(str(stock.is_df.iloc[0, 0])) <= 6:
        report_unit = 1
    elif len(str(stock.is_df.iloc[0, 0])) <= 9:
        report_unit = 1000
    else:
        report_unit = int((len(str(stock.is_df.iloc[0, 0])) - 9) / 3 + 0.99) * 1000
    data_sheet.range('C4').value = report_unit
    # load income statement
    for i in range(len(stock.is_df.columns)):
        data_sheet.range((7, i + 3)).value = int(stock.is_df.iloc[0, i] / report_unit)
        data_sheet.range((9, i + 3)).value = int(stock.is_df.iloc[1, i] / report_unit)
        data_sheet.range((11, i + 3)).value = int(stock.is_df.iloc[2, i] / report_unit)
        data_sheet.range((17, i + 3)).value = int(stock.is_df.iloc[3, i] / report_unit)
        data_sheet.range((18, i + 3)).value = int(stock.is_df.iloc[4, i] / report_unit)
    # load balance sheet
    for i in range(1, len(stock.bs_df.columns)):
        data_sheet.range((20, i + 3)).value = int(stock.bs_df.iloc[0, i] / report_unit)
        data_sheet.range((21, i + 3)).value = int(stock.bs_df.iloc[1, i] / report_unit)
        data_sheet.range((22, i + 3)).value = int(stock.bs_df.iloc[2, i] / report_unit)
        data_sheet.range((23, i + 3)).value = int(stock.bs_df.iloc[3, i] / report_unit)
        data_sheet.range((25, i + 3)).value = int(stock.bs_df.iloc[4, i] / report_unit)
        data_sheet.range((26, i + 3)).value = int(stock.bs_df.iloc[5, i] / report_unit)
        data_sheet.range((27, i + 3)).value = int(stock.bs_df.iloc[6, i] / report_unit)
        data_sheet.range((28, i + 3)).value = int(stock.bs_df.iloc[7, i] / report_unit)

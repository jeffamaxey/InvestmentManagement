import xlwings
import pathlib
import shutil
import os
from datetime import datetime
import pandas as pd
import re


class StockModel:
    def __init__(self, ticker):
        """ """


    def new_stock_model(self):
        """Return a raw_fin_data xlsx for the stock"""

        new_bool = False
        r = re.compile(".*Valuation_v")

        # Copy the latest Valuation template
        cwd = pathlib.Path.cwd().resolve()
        try:
            template_folder_path = cwd / 'templates' /'Listed_template'
            if pathlib.Path(template_folder_path).exists():
                path_list = [val_file_path for val_file_path in template_folder_path.iterdir()
                             if template_folder_path.is_dir() and val_file_path.is_file()]
                template_path_list = list(item for item in path_list if r.match(str(item)))
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
            new_val_name = self.security_code + "_" + os.path.basename(template_path_list[0])
            new_val_path = cwd / new_val_name
            if not pathlib.Path(new_val_path).exists():
                print(f'Copying template to create {new_val_name}...')
                shutil.copy(template_path_list[0], new_val_path)
                new_bool = True
            # load and update the new valuation xlsx
            if os.path.exists(new_val_path):
                print(f'Updating {new_val_name}...')
                with xlwings.App(visible=False) as app:
                    xl_book = xlwings.Book(new_val_path)
                    self.update_dashboard(xl_book.sheets('Dashboard'), new_bool)
                    self.update_data(xl_book.sheets('Data'))
                    xl_book.save(new_val_name)
                    xl_book.close()
            else:
                raise FileNotFoundError("The valuation file error", "val_file")


def update_dashboard(self, dash_sheet, new_bool=False):
    """Update the Dashboard sheet"""

    if new_bool:
        dash_sheet.range('C4').value = self.name
        dash_sheet.range('C5').value = datetime.today().strftime('%Y-%m-%d')
    dash_sheet.range('C3').value = self.security_code
    dash_sheet.range('H3').value = self.exchange
    dash_sheet.range('H12').value = self.report_currency
    dash_sheet.range('C6').value = self.next_earnings
    if pd.to_datetime(dash_sheet.range('C5').value) > pd.to_datetime(dash_sheet.range('C6').value):
        self.val_status = "Outdated"
    else:
        self.val_status = ""
    dash_sheet.range('E6').value = self.val_status
    dash_sheet.range('H4').value = self.price[0]
    dash_sheet.range('I4').value = self.price[1]
    dash_sheet.range('H5').value = self.shares
    dash_sheet.range('H13').value = self.fx_rate


def update_data(self, data_sheet):
    """Update the Data sheet"""

    data_sheet.range('C3').value = self.is_df.columns[0]  # last financial year
    if len(str(self.is_df.iloc[0, 0])) <= 6:
        figures_in = 1
    elif len(str(self.is_df.iloc[0, 0])) <= 9:
        figures_in = 1000
    else:
        figures_in = int((len(str(self.is_df.iloc[0, 0])) - 9) / 3 + 0.99) * 1000
    data_sheet.range('C4').value = figures_in
    # load income statement
    for i in range(len(self.is_df.columns)):
        data_sheet.range((7, i + 3)).value = int(self.is_df.iloc[0, i] / figures_in)
        data_sheet.range((9, i + 3)).value = int(self.is_df.iloc[1, i] / figures_in)
        data_sheet.range((11, i + 3)).value = int(self.is_df.iloc[2, i] / figures_in)
        data_sheet.range((17, i + 3)).value = int(self.is_df.iloc[3, i] / figures_in)
        data_sheet.range((18, i + 3)).value = int(self.is_df.iloc[4, i] / figures_in)
    # load balance sheet
    for i in range(1, len(self.bs_df.columns)):
        data_sheet.range((20, i + 3)).value = int(self.bs_df.iloc[0, i] / figures_in)
        data_sheet.range((21, i + 3)).value = int(self.bs_df.iloc[1, i] / figures_in)
        data_sheet.range((22, i + 3)).value = int(self.bs_df.iloc[2, i] / figures_in)
        data_sheet.range((23, i + 3)).value = int(self.bs_df.iloc[3, i] / figures_in)
        data_sheet.range((25, i + 3)).value = int(self.bs_df.iloc[4, i] / figures_in)
        data_sheet.range((26, i + 3)).value = int(self.bs_df.iloc[5, i] / figures_in)
        data_sheet.range((27, i + 3)).value = int(self.bs_df.iloc[6, i] / figures_in)
        data_sheet.range((28, i + 3)).value = int(self.bs_df.iloc[7, i] / figures_in)
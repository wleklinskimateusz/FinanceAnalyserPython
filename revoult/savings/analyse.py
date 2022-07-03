

# get a list of all files in this directory
import datetime
import os
import pandas as pd


def extract_money(money_str):
    return float(money_str.replace("PLN", "").replace(",", ".").replace(" ", ""))


class Period:
    def __init__(self, filename: str):
        self.start = None
        self.end = None
        self.filename = filename
        self.data = None
        self.set_dates()

    def set_dates(self):
        """
        Set the start and end dates of the period
        """
        try:
            start_str, end_str = self.filename.replace(".csv", "").split('__')
        except ValueError:
            raise ValueError(
                f"Invalid filename: {self.filename}, Correct one is: start_date__end_date.csv")

        try:
            d, m, y = start_str.split('_')
            self.start = datetime.date(int(y), int(m), int(d))
        except ValueError:
            raise ValueError(
                f"Invalid date format: {start_str}, Correct one: dd_mm_yyyy")

        try:
            d, m, y = end_str.split('_')
            self.end = datetime.date(int(y), int(m), int(d))
        except ValueError:
            raise ValueError(
                f"Invalid date format: {end_str}, Correct one: dd_mm_yyyy")

    def load_data(self):
        """
        Load the data from the file
        """
        self.data = pd.read_csv(self.filename)

    def analyse(self):
        """
        Analyse the data
        """
        funding = 0
        cashout = 0
        interest = 0

        for row in self.data.iterrows():
            option = row[1]['Description']

            if option == "Deposit":
                funding += extract_money(row[1]["Money in"])

            if option == "Withdrawal":
                cashout += extract_money(row[1]["Money out"])

            if "Gross interest" in option:
                interest += extract_money(row[1]["Money in"])

        return funding, cashout, interest


def get_files(path=os.getcwd()):
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)) and name.endswith('.csv'):
            files.append(name)
    return files


for file in get_files():
    p = Period(file)
    p.load_data()
    f, c, i = p.analyse()
    print("______________________________________________________")
    print(f"{p.start} - {p.end}")
    print(f"Funding: {f:.2f} PLN")
    print(f"Cashout: {c:.2f} PLN")
    print(f"Funding + Cashout: {(f + c):.2f} PLN")
    print(f"Interest: {i:.2f} PLN")
    print(f"Total: {(f + c + i):.2f} PLN")
    print("______________________________________________________")

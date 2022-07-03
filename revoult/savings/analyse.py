

# get a list of all files in this directory
import datetime
import os
import pandas as pd


def extract_money(money: str) -> float:
    return float(money.replace("PLN", "").replace(",", ".").replace(" ", ""))


def extract_date(date: str) -> datetime.date:
    return datetime.datetime.strptime(date, "%d_%m_%Y").date()


class Period:
    def __init__(self, filename: str) -> None:
        self.start = None
        self.end = None
        self.filename = filename
        self.data = None
        self.set_dates()

    def set_dates(self) -> None:
        """
        Set the start and end dates of the period
        """
        try:
            start_str, end_str = self.filename.replace(".csv", "").split('__')
        except ValueError:
            raise ValueError(
                f"Invalid filename: {self.filename}, Correct one is: start_date__end_date.csv")

        try:
            self.start = extract_date(start_str)
        except ValueError:
            raise ValueError(
                f"Invalid date format: {start_str}, Correct one: dd_mm_yyyy")

        try:
            self.end = extract_date(end_str)
        except ValueError:
            raise ValueError(
                f"Invalid date format: {end_str}, Correct one: dd_mm_yyyy")

    def load_data(self) -> None:
        """
        Load the data from the file
        """
        self.data = pd.read_csv(self.filename)

    def analyse(self) -> tuple[float, float, float]:
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


def get_files(path: str = os.getcwd()) -> list[str]:
    """
    Get all files in the given (default: current) directory
    """
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)) and name.endswith('.csv'):
            files.append(name)
    return files


def main() -> float:
    for file in get_files():
        p = Period(file)
        p.load_data()
        f, c, i = p.analyse()
        print("----------------------------------------------------")

        print(f"{p.start} - {p.end}\n")

        print(f"Funding: {f:.2f} PLN")
        print(f"Cashout: {c:.2f} PLN")
        print(f"Interest: {i:.2f} PLN")
        print("_" * 18)
        print(f"Total: {(f + c + i):.2f} PLN")
        print("_" * 18)
        print("----------------------------------------------------")


if __name__ == "__main__":
    main()

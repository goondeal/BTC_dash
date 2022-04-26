import pandas as pd

class DataProvider:
    def __init__(self) -> None:
        self.df = pd.read_csv('./data/Binance_BTCUSDT_d.csv', parse_dates=True, index_col='date')
        self.df = self.df.drop(columns=['unix', 'symbol'])



import pandas as pd

from strategies import BFStrategy
from views.strategy_graph import StrategyGraph

class DataProvider:
    def __init__(self) -> None:
        self.df = pd.read_csv('./data/Binance_BTCUSDT_1h.csv', parse_dates=True, index_col='date', usecols=['date', 'close'])
        # self.df = self.df.drop(columns=['unix', 'symbol'])
        self.strategy = BFStrategy(data=self.df['close'][::-1], cash=100.0)
        

    def get_strategy_graph(self):
        self.strategy.trade()
        graph = StrategyGraph(data=self.strategy.get_results_df())
        return graph.fig


    def get_strategy_summary(self):
        return self.strategy.get_summary()

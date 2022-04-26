from matplotlib import markers
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from controller import DataProvider


# Brute-force Strategy
class BFStrategy:
    TAX = 0.001
    BOUNCING_COEF = 1.01
    
    def __init__(self, data, cash=0.0, crypto=0.0):
        self.data = data
        self.high = self.low = data[0]
        self.last_buy_price = self.last_sell_price = data[0]
        
        self.cash = cash
        self.crypto = crypto
        
        self.up_rate = self.down_rate = 1.0
        self.last_up_rate = self.last_down_rate= 1.0
        
        self.trades_count = 0
        self.last_trade = 'sell' if cash else 'buy'
        self.buy_l = []
        self.sell_l = []
        self.assets = self.profit()
    

    def buy(self, price):
        if self.cash > 0.0:
            self.crypto += (1-BFStrategy.TAX) * self.cash / price
            self.cash = 0.0
            self.last_buy_price = price
            self.last_trade = 'buy'
            return True
        
        return False     
    
    
    def sell(self, price):
        if self.crypto > 0.0: # > (10.0 / buy_price):
            self.cash += (1-BFStrategy.TAX) * self.crypto * price
            self.crypto = 0.0
            self.last_sell_price = price
            self.last_trade = 'sell'
            self.trades_count += 1
            return True

        return False
    

    def profit(self):
        return self.cash + self.crypto * self.last_buy_price


    def get_return(self):
        return (self.profit() / self.assets - 1.0) * 100.0    


    def __str__(self):
        return f'''
        PROFIT = {self.profit()} $
        RETURN = {self.get_return()} %
        CASH = {self.cash} $
        CRYPTO = {self.crypto}
        HIGH = {self.high}, LOW = {self.low}
        TRADES_COUNT = {self.trades_count}
        LAST_TRADE = {self.last_trade}
        LBP = {self.last_buy_price}, LSP = {self.last_sell_price}
        '''
        
        
    def trade(self):
        for price in data:
            # print(self)
            if price < self.low:
                self.low = price
                self.last_down_rate = self.high / price
            
            if price > self.high:
                self.high = price
                self.last_up_rate = price / self.low
                
                
            if self.last_trade == 'sell':
                self.down_rate = self.high / price
                # print('SELL', self.last_down_rate / self.down_rate )
                if self.last_down_rate / self.down_rate > BFStrategy.BOUNCING_COEF:
                    if self.buy(price):
                        self.high = price
                        self.buy_l.append(price)
                else:
                    self.buy_l.append(np.nan)
                
                self.sell_l.append(np.nan)
                    # self.last_up_rate = 1.0
                    
            else: # self.last_trade == 'buy'
                if price > self.last_buy_price:
                    self.up_rate = price / self.low
                    if self.up_rate > 1.25 and self.last_up_rate / self.up_rate > Agent.BOUNCING_COEF:
                        if self.sell(price):
                            self.low = price
                            # self.last_down_rate = 1.0
                            self.sell_l.append(price)
                    else:
                        self.sell_l.append(np.nan)
                        
                    self.buy_l.append(np.nan)


# print(agent_1.trades_count, agent_1.cash)    
# print(agent_2.trades_count, agent_2.cash)    

# print(agent_1)

# plt.figure(figsize=(24, 8))

# plt.scatter(df.index[76:1000], agent_1.buy_l, label='Buy', color='green', marker='^', alpha=1)
# plt.scatter(df.index[76:1000], agent_1.sell_l, label='Sell', color='red', marker='v', alpha=1)

# plt.plot(df['close'][75:1000], label='Close', color='blue', alpha=0.35)
# plt.show()


# print(agent_1.sell)    


class SMA:
    def __init__(self, data, short=20, long=50, period=30):
        self.data = pd.DataFrame(data={'price': data.copy()})
        self.data['short'] = self.get_sma(short)
        self.data['long'] = self.get_sma(long)
        self.data['signal'] = np.where(self.short > self.long, 1, 0)
        self.data['position'] = self.signal.diff()
        self.data['buy'] = np.where(self.position == 1, self.data, np.nan)
        self.data['sell'] = np.where(self.position == -1, self.data, np.NAN)
        self.period = period
        
    def get_sma(self, window):
        return self.data.rolling(window=window).mean()




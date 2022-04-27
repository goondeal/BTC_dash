import numpy as np
import pandas as pd


# Brute-force Strategy
class BFStrategy:
    TAX = 0.001
    BOUNCING_COEF = 1.02

    def __init__(self, data, cash=0.0, crypto=0.0):
        self.data = data
        self.high = self.low = data[0]
        self.last_buy_price = self.last_sell_price = data[0]

        self.cash = cash
        self.crypto = crypto

        self.up_rate = self.down_rate = 1.0
        self.max_up_rate = self.max_down_rate = 1.0

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
        if self.crypto > 0.0:  # > (10.0 / buy_price):
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


    def get_summary(self):
        return {
            'profit': self.profit(),
            'return': self.get_return(),
            'cash': self.cash,
            'crypto': self.crypto,
            'trades_count': self.trades_count,
            'last_order': self.last_trade
            }


    def get_results_df(self):
        return pd.DataFrame(data={'price': self.data.values, 'buy': self.buy_l, 'sell': self.sell_l}, index=self.data.index)


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
        for price in self.data:
            if price < self.low:
                self.low = price
                self.max_down_rate = self.high / price

            if price > self.high:
                self.high = price
                self.max_up_rate = price / self.low

            if self.last_trade == 'sell':
                self.down_rate = self.high / price
                if self.max_down_rate / self.down_rate > BFStrategy.BOUNCING_COEF:
                    if self.buy(price):
                        self.high = price
                        # self.low = price
                        self.buy_l.append(price)
                    else:
                        self.buy_l.append(np.nan)    
                else:
                    self.buy_l.append(np.nan)

                self.sell_l.append(np.nan)
                
            else:  # self.last_trade == 'buy'
                if price > self.last_buy_price:
                    self.up_rate = price / self.low
                    if price > self.last_buy_price and self.max_up_rate > 1.035 and self.max_up_rate / self.up_rate > BFStrategy.BOUNCING_COEF:
                        if self.sell(price):
                            # self.low = price
                            self.high = price
                            # self.max_down_rate = 1.0
                            self.sell_l.append(price)
                        else:
                            self.sell_l.append(np.nan)    
                    else:
                        self.sell_l.append(np.nan)
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
        self.data['short'] = self.get_sma(data, short)
        self.data['long'] = self.get_sma(data, long)
        self.data['signal'] = np.where(self.short > self.long, 1, 0)
        self.data['position'] = self.signal.diff()
        self.data['buy'] = np.where(self.position == 1, self.data, np.nan)
        self.data['sell'] = np.where(self.position == -1, self.data, np.NAN)
        self.period = period

    def get_sma(self, data, window):
        return data.rolling(window=window).mean()


class MACDStrategy:
    def __init__(self, data, **history):
        self.data = pd.DataFrame(data={'price': data})
        self.data['short_ema'] = data.ewm(span=12, adjust=False).mean()
        self.data['long_ema'] = data.ewm(span=26, adjust=False).mean()
        self.data['macd'] = self.data['short_ema'] - self.data['long_ema']
        self.data['signal'] = self.data['macd'].ewm(
            span=9, adjust=False).mean()

    def buy_sell(macd, signal):
        buy = []
        sell = []
        flag = -1

        for i in range(len(macd)):
            if macd[i] > signal[i]:
                sell.append(np.nan)
                if flag != 1:
                    buy.append(df['close'][i])
                    flag = 1
                else:
                    buy.append(np.nan)

            if macd[i] < signal[i]:
                buy.append(np.nan)
                if flag != 0:
                    sell.append(df['close'][i])
                    flag = 0
                else:
                    sell.append(np.nan)

            else:
                buy.append(np.nan)
                sell.append(np.nan)

        return buy, sell

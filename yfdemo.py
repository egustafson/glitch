#!/usr/bin/env python3
#
# https://github.com/ranaroussi/yfinance
#
# Demo the use of yfinance

import yfinance as yf

if __name__ == '__main__':

    pythonic = True

    if pythonic:

        msft = yf.Ticker("AAPL")

        print(msft.info)
        print("==========")
        print(msft.dividends)
        print("==========")
        print(msft.splits)
        print("==========")
        print(msft.history(start="2014-06-01", end="2014-06-30", auto_adjust=False))

    else:
        tickers = ["SPY", "AAPL"]   # note, there has to be >1 tick in the list
        print(type(tickers))
        print(tickers)
        print("-----")
        t = tickers if isinstance(
            tickers, list) else tickers.replace(',', ' ').split()
        t = list(set([ticker.upper() for ticker in t]))
        print(type(t))
        print(t)

        data = yf.download(tickers, period="5d", group_by="ticker", threads=False)

        print(data['SPY'])

        for (k, v) in data.items():
            print("key: {}".format(k))

        for col in data.columns:
            print("Col: {}".format(col))

        print(data.dtypes)

        reform = []
        for index, row in data['SPY'].iterrows():
            reform.append((index, row['Open'], row['High'], row['Low'], row['Close'], int(row['Volume'])))

        for (d, o, h, l, c, v) in reform:
            print("Row[{}]: {:8.2f} {:8.2f} {:8.2f} {:8.2f} {}".format(d, o, h, l, c, v))

    print("done.")

#!/usr/bin/env python3
#
# https://github.com/ranaroussi/yfinance
#
# Demo the use of yfinance

import yfinance as yf

if __name__ == '__main__':

    pythonic = False

    if pythonic:

        msft = yf.Ticker("MSFT")

        print(msft.info)
        print("==========")
        print(msft.dividends)
        print("==========")
        print(msft.splits)
        print("==========")
        print(msft.history(period="max", auto_adjust=False))

    else:
        data = yf.download(["SPY", "AAPL"], start="2019-01-01", end="2019-02-01", group_by="ticker")

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

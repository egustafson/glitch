#!/usr/bin/env python3
#
# https://github.com/ranaroussi/yfinance
#

import yfinance as yf

msft = yf.Ticker("MSFT")

print(msft.info)
print("==========")
print(msft.history(period="max", auto_adjust=False))

print("done.")

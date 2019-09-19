# -*- coding: utf-8 -*-
""" DAO for yfinance """
#
# https://github.com/ranaroussi/yfinance
#

import yfinance as yf

def info(symbol):
    return yf.Ticker(symbol).info

def load(sym):
    t = yf.Ticker(sym)
    hdf = t.history(period='max', interval='1d', prepost=False,
                  auto_adjust=False) ##, rounding=False)
    hist = []
    for index, row in hdf.iterrows():
            hist.append( { 'date':  index.date(),
                           'tick':  sym.upper(),
                           'open':  row['Open'].item(),
                           'high':  row['High'].item(),
                           'low':   row['Low'].item(),
                           'close': row['Close'].item(),
                           'vol':   row['Volume'].item() } )
    divs = []
    for index, value in t.get_dividends().items():
            divs.append( { 'date':  index.date(),
                           'tick':  sym.upper(),
                           'div':   value } )
    splits = []
    for index, value in t.get_splits().items():
        splits.append( { 'date':  index.date(),
                         'tick':  sym.upper(),
                         'ratio': value } )

    return (hist, splits, divs)

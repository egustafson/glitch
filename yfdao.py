# -*- coding: utf-8 -*-
""" DAO for yfinance """
#
# https://github.com/ranaroussi/yfinance
#

import yfinance as yf

def download(tickers, **args):

    df = yf.download(tickers, group_by="ticker", threads=False, progress=False, **args)

    results = []
    if len(tickers) == 1:  ## then the dataframe doesn't have an axis for the tick
        for index, row in df.iterrows():
            results.append( { 'date':  index.date(),
                                  'tick':  tickers[0].upper(),
                                  'open':  row['Open'].item(),
                                  'high':  row['High'].item(),
                                  'low':   row['Low'].item(),
                                  'close': row['Close'].item(),
                                  'vol':   row['Volume'].item() } )
    else:
        for tick in tickers:
            for index, row in df[tick].iterrows():
                results.append( { 'date':  index.date(),
                                  'tick':  tick,
                                  'open':  row['Open'].item(),
                                  'high':  row['High'].item(),
                                  'low':   row['Low'].item(),
                                  'close': row['Close'].item(),
                                  'vol':   row['Volume'].item() } )

    return results

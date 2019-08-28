# -*- coding: utf-8 -*-
""" DAO for yfinance """
#
# https://github.com/ranaroussi/yfinance
#

import yfinance as yf

def download(tickers, **args):

    df = yf.download(tickers, group_by="ticker", **args)

    results = []
    for tick in tickers:
        for index, row in df[tick].iterrows():
            results.append( ( index, tick,
                              row['Open'], row['High'],
                              row['Low'], row['Close'],
                              int(row['Volume']) ) )

    return results

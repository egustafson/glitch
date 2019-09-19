# -*- coding: utf-8 -*-
""" Manage Historical Data """

import yfdao
import sql


def add_symbol(symbol):
    info = yfdao.info(symbol.upper())
    name = info['longName']
    ex = info['fullExchangeName']
    region = info['region']
    ex_tz = info['exchangeTimezoneShortName']
    sql.dao.add_symbol(symbol, name, ex, ex_tz)

def enable_symbol(symbol, en=True):
    sql.dao.enable_symbol(symbol.upper(), en)

def load_symbols(syms):
    for s in syms:
        load_symbol(s.upper())

def load_symbol(sym):
    sql.dao.clear_history(sym)
    period = "max"
    (hist, splits, divs) = yfdao.load(sym)
    sql.dao.add_history_bulk( hist )
    sql.dao.add_splits( splits )
    sql.dao.add_dividends( divs )

def update_symbols():
    None

def reset_symbol(symbol):
    sql.dao.clear_history(symbol.upper())
    sql.dao.enable_symbol(symbol.upper(), enable=False)

def list_symbols(inactive=False):
    return sql.dao.list_symbols(inactive)

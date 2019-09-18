# -*- coding: utf-8 -*-
""" Manage Historical Data """

import yfdao
import sql


def add_symbol(symbol):
    info = yfdao.info(symbol)
    name = info['longName']
    ex = info['fullExchangeName']
    region = info['region']
    ex_tz = info['exchangeTimezoneShortName']
    sql.dao.add_symbol(symbol, name, ex, ex_tz)

def enable_symbol(symbol, en=True):
    sql.dao.enable_symbol(symbol, en)

def load_symbols():
    None

def update_symbols():
    None

def reset_symbol(symbol):
    None

def list_symbols(inactive=False):
    return sql.dao.list_symbols(inactive)

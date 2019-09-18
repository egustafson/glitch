#!/usr/bin/env python3
#
# https://github.com/ranaroussi/yfinance
#

import time
import click

import yfdao
import sql

import db

default_db_url = "sqlite:///test.sqlite"
#default_db_url = "mysql+pymysql://root:passwd@localhost:3306/glitch"


@click.group()
@click.option('-d', '--debug', default=False, is_flag=True)
@click.option('--dburl', default=default_db_url)
@click.pass_context
def cli(ctx, debug, dburl):
    ctx.ensure_object(dict)
    ctx.obj['debug'] = debug
    ctx.obj['dburl'] = dburl
    sql.init_dao(dburl, debug)

@cli.command()
@click.argument('symbol', required=True)
@click.pass_context
def add(ctx, symbol):
    db.add_symbol(symbol)

@cli.command()
@click.argument('symbol', required=True)
@click.pass_context
def enable(ctx, symbol):
    db.enable_symbol(symbol, en=True)

@cli.command()
@click.argument('symbol', required=True)
@click.pass_context
def disable(ctx, symbol):
    db.enable_symbol(symbol, en=False)

@cli.command()
@click.option('-a', '--all', 'all_syms', is_flag=True)
@click.pass_context
def list(ctx, all_syms):
    symbols = db.list_symbols(all_syms)
    for s in symbols:
        print("{}".format(s))

@cli.command()
@click.argument('tickers', required=True, nargs=-1)
@click.pass_context
def load(ctx, tickers):
    #tickers = ["AAPL", "MSFT", "SPY"]
    tickers = [ t.upper() for t in tickers ]
    period = "max"
    db_url = ctx.obj['dburl']
    #
    loadcnt = 0
    starttime = time.time()
    for tick in tickers:
        data = yfdao.download([tick], period=period)
        #print("fetched [{}] items, next step: insert into DB.".format(len(data)))
        sql.dao.add_history_bulk( data )
        #print("inserted [{}] items.".format(len(data)))
        print("{}({})".format(tick, len(data)), end=" ", flush=True)
        loadcnt += len(data)
    sql.dao.close()
    endtime = time.time()
    print("")
    print("Loaded {} rows, {} tickers, in {:.2} seconds".format(loadcnt, len(tickers), endtime-starttime))

@cli.command()
@click.pass_context
def pingdb(ctx):
    sql.dao.ping()
    sql.dao.close()


@cli.command()
@click.pass_context
def resetdb(ctx):
    sql.dao.reset()


## ########## Old / debug commands ##########

@cli.command()
@click.pass_context
def diag(ctx):
    print("Context:")
    for (k,v) in ctx.obj.items():
        print("  {}: {}".format(k, v))

@cli.command()
@click.argument('tickers', required=True, nargs=-1)
@click.option('-p', '--period', default=None)
@click.option('-s', '--start', default=None)
@click.option('-e', '--end', default=None)
@click.pass_context
def csv(ctx, period, start, end, tickers):
    tickers = [ t.upper() for t in tickers ]
    data = yfdao.download(tickers, period=period, start=start, end=end, auto_adjust=False)
    for row in data:
        print("{date}, {tick:>4}, {open:8.2f}, {high:8.2f}, {low:8.2f}, {close:8.2f}, {vol:>12}".format(**row))

@cli.command()
@click.argument('symbol', required=True, nargs=1)
@click.pass_context
def dump(ctx, symbol):
    hist = sql.dao.history(symbol)
    for row in hist:
        print("{date}, {tick:>4}, {open:8.2f}, {high:8.2f}, {low:8.2f}, {close:8.2f}, {vol:>12}".format(**row))




##
##  Main Program
##
if __name__ == '__main__':
    cli(obj={})

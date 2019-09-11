#!/usr/bin/env python3
#
# https://github.com/ranaroussi/yfinance
#

import time
import click

import yfdao
import sql

#default_db_url = "sqlite:///test.sqlite")
default_db_url = "mysql+pymysql://root:passwd@localhost:3306/glitch"


@click.group()
@click.option('-d', '--debug', default=False, is_flag=True)
@click.option('--dburl', default=default_db_url)
@click.pass_context
def cli(ctx, debug, dburl):
    ctx.ensure_object(dict)
    ctx.obj['debug'] = debug
    ctx.obj['dburl'] = dburl
    None

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
    dao = sql.init_dao(ctx.obj['dburl'], ctx.obj['debug'])
    hist = dao.history(symbol)
    for row in hist:
        print("{date}, {tick:>4}, {open:8.2f}, {high:8.2f}, {low:8.2f}, {close:8.2f}, {vol:>12}".format(**row))


@cli.command()
@click.pass_context
def list(ctx):
    dao = sql.init_dao(ctx.obj['dburl'], ctx.obj['debug'])
    symbols = dao.list_symbols()
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
        dao = sql.init_dao(ctx.obj['dburl'], ctx.obj['debug'])
        #print("Successfully opened connection to DB.")
        dao.add_history_bulk( data )
        #print("inserted [{}] items.".format(len(data)))
        print("{}({})".format(tick, len(data)), end=" ", flush=True)
        loadcnt += len(data)
    dao.close()
    endtime = time.time()
    print("")
    print("Loaded {} rows, {} tickers, in {:.2} seconds".format(loadcnt, len(tickers), endtime-starttime))

@cli.command()
@click.pass_context
def pingdb(ctx):
    dao = sql.init_dao(ctx.obj['dburl'], ctx.obj['debug'])
    dao.ping()
    dao.close()


@cli.command()
@click.pass_context
def resetdb(ctx):
    dao = sql.init_dao(ctx.obj['dburl'], ctx.obj['debug'])
    dao.reset()

@cli.command()
@click.pass_context
def diag(ctx):
    print("Context:")
    for (k,v) in ctx.obj.items():
        print("  {}: {}".format(k, v))

if __name__ == '__main__':
    cli(obj={})

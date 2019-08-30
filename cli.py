#!/usr/bin/env python3
#
# https://github.com/ranaroussi/yfinance
#

import click

import yfdao
import sql


@click.group()
@click.pass_context
def cli(ctx):
    None

@cli.command()
@click.pass_context
def fetch(ctx):
    data = yfdao.download(['MSFT', 'SPY', 'AAPL'], period="5d")
    for (d, t, o, h, l, c, v) in data:
        print("Row[{}]: {:>4} - {:8.2f} {:8.2f} {:8.2f} {:8.2f} {:>12}".format(d, t, o, h, l, c, v))

@cli.command()
@click.pass_context
def loadsome(ctx):
    data = yfdao.download(['AAPL', 'MSFT'], period="30d")
    #dao = sql.init_dao("sqlite:///test.sqlite")
    dao = sql.init_dao("mysql+pymysql://root:passwd@localhost:3306/glitch")
    dao.add_bulk_history( data )
    dao.close()
    print("inserted [{}] items.".format(len(data)))

@cli.command()
@click.pass_context
def pingdb(ctx):
    dao = sql.init_dao("mysql+pymysql://root:passwd@localhost:3306/glitch")
    dao.ping()
    dao.close()


if __name__ == '__main__':
    cli(obj={})

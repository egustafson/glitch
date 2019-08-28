#!/usr/bin/env python3
#
# https://github.com/ranaroussi/yfinance
#

import click
import yfdao


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
def loadone(ctx):
    click.echo('load-one')



if __name__ == '__main__':
    cli(obj={})

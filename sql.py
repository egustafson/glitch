# -*- coding: utf-8 -*-
""" SQL DB Definitions """

from sqlalchemy import create_engine
from sqlalchemy import Table, Index, Column, MetaData, ForeignKey
from sqlalchemy import Integer, Float, String, Date, Boolean
from sqlalchemy.sql import select, func

metadata = MetaData()
history = Table('history', metadata,
    Column('id', Integer, primary_key=True),
    Column('tick', String(10), nullable=False),
    Column('date', Date, nullable=False),
    Column('open', Float, nullable=False),
    Column('close', Float, nullable=False),
    Column('high', Float, nullable=False),
    Column('low', Float, nullable=False),
    Column('vol', Integer, nullable=False),
    Index("hist_tick_date", "tick", "date", unique=True)
)

splits = Table('splits', metadata,
    Column('id', Integer, primary_key=True),
    Column('tick', String(10), nullable=False, index=True),
    Column('date', Date, nullable=False),
    Column('ratio', Float, nullable=False),
)

dividends = Table('dividends', metadata,
    Column('id', Integer, primary_key=True),
    Column('tick', String(10), nullable=False, index=True),
    Column('date', Date, nullable=False),
    Column('div', Float, nullable=False),
)

symbols = Table('symbols', metadata,
    Column('id', Integer, primary_key=True),
    Column('tick', String(10), nullable=False, index=True),
    Column('longname', String(256)),
    Column('exchange', String(256)),
    Column('exchange_tz', String(256)),
    Column('active', Boolean),
)

indicators = Table('indicators', metadata,
    Column('id', Integer, primary_key=True),
    Column('tick', String(10), nullable=False, index=True),
    Column('date', Date, nullable=False),
    Column('ind_id', String(10), nullable=False),
    Column('value', Float, nullable=False),
)


class DAO(object):

    def __init__(self, engine):
        self._engine = engine

    def close(self):
        self._engine.dispose()
        self._engine = None

    def reset(self):
        conn = self._engine.connect()
        conn.execute(history.delete())
        conn.execute(splits.delete())
        conn.execute(dividends.delete())
        conn.execute(symbols.delete())
        conn.close()

    def ping(self):
        with self._engine.connect() as conn:
            rs = conn.execute('SELECT 1')

    ## Accessors

    def add_symbol(self, symbol, name, ex, ex_tz):
        with self._engine.connect() as conn:
            conn.execute(symbols.insert(), [
                {'tick':symbol, 'longname':name,'exchange':ex,
                 'exchange_tz': ex_tz, 'active':False} ])

    def enable_symbol(self, symbol, enable=True):
        with self._engine.connect() as conn:
            conn.execute(symbols.update().\
                          where(symbols.c.tick == symbol).\
                          values(active=enable))

    def list_symbols(self, inactive=False):
        ll = []
        with self._engine.connect() as conn:
            if inactive:
                s = select([symbols.c.tick]).order_by(symbols.c.tick)
            else:
                s = select([symbols.c.tick]).\
                     where(symbols.c.active == True).\
                     order_by(symbols.c.tick)
            for row in conn.execute(s):
                ll.append(row[0])
        return ll

    def clear_history(self, symbol):
        with self._engine.connect() as conn:
            dh = history.delete().where(history.c.tick == symbol)
            conn.execute(dh)
            ds = splits.delete().where(splits.c.tick == symbol)
            conn.execute(ds)
            dd = dividends.delete().where(dividends.c.tick == symbol)
            conn.execute(dd)

    def history(self, symbol):
        hist = []
        with self._engine.connect() as conn:
            s = select([history]).\
              where(history.c.tick == symbol).order_by(history.c.date)
            for r in conn.execute(s):
                hist.append({ 'tick': r[1], 'date': r[2], 'open': r[3],
                              'close': r[4], 'high': r[5], 'low': r[6], 'vol': r[7] })
        return hist

    def add_history(self, date, symbol, o, h, l, c, v):
        with self._engine.connect() as conn:
            conn.execute(history.insert(), [
                {'date': date, 'tick': symbol,
                 'open': o, 'high': h, 'low': l, 'close': c, 'vol': v } ])

    def add_history_bulk(self, data):
        with self._engine.connect() as conn:
            conn.execute(history.insert(), data)

    def add_splits(self, split_list):
        with self._engine.connect() as conn:
            conn.execute(splits.insert(), split_list)

    def add_dividends(self, div_list):
        with self._engine.connect() as conn:
            conn.execute(dividends.insert(), div_list)


dao = None

def init_dao(url, debug=False):
    engine = create_engine(url, echo=debug)
    metadata.create_all(engine)
    global dao
    dao = DAO(engine)
    return dao

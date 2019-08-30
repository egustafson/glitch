# -*- coding: utf-8 -*-
""" SQL DB Definitions """

from sqlalchemy import create_engine
from sqlalchemy import Table, Index, Column, MetaData, ForeignKey
from sqlalchemy import Integer, Float, String, Date
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
    Column('from', Integer, nullable=False),
    Column('to', Integer, nullable=False),
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
    ##   none yet

    def add_history(self, date, symbol, o, h, l, c, v):
        with self._engine.connect() as conn:
            conn.execute(history.insert(), [
                {'date': date, 'tick': symbol,
                 'open': o, 'high': h, 'low': l, 'close': c, 'vol': v } ])

    def add_bulk_history(self, data):
        with self._engine.connect() as conn:
            for (d, t, o, h, l, c, v) in data:
                conn.execute(history.insert(), [
                    {'date': d, 'tick': t,
                    'open': o, 'high': h, 'low': l, 'close': c, 'vol': v } ])


dao = None

def init_dao(url):
    engine = create_engine(url)
    metadata.create_all(engine)
    global dao
    dao = DAO(engine)
    return dao

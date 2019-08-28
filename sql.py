# -*- coding: utf-8 -*-
""" SQL DB Definitions """

from sqlalchemy import create_engine
from sqlalchemy import Table, Index, Column, MetaData, ForeignKey
from sqlalchemy import Integer, Float, String, Date
from sqlalchemy.sql import select, func

metadata = MetaData()
history = Table('history', metadata,
    Column('id', Integer, primary_key=True),
    Column('tick', String),
    Column('date', Date),
    Column('open', Float),
    Column('close', Float),
    Column('high', Float),
    Column('low', Float),
    Column('vol', Integer),
    Index("hist_tick_date", "tick", "date", unique=True)
)

splits = Table('splits', metadata,
    Column('id', Integer, primary_key=True),
    Column('tick', String),
    Column('date', Date),
    Column('from', Integer),
    Column('to', Integer),
    Index('split_tick_idx', 'tick')
)

dividends = Table('dividends', metadata,
    Column('id', Integer, primary_key=True),
    Column('tick', String),
    Column('date', Date),
    Column('div', Float),
    Index('div_tick_idx', 'tick')
)

symbols = Table('symbols', metadata,
    Column('id', Integer, primary_key=True),
    Column('tick', String),
    Column('longname', String),
    Column('exchange', String),
    Index('sym_tick_idx', 'tick')
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

    ## Accessors
    ##   none yet

    def add_history(self, symbol, date, o, c, h, l, v):
        with self._engine.connect() as conn:
            conn.execute(history.insert(), [
                {'tick': symbol, 'date': date,
                 'open': o, 'close': c, 'high': h, 'low': l, 'vol': v } ])


dao = None

def init_dao(url):
    engine = create_engine(url)
    metadata.create_all(engine)
    global dao
    dao = DAO(engine)
    return dao

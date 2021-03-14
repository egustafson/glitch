# -*- coding: utf-8 -*-
""" Accounts """

from datetime import date as Date
from decimal import *

Dollar = Decimal('0.01')

class Transaction(object):

    def __init__(self, date, eqname, eqcost, eqamt, fee):
        self._date   = date
        self._eqname = eqname
        self._eqcost = Decimal(eqcost)
        self._eqamt  = Decimal(eqamt)
        self._fee    = Decimal(fee).quantize(Dollar)

    @property
    def date(self):
        return self._date

    @property
    def eqname(self):
        return self._eqname

    @property
    def eqcost(self):
        return self._eqcost

    @property
    def eqamt(self):
        return self._eqamt

    @property
    def fee(self):
        return self._fee

    @property
    def credit(self):
        return (-(self._eqcost * self._eqamt) - self._fee).quantize(Dollar)


class Account(object):

    def __init__(self):
        self._txns = {}

    def _insert(self, txn):
        day_txns = []
        if txn.date not in self._txns:
            self._txns[txn.date] = [txn]
        else:
            self._txns.get(txn.date).append(txn)

    def deposit(self, date, ammount, fee=0):
        txn = Transaction(date, '', -1, ammount, fee)
        self._insert(txn)

    def withdraw(self, date, ammount, fee=0):
        txn = Transaction(date, '', 1, ammount, fee)
        self._insert(txn)

    def buy(self, date, eqname, eqcost, eqamt, fee):
        txn = Transaction(date, eqname, eqcost, eqamt, fee)
        self._insert(txn)

    def sell(self, date, eqname, eqcost, eqamt, fee):
        txn = Transaction(date, eqname, eqcost, -eqamt, fee)
        self._insert(txn)

    def history(self):
        """ Return (date, valuation) for every day a transaction exits.
            'value' is the end of day value of the account
        """
        total = Decimal(0)
        assets = {}
        hist  = []
        for (date, txns) in self._txns.items():
            for tx in txns:
                total += tx.credit
            hist.append( (date, Decimal(total)) )
        if len(hist) < 1:
            hist.append( (Date.today(), Decimal(0)) )
        return hist

    def cash(self, date=Date.today()):
        #
        # Todo:  search through history to find newest date <= Today
        #
        return self.history()[-1][1]

    def valuation(self, date=Date.today()):
        #
        # Todo: calculate cash + assets
        #
        return Decimal(0)

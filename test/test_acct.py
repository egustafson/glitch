# -*- coding: utf-8 -*-

from datetime import date as Date
from decimal import *

import unittest
import acct


class TestAcct(unittest.TestCase):

    def test_transaction(self):
        d = Date( 2019, 1, 1 )
        n = "EQN"
        c = 2.12
        a = 100
        f = 0.01
        txn = acct.Transaction(d, n, c, a, f)
        self.assertEqual(txn.date, d)
        self.assertEqual(txn.eqname, n)
        self.assertEqual(txn.eqcost, Decimal(c))
        self.assertEqual(txn.eqamt, Decimal(a))
        self.assertEqual(txn.fee, Decimal(f).quantize(Decimal('0.01')))
        credit = Decimal( -(c * a) - f ).quantize(Decimal('0.01'))
        self.assertEqual(txn.credit, credit)

    def test_account_create(self):
        a = acct.Account()
        a.deposit(Date.today(), 1)
        a.withdraw(Date.today(), 1)
        h = a.history()
        self.assertEqual(len(h), 1)
        self.assertEqual( h[0][0], Date.today() )
        self.assertEqual( h[0][1], Decimal(0) )
        self.assertEqual(a.cash(), Decimal(0))

    def test_account_empty(self):
        a = acct.Account()
        h = a.history()
        self.assertEqual(len(h), 1)
        self.assertEqual( h[0][0], Date.today() )
        self.assertEqual( h[0][1], Decimal(0) )
        self.assertEqual(a.cash(), Decimal(0))


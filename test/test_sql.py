# -*- coding: utf-8 -*-

import datetime
import unittest

import sql

URL = 'sqlite:///:memory:'
#URL = 'sqlite:///test.sqlite'


class TestSQL(unittest.TestCase):

    def test_pass(self):
        self.assertTrue(True)

    def test_init_dao(self):
        dao = sql.init_dao(URL)
        self.assertIsNotNone(dao)
        dao.close()

    def test_add_history(self):
        dao = sql.init_dao(URL)
        now = datetime.date.today()
        dao.add_history( now, 'TEST', 10, 20, 25, 5, 100 )

# -*- coding: utf-8 -*-
import unittest

from Model.DbTableModel.SupportItemModel import *
from Test.Utility import init_test_db, test_db_filename

init_test_db()


class SupportItemTest(unittest.TestCase):
    def test_accessor(self):
        self.assertEqual(SupportItem, SupportItemModel.ACCESSOR)

    def test_get_column_names(self):
        expect = ['Id', 'Name', 'Cheat']
        actual = SupportItemModel.get_column_names()
        self.assertEqual(expect, actual)

    def test_column_getters(self):
        data = SupportItemModel.get_data()
        self.assertEqual(2, len(data))
        definition = SupportItemModel.get_columns_definition()
        self.assertEqual(3, len(definition))

        belt = data[0]
        self.assertEqual(1, definition['Id'](belt))
        self.assertEqual("Belt", definition['Name'](belt))
        self.assertEqual(False, definition['Cheat'](belt))

        ls = data[1]
        self.assertEqual(2, definition['Id'](ls))
        self.assertEqual("Lifting Straps", definition['Name'](ls))
        self.assertEqual(True, definition['Cheat'](ls))

    def test__default_columns(self):
        expect = ['id', 'name', 'cheat']
        actual = SupportItemModel._default_columns()
        self.assertEqual(expect, actual)


if __name__ == "__main__":
    init_test_db("../../Data/" + test_db_filename)
    unittest.main()

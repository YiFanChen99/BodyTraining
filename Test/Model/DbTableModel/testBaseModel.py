# -*- coding: utf-8 -*-
import unittest
from collections import OrderedDict


from Model.DbTableModel.BaseModel import *


class BaseModelNonAccessorTest(unittest.TestCase):
    def test_get_column_names(self):
        with self.assertRaises(NotImplementedError):
            BaseModel.get_column_names()

    def test_get_data(self):
        with self.assertRaises(NotImplementedError):
            BaseModel.get_data()

    def test__default_columns(self):
        with self.assertRaises(NotImplementedError):
            BaseModel._default_columns()

    def test_select(self):
        with self.assertRaises(NotImplementedError):
            BaseModel.select()

    def test_create(self):
        with self.assertRaises(NotImplementedError):
            BaseModel.create()


class MockColumnsDefinable(ColumnsDefinable, BaseModel):
    @classmethod
    def get_columns_definition(cls, *args):
        return OrderedDict((
            ('id', '9'),
            ('name', 'ekko'),
            ('other', lambda x: x+1),
        ))


class ColumnsDefinableTest(unittest.TestCase):
    def test_not_implemented_get_columns_definition(self):
        with self.assertRaises(NotImplementedError):
            ColumnsDefinable.get_columns_definition()

    def test_get_columns_definition(self):
        definition = MockColumnsDefinable.get_columns_definition()
        self.assertEqual(3, len(definition))
        self.assertTrue(isinstance(definition, OrderedDict))
        self.assertEqual(('id', 'name', 'other'),
                         tuple(def_ for def_ in definition))

    def test_get_column_names(self):
        names = MockColumnsDefinable.get_column_names()
        self.assertEqual(['id', 'name', 'other'], names)

    def test_get_column_getters(self):
        getters = MockColumnsDefinable.get_column_getters()
        self.assertEqual(['9', 'ekko'], getters[:2])
        self.assertEqual(51, getters[2](50))


if __name__ == "__main__":
    unittest.main()

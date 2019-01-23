# -*- coding: utf-8 -*-
import unittest
import datetime

from Model.DbTableModel.DateRecordModel import *
from Test.Utility import init_test_db, test_db_filename

init_test_db()


class DateRecordTest(unittest.TestCase):
    def test_accessor(self):
        self.assertEqual(DateRecord, DateRecordModel.ACCESSOR)

    def test_get_column_names(self):
        expect = ['Id', 'Date', 'Order', 'Name', 'Form',
                  'Sets', 'Volume', 'Rest', 'Summary', 'MaxWeight', 'MedianRep.']
        actual = DateRecordModel.get_column_names()
        self.assertEqual(expect, actual)

    def test_column_getters(self):
        data = DateRecordModel.get_data()
        self.assertEqual(3, len(data))
        definition = DateRecordModel.get_columns_definition()
        self.assertEqual(11, len(definition))

        d0101_o3 = data[0]
        self.assertEqual(1, definition['Id'](d0101_o3))
        self.assertEqual(datetime.date(2019, 1, 1), definition['Date'](d0101_o3))
        self.assertEqual("DeadLift", definition['Name'](d0101_o3))
        self.assertEqual("Conventional", definition['Form'](d0101_o3))
        self.assertEqual(1, definition['Sets'](d0101_o3))
        self.assertEqual(25, definition['Volume'](d0101_o3))
        self.assertEqual(10, definition['Rest'](d0101_o3))
        self.assertEqual("", definition['Summary'](d0101_o3))
        self.assertEqual(5, definition['MaxWeight'](d0101_o3))
        self.assertEqual(5, definition['MedianRep.'](d0101_o3))

        d0101_o5 = data[1]
        self.assertEqual(0, definition['Sets'](d0101_o5))
        self.assertEqual(0.0, definition['Volume'](d0101_o5))
        self.assertEqual("Dr5Test1", definition['Summary'](d0101_o5))
        self.assertEqual(None, definition['MaxWeight'](d0101_o5))
        self.assertEqual(None, definition['MedianRep.'](d0101_o5))

        d0109_o1 = data[2]
        self.assertEqual("Dr1Test [4:Sr4Test]", definition['Summary'](d0109_o1))
        self.assertEqual(None, definition['MaxWeight'](d0109_o1))  # max([... for [2, 3] >= 5])
        self.assertEqual(10, d0109_o1.get_max_weight(3))  # max([... for [2, 3] >= 2])
        self.assertEqual(12.5, d0109_o1.get_max_weight(2))  # max([... for [2, 3] >= 2])
        self.assertEqual(2.5, definition['MedianRep.'](d0109_o1))  # median(2, 3)

    def test__default_columns(self):
        expect = ['id', 'date_id', 'order', 'exercise_id', 'rest_between']
        actual = DateRecordModel._default_columns()
        self.assertEqual(expect, actual)


if __name__ == "__main__":
    init_test_db("../../Data/" + test_db_filename)
    unittest.main()

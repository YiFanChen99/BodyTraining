# -*- coding: utf-8 -*-
import unittest
import datetime

from Model.DbTableModel.SetRecordModel import *
from Test.Utility import init_test_db, test_db_filename

init_test_db()


class SetRecordTest(unittest.TestCase):
    def test_accessor(self):
        self.assertEqual(SetRecord, SetRecordModel.ACCESSOR)

    def test_get_column_names(self):
        expect = ['Id', 'Date', 'Name', 'Form', 'Order',
                  'Weight', 'Repetition', 'Supports', 'Note']
        actual = SetRecordModel.get_column_names()
        self.assertEqual(expect, actual)

    def test_column_getters(self):
        data = SetRecordModel.get_data()
        self.assertEqual(3, len(data))
        definition = SetRecordModel.get_columns_definition()
        self.assertEqual(9, len(definition))

        d0109_o3_o2 = data[0]
        self.assertEqual(1, definition['Id'](d0109_o3_o2))
        self.assertEqual(datetime.date(2019, 1, 9), definition['Date'](d0109_o3_o2))
        self.assertEqual("DeadLift", definition['Name'](d0109_o3_o2))
        self.assertEqual("Romania", definition['Form'](d0109_o3_o2))
        self.assertEqual(2, definition['Order'](d0109_o3_o2))
        self.assertEqual(10, definition['Weight'](d0109_o3_o2))
        self.assertEqual(3, definition['Repetition'](d0109_o3_o2))
        self.assertEqual({"Belt"}, definition['Supports'](d0109_o3_o2))
        self.assertEqual("", definition['Note'](d0109_o3_o2))

        d0109_o3_o4 = data[1]
        self.assertEqual(4, definition['Order'](d0109_o3_o4))
        self.assertEqual(12.5, definition['Weight'](d0109_o3_o4))
        self.assertEqual(2, definition['Repetition'](d0109_o3_o4))
        self.assertEqual({"Lifting Straps", "Belt"}, definition['Supports'](d0109_o3_o4))
        self.assertEqual("Sr4Test", definition['Note'](d0109_o3_o4))

    def test__default_columns(self):
        expect = ['id', 'date_record_id', 'order', 'weight', 'repetition']
        actual = SetRecordModel._default_columns()
        self.assertEqual(expect, actual)


if __name__ == "__main__":
    init_test_db("../../Data/" + test_db_filename)
    unittest.main()

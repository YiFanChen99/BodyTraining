# -*- coding: utf-8 -*-
import unittest
import datetime

from Model.DbTableModel.DateRecordModel import *
from Model.DataAccessor.DbTableAccessor import SetRecord
from Test.Utility import init_test_db, test_db_filename

init_test_db()


class DateRecordTest(unittest.TestCase):
    def test_accessor(self):
        self.assertEqual(DateRecord, DateRecordModel.ACCESSOR)

    def test_get_column_names(self):
        expect = ['Id', 'Date', 'Order', 'Name', 'Form',
                  'Sets', 'Volume', 'Rest', 'Summary', 'MaxWeightSet', 'MaxRepetitionSet']
        actual = DateRecordModel.get_column_names()
        self.assertEqual(expect, actual)

    def test_get_data(self):
        data = DateRecordModel.get_data()
        self.assertEqual(3, len(data))

        s_rec = SetRecord.get(id=3)
        self.assertEqual((1, datetime.date(2019, 1, 1), 3, 'DeadLift', 'Conventional',
                          1, 25, 10, "", s_rec, s_rec), data[0])

        self.assertEqual((0, 0.0), data[1][5:7])
        self.assertEqual((2, 55), data[2][5:7])
        self.assertEqual("Dr5Test1", data[1][8])
        self.assertEqual("Dr1Test [4:Sr4Test]", data[2][8])

        set_weight = data[2][9]
        self.assertEqual((2, 12.5, 2), (set_weight.id, set_weight.weight, set_weight.repetition))
        set_rep = data[2][10]
        self.assertEqual((1, 10, 3), (set_rep.id, set_rep.weight, set_rep.repetition))

    def test__default_columns(self):
        expect = ['id', 'date_id', 'order', 'exercise_id', 'rest_between']
        actual = DateRecordModel._default_columns()
        self.assertEqual(expect, actual)


if __name__ == "__main__":
    init_test_db("../../Data/" + test_db_filename)
    unittest.main()

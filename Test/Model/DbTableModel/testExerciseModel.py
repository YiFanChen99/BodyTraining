# -*- coding: utf-8 -*-
import unittest

from Model.DbTableModel.ExerciseModel import *
from Test.Utility import init_test_db, test_db_filename

init_test_db()


class ExerciseTest(unittest.TestCase):
    def test_accessor(self):
        self.assertEqual(Exercise, ExerciseModel.ACCESSOR)

    def test_get_column_names(self):
        expect = ['Id', 'Name', 'Form', 'Note', 'Def. weight',
                  'Def. increment', 'Def. rest', 'Def. supports']
        actual = ExerciseModel.get_column_names()
        self.assertEqual(expect, actual)

    def test_get_data(self):
        data = ExerciseModel.get_data()
        self.assertEqual(2, len(data))

        self.assertEqual((1, 'DeadLift', 'Conventional', 'Normal'), data[0][:4])

        self.assertEqual((17.0, 0.0, 120), data[1][4:7])
        self.assertEqual({'Belt', 'Lifting Straps'}, data[1][7])

    def test__default_columns(self):
        expect = ['id', 'name', 'form']
        actual = ExerciseModel._default_columns()
        self.assertEqual(expect, actual)


if __name__ == "__main__":
    init_test_db("../../Data/" + test_db_filename)
    unittest.main()

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

    def test_column_getters(self):
        data = ExerciseModel.get_data()
        self.assertEqual(2, len(data))
        definition = ExerciseModel.get_columns_definition()
        self.assertEqual(8, len(definition))

        dl_conv = data[0]
        self.assertEqual(1, definition['Id'](dl_conv))
        self.assertEqual("DeadLift", definition['Name'](dl_conv))
        self.assertEqual("Conventional", definition['Form'](dl_conv))
        self.assertEqual("Normal", definition['Note'](dl_conv))

        dl_roma = data[1]
        self.assertEqual(17.0, definition['Def. weight'](dl_roma))
        self.assertEqual(0.0, definition['Def. increment'](dl_roma))
        self.assertEqual(120, definition['Def. rest'](dl_roma))
        items = {"Belt", "Lifting Straps"}
        self.assertEqual(items, definition['Def. supports'](dl_roma))

    def test__default_columns(self):
        expect = ['id', 'name', 'form']
        actual = ExerciseModel._default_columns()
        self.assertEqual(expect, actual)


if __name__ == "__main__":
    init_test_db("../../Data/" + test_db_filename)
    unittest.main()

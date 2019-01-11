# -*- coding: utf-8 -*-
import unittest

from Model.DataAccessor.DbTableAccessor import *

test_db_filename = "testDbTableAccessor.db"
test_db_path = "./Test/Model/DataAccessor/" + test_db_filename


def init_tables():
    db.create_tables([Timeline])
    db.create_tables([Exercise, SupportItem, ExerciseDefault, ExerciseDefaultSupport])


class RecordCountTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db.init(test_db_path)

    def test_exercise_tables(self):
        self.assertEqual(2, Exercise.select().count())
        self.assertEqual(2, SupportItem.select().count())
        self.assertEqual(1, ExerciseDefault.select().count())
        self.assertEqual(2, ExerciseDefaultSupport.select().count())

    def test_other_tables(self):
        self.assertEqual(2, Timeline.select().count())


class TableOperationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db.init(test_db_path)

    def test_create_tables(self):
        with self.assertRaises(OperationalError):  # table already exists
            db.create_tables([Timeline], safe=False)

    def test_drop_tables(self):
        with db.atomic() as transaction:
            db.drop_tables([ExerciseDefault, ExerciseDefaultSupport])

            with self.assertRaises(OperationalError):  # no such table
                ExerciseDefault.select().count()
            with self.assertRaises(OperationalError):  # no such table
                ExerciseDefaultSupport.select().count()

            transaction.rollback()

    def test_create_record_single_column_constraint(self):
        with db.atomic() as transaction:
            Timeline.create(date=datetime.date(2019, 1, 3))
            self.assertEqual(3, Timeline.select().count())

            with self.assertRaises(IntegrityError):  # UNIQUE constraint failed
                Timeline.create(date=datetime.date(2019, 1, 3))

            transaction.rollback()

    def test_create_record_multi_column_constraint(self):
        with db.atomic() as transaction:
            with self.assertRaises(IntegrityError):  # UNIQUE constraint failed
                Exercise.create(name="DeadLift", form="Conventional")
            Exercise.create(name="DeadLift9", form="Conventional")
            Exercise.create(name="DeadLift", form="Conventional9")

            self.assertEqual(4, Exercise.select().count())

            transaction.rollback()

    def test_select_condition_unmatched(self):
        with self.assertRaises(DoesNotExist):
            Exercise.select().where(
                Exercise.name == "DeadLift" and Exercise.form == "111").get()


class ExerciseRelationTest(unittest.TestCase):
    @staticmethod
    def get_dead_lift(form):
        return Exercise.select().where(
            Exercise.name == "DeadLift" and (Exercise.form == form)).get()

    @classmethod
    def setUpClass(cls):
        db.init(test_db_path)

    def test_no_default(self):
        conventional = self.get_dead_lift("Conventional")
        self.assertEqual(0, len(conventional._default))

        default = conventional.default
        self.assertEqual(0.0, default.basic_weight)
        self.assertEqual(0.0, default.increment)
        self.assertEqual("", default.unit)
        self.assertEqual(0, default.rest)

    def test_default(self):
        romania = self.get_dead_lift("Romania")
        self.assertEqual(1, len(romania._default))

        default = romania.default
        self.assertEqual(17, default.basic_weight)
        self.assertEqual(0.0, default.increment)
        self.assertEqual("kg", default.unit)
        self.assertEqual(120, default.rest)

    def test_no_support(self):
        conventional = self.get_dead_lift("Conventional")
        self.assertEqual(0, len(conventional.supports))

    def test_multi_support(self):
        romania = self.get_dead_lift("Romania")
        self.assertEqual(2, len(romania.supports))

        expect = {"Lifting Straps", "Belt"}
        actual = set((str(sup) for sup in romania.supports))
        self.assertEqual(expect, actual)


if __name__ == "__main__":
    pass

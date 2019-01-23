# -*- coding: utf-8 -*-
import unittest

from Model.DataAccessor.DbTableAccessor import *
from Test.Utility import init_test_db, test_db_filename

init_test_db()


def init_tables():
    db.create_tables([Timeline])
    db.create_tables([Exercise, ExerciseNote, SupportItem, ExerciseDefault, ExerciseDefaultSupport])
    db.create_tables([DateRecord, DateRecordNote, SetRecord, SetRecordSupport, SetRecordNote])


class RecordCountTest(unittest.TestCase):
    def test_exercise_tables(self):
        self.assertEqual(2, Exercise.select().count())
        self.assertEqual(1, ExerciseNote.select().count())
        self.assertEqual(2, SupportItem.select().count())
        self.assertEqual(1, ExerciseDefault.select().count())
        self.assertEqual(2, ExerciseDefaultSupport.select().count())

    def test_record_tables(self):
        self.assertEqual(3, DateRecord.select().count())
        self.assertEqual(2, DateRecordNote.select().count())
        self.assertEqual(3, SetRecord.select().count())
        self.assertEqual(3, SetRecordSupport.select().count())
        self.assertEqual(1, SetRecordNote.select().count())

    def test_other_tables(self):
        self.assertEqual(2, Timeline.select().count())


class TableOperationTest(unittest.TestCase):
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

    def test_exercise_no_default(self):
        conventional = self.get_dead_lift("Conventional")
        self.assertEqual(0, len(conventional._default))

        default = conventional.default
        self.assertEqual(0.0, default.weight)
        self.assertEqual(0.0, default.increment)
        self.assertEqual(0, default.rest)

    def test_exercise_default(self):
        romania = self.get_dead_lift("Romania")
        self.assertEqual(1, len(romania._default))

        default = romania.default
        self.assertEqual(17, default.weight)
        self.assertEqual(0.0, default.increment)
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

    def test_exercise_with_note(self):
        e1 = Exercise.get(id=1)
        self.assertEqual(1, len(e1._note))
        self.assertEqual("Normal", e1.note)

        e2 = Exercise.get(id=2)
        self.assertEqual(0, len(e2._note))
        self.assertEqual("", e2.note)


class DateRecordRelationTest(unittest.TestCase):
    def test_record_on_date(self):
        def get_by_date(id_):
            return DateRecord.select().where(DateRecord.date == Timeline.get(id=id_))

        date_id1 = get_by_date(1)
        self.assertEqual(1, len(date_id1))

        date_id2 = get_by_date(2)
        self.assertEqual(2, len(date_id2))

    def test_record_on_date_and_order(self):
        def get_by_date_and_order(id_, order):
            return DateRecord.select().where(
                (DateRecord.date == Timeline.get(id=id_)) and
                (DateRecord.order == order)).get()

        date_id1o5 = get_by_date_and_order(2, 5)
        self.assertEqual(20, date_id1o5.rest_between)

        date_id1o3 = get_by_date_and_order(2, 3)
        self.assertEqual(10, date_id1o3.rest_between)

        with self.assertRaises(DoesNotExist):
            get_by_date_and_order(2, 4)

    def test_record_with_exercise(self):
        rec2 = DateRecord.get(id=2)
        self.assertEqual("DeadLift", rec2.exercise.name)
        self.assertEqual("Romania", rec2.exercise.form)

        rec1 = DateRecord.get(id=1)
        self.assertEqual("DeadLift", rec1.exercise.name)
        self.assertEqual("Conventional", rec1.exercise.form)

    def test_record_with_note(self):
        rec2 = DateRecord.get(id=2)
        self.assertEqual(1, len(rec2._note))
        self.assertEqual("Dr5Test1", rec2.note)

        rec1 = DateRecord.get(id=1)
        self.assertEqual(0, len(rec1._note))
        self.assertEqual("", rec1.note)

    def test_set_note_format(self):
        self.assertEqual("{0}:{1}", DateRecord.SET_NOTE_REPR)

    def test_summary(self):
        r2 = DateRecord.get(id=2)
        self.assertEqual("", r2.sets_notes)
        self.assertEqual("Dr5Test1", r2.summary)

        r3 = DateRecord.get(id=3)
        self.assertEqual("4:Sr4Test", r3.sets_notes)
        self.assertEqual("Dr1Test [4:Sr4Test]", r3.summary)

    def test_volume(self):
        r1 = DateRecord.get(id=1)
        self.assertEqual(25, r1.volume)

        r2 = DateRecord.get(id=2)
        self.assertEqual(0, r2.volume)


class SetRecordRelationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_record_on_date_record(self):
        dr3 = DateRecord.get(id=3)
        self.assertEqual(2, len(dr3.set_record))

        dr1 = DateRecord.get(id=1)
        self.assertEqual(1, len(dr1.set_record))

        dr2 = DateRecord.get(id=2)
        self.assertEqual(0, len(dr2.set_record))

    def test_record_with_specific_date_record_and_order(self):
        dr3 = DateRecord.get(id=3)
        sr1 = dr3.set_record.where(SetRecord.order == 2).get()
        self.assertEqual(10, sr1.weight)
        self.assertEqual(3, sr1.repetition)

        sr2 = dr3.set_record.where(SetRecord.order == 4).get()
        self.assertEqual(2, sr2.id)

        with self.assertRaises(DoesNotExist):
            dr3.set_record.where(SetRecord.order == 3).get()

    def test_record_with_note(self):
        r2 = SetRecord.get(id=2)
        self.assertEqual(1, len(r2._note))
        self.assertEqual("Sr4Test", r2.note)

        r1 = SetRecord.get(id=1)
        self.assertEqual(0, len(r1._note))
        self.assertEqual("", r1.note)

    def test_record_with_support(self):
        r3 = SetRecord.get(id=3)
        self.assertEqual(0, len(r3.supports))

        r1 = SetRecord.get(id=1)
        self.assertEqual(1, len(r1.supports))
        self.assertEqual("Belt", str(r1.supports[0]))

        r2 = SetRecord.get(id=2)
        self.assertEqual(2, len(r2.supports))
        expect = {"Lifting Straps", "Belt"}
        actual = set((str(sup) for sup in r2.supports))
        self.assertEqual(expect, actual)

    def test_volume(self):
        r1 = SetRecord.get(id=1)
        self.assertEqual(30, r1.volume)

        r2 = SetRecord.get(id=2)
        self.assertEqual(25, r2.volume)


if __name__ == "__main__":
    init_test_db("../../Data/" + test_db_filename)
    unittest.main()

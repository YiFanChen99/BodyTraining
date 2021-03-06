# -*- coding: utf-8 -*-
from peewee import *
import datetime
from statistics import median, StatisticsError

from Model.DataAccessor.DbAccessor.DbOrmAccessor import db, BaseModel


def atomic():
    return db.atomic()


class Timeline(BaseModel):
    date = DateField(unique=True, default=datetime.date.today)


class Exercise(BaseModel):
    name = TextField()
    form = TextField()

    class Meta:
        indexes = (
            (('name', 'form'), True),  # unique
        )

    @property
    def defaults(self):
        try:
            return self._default[0]
        except IndexError:
            return ExerciseDefault.get_default_record()

    @property
    def supports(self):
        return {sup.item for sup in self._support}

    @property
    def note(self):
        try:
            return self._note[0].note
        except IndexError:
            return ""


class ExerciseNote(BaseModel):
    exercise = ForeignKeyField(Exercise, backref='_note', unique=True)
    note = TextField()


class SupportItem(BaseModel):
    name = TextField(unique=True)
    cheat = BooleanField()

    def __str__(self):
        return self.name


class ExerciseDefault(BaseModel):
    exercise = ForeignKeyField(Exercise, backref='_default', unique=True)
    weight = FloatField(default=0)
    increment = FloatField(default=0)
    rest = IntegerField()

    @staticmethod
    def get_default_record():
        return ExerciseDefault(rest=0)


class ExerciseDefaultSupport(BaseModel):
    exercise = ForeignKeyField(Exercise, backref='_support')
    item = ForeignKeyField(SupportItem, backref='exercise')

    class Meta:
        indexes = (
            (('exercise', 'item'), True),  # unique
        )


class DateRecord(BaseModel):
    date = ForeignKeyField(Timeline, backref='date_record')
    order = IntegerField()
    exercise = ForeignKeyField(Exercise, backref='date_record')
    rest_between = IntegerField()

    SET_NOTE_REPR = "{0}:{1}"
    MIN_REPETITION_FOR_VALID_WEIGHT = 5

    class Meta:
        indexes = (
            (('date', 'order'), True),  # unique
        )

    @property
    def note(self):
        try:
            return self._note[0].note
        except IndexError:
            return ""

    @property
    def sets_notes(self):
        return ', '.join((self.SET_NOTE_REPR.format(s_rec.order, s_rec.note)
                         for s_rec in self.set_record if s_rec.note != ""))

    @property
    def summary(self):
        s_notes = self.sets_notes
        return self.note if s_notes == "" else "{0} [{1}]".format(self.note, s_notes)

    @property
    def volume(self):
        return sum(s_rec.volume for s_rec in self.set_record)

    @property
    def max_valid_weight(self):
        try:
            return self.get_max_weight(self.MIN_REPETITION_FOR_VALID_WEIGHT)
        except ValueError:
            return None

    @property
    def median_repetition(self):
        try:
            return median(map(lambda rec: rec.repetition, self.set_record))
        except StatisticsError:
            return None

    def get_max_weight(self, threshold_rep):
        return max((rec.weight for rec in self.set_record if rec.repetition >= threshold_rep))


class DateRecordNote(BaseModel):
    date_record = ForeignKeyField(DateRecord, backref='_note', unique=True)
    note = TextField()


class SetRecord(BaseModel):
    date_record = ForeignKeyField(DateRecord, backref='set_record')
    order = IntegerField()
    weight = FloatField()
    repetition = IntegerField()

    class Meta:
        indexes = (
            (('date_record', 'order'), True),  # unique
        )

    @property
    def note(self):
        try:
            return self._note[0].note
        except IndexError:
            return ""

    @property
    def supports(self):
        return {sup.item for sup in self._support}

    @property
    def volume(self):
        return self.weight * self.repetition

    @property
    def date(self):
        return self.date_record.date


class SetRecordSupport(BaseModel):
    set_record = ForeignKeyField(SetRecord, backref='_support')
    item = ForeignKeyField(SupportItem, backref='set_record')

    class Meta:
        indexes = (
            (('set_record', 'item'), True),  # unique
        )


class SetRecordNote(BaseModel):
    set_record = ForeignKeyField(SetRecord, backref='_note', unique=True)
    note = TextField()


def _create_tables():
    """
    Peewee will create tables in all-lowercases.
    Needs to be renamed manually in camel-style.
    """
    db.create_tables([Timeline])
    db.create_tables([Exercise, ExerciseNote, SupportItem, ExerciseDefault, ExerciseDefaultSupport])
    db.create_tables([DateRecord, DateRecordNote, SetRecord, SetRecordSupport, SetRecordNote])


if __name__ == "__main__":
    pass

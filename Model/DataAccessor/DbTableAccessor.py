# -*- coding: utf-8 -*-
from peewee import *
import datetime

from Model.DataAccessor.DbAccessor.DbOrmAccessor import db, BaseModel
from Model.DataAccessor.Configure import config


def atomic():
    return db.atomic()


def create(model, **kwargs):
    try:
        return model.create(**kwargs)
    except IntegrityError as ex:
        raise ValueError("IntegrityError") from ex


class Timeline(BaseModel):
    date = DateField(unique=True, default=datetime.date.today)


class Exercise(BaseModel):
    name = TextField()
    form = TextField()

    class Meta:
        indexes = (
            (('name', 'form'), True),  # unique
        )

    def __getattr__(self, item):
        if item == 'default':
            try:
                return self._default[0]
            except IndexError:
                return ExerciseDefault.get_default_record()
        elif item == 'supports':
            return [sup.item for sup in self._support]
        if item == 'note':
            try:
                return self._note[0].note
            except IndexError:
                return ""
        else:
            return super().__getattr__(item)


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
    basic_weight = FloatField(default=0)
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

    class Meta:
        indexes = (
            (('date', 'order'), True),  # unique
        )

    def __getattr__(self, item):
        if item == 'note':
            try:
                return self._note[0].note
            except IndexError:
                return ""
        else:
            return super().__getattr__(item)


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

    def __getattr__(self, item):
        if item == 'note':
            try:
                return self._note[0].note
            except IndexError:
                return ""
        elif item == 'supports':
            return [sup.item for sup in self._support]
        else:
            return super().__getattr__(item)


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


db.init(config['db_path'])
db.connect()

if __name__ == "__main__":
    pass

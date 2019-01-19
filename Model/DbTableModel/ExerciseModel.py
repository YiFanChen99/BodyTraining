#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict

from Model.DbTableModel.BaseModel import BaseModel, ColumnsDefinable
from Model.DataAccessor.DbTableAccessor import Exercise


class ExerciseModel(ColumnsDefinable, BaseModel):
    ACCESSOR = Exercise

    @classmethod
    def get_columns_definition(cls, *args):
        return OrderedDict((
            ('Id', lambda rec: rec.id),
            ('Name', lambda rec: rec.name),
            ('Form', lambda rec: rec.form),
            ('Note', lambda rec: rec.note),
            ('Def. weight', lambda rec: rec.default.weight),
            ('Def. increment', lambda rec: rec.default.increment),
            ('Def. rest', lambda rec: rec.default.rest),
            ('Def. supports', lambda rec: set(str(sup) for sup in rec.supports)),
        ))

    @classmethod
    def get_column_names(cls, *args):
        """
        >>> ExerciseModel.get_column_names()
        ['Id', 'Name', 'Form', 'Note', 'Def. weight', 'Def. increment', 'Def. rest', 'Def. supports']
        """
        return super().get_column_names(*args)

    @classmethod
    def get_data(cls, *args):
        records = super().get_data(*args)
        getters = cls.get_column_getters(*args)
        return tuple(tuple(getter(rec) for getter in getters) for rec in records)


if __name__ == "__main__":
    import doctest
    doctest.testmod(report=True)

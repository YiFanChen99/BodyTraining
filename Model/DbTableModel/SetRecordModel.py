#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict

from Model.DbTableModel.BaseModel import BaseModel, ColumnsDefinable
from Model.DataAccessor.DbTableAccessor import SetRecord


class SetRecordModel(ColumnsDefinable, BaseModel):
    ACCESSOR = SetRecord

    @classmethod
    def get_columns_definition(cls, *args):
        return OrderedDict((
            ('Id', lambda rec: rec.id),
            ('Date', lambda rec: rec.date.date),
            ('Name', lambda rec: rec.date_record.exercise.name),
            ('Form', lambda rec: rec.date_record.exercise.form),
            ('Order', lambda rec: rec.order),
            ('Weight', lambda rec: rec.weight),
            ('Repetition', lambda rec: rec.repetition),
            ('Supports', lambda rec: set(str(sup) for sup in rec.supports)),
            ('Note', lambda rec: rec.note),
        ))

    @classmethod
    def get_column_names(cls, *args):
        """
        >>> SetRecordModel.get_column_names()
        ['Id', 'Date', 'Name', 'Form', 'Order', 'Weight', 'Repetition', 'Supports', 'Note']
        """
        return super().get_column_names(*args)


if __name__ == "__main__":
    import doctest
    doctest.testmod(report=True)

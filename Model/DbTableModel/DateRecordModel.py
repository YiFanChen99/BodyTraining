#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict

from Model.DbTableModel.BaseModel import BaseModel, ColumnsDefinable
from Model.DataAccessor.DbTableAccessor import DateRecord


class DateRecordModel(ColumnsDefinable, BaseModel):
    ACCESSOR = DateRecord

    @classmethod
    def get_columns_definition(cls, *args):
        return OrderedDict((
            ('Id', lambda rec: rec.id),
            ('Date', lambda rec: rec.date.date),
            ('Order', lambda rec: rec.order),
            ('Name', lambda rec: rec.exercise.name),
            ('Form', lambda rec: rec.exercise.form),
            ('Sets', lambda rec: len(rec.set_record)),
            ('Volume', lambda rec: rec.volume),
            ('Rest', lambda rec: rec.rest_between),
            ('Summary', lambda rec: rec.summary),
            ('MaxWeightSet', lambda rec: rec.max_weight_set),
            ('MaxRepetitionSet', lambda rec: rec.max_repetition_set),
        ))

    @classmethod
    def get_column_names(cls, *args):
        """
        >>> DateRecordModel.get_column_names()
        ['Id', 'Date', 'Order', 'Name', 'Form', 'Sets', 'Volume', 'Rest', 'Summary', 'MaxWeightSet', 'MaxRepetitionSet']
        """
        return super().get_column_names(*args)


if __name__ == "__main__":
    import doctest
    doctest.testmod(report=True)

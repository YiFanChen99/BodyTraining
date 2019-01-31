#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict

from Model.DbTableModel.BaseModel import BaseModel, ColumnsDefinable
from Model.DataAccessor.DbTableAccessor import SupportItem


class SupportItemModel(ColumnsDefinable, BaseModel):
    ACCESSOR = SupportItem

    @classmethod
    def get_columns_definition(cls, *args):
        return OrderedDict((
            ('Id', lambda rec: rec.id),
            ('Name', lambda rec: rec.name),
            ('Cheat', lambda rec: rec.cheat),
        ))

    @classmethod
    def get_column_names(cls, *args):
        """
        >>> SupportItemModel.get_column_names()
        ['Id', 'Name', 'Cheat']
        """
        return super().get_column_names(*args)


if __name__ == "__main__":
    import doctest
    doctest.testmod(report=True)

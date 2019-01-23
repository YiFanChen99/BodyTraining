#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Model.DataAccessor.DbTableAccessor import IntegrityError


class BaseModel(object):
    # Used on create, select, _default_columns.
    ACCESSOR = None

    @classmethod
    def get_column_names(cls, *args):
        """
        Can easily be implemented with cls._default_columns().
        Should add doctest for readability.
        """
        raise NotImplementedError()

    @classmethod
    def get_data(cls, *args):
        return cls.select()

    @classmethod
    def get_record_attr(cls, record, attr):
        return getattr(record, attr)

    @classmethod
    def _default_columns(cls):
        if cls.ACCESSOR:
            return list(cls.ACCESSOR.get_column_names())
        raise NotImplementedError

    @classmethod
    def select(cls, *args):
        if not cls.ACCESSOR:
            raise NotImplementedError

        return cls.ACCESSOR.select(*args)

    @classmethod
    def create(cls, model=None, **kwargs):
        """
        Delegate create with IntegrityError wrapped.
        """
        if model is None:
            model = cls.ACCESSOR
        if model is None:
            raise NotImplementedError

        try:
            return model.create(**kwargs)
        except IntegrityError as ex:
            raise ValueError("IntegrityError") from ex


class ColumnsDefinable(object):
    @classmethod
    def get_columns_definition(cls, *args):
        raise NotImplementedError

    @classmethod
    def get_column_names(cls, *args):
        return list(cls.get_columns_definition(*args).keys())

    @classmethod
    def get_column_getters(cls, *args):
        return list(cls.get_columns_definition(*args).values())


if __name__ == "__main__":
    pass

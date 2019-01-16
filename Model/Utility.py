#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Model.DataAccessor.DbAccessor.DbOrmAccessor import db


def init_db(path):
    db.init(path)


if __name__ == "__main__":
    pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Model.Utility import init_db

test_db_filename = "MockDb.db"


def init_test_db(path="./Test/Data/" + test_db_filename):
    init_db(path)

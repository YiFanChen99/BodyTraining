#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from enum import Enum

from Model.DataAccessor.ConfigureIntegrator.Loader import ConfigureLoader as ConLoader


class Path(str, Enum):
    DATA_DIR = os.getcwd() + os.sep + "Data"


class Configure(object):
    CONFIG = ConLoader.load_integrated_config(Path.DATA_DIR)
    OTHER_INFO = ConLoader.load_file(Path.DATA_DIR, "OtherInfo.json")

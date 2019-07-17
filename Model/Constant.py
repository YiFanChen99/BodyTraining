#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from enum import Enum

from Model.DataAccessor.ConfigureIntegrator.Loader import ConfigureLoader as ConLoader


class Path(object):
    DATA_DIR = os.getcwd() + os.sep + "Data"


class Configure(object):
    CONFIG = ConLoader.load_integrated_config(Path.DATA_DIR)
    OTHER_INFO = ConLoader.load_file(Path.DATA_DIR, "OtherInfo.json")


class StrEnum(str, Enum):
    pass


class ConfigGroup(StrEnum):
    WINDOWS = 'windows'
    WINDOWS_MAIN = 'main'

    def get_config(self, config):
        try:
            return config[self]
        except KeyError:
            return {}

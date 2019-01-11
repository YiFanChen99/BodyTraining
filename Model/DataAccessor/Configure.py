#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from Model.DataAccessor.JsonAccessor.JsonAccessor import load_json, save_json


class Configure(object):
    def __init__(self, dir_path):
        super(Configure, self).__init__()
        self.dir_path = dir_path
        self.default_config = None
        self.config = None

        self.load_default_config()
        self.load_config()

    def load_config(self):
        try:
            self.config = load_json(self.dir_path + "ConfigUser.json")
        except FileNotFoundError:
            self.config = {}

    def load_default_config(self):
        self.default_config = load_json(self.dir_path + "ConfigDefault.json")

    def save_config(self):
        save_json(self.dir_path + "ConfigUser.json", self.config)

    def __getitem__(self, name):
        try:
            return self.config[name]
        except KeyError:
            return self.default_config[name]


def get_matched_dir(path, project_dir_name="BodyTraining"):
    while True:
        head, tail = os.path.split(path)
        if tail == project_dir_name:
            return path
        elif head == path:
            raise ValueError(path)
        else:
            path = head


config = {}
other_info = {}

if __name__ == "__main__":
    pass
else:
    dir_path = get_matched_dir(os.getcwd()) + os.sep + "Data" + os.sep

    config = Configure(dir_path)

    other_info = load_json(dir_path + "OtherInfo.json")

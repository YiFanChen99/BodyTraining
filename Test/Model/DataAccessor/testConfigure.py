#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from Model.DataAccessor.Configure import *


class GetMatchedDirTest(unittest.TestCase):
    EXPECT = "D:\\Projects\\BodyTraining"

    def assert_get_matched_dir(self, path, *args, **kwargs):
        self.assertEqual(self.EXPECT, get_matched_dir(path, *args, **kwargs))

    def test_get_matched_dir(self):
        self.assert_get_matched_dir(self.EXPECT)
        self.assert_get_matched_dir(self.EXPECT + "\\ModelUtility\\DataAccessor")

    def test_get_matched_dir_invalid_path(self):
        with self.assertRaises(ValueError):
            self.assert_get_matched_dir("")

        with self.assertRaises(ValueError):
            self.assert_get_matched_dir(self.EXPECT[:-1])

    def test_get_matched_dir_with_project_dir(self):
        self.assert_get_matched_dir(self.EXPECT, "BodyTraining")
        self.assert_get_matched_dir(self.EXPECT + "\\DDD\\", project_dir_name="BodyTraining")

        with self.assertRaises(ValueError):
            self.assert_get_matched_dir(self.EXPECT, project_dir_name="AAA")

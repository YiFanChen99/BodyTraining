# -*- coding: utf-8 -*-
import unittest

from Model.Constant import ConfigGroup


class ConfigGroupTest(unittest.TestCase):
    def test_instance(self):
        self.assertEqual(ConfigGroup, type(ConfigGroup.WINDOWS))
        self.assertEqual('windows', ConfigGroup.WINDOWS)
        self.assertEqual('main', ConfigGroup.WINDOWS_MAIN)

    def test_get_config(self):
        config = {'': 3}
        self.assertEqual({}, ConfigGroup.WINDOWS.get_config(config))

        config = {'windows': 8}
        self.assertEqual(8, ConfigGroup.WINDOWS.get_config(config))


if __name__ == "__main__":
    unittest.main()

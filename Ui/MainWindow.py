#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *

from Model.Constant import Configure, ConfigGroup
from Model.DbTableModel.DateRecordModel import DateRecordModel
from Ui.PyQtComponent.Window import BaseWindow, Key as WinKeys
from Ui.PyQtComponent.Panel import TabPanel, Key as PanKey, BaseVBoxPanel


class MainWindow(BaseWindow):
    CONFIG_KEY = ConfigGroup.WINDOWS_MAIN

    def _create_main_panel(self):
        return MainPanel(self)

    def _load_config(self):
        return Configure.CONFIG[ConfigGroup.WINDOWS][self.CONFIG_KEY]

    def apply_config(self, config):
        self.resize(config[WinKeys.WIDTH], config[WinKeys.HEIGHT])
        self.move(config[WinKeys.X_AXIS], config[WinKeys.Y_AXIS])
        self.setWindowTitle(config[WinKeys.TITLE])


class MainPanel(TabPanel):
    def __init__(self, *args):
        config = {
            PanKey.TABS: [{
                PanKey.CONSTRUCTOR: QLabel,
                PanKey.ARGS: ['LAAAAAAAAAA'],
                PanKey.TEXT: 'Label'
            }, {
                PanKey.CONSTRUCTOR: MockPanel,
                PanKey.KWARGS: {'maxLength': 3},
                PanKey.TEXT: 'LE'
            }],
            PanKey.DEFAULT_INDEX: 1
        }
        super().__init__(*args, config=config)


class MockPanel(BaseVBoxPanel):
    def __init__(self, **kwargs):
        super().__init__()

    def _init_layout(self):
        layout = self.layout()
        layout.addWidget(QLabel("Test"))
        layout.addWidget(QLineEdit())

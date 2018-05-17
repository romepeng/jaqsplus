# -*- encoding: utf-8 -*-

import time
import pandas as pd

from jaqs.data import RemoteDataService
from jaqs.data import DataView
import jaqs.util as jutil

from config_path import DATA_CONFIG_PATH, TRADE_CONFIG_PATH
data_config = jutil.read_json(DATA_CONFIG_PATH)
trade_config = jutil.read_json(TRADE_CONFIG_PATH)

#dataview_dir_path = '../../output/test_dataview/dataview'

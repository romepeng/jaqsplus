# -*- encoding: utf-8 -*-

import time
import pandas as pd

from jaqs.data import RemoteDataService
from jaqs.data import DataView
import jaqs.util as jutil

from config_path import DATA_CONFIG_PATH, TRADE_CONFIG_PATH
data_config = jutil.read_json(DATA_CONFIG_PATH)
trade_config = jutil.read_json(TRADE_CONFIG_PATH)


dataview_dir_path = '../../output/canslim/dataview'
props = {'start_date': 20170101, 'end_date': 20180516, 'universe': '000905.SH',
             'fields': "",
             'freq': 1}

ds = RemoteDataService()
ds.init_from_config(data_config)


dv = DataView()
dv.init_from_config(props, ds)
dv.prepare_data()

factor_formula = 'Quantile(-float_mv,5)'
dv.add_formula('rank_mv', factor_formula, is_quarterly=False)

dv.save_dataview(folder_path=dataview_dir_path)
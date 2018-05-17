# -*- encoding: utf-8 -*-

import time
import pandas as pd

from jaqs.data import RemoteDataService
from jaqs.data import DataView
import jaqs.util as jutil

from config_path import DATA_CONFIG_PATH, TRADE_CONFIG_PATH
data_config = jutil.read_json(DATA_CONFIG_PATH)
trade_config = jutil.read_json(TRADE_CONFIG_PATH)

dataview_dir_path = '../../output/test_dataview/dataview'

def test_save_dataview(sub_folder='test_dataview'):
    ds = RemoteDataService()
    ds.init_from_config(data_config)
    dv = DataView()
    
    props = {'start_date': 20150101, 'end_date': 20170930, 'universe': '000905.SH',
             'fields': ('float_mv,tot_shrhldr_eqy_excl_min_int,deferred_tax_assets,sw2'),
             'freq': 1}
    
    dv.init_from_config(props, ds)
    dv.prepare_data()
    
    factor_formula = 'Quantile(-float_mv,5)'
    dv.add_formula('rank_mv', factor_formula, is_quarterly=False)
    
    factor_formula = 'Quantile(float_mv/(tot_shrhldr_eqy_excl_min_int+deferred_tax_assets), 5)'
    dv.add_formula('rank_pb', factor_formula, is_quarterly=False)
    
    dv.save_dataview(folder_path=dataview_dir_path)


def my_selector(context, user_options=None):
    dv = context.dataview
    rank_mv = dv.get_snapshot(context.trade_date, fields='rank_mv')
    rank_pb = dv.get_snapshot(context.trade_date, fields='rank_pb')
    # rank_pe = dv.get_snapshot(context.trade_date, fields='rank_pe')
    rank = pd.DataFrame()
    rank['rank_total'] = rank_mv['rank_mv'] + rank_pb['rank_pb']
    rank = rank.sort_values('rank_total', ascending=True)
    length = int(rank.shape[0] * 0.2)
    return rank.isin(rank.head(length))


if __name__ == "__main__":
    # dv_subfolder_name = 'graham'
    t_start = time.time()
    test_save_dataview()
    t3 = time.time() - t_start
    print("\n\n\nTime lapsed in total: {:.1f}".format(t3))

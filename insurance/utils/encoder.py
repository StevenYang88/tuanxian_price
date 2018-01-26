# -*- coding: utf-8 -*-

################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
Encode the raw data.
"""

import json
import numpy as np
import pandas as pd
from collections import OrderedDict


class Encode(object):
    """
    Data encoding
    """
    def __init__(self, path, file, feature_list):
        """

        :param path:
        :param file:
        :param feature_list:
        """
        self.path = path
        self.file = file
        self.feature_list = feature_list
        self.data_train = np.nan
        self.row_cnt = 0

    def _get_format_table(self):
        """

        :return:
        """
        table_str = open(self.path + 'format_table.json').read()
        table_dict = json.loads(table_str, object_pairs_hook=OrderedDict)
        table_list = table_dict['values']
        return table_list

    def _find_index(self, x, feature, table_list):
        """

        :param x:
        :param feature:
        :param table_list:
        :return:
        """
        for item_dict in table_list:
            if item_dict['group'] == feature and item_dict['id_in_group'] == x:
                index = item_dict['index']
                self.data_train[self.row_cnt][index] = 1
                self.row_cnt += 1
                return index

    def feature_encoding(self):
        """

        :return:
        """
        df_raw = pd.read_csv(self.path + self.file, low_memory=True, dtype=str)
        df_cat = df_raw[self.feature_list]
        table_list = self._get_format_table()
        self.data_train = np.zeros((df_cat.shape[0], len(table_list)), dtype=int)

        for feature in self.feature_list:
            self.row_cnt = 0
            df_cat.ix[:, feature].apply(self._find_index, args=(feature, table_list))

        return pd.DataFrame(self.data_train)


if __name__ == '__main__':
    category_feature = ['policy', 'coverage', 'industry', 'occupation', 'city', 'avg_age']
    encode = Encode(path='./', file='data_raw_1.csv', feature_list=category_feature)
    encode.feature_encoding()

# -*- coding: utf-8 -*-

################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
Create format table
"""

import json
import pandas as pd
from collections import OrderedDict


class Table(object):
    """
    模型字段one-hot编码映射表
    """
    def __init__(self, df, feature_list, prefix_list):
        """

        :param df:
        :param feature_list:
        :param prefix_list:
        """
        self.df = df
        self.table_list = []
        self.table_index = 0
        self.feature_list = feature_list
        self.prefix_list = prefix_list

    def get_feature_dict(self, feature):
        """

        :param feature:
        :return:
        """
        self.df[feature] = self.df[feature].astype('category')
        feature_id = self.df[feature].cat.categories
        feature_index = range(1, len(feature_id) + 1)
        if feature in ['policy', 'city']:
            feature_dict = dict(zip(feature_id, feature_id))
        else:
            feature_dict = dict(zip(feature_id, feature_index))
        return feature_dict

    def get_table_list(self, feature_name, prefix_str):
        """

        :param feature_name:
        :param prefix_str:
        :return:
        """
        feature_dict = self.get_feature_dict(feature_name)
        index_in_group = 1

        for key, value in feature_dict.items():
            temp_dict = OrderedDict()
            temp_dict['id'] = feature_name + '_' + str(value)
            temp_dict['index'] = self.table_index
            temp_dict['debug_doc'] = prefix_str + key
            temp_dict['group'] = feature_name
            temp_dict['id_in_group'] = key
            temp_dict['index_in_group'] = index_in_group
            index_in_group += 1
            self.table_index += 1
            self.table_list.append(temp_dict)

    def get_format_table(self, path):
        """

        :param path:
        :return:
        """
        for feature_name, prefix_str in zip(self.feature_list, self.prefix_list):
            self.get_table_list(feature_name, prefix_str)

        table_size = len(self.table_list)
        table_dict = OrderedDict()
        table_dict['size'] = table_size
        table_dict['values'] = self.table_list

        with open(path + 'format_table.json', 'w') as outfile:
            json.dump(table_dict, outfile, ensure_ascii=False)


def create_table(path):
    """

    :param path:
    :return:
    """
    df = pd.read_csv(path + 'data_raw.csv', low_memory=True, dtype=str)
    features = ['policy', 'coverage', 'industry', 'occupation', 'city', 'avg_age']
    prefix = ['险种代码', '', '', '', '分公司', '年龄区间']
    table = Table(df, feature_list=features, prefix_list=prefix)
    table.get_format_table(path)


if __name__ == '__main__':
    data_path = './'
    create_table(data_path)

# -*- coding: utf-8 -*-

################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
Dnn model
"""

import numpy as np
import pandas as pd
from keras.models import Model
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import concatenate
from keras.layers import add
from keras.models import model_from_json
from keras.callbacks import CSVLogger
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


class Dnn(object):
    """
    Dnn model
    """
    def __init__(self, path):
        """

        :param path:
        """
        self.path = path
        self.model = None

    def dnn_net(self, input_shape=None):
        """

        :param input_shape: 数据维数
        :return:
        """
        a = Input(shape=(input_shape,))
        t1 = Dense(30, activation='relu', kernel_initializer='random_normal')(a)
        t1 = Dense(60, activation='relu', kernel_initializer='normal')(t1)
        t1 = Dropout(0.2)(t1)
        t1 = Dense(10, activation='relu', kernel_initializer='normal')(t1)
        t2 = Dense(120, activation='relu', kernel_initializer='normal')(a)
        t2 = Dense(10, activation='relu', kernel_initializer='normal')(t2)
        t2 = Dropout(0.2)(t2)
        x1 = add([t1, t2])
        x2 = Dense(60, activation='relu', kernel_initializer='random_normal')(a)
        x2 = Dense(30, activation='relu', kernel_initializer='normal')(x2)
        x2 = Dropout(0.2)(x2)
        x2 = Dense(15, activation='relu', kernel_initializer='he_normal')(x2)
        x3 = Dense(100, activation='relu', kernel_initializer='he_normal')(a)
        x3 = Dropout(0.2)(x3)
        x3 = Dense(20, activation='relu', kernel_initializer='normal')(x3)
        x4 = Dense(5, activation='relu', kernel_initializer='he_normal')(a)
        x4 = Dropout(0.2)(x4)
        x4 = Dense(30, activation='relu', kernel_initializer='normal')(x4)
        x = concatenate([x1, x2, x3, x4])
        b = Dense(1, activation='relu', kernel_initializer='normal')(x)
        self.model = Model(inputs=a, outputs=b)

    def train_model(self, metrics_file, train_set, label, epoch):
        """

        :param metrics_file: loss记录文件
        :param train_set: 训练集
        :param label: 数据标签
        :param epoch: 迭代次数
        :return:
        """
        # 损失函数日志
        csv_metrics = CSVLogger(metrics_file, separator=',', append=False)
        # 训练集
        x_train = train_set.drop(label, axis=1).values
        y_train = train_set[label].values
        self.model.compile(loss='msle', optimizer='adam')
        self.model.fit(x_train, y_train, batch_size=128, epochs=epoch,
                       verbose=1, callbacks=[csv_metrics])

    def predict(self, data_set, label):
        """

        :param data_set: 数据集
        :param label: 数据标签
        :return: 实际值，预测值
        """
        x = data_set.drop(label, 1).values
        y = data_set[label].values
        yp = self.model.predict(x).transpose()
        yp = np.transpose(yp).reshape(y.size)
        return y, yp

    @staticmethod
    def cal_error(y, yp):
        """

        :param y: 实际值
        :param yp: 预测值
        :return:
        """
        mae = mean_absolute_error(y, yp)
        rmse = np.sqrt(mean_squared_error(y, yp))
        r2 = r2_score(y, yp)
        error = (mae, rmse, r2)
        return error

    @staticmethod
    def save_result(path, y, yp):
        """

        :param path: 预测结果路径
        :param y: 实际值
        :param yp: 预测值
        :return:
        """
        temp = {'y': y, 'yp': yp}
        validate_result = pd.DataFrame(temp)
        validate_result.to_csv(path + 'result.csv', float_format='%9.2f', index=None)

    def save_model(self):
        """
        保存模型
        :return:
        """
        json_string = self.model.to_json()
        model_file = open(self.path + 'keras/keras_network.json', 'w')
        model_file.write(json_string)
        model_file.close()
        self.model.save_weights(self.path + 'keras/keras_weights.h5')

    def load_model(self):
        """
        加载模型
        :return:
        """
        self.model = model_from_json(open(self.path + 'keras/keras_network.json').read())
        self.model.load_weights(self.path + 'keras/keras_weights.h5')


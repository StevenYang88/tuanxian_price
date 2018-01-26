#!/bin/bash
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
set -e
nohup python3 -m model_serving --conf conf/model-serving.json -host 0.0.0.0 >nohup.out 2>&1 &
pid=$!
echo $pid > model-serving.pid
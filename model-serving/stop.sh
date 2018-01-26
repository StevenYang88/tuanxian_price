#!/bin/bash
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
if [ -f $SCHEDULE_PID ]; then
    pid=`cat model-serving.pid`
    kill -9 $pid > /dev/null 2>&1
fi
#!/bin/env python
# -*- coding=utf8 -*-
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
Load Utils
Zip
Download
"""
import os
import shutil
import zipfile


def _extract_zip(zip_file, destination):
    """
    Extract zip to destination without keeping directory structure
        Parameters
        ----------
        zip_file : str
            Path to zip file.
        destination : str
            Destination directory.
    """
    with zipfile.ZipFile(zip_file) as file_buf:
        for item in file_buf.namelist():
            filename = os.path.basename(item)
            # skip directories
            if not filename:
                continue

            # copy file (taken from zipfile's extract)
            source = file_buf.open(item)
            target = open(os.path.join(destination, filename), 'wb')
            with source, target:
                shutil.copyfileobj(source, target)

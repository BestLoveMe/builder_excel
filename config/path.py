# -*- coding: utf-8 -*-
# @Time  : 2022/11/7 10:03
# @Author: 86136
import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


FILE_DIR = os.path.join(BASE_DIR, 'file')

API_DIR = os.path.join(BASE_DIR, 'api')

SHELVE_DIR = os.path.join(BASE_DIR, 'shelve_dir')
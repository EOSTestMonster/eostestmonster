#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from __future__ import unicode_literals
import os
import sys
import time
import json
import requests
import argparse
import subprocess 
import traceback
import multiprocessing
from decimal import Decimal, getcontext

def main():
    if len(sys.argv)<1:
        print('ERROR:Please supply the param file')
        return False
    param_dict, param_str = None, ''
    with open(sys.argv[1], 'r') as fp:
        param_str = fp.read()
        param_dict = json.loads(param_str)
    if not param_dict:
        print('ERROR:param file can NOT be empty')
        return False
    print('Get params:', sys.argv[0], param_str)
    return True

if __name__ == '__main__':
    sys.exit( 0 if main() else 1)
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from __future__ import unicode_literals
import os
import sys
import time
import json
import yaml
import requests
import argparse
import subprocess 
import traceback
import simplejson as json
import multiprocessing
from bs4 import BeautifulSoup
from decimal import Decimal, getcontext


def main():
    if len(sys.argv)<1:
        print 'ERROR:Please supply the param file'
        return False
    param_dict = None
    with open(sys.argv[1], 'r') as fp:
        param_dict = json.loads(fp.read())
    if not param_dict:
        print 'ERROR:param file can NOT be empty'
        return False
    print 'Get params:', sys.argv[0], param_dict
    return True

if __name__ == '__main__':
    sys.exit( 0 if main() else 1)
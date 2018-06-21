#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from __future__ import unicode_literals

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback

from logs.log import logger

TMP_PATH = './tmp'


############################################
#            Start run testcase            #
############################################

def check_exist_acct(conf_dict):
    '''check the common_params.exist_account availability'''
    # TODO: need to be realized
    return True


def setup_env():
    if os.path.exists(TMP_PATH):
        shutil.rmtree(TMP_PATH)
    os.mkdir(TMP_PATH)


def run_testcase(case_dict, common_params):
    cmdline = ''
    try:
        if 'pre_call' in case_dict and case_dict['pre_call']:
            cmdline = case_dict['pre_call']
            logger.info('Going to execute PRE call: {} {}'.format(case_dict['casename'], cmdline))
            pmsg = subprocess.check_output(cmdline, stderr=subprocess.STDOUT, shell=True)
            logger.info(pmsg)
        if 'cmdline' not in case_dict or not case_dict['cmdline']:
            logger.error('Error: cmdline can NOT be empty {}'.format(case_dict['casename']))
            return False
        params = {}
        params.update(common_params)
        params.update(case_dict['params'])
        params_file = os.path.join(TMP_PATH, str(re.sub(r"\s+", "", case_dict['casename'])).lower() + ".json")
        with open(params_file, "w") as fp:
            fp.write(json.dumps(params, indent=True, sort_keys=True, ensure_ascii=False))

        cmdline = case_dict['cmdline'] + " " + params_file
        logger.info('Going to execute cmdline: {} {}'.format(case_dict['casename'], cmdline))
        pmsg = subprocess.check_output(cmdline, stderr=subprocess.STDOUT, shell=True)
        logger.info(pmsg)

        if 'post_call' in case_dict and case_dict['post_call']:
            cmdline = case_dict['post_call']
            logger.info('Going to execute POST call: {} {}'.format(case_dict['casename'], cmdline))
            pmsg = subprocess.check_output(cmdline, stderr=subprocess.STDOUT, shell=True)
            logger.info(pmsg)
        return True
    except Exception as e:
        logger.error('get exception: {} {}'.format(case_dict['casename'], cmdline))
        logger.error(traceback.print_exc())
        return False


def run_monster(conf_dict):
    for case_dict in conf_dict['testcases']:
        result = run_testcase(case_dict, conf_dict['common_params'])
        if case_dict['stoponfail'] and not result:
            return False
    return True


####################################################################


def main():
    parser = argparse.ArgumentParser(description='EOSIO testcase collections running tool.')
    parser.add_argument('--config', default="./config.json", type=str, help='config.json config file path')
    args = parser.parse_args()
    conf_file = os.path.abspath(os.path.expanduser(args.config))
    # Check the parameters
    if not os.path.exists('testcases'):
        logger.error('call startmonster.py in the eostestmonster directory')
        sys.exit(1)

    conf_dict = None
    with open(conf_file, 'r') as fp:
        conf_dict = json.loads(fp.read())
    if not conf_dict:
        logger.error('validator config can not be empty: {}'.format(conf_file))
        sys.exit(1)
    if not check_exist_acct(conf_dict):
        logger.error('ERROR: the exist_account is NOT available')
        sys.exit(1)

    setup_env()

    # Start the testcase
    try:
        time_start = time.time()
        result = run_monster(conf_dict)
        if not result:
            logger.error('!!! Call testcases FAILED !!!')
        else:
            logger.info('Call testcases SUCCESS !!!')
        time_usage = time.time() - time_start
        logger.info('TIME USAGE:%ss' % (time_usage,))
        return result
    except Exception as e:
        logger.error(traceback.print_exc())


if __name__ == '__main__':
    sys.exit(0 if main() else 1)

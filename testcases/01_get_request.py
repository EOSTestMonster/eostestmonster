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
from subprocess import Popen, PIPE 
import traceback
import multiprocessing
from decimal import Decimal, getcontext



#get info 

def get_info():
    cmdline = "cleos get info"
    process = Popen(cmdline, stdout=PIPE, stderr=PIPE,shell=True)
    stdout, stderr = process.communicate()
    if stdout:
        print(f'{cmdline} ===========================  ok')
        return True
    if stderr:
        print(f'{cmdline} =========================== fail')
        print(stderr)
        return False 

#transfer
def transfer():
    account1_balance1 = 0
    account1_balance2 = 0
    account2_balance1 = 0
    account2_balance2 = 0
    #获取转账钱的=余额
    cmdline = "cleos get currency balance eosio.token zhangshiqi12"
    process = Popen(cmdline, stdout=PIPE, stderr=PIPE,shell=True)
    stdout, stderr = process.communicate()
    if stdout:
        print(f'{cmdline} ===========================  ok')
        account1_balance1 = stdout
        print("account1_balance1 ==",account1_balance1)
    if stderr:
        print(f'{cmdline} =========================== fail')
        print(stderr)
    
    cmdline = "cleos get currency balance eosio.token zhangshiqi11"
    process = Popen(cmdline, stdout=PIPE, stderr=PIPE,shell=True)
    stdout, stderr = process.communicate()
    if stdout:
        print(f'{cmdline} ===========================  ok')
        account2_balance1 = stdout
        print("account2_balance1 ==",account2_balance1)
    if stderr:
        print(f'{cmdline} =========================== fail')
        print(stderr)
    #执行转账
    cmdline2 = 'cleos transfer zhangshiqi12 zhangshiqi11 \"2.0000 EOS\" '
    process = Popen(cmdline2, stdout=PIPE, stderr=PIPE,shell=True)
    stdout, stderr = process.communicate()
    if stdout:
        print(f'{cmdline2} ===========================  ok')
    if stderr:
        print(f'{cmdline2} =========================== fail')
        print(stderr)
    time.sleep(3)
    #查看转账后的余额
    cmdline = "cleos get currency balance eosio.token zhangshiqi12"
    process = Popen(cmdline, stdout=PIPE, stderr=PIPE,shell=True)
    stdout, stderr = process.communicate()
    if stdout:
        account1_balance2 = stdout
        print("account1_balance1 ==",account1_balance2)
    if stderr:
        print(f'{cmdline} =========================== fail')
        print(stderr)

    cmdline = "cleos get currency balance eosio.token zhangshiqi11"
    process = Popen(cmdline, stdout=PIPE, stderr=PIPE,shell=True)
    stdout, stderr = process.communicate()
    if stdout:
        account2_balance2 = stdout
        print("account2_balance2 ==",account2_balance2)
    if stderr:
        print(f'{cmdline} =========================== fail')
        print(stderr)
    #判断是否与预期相等
    #if (int(account1_balance1)- int(account1_balance2)) == (int(account2_balance2) - int(account2_balance1)):
    #    print(f'{cmdline2} ===========================  ok')
    #else:
    #    print(f'{cmdline2} ===========================  fail')

#system contract
def system_contract():
    #reprod
    cmdline = "cleos system regproducer zhangshiqi11 EOS5NKY5vhyqWNgKeNbiUx2iC6cEnooiQsYQMjCmFFMoVLUExGHba https://www.eos.store 900"
    process = Popen(cmdline, stdout=PIPE, stderr=PIPE,shell=True)
    time.sleep(2)
    cmdline1 = "cleos get table eosio eosio producers -l 100"
    process = Popen(cmdline1, stdout=PIPE, stderr=PIPE,shell=True)
    stdout, stderr = process.communicate()
    if stdout:
        result = json.loads(stdout)
        pro = result['rows']
        for i in pro:
             if i['owner'] == 'zhangshiqi11':
                 print(f'{cmdline} =========================== ok')
                 res = True
    if stderr:
        print(f'{cmdline} =========================== fail')
        print(stderr)
        res = False 
    
    cmdline = "cleos system unregprod zhangshiqi11"
    process = Popen(cmdline, stdout=PIPE, stderr=PIPE,shell=True)
    time.sleep(2)
    cmdline1 = "cleos get table eosio eosio producers -l 100"
    process = Popen(cmdline1, stdout=PIPE, stderr=PIPE,shell=True)
    stdout, stderr = process.communicate()
    if stdout:
        result = json.loads(stdout)
        pro = result['rows']
        for i in pro:
            if i['owner'] == 'zhangshiqi11':
                print(f'{cmdline} =========================== ok')
                res = True
    if stderr:
        print(f'{cmdline} =========================== fail')
        print(stderr) 
        res = False 
    return res    

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
    get_info()
    system_contract()
    transfer()
    print('Get params:', sys.argv[0], param_str)
    return True

if __name__ == '__main__':
    sys.exit( 0 if main() else 1)

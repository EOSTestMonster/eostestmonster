#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from __future__ import unicode_literals
import os
import sys
import time
import json
import string
import requests
import argparse
import random
from subprocess import Popen, PIPE 
import traceback
import multiprocessing
from decimal import Decimal, getcontext


#creator = 'zhangshiqi12'
#creator = sys.argv[1]
#chain_id = sys.argv[4]
def account_random():
    seed = "12345abcdefghijklmnopqrstuvwxyz"
    sa = []
    for i in range(12):
        sa.append(random.choice(seed))
    res = ''.join(sa)
    return res

#get info 
def get_info(chain_id):
    cmdline = "cleos get info"
    process = Popen(cmdline, stdout=PIPE, stderr=PIPE,shell=True)
    stdout, stderr = process.communicate()
    if stdout:
        param = json.loads(stdout)
        print('param:',param)
        if param['chain_id'] == chain_id:
            print(f'chain_id is right')
            return True
        else:
            print(f'chain_id is wrong')
            return False
    if stderr:
        print(f'{cmdline} =========================== fail')
        print(stderr)
        return False 

#transfer
def transfer(params):
    account1_balance1 = 0
    account1_balance2 = 0
    account2_balance1 = 0
    account2_balance2 = 0
    #创建一个账户
    #newaccount = account_random()
    creator = params["creator"]
    newaccount = params["newaccount"]
    print('creator:',creator)
    print('new account :',newaccount)
    #cmdline = f'cleos system newaccount --stake-net \"5 EOS\" --stake-cpu \"5 EOS\" --buy-ram \"2 EOS\"  {creator} {newaccount}   '
    #process = Popen(cmdline, stdout=PIPE, stderr=PIPE,shell=True)
    #time.sleep(1)
    #cmdlinel = f"cleos get account {newaccount}"
    #process = Popen(cmdlinel, stdout=PIPE, stderr=PIPE,shell=True)
    #stdout, stderr = process.communicate()
    #if stdout:
    #    print(f'{cmdline} ===========================  ok')
    #if stderr:
    #    print(f'{cmdline} =========================== fail')
    #    print(stderr)
    
    #获取转账钱的=余额
    cmdline = f"cleos get currency balance eosio.token {creator}"
    process = Popen(cmdline, stdout=PIPE, stderr=PIPE,shell=True)
    stdout, stderr = process.communicate()
    if stdout:
        print(f'{cmdline} ===========================  ok')
        account1_balance1 = stdout
        print("account1_balance1 ==",account1_balance1)
    if stderr:
        print(f'{cmdline} =========================== fail')
        print(stderr)
    
    cmdline = f"cleos get currency balance eosio.token  {newaccount} "
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
    cmdline2 = f'cleos transfer {creator} {newaccount}  \"2.0000 EOS\" '
    process = Popen(cmdline2, stdout=PIPE, stderr=PIPE,shell=True)
    
    time.sleep(3)
    #查看转账后的余额
    cmdline = f"cleos get currency balance eosio.token {creator} "
    process = Popen(cmdline, stdout=PIPE, stderr=PIPE,shell=True)
    stdout, stderr = process.communicate()
    if stdout:
        account1_balance2 = stdout
        print("account1_balance1 ==",account1_balance2)
    if stderr:
        print(f'{cmdline} =========================== fail')
        print(stderr)

    cmdline = f"cleos get currency balance eosio.token {newaccount}"
    process = Popen(cmdline, stdout=PIPE, stderr=PIPE,shell=True)
    stdout, stderr = process.communicate()
    if stdout:
        account2_balance2 = stdout
        print("account2_balance2 ==",account2_balance2)
    if stderr:
        print(f'{cmdline} =========================== fail')
        print(stderr)
    #判断是否与预期相等
    if (float(account1_balance1[:-4])- float(account1_balance2[:-4])) == (float(account2_balance2[:-4]) - float(account2_balance1[:-4])):
        print(f'{cmdline2} ===========================  ok')
    else:
        print(f'{cmdline2} ===========================  fail')

#system contract
def system_contract(params):
    #reprod
    newaccount= params["newaccount"]
    bppubkey = params["bppubkey"]
    cmdline = f"cleos system regproducer {newaccount} {bppubkey} https://www.xxx.com 900"
    process = Popen(cmdline, stdout=PIPE, stderr=PIPE,shell=True)
    time.sleep(2)
    cmdline1 = "cleos get table eosio eosio producers -l 100"
    process = Popen(cmdline1, stdout=PIPE, stderr=PIPE,shell=True)
    stdout, stderr = process.communicate()
    if stdout:
        result = json.loads(stdout)
        pro = result['rows']
        for i in pro:
             if i['owner'] == newaccount:
                 print(f'{cmdline} =========================== ok')
                 res = True
    if stderr:
        print(f'{cmdline} =========================== fail')
        print(stderr)
        res = False 
    
    cmdline = f"cleos system unregprod {newaccount}"
    process = Popen(cmdline, stdout=PIPE, stderr=PIPE,shell=True)
    time.sleep(2)
    cmdline1 = "cleos get table eosio eosio producers -l 100"
    process = Popen(cmdline1, stdout=PIPE, stderr=PIPE,shell=True)
    stdout, stderr = process.communicate()
    if stdout:
        result = json.loads(stdout)
        pro = result['rows']
        for i in pro:
            if i['owner'] == newaccount:
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
    print('Get params:', sys.argv[0], param_str)
    res = get_info(param_dict["chain_id"])
    if not res:
        return False
    system_contract(param_dict)
    transfer(param_dict)
    return True

if __name__ == '__main__':
    sys.exit( 0 if main() else 1)

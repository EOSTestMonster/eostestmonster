# eostestmonster
Collection of EOSIO function testcase scripts from the community.

Main functionatily of this project is to test the function of the eosio-mainnet conveniently.

We choose to use **Python3** for future.

[点击查看中文](README_CN.md)

## Principle

`startmonster.py` will call in a loop and merge common_params with the param specified by testcase, stored in a file in the ./tmp directory, passed as the first argument when calling cmdline, and then parsed through the program in the testcase folder.

Steps:

1. Add testcase information and the corresponding parameters in config.json

2. Create the function you want to test in the `testcases/` folder.

   Demo `config.json`:

   ```
   {
     "common_params": {
       "nodeos_url": "http://127.0.0.1:8888",
       "wallet_url": "http://127.0.0.1:9800",
       "exist_account": "eosttmonster",
       "exist_acct_active_pub": "EOS8TfBSfwjPeKCgUfCCEfJPx1UhP2CS1Xh8xoYoELtkQJQ9g99vP",
       "exist_acct_active_pri": "5KdJZv62ZKzxhasNSojk7gC712pF9sRad4KhVyugg442qYvhWYw",
       "req_timeout": 3
     },
     "testcases": [
       {
         "casename": "Testcase Demo",
         "pre_call": "echo 'This is called BEFORE cmdline call'",
         "post_call": "echo 'This is called AFTER cmdline call'",
         "stoponfail": "true",
         "cmdline": "python testcases/testcasedemo.py",
         "params": {
           "demo_param1": "demo_param1",
           "demo_param2": 100
         }
       }
     ]
   }
   ```

3. run startmoster.py

   ```
   python3 ./startmoster.py
   ```

![image](./image/startmonster.png)

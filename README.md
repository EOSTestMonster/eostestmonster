# eostestmonster
Collection of EOSIO function testcase scripts from the community

如果增加testcase，只需要在 config.json 里面添加testcase信息，以及对应参数，startmonster.py 会轮着调用，并把 common_params 和 这个testcase指定的param合并，存储到./tmp目录下面一个文件，在调用 cmdline 时作为第一个参数传递进去，然后再testcase的程序里面解析就行。




![image](./image/config.png)
![image](./image/startmonster.png)

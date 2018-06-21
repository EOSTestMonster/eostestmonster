#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
描述: 默认的日志调用

如果你需要调整log输出的格式,你可以修改logging.conf文件,或者新建一个配置文件,然后再根据需求来设置不同的输出,你也可以在你需要修改的页面中重新覆盖logging,然后自己调用不同的log配置.

Description: default log config

If you need to adjust the format of the log output, you can modify the logging.conf file, or create a new configuration file, and then set different output according to requirements. You can also rewrite logging in the page you need to modify, and then call it yourself in current file.
"""

import logging
from os import path
from logging.config import fileConfig

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
fileConfig(log_file_path)
logger = logging.getLogger(__name__)

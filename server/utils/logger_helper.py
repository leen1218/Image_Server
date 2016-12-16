# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 en li. All rights reserved.
#
# @author: En Li <hunterli1218@gmail.com>
# Created on  Nov 17, 2016
#

import os
import inspect
import logging
from logging import Logger
from logging.handlers import TimedRotatingFileHandler

#for test

def init_logger(logger_name):
    if logger_name not in Logger.manager.loggerDict:
        logger1 = logging.getLogger(logger_name)
        # logger1.setLevel(logging.INFO)  # 设置最低级别
        logger1.setLevel(logging.DEBUG)  # 设置最低级别
        df = '%Y-%m-%d %H:%M:%S'
        format_str = '[%(asctime)s]: %(name)s %(levelname)s %(lineno)s %(message)s'
        formatter = logging.Formatter(format_str, df)
        # handler all
        try:
            alllogfilepath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../log/all.log'
            print alllogfilepath
            handler1 = TimedRotatingFileHandler(alllogfilepath, when='D', interval=1, backupCount=7)
        except Exception:
            print 'No log file all.log find!'
        handler1.setFormatter(formatter)
        handler1.setLevel(logging.DEBUG)
        logger1.addHandler(handler1)
        # handler error
        try:
            errorlogfilepath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../log/error.log'
            print errorlogfilepath
            handler2 = TimedRotatingFileHandler(errorlogfilepath, when='D', interval=1, backupCount=7)
        except Exception:
            print 'No log file error.log find!'
        handler2.setFormatter(formatter)
        handler2.setLevel(logging.ERROR)
        logger1.addHandler(handler2)

        # console
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        # 设置日志打印格式
        console.setFormatter(formatter)
        # 将定义好的console日志handler添加到root logger
        logger1.addHandler(console)

    logger1 = logging.getLogger(logger_name)
    return logger1


logger = init_logger('runtime-log')

if __name__ == '__main__':
    logger.debug('test-debug')
    logger.info('test-info')
    logger.warn('test-warn')
    logger.error('test-error')

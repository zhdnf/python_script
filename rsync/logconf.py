#!/usr/bin/env python
# coding:utf-8

"""logconf.py -- log module"""

import logging
from logging.config import dictConfig
import time

class LogConf(object):
    def __init__(self, path):
        """采用字典方式配置logging的配置，下面初始化的内容既是配置参数"""
        self.logging_config = dict(
            version=1,
            formatters={
                'DiggerFormatter': {
                    'format': '%(asctime)s [%(threadName)s] %(levelname)s %(module)s - %(message)s',
                    'datefmt': '%y-%m-%d.%H:%M:%S',
                }
            },
            handlers={
                'UpdateHandler': {
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'filename': path,
                    'when': 'midnight',
                    'backupCount': 30,
                    'encoding': None,
                    'delay': False,
                    'utc': False,
                    'level': logging.INFO,
                    'formatter': 'DiggerFormatter'
                },
                'ErrorHandler': {
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'filename': path,
                    'when': 'midnight',
                    'backupCount': 30,
                    'encoding': None,
                    'delay': False,
                    'utc': False,
                    'level': logging.INFO,
                    'formatter': 'DiggerFormatter'
                }

            },
            loggers={
                'UpdateLogger': {
                    'level': 'INFO',
                    'handlers': ['UpdateHandler'],
                    'propagate': False
                },

                'ErrorLogger': {
                    'level': 'ERROR',
                    'handlers': ['ErrorHandler'],
                    'propagate': False
                }
            }
        )
        dictConfig(self.logging_config)

    def logger_update(self):
        dictConfig(self.logging_config)
        return logging.getLogger('UpdateLogger')
    
    def logger_error(self):
        dictConfig(self.logging_config)
        return logging.getLogger('ErrorLogger')


if __name__ == '__main__':
    abc = LogConf('/export/rsync/update.log')

#!/usr/local/python/bin
# coding=utf-8

__status__ = "Development"

__all__ = ['set_logger', 'debug', 'info', 'warning', 'error',
           'critical', 'exception']

import os
import sys
import logging

# Color escape string
COLOR_RED = '\033[1;31m'
COLOR_GREEN = '\033[1;32m'
COLOR_YELLOW = '\033[1;33m'
COLOR_BLUE = '\033[1;34m'
COLOR_PURPLE = '\033[1;35m'
COLOR_CYAN = '\033[1;36m'
COLOR_GRAY = '\033[1;37m'
COLOR_WHITE = '\033[1;38m'
COLOR_RESET = '\033[1;0m'


STYLE_DEBUG = '\033[1;34m'
STYLE_INFO = '\033[1;36m'
STYLE_WARNING = '\033[4;31m'
STYLE_CRITICAL = '\033[1;41;33m'
# Define log color
LOG_COLORS = {
    'DEBUG': STYLE_DEBUG + '%s' + COLOR_RESET,
    'INFO': STYLE_INFO + '%s' + COLOR_RESET,
    'WARNING': STYLE_WARNING + '%s' + COLOR_RESET,
    'ERROR': STYLE_CRITICAL + '%s' + COLOR_RESET,
    'CRITICAL': STYLE_CRITICAL + '%s' + COLOR_RESET,
    'EXCEPTION': STYLE_CRITICAL + '%s' + COLOR_RESET,
}

# Global logger
g_logger = None
class ColoredFormatter(logging.Formatter):
    '''A colorful formatter.'''

    def __init__(self, fmt=None, datefmt=None):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        level_name = record.levelname
        msg = logging.Formatter.format(self, record)

        return LOG_COLORS.get(level_name, '%s') % msg

def add_handler(cls, level, fmt, colorful, **kwargs):
    '''Add a configured handler to the global logger.'''
    global g_logger

    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.DEBUG)

    handler = cls(**kwargs)
    handler.setLevel(level)

    if colorful:
        formatter = ColoredFormatter(fmt)
    else:
        formatter = logging.Formatter(fmt)

    handler.setFormatter(formatter)
    g_logger.addHandler(handler)

    return handler

def add_streamhandler(level, fmt):
    '''Add a stream handler to the global logger.'''
    return add_handler(logging.StreamHandler, level, fmt, os.name != 'nt')

def init_logger():
    '''Reload the global logger.'''
    global g_logger

    if g_logger is None:
        g_logger = logging.getLogger()
    else:
        logging.shutdown()
        g_logger.handlers = []

    g_logger.setLevel(logging.DEBUG)

def set_logger(filename=None, mode='a', level='ERROR',
               fmt='[%(levelname)s] %(asctime)s %(message)s',
               backup_count=5, limit=20480, when=None):
    '''Configure the global logger.'''
    s_level = ''
    if len(level) == 1:  # Both set to the same level
        s_level = level

    init_logger()
    add_streamhandler(s_level, fmt)
    # Import the common log functions for convenient
    import_log_funcs()

def import_log_funcs():
    '''Import the common log functions from the global logger to the module.'''
    global g_logger

    curr_mod = sys.modules[__name__]
    log_funcs = ['debug', 'info', 'warning', 'error', 'critical',
                 'exception']

    for func_name in log_funcs:
        func = getattr(g_logger, func_name)
        setattr(curr_mod, func_name, func)

# Set a default logger
set_logger(level='DEBUG',
           fmt='[%(filename)s:+%(lineno)d | %(asctime)s] ** %(levelname)8s ** : %(message)s')
if __name__ == '__main__':
    debug('hello, world')
    info('hello, world')
    warning('hello, world')
    error('hello, world')
    critical('hello, world')
    pass

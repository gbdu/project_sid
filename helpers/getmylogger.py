"""
Returns a logger right away
    ~ gbdu
"""

__author__ = 'gbdu'
__copyright__ = "Copyright 2015, gbdu"
__credits__ = ["gbdu"]
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "ogrum@live.com"
__status__ = "dev"

import logging

formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(name)s:%(lineno)d} %(levelname)s - %(message)s','%H:%M:%S')

def silent_logger(name):
    """use for high/busy logs"""
    l= logging.getLogger(name)
    hdlr = logging.FileHandler('logs/' + name)
    hdlr.setFormatter(formatter)
    l.addHandler(hdlr)
    return l

def loud_logger(name):
    """use for less busy logs..."""
    logger = logging.getLogger(name)
    hdlr = logging.FileHandler('logs/' + name)
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

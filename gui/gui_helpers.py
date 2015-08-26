"""
A few functions to help create a pygame and init a font

---- init_pygame()
---- create_font()

"""

__author__ = 'gbdu'
__copyright__ = "Copyright 2015, gbdu"
__credits__ = ["gbdu"]
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "ogrum@live.com"
__status__ = "dev"

try:
        import pygame
        import os,sys

except ImportError as e:
        print "Couldnt load sys files from gui_helpers.py"
        print e
        raise e
try:
        #from helpers.getmylogger import loud_logger,silent_logger
        from helpers.getmylogger import silent_logger,loud_logger

except ImportError as e:
        print "Couldn't load internal stuff from gui_helpers.py"
        print e
        raise e

logger = loud_logger("gui_helpers")

def init_pygame():
        '''init pygame and return a seeen object'''
        try:
                pygame.init()
                screen = pygame.display.set_mode((640, 480))
                logger.info("screen initd")
                return screen
        except :
                logger.error("unable to init screen")
                exit(1)


def create_font(name="default.ttf",size=8):
        '''
        returns a font from pygame.font.Font() using the
        "resources/fonts/(name)" dir,
        name -- name of font in resources/fonts, defaults to "default.ttf"
        '''
        try:
                wk_dir = os.path.dirname(os.path.realpath('__file__'))
                font_dir = os.path.join(wk_dir, "resources/fonts/" )
                font_path = os.path.join(font_dir, name)
                font = pygame.font.Font(font_path, size)
                return font
        except IOError as e:
                print font_path
                logger.error("unable to create font... %s " , sys.exc_info()[0])
                raise e
        except:
                logger.error("unable to create error for unkown reason: %s ", sys.exc_info()[0])
                raise e
                return None

def log(msg, log=None, console=None): # visual log that also goes to user console
        if console:
            console.out(msg)
        if log:
                log.info(msg)

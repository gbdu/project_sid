import pygame
from pyconsole import Console
import os,sys
import getmylogger

logger = getmylogger.loud_logger("gui_helpers")

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
                
                
def create_font():
        try:
                wk_dir = os.path.dirname(os.path.realpath('__file__'))
                font_dir = os.path.join(wk_dir, "fonts")
                font = pygame.font.Font(os.path.join(font_dir, "forb.ttf"), 8)
                return font
        except:
                logger.error("unable to create font... %s " , sys.exc_info()[0])
                exit(1)
        pass


def log(msg, log=None, console=None): # visual log that also goes to user console
        if console:
            console.out(msg)
        if log:
                log.info(msg)
                
__author__ = 'gargantua'

import time
from numpy import *

class component:
    thread_id = None
    alive = False # Component state
    myinput = None
    MyRef = None

    def __init__(self, id, type):
        self.type = type
        self.thread_id = id
        self.MyRef = self

        if(type == "audio"):
            self.myinput = array(1024) # input is 153600 matrix
        elif(type == "video"):
            self.myinput = array((480, 320)) # input is 153600 matrix
        elif(type == "langu"):
            self.myinput = array(1024) # text to process...
        else: # must be x type...
            self.myinput = array (10)

    def __call__(self, *args, **kwargs):
        self.alive = True
        self.run()
        return

    def die(self):
        alive = False
        return

    def read_user_input(self):
        print (self.user_input_message)
        pass

    def run(self):
        while True :
            if self.alive:
                # say hi and sleep for a sec
                pass
            else:
                print ("component thread " + thread_id + " terminated")
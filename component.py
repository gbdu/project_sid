__author__ = 'gargantua'

import time
from numpy import *

class component:
    thread_id = None
    alive = False # Component state

    # TODO: multiple layers of neurons here, to process input
    #

    MyRef = None

    def __init__(self, id):
        self.thread_id = id
        self.MyRef = self

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
                self.myinput = array((480, 320)) # input is 153600 matrix
            else:
                print ("component thread " + thread_id + " terminated")
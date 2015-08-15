import numpy

__author__ = 'gargantua'

import threading

import numpy

class component:
    thread_id = None
    alive = False  # Component state
    myinput = None
    MyRef = None

    # REMEMBER: THESE ARE RUN AS ASYNCH THREADS
    # EACH COMPONENT IS CREATED AS A THREAD
    # t_id is the python thread id in case needed
    def __init__(self, type, t_id):
        self.type = type # a string of type hints, current: langu,audio,video
        self.thread_id = t_id
        self.MyRef = self

        print "I am %d" %t_id

        if (type == "audio"):  # these are numpy arrays
            self.myinput = numpy.array(1024)  # input is 153600 matrix
        elif (type == "video"):
            self.myinput = numpy.array((480, 320))  # input is 153600 matrix
        elif (type == "langu"):
            self.myinput = numpy.array(1024)  # text to process...
        else:  # must be x type...
            self.myinput = numpy.array(10)

    def __call__(self, *args, **kwargs):
        self.alive = True
        self.run()
        return

    def die(self):
        alive = False
        return

    def read_user_input(self):
        pass

    def run(self):
        while True:
            if self.alive:
                # say hi and sleep for a sec
                pass
            else:
                pass
                # print ("component thread " + thread_id + " terminated")

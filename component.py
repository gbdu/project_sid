__author__ = 'gargantua'

import numpy
import random
import threading
import numpy

class component:
    alive = False  # Component state
    myinput = None
    MyRef = None

    # REMEMBER: THESE ARE RUN AS ASYNCH THREADS
    # EACH COMPONENT IS CREATED AS A THREAD
    # t_id is the python thread id in case needed
    def __init__(self, type):
        #innit all data types, this is not running yet
        self.type = type # a string of type hints, current: langu,audio,video
        if (type == "audio"):  # these are numpy arrays
            self.myinput = numpy.array(1024)  # input is 153600 matrix
        elif (type == "video"):
            self.myinput = numpy.array((480, 320))  # input is 153600 matrix
        elif (type == "langu"):
            self.myinput = numpy.array(1024)  # text to process...
        else:  # must be x type...
            self.myinput = numpy.array(10)


    def set_thread(self, mid):
        self.thread_id = mid
        self.alive = True
        return mid

    def get_color_dim(self):
        pass


    def run(self):
        self.alive = True
        print "Thread:%s" % (self.thread_id)
        return

    def get_color_dim(self):
	    # return a random color

	    r = random.randint(0, 255)
	    g = random.randint(50, 255)
	    b = random.randint(40, 255)

	    return (r,g,b)

    def die(self):
        alive = False
        return

    def read_user_input(self):
        pass


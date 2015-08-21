__author__ = 'gargantua'

import numpy
import random
from multiprocessing import Process, Value
import numpy
from time import sleep
import logging

formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(name)s:%(lineno)d} %(levelname)s - %(message)s','%H:%M:%S')

logger = logging.getLogger("component")
hdlr = logging.FileHandler('logs/component')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
# logger.setLevel(logging.DEBUG)
# ch = logging.StreamHandler()
# ch.setFormatter(formatter)
# logger.addHandler(ch)


class component:
    ''' an octo is an 8 channel parallel (list of 8 floats from numpy)
            perform thread synch when playing with it
    '''

    octo_layer_average = []
    mystate = None
    mypipe = None
    mycolor = None
    
    def init_data(self, hints):
        '''inits the internal data stream, these are numpy arrays'''
        if (hints == "audio"):
            # 8 layers of 8192 (2^13) = 65536 (2^16)
            self.mydatastream = numpy.zeros((8, 8192))
        elif (hints == "video"):
            # input is 153600 matrix
            self.mydatastream = numpy.zeros((8, 8192))
        elif (hints == "langu"):
            self.mydatastream = numpy.zeros((8, 8192))  # text to process...
        else:  # must be x type...
            self.mydatastream = numpy.zeros((8, 8192))
            
        self.mycolor = [random.randint(0, 100), random.randint(40, 150),
                        random.randint(40, 150)]
        return
    
    
    # todo: components that fire together wire together
    
    def __init__(self, global_state, component_state, pipe, type_hints):
        self.type_hints = type_hints
        self.state = component_state
        self.mypipe = pipe
        self.global_state = global_state
        self.init_data(type_hints)

    def OctoChannel_layer_average(self):
        if(self.mydatastream.any()):
            return numpy.mean(self.mydatastream)
        else:
            print "none set yet"
        return 0

    def get_input(self):
        # if self.type_hints == "rand":
        #self.mydatastream = numpy.fromfile()
        pass

    def _get_color_dim(self):
        '''returns a random color for now....'''
        # return a random color
#		avg = self.OctoChannel_layer_average()
        
        r = self.mycolor[0]
        g = self.mycolor[1]
        b = self.mycolor[2]
        
        if r >= 254:
            r = 100;
        
        if g >= 254:
            r = 150;
        
        if b >= 254:
            r = 150;
        
        self.mycolor = [r, g, b]
        return self.mycolor

    def send_octo(self, connection):
        '''send an 8 channel list representing current state of component'''
        octo = [self._get_color_dim(), 2, 3, 4, 5, 6, 7, 8 ]
        connection.send(octo)
        
    def live_loop(self):
        '''loop repeatedly until global_state is not 1'''
        
        while self.global_state.value == 1:
            if self.state.value == 1:
                self.get_input()  # get a new data frame for this run
                self.send_octo(self.mypipe)
                sleep(1)
            else:
                # the component is not in a running state, do nothing
                sleep(5)
        
        self.mypipe.close()
        
        return

        
    def read_user_input(self):
        pass

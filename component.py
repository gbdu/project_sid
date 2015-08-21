__author__ = 'gargantua'

import numpy
import random
from multiprocessing import Process, Value, Lock
import numpy
from time import sleep
import logging
from neuron import Neuron
import getmylogger

log = getmylogger.loud_logger("component")

def error(n):
    log.exception(RuntimeError(n))
    raise(RuntimeError(n))

DEFAULT_NEURONS_PER_LAYER = 16384
DEFAULT_LAYERS_FOR_EACH_TYPE = 8

class component:
    ''' an octo is an 8 channel parallel (list of 8 floats from numpy)
            perform thread synch when playing with it
    '''

    octo_layer_average = []
    mystate = None # You get this from parent
    mypipe = None # You get this from parent
    mycolor = None # You give this to parent
    
    mymolecules = None # Internal list of neurotransmitter-like communication
    
    def _create_molecules(self):
        '''returns a list of molecules for internal use'''
        molecules = {}
        for name in get_molecule_list():
            molecules[name] = (Lock(), random.randint(40, 100000))
        
        return molecules
        
    def create_default_neuron_layer(self, size):
        """returns a default, basic neuron layer"""
        if not self.mymolecules:
            log.exception("need to set neurotransmitters first!")
            raise(RuntimeError("no internal mymolecules list"))
        
        l = [ Neuron(self.mymolecules) for x in range(size)]
        return l
        
    def create_get_default_layers(self):
        l = []
        # Create 8 layers of 128^2 neurons
        for i in DEFAULT_LAYERS_FOR_EACH_TYPE:
            for j in DEFAULT_NEURONS_PER_LAYER:
                l.append(self.create_default_neuron_layer(DEFAULT_NEURONS_PER_LAYER))
        
        return l
    
    def get_audio_layers(self):
        pass
    
    def create_layers(self):
        if not self.hints:
            error("no hints set on this component... cannnot create layers")
            
            
        
    def init_data(self, hints):
        '''inits the internal data stream, these are numpy arrays'''
        
        self.mylayers = self.create_layers()
            
        self.mycolor = [random.randint(0, 100), random.randint(40, 150),
                        random.randint(40, 150)]
        return
    
    
    # todo: components that fire together wire together
    
    def __init__(self, global_state, component_state, pipe, type_hints):
        # from parent:
        self.type_hints = type_hints
        self.state = component_state
        self.mypipe = pipe
        self.global_state = global_state
        
        #internal:
        self.mymolecules = _create_molecules()
        
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

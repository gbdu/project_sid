__author__ = 'gargantua'

import random
from multiprocessing import Process, Value, Lock
from time import sleep
from neuron import Neuron
import getmylogger

log = getmylogger.silent_logger("component")

def error(n):
    log.exception(RuntimeError(n))
    raise(BadValue(n))

DEFAULT_NEURONS_PER_LAYER = 8
DEFAULT_LAYERS_FOR_EACH_TYPE = 256

class component:
    ''' an octo is an 8 channel parallel (list of 8 floats from numpy)
            perform thread synch when playing with it
    '''

    octo_layer_average = []
    mystate = None # You get this from parent
    mypipe = None # You get this from parent
    mycolor = None # You give this to parent
    mynumber = None # You get this from parent
    
    #internal:
    mymolecules = None # Internal list of neurotransmitter-like communication
    mylayers = None # a list of neurons + their neurotransmitters
    
    def get_molecule_list(self):
        return ["dopamine", "beans", "potato", "from component"]
    
    
    def create_molecule_pool(self):
        '''returns a list of molecules for internal use'''
        
        molecules = {}
        for name in self.get_molecule_list():
            molecules[name] = (Lock(), random.randint(40, 100000)) #random molecules for each layers 
        
        return molecules
        
    def create_default_neuron_layer(self, size, molecule_pool):
        """returns a default, basic neuron layer"""
        if not molecule_pool:
            error("need to set neurotransmitters first!")
        
        
        l = []
        for i in range(size):
            new_neuron = Neuron(molecule_pool, l)
            l.append(new_neuron)
            
        return l
        
    def create_layers(self):
        l = []
        # Create 8 layers of 128^2 neurons
        for i in range(DEFAULT_LAYERS_FOR_EACH_TYPE):
            for j in range(DEFAULT_NEURONS_PER_LAYER):
                #log.info("created layer")
                new_pool = self.create_molecule_pool()
                new_layer = self.create_default_neuron_layer(DEFAULT_NEURONS_PER_LAYER, new_pool)
                
                l.append(new_layer)
        return 
        
        log.info("created layers")
            
        
    def init_layers(self, hints):
        '''inits the internal data stream, these are numpy arrays'''
        log.info("setting the data for component with hints %s", hints)
        
        self.mylayers = self.create_layers()
        
        log.info("layers created ")
        
        
        return
    
    

    
    def __init__(self, global_state, component_state, pipe, type_hints="audio", mynumber=0):
        # from parent:
        self.type_hints = type_hints
        self.state = component_state
        self.mypipe = pipe
        self.mynumber = mynumber
        self.global_state = global_state
        self.mycolor = [random.randint(0, 100), random.randint(40, 150),
                        random.randint(40, 150)]
        
        #internal:
        self.init_layers(type_hints)
         
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
                log.info("COMPONENT %d RAN!", self.mynumber)
            else:
                # the component is not in a running state, do nothing
                sleep(5)
        
        self.mypipe.close()
        
        return

        
    def read_user_input(self):
        pass

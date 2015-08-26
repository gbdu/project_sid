"""

AI component object, ran as a single asynch process to compute data streams
Thing of it as a region in the brain. All components run asynchronously from
one another.
    ~ gbdu

"""

__author__ = 'gbdu'
__copyright__ = "Copyright 2015, gbdu"
__credits__ = ["gbdu"]
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "ogrum@live.com"
__status__ = "dev"

import random
from multiprocessing import Process, Value, Lock
from time import sleep

try :
    from neuron import Neuron
    from helpers.getmylogger import loud_logger,silent_logger

except ImportError as e:
    print "Could not import from component"
    print e
    raise e

log = silent_logger("component")

def error(n):
    log.exception(RuntimeError(n))
    raise(BadValue(n))

DEFAULT_NEURONS_PER_LAYER = 8
DEFAULT_NUMBER_OF_LAYERS = 8

class component:
    ''' an octo is an 8 channel parallel (list of 8 floats from numpy)
            perform thread synch when playing with it
    '''

    octo_layer_average = []
    mystate = None # You get this from parent
    mycolor = (0,0,0) # You give this to parent
    mynumber = None # You get this from parent
    myid = None # You get this from parent
    mysource = "None so far..."
    #internal:
    mymolecules = None # Internal list of neurotransmitter-like communication
    layers = [ ] # a list of neurons + their neurotransmitters
    myfriends = [] # a list of friend IDS

    def add_friend(self, friendid):
        if friendid in self.myfriends:
            return False

        self.myfriends.append(friendid)
        log.info("friend added")
        #print self.get_octo()

    def get_molecule_list(self):
        return ["dopamine", "beans", "potato", "from component"]


    def create_molecule_pool(self):
        '''returns a list of molecules for internal use'''

        molecules = {}
        for name in self.get_molecule_list():
            molecules[name] = (Lock(), random.randint(40, 100000)) #random molecules for each layers

        return molecules




    def init_layers(self, hints):
        '''inits the internal data stream, these are numpy arrays'''
        #log.warning("setting the data for component with hints %s", hints)
        #self.mylayers = self.create_layers()
        #log.warning("layers created ")

        molecule_pool = {"dopamine":10, "serotonin":20}


        for l in range(DEFAULT_NUMBER_OF_LAYERS):
            for n in range(DEFAULT_NEURONS_PER_LAYER):
                self.layers.append( Neuron() )

        #return 1
        pass


    def get_id(self):
        return self.myid

    def __init__(self, global_state, type_hints="langu", myid=0):
        # from parent:
        self.type_hints = type_hints
        self.mystate = Value("d", 1)
        self.myid = myid
        self.global_state = global_state
        self.myfriends = [ ]
        self.mycolor = (random.randint(0, 100), random.randint(40, 150),
                        random.randint(40, 150))

        #internal:
        self.init_layers(type_hints)
    def OctoChannel_layer_average(self):
        if(self.mydatastream.any()):
            return numpy.mean(self.mydatastream)
        else:
            print "none set yet"
        return 0

    def get_input(self):
        '''reads from data stream...'''

        ## For now just change the octo randomly...

        pass

    def _get_color_dim(self):
        '''returns a random color for now....'''
        return (200,0,0)

    def get_octo(self):
        '''send an 8 channel list representing current state of component'''

        octo = {
            "type_hints": self.type_hints,
            "mycolor":self.mycolor,
            "source":self.mysource,
            "id": self.myid,
            "friends":self.myfriends,
            "layers":self.layers,
            "neurons_per_layer":7,
            "eight":8
        }

        return octo

    def live_loop(self):
        '''loop repeatedly until global_state is not 1'''

        while self.global_state.value == 1:
            if self.mystate.value == 1:
                self.get_input()  # get a new data frame for this run
                sleep(1)
                log.warning("COMPONENT %d RAN!", self.mynumber)
            elif self.mystate.value == 0:
                #self.clean()
                return
            else:
                # the component is not in a running state, do nothing
                sleep(5)

        return

    def signal_death(self):
        self.mystate.value = 0


    def read_user_input(self):
        pass

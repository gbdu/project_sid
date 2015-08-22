# /usr/bin/python3

__author__ = 'gargantua'

from multiprocessing import Process, Pipe, Value
from component import component
import getmylogger

last_component_number = 0

log = getmylogger.silent_logger("sid")

class Sid:
    '''create 256 components, then hang and print a message every 1 sec as
    the components run'''

    # locks, myname
    mystate = Value("d", 0) # 0 for dead, 1 for alive, set by creator
    components = []
    processes = []

    def add_component(self, component_hints):
        '''add a tuple of the form (component, state, parent_pipe, child_pipe,
        hints) and append it to list components
        
        state is an integer, 0 for dead, 1 for alive
        '''
        log.info("adding component")
        a, b = Pipe() ## parent,child 
        s = Value("d", 0)
        h = component_hints
        c = component(self.mystate, s, b, component_hints, last_component_number)
        tup = (c, s, a, b, h)
        log.info("added a component with hints %s ", component_hints)
        self.components.append(tup)
        
    def get_component_tuples (self):
        '''returns a list of pipes which may be recv'd for info coming in from
        the component itself'''
        
        log.info("get components")
    
        l = []
        for c in self.components:
            l.append(c)
        
        return l

    def __init__(self):
        log.info("a new sid wants to be created")
        
        for i in range(21):
            self.add_component("langu")
        for i in range(21, 42):
            self.add_component("audio")
        for i in range(42, 63):
            self.add_component("video")
        
        log.info("a new sid is init'd")
        
    def create_process(self, c):
        '''start the asynch process and append it to list processes'''
        log.info("creating process")
        p = Process(target=c.live_loop)
        self.processes.append(p)
        p.start()

    def getname(self):
        return self.myname

    def setname(self, myn):
        self.myname = myn

    def live(self):
        '''this tells sid to live, it goes over the compnents and sets their
        states to alive and creates new processes to run them, then it waits
        for the processes to finish and dies'''
        
        log.info("living sid")
        self.mystate.value = 1 # set global state as alive
        
        for c in self.components:
            c[1].value = 1  # set shared value to 1 (indicating live)
            self.create_process(c[0])
        
        ## This is where we block:
        for p in self.processes:
            p.join() ## These will die once global state is set to 0
        
        return

    def count_human_components(self):
        return 3

    def get_media_numbers(self):
        return 0
        # todo: add code to watch media to ned

    def last_words(self):
        return "Default last word for ", self.myname


    def signal_extinguish(self):
        '''called from another process. Kill the sid, sets the global value to 0,
        then it goes over all the components and sets their state to dead. This
        will (hopefully) cause the live() loop to die and the forked processes
        to join'''
        
        self.mystate.value = 0 # set global state to dead
        
        for c in self.components:
            c[1].value = 0 # Go over all forked components and set them to dead
                            # this will (hopefully) cause their live_loop to die
        
        print self.last_words()
            

    def print_panel(self):
        sid_panel = ""
        return sid_panel

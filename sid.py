# /usr/bin/python3

__author__ = 'gargantua'

from multiprocessing import Process, Pipe, Value, Lock
from component import component
import getmylogger
import os,sys
import exceptions

last_component_number = 0

log = getmylogger.loud_logger("sid")
qlog = getmylogger.silent_logger("sid_silent")

class Sid:
    '''create 256 components, then hang and print a message every 1 sec as
    the components run'''
    
    # locks, myname
    mystate = Value("d", 0) # 0 for dead, 1 for alive, set by creator
    components = [] # alist of tuples of form  (c, s, a, b, h, l)
    processes = []

    def add_component(self, component_hints):
        '''add a tuple of the form (component, state, parent_pipe, child_pipe,
        hints) and append it to list components
        
        state is an integer, 0 for dead, 1 for alive
        '''
        
        global last_component_number
        
        # Components get their id based on the order they were added to the list...
        c = component(self.mystate, component_hints, len(self.components))
        lock = Lock()
        
        self.components.append({"component":c, "lock":lock})

    def get_component_by_id(self, c_id):
        '''returns a handle to the component object if found'''
        for i in self.components:
            if i["component"].get_id() == c_id:
                return i
        
        raise exceptions.ValueError("component not found [%d]" % c_id)
   
    def __init__(self):
        log.info("a new sid wants to be created")
        for i in range(21):
            self.add_component("langu")
        log.info("-----> (1/3) langu components added [ SUCCESS ]")
        for i in range(21):
            self.add_component("audio")
        log.info("-----> (2/3) langu components added [ SUCCESS ]")
        for i in range(22):
            self.add_component("video")
        log.info("-----> (3/3) langu components added [ SUCCESS ] ")
        
    def create_process(self, c):
        '''start the asynch process and appends it to list processes'''
        qlog.info("creating process for new sid component ... ")
        p = Process(target=c.live_loop)
        self.processes.append(p)
        p.start()
        # do not join, just return
        return
    
    def getname(self):
        return self.myname

    def setname(self, myn):
        self.myname = myn

    def live(self):
        '''this tells sid to live, it goes over the compnents and sets their
        states to alive and creates new processes to run them, then it waits
        for the processes to finish and dies'''
        
        log.info("* PROCESS living sid")
        
        self.mystate.value = 1 # set global state as alive
        
        for c in self.components:
            self.create_process(c['component'])
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
        
        log.info("got signal extinguish")
        self.mystate.value = 0 # set global state to dead
        
        for c in self.components:
            c['component'].signal_death() # Go over all forked components and set them to dead
                            # this will (hopefully) cause their live_loop to die
        
        log.info("  ----> got signal extinguish [ SUCCESS ]")
        print self.last_words()
            

    def print_panel(self):
        sid_panel = ""
        return sid_panel



if __name__ == "__main__":
    ned = Sid()  # create a new instance of our AI
    ned.setname("ned")
    ned.live()


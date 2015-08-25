# /usr/bin/python3

__author__ = 'gargantua'

import exceptions
from multiprocessing import Process, Pipe, Value, Lock
import os,sys
from time import sleep

try:
    from component import component
    from helpers import getmylogger

except ImportError as e:
    print "could not import internal from sid"
    print e
    exit(1)
last_component_number = 0

log = getmylogger.loud_logger("sid")
qlog = getmylogger.silent_logger("sid_silent")

class Sid:
    '''create 256 components, then hang and print a message every 1 sec as
    the components run'''

    # locks, myname
    mystate = Value("d", 0) # 0 for dead, 1 for alive, set by creator
    components = [] # A list of dictionaries {'component':c, 'lock'}:l
    component_friends = [] # a list of the tuples of the form (id1,id2)
    # id 1 ==
    processes = []



    def make_components_friends(self, componentid1, componentid2):
        '''componentids must be in the form of integers!'''
        self.component_friends.append((componentid1, componentid2))

    def get_component_friends(self):
        return self.component_friends

    def add_component(self, component_hints):
        '''
        add a tuple of the form (component, state, parent_pipe, child_pipe,
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
                return i

        raise exceptions.ValueError("component not found [%d]" % c_id)

    def __init__(self):
        log.info("a new sid wants to be created")
        for i in range(21):
            self.add_component("langu")
        log.info("-----> (1/3) langu components added [ SUCCESS ]")
        for i in range(21):
            self.add_component("audio")
        log.info("-----> (2/3) audio components added [ SUCCESS ]")
        for i in range(22):
            self.add_component("video")
        log.info("-----> (3/3) video components added [ SUCCESS ] ")

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

    # XXX: live loop #2, for sid
    def live_loop(self, break_flag_ref):
        '''
        this tells sid to live, it goes over the compnents and sets their
        states to alive and creates new processes to run them, then it waits
        for the processes to finish and dies
        '''

        log.info("other process entering live_loop...")
        while 1:
            if(break_flag_ref.value == -1):
                ## Slee for a bit
                sleep(2)
                continue;
            if(break_flag_ref.value == 0):
                self.mystate.value = 0
                break ;
            else:
                for c in self.components:
                    self.create_process(c['component'])

                for p in self.processes:
                    p.join() ## These will die once global state is set to 0

        log.info("other process sid live_loop exited")
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
            # Go over all forked components and set them to dead
            # this will (hopefully) cause their live_loop to die

            c['component'].signal_death()

        log.info("  ----> got signal extinguish [ SUCCESS ]")


    def print_panel(self):
        sid_panel = ""
        return sid_panel



if __name__ == "__main__":
    ned = Sid()  # create a new instance of our AI
    ned.setname("ned")
    ned.live()

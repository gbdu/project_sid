# /usr/bin/python3

__author__ = 'gargantua'

import exceptions
from multiprocessing import *
from pickle import *
from time import sleep
import sys
allow_connection_pickling
try:
    from helpers import getmylogger
    from component import component
    from helpers.octo import Octo
except ImportError as e:
    print "could not import internal from sid"
    print e
    exit(1)
last_component_number = 0

log = getmylogger.loud_logger("sid")
qlog = getmylogger.silent_logger("sid_silent")


DEFAULT_OCTO = {
    "type_hints": "DEFAULT OCTO",
    "mycolor":(100,100,100),
    "source":"DEFAULT OCTO",
    "id": 10,
    "friends":[],
    "layers":[],
    "neurons_per_layer":8,
    "eight":"DEFAULT OCTO"
}

class Sid:
    '''create 256 components, then hang and print a message every 1 sec as
    the components run'''

    # locks, myname
    components = [] # A list of component objects
    processes = []
    cid_pipes = [] #(cid,(ppipe,cpipe))
    latest_octos = {} # a list of unique Octo objects for each component

    def add_component(self, component_hints):
        '''
        add a tuple of the form (component, state, parent_pipe, child_pipe,
        hints) and append it to list components

        state is an integer, 0 for dead, 1 for alive
        '''

        global last_component_number

        # Components get their id based on the order they were added to the list...
        c = component(0, component_hints, len(self.components))

        self.components.append(c)

    def get_component_by_id(self, c_id):
        '''returns a handle to the component object if found'''
        for i in self.components:
            if i.get_id() == c_id:
                return i

        raise exceptions.ValueError("component not found [%d]" % c_id)

    def make_components_friends(self, componentid1, componentid2):
        '''componentids must be in the form of integers!'''
        a = (self.get_component_by_id(componentid1))
        b = (self.get_component_by_id(componentid2))

        a.add_friend(componentid2)
        b.add_friend(componentid1)

        #log.info("added friends %d %d" % (componentid1,componentid2))
        pass

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

    def getname(self):
        return self.myname

    def setname(self, myn):
        self.myname = myn

    # XXX: live loop 2, for sid
    def start_and_block(self, break_flag, octo_q, latest_octos):
        '''
        this tells sid to live, it goes over the compnents and sets their
        states to alive and creates new processes to run them, then it waits
        for the processes to finish and dies
        '''

        log.info("other process entering live_loop...")

        # Just create the 64 components and return...
        counter = 0

        for comp_obj in self.components:
            p = Process(target=comp_obj.live_loop, args=(break_flag, octo_q))

            self.processes.append(p)

            p.start()
            counter += 1


        log.info("sid now filling cache... ")

        while True:
            if break_flag.value == -1:
                sleep(2)
                continue

            if break_flag.value == 0:
                done = 0
                out_of = len(self.processes)
                for p in self.processes:
                    p.join()
                    done += 1
                    progress_string = ('*' * (done/3)) + ('-' * ((out_of-done)/3))  
                    progress_string += " [%d %% processes joined] \r" % int(float(done)/out_of * 100.0)
                    sys.stdout.flush()
                    sys.stdout.write(progress_string)
                print progress_string
                return

            if break_flag.value == 1:  # 1 signals "work"
                # Try to fill from queue
                if octo_q.empty():
                    sleep(1)
                    continue
                else:
                    popped = octo_q.get()
                    latest_octos[str(popped.myid)] = popped
                    log.info(popped.color)
        return




    def count_human_components(self):
        return 3

    def get_media_numbers(self):
        '''returns some stats about the sid'''
        return 0
        # todo: add code to watch media to ned

    def last_words(self):
        '''hello world'''
        return "Default last word for ", self.myname

if __name__ == "__main__":
    ned = Sid()  # create a new instance of our AI
    ned.setname("ned")
    ned.live()

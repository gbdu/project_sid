# /usr/bin/python3

__author__ = 'gargantua'

import exceptions
from multiprocessing import *
from multiprocessing import forking

from pickle import *
import os,sys
import io
from time import sleep
import cPickle as pickle

try:
    from helpers import getmylogger
    from component import component
    from helpers import getmylogger

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

    def find_octo(self, cid, pipe_list):
        # first fine the two way pipe for this component id

        for d in pipe_list:
            dc = d[0]  # the component id
            dt = d[1]  # two way pipe tuple (parent,child)
            if dc == cid:
                return dt[0].recv()
        return DEFAULT_OCTO

    # XXX: live loop 2, for sid
    def start_and_block(self, break_flag_ref, octo_q):
        '''
        this tells sid to live, it goes over the compnents and sets their
        states to alive and creates new processes to run them, then it waits
        for the processes to finish and dies
        '''

        log.info("other process entering live_loop...")

        # Just create the 64 components and return...
        counter = 0

        for comp_obj in self.components:
            p = Process(target=comp_obj.live_loop, args=(break_flag_ref, octo_q))

            self.processes.append(p)

            p.start()
            counter += 1

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

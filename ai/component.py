"""

AI component object, ran as a single asynch process to compute data streams
Thing of it as a region in the brain. All components run asynchronously from
one another.
    ~ gbdu

"""

__author__ = 'gbdu'

import random
from multiprocessing import Lock
from time import sleep

try:
    from neuron import Neuron
    from helpers.octo import Octo
    from helpers.getmylogger import silent_logger

except ImportError as e:
    print("Could not import from component")
    print(e)
    raise e

log = silent_logger("component")

DEFAULT_NEURONS_PER_LAYER = 8
DEFAULT_NUMBER_OF_LAYERS = 8


class component:

    ''' an octo is an 8 channel parallel (list of 8 floats from numpy)
            perform thread synch when playing with it
    '''

    octo_layer_average = []
    mycolor = (0, 0, 0)  # You give this to parent
    mynumber = None  # You get this from parent
    myid = None  # You get this from parent
    mysource = "None so far..."
    # internal:
    mymolecules = None  # Internal list of neurotransmitter-like communication
    #layers = []  # a list of neurons + their neurotransmitters
    myfriends = []  # a list of friend IDS
    isselected = None

    def add_friend(self, friendid):
        if friendid in self.myfriends:
            return False

        self.myfriends.append(friendid)
        log.info("friend added")
        # print self.get_octo()

    def get_molecule_list(self):
        return ["dopamine", "beans", "potato", "from component"]

    def create_molecule_pool(self):
        '''returns a list of molecules for internal use'''

        molecules = {}
        for name in self.get_molecule_list():
            # random molecules for each layers
            molecules[name] = (Lock(), random.randint(40, 100000))

        return molecules

    def initlayers(self, hints):
        '''inits the internal data stream, these are numpy arrays'''
        #log.warning("setting the data for component with hints %s", hints)
        #self.mylayers = self.createlayers()
        #log.warning("layers created ")
        
        self.layers = []

        for l in range(DEFAULT_NUMBER_OF_LAYERS):
            for n in range(DEFAULT_NEURONS_PER_LAYER):
                self.layers.append(Neuron(parent_id=self.myid))


    def get_id(self):
        '''returns the id for the object'''
        return self.myid

    def __init__(self, global_state, type_hints="langu", myid=0):
        # from parent:
        self.type_hints = type_hints
        self.myid = myid
        self.global_state = global_state
        self.myfriends = []
        self.isselected = False
        self.mycolor = (random.randint(0, 100), random.randint(40, 150),
                        random.randint(40, 150))

        # internal:
        self.initlayers(type_hints)

    def do_work_on_input(self, inn):
        ''' works on the input data '''
        
        pass

    def get_input(self):
        '''reads from data stream...'''

        # For now just change the octo randomly...

        # TODO: mycolor responds to actual data state

        self.mycolor = (random.randint(50, 150), random.randint(
            50, 150), random.randint(50, 250))


        return self.mycolor

    def proc_cmd_q(self, q):
        if q.empty():
            pass
        try:
            cmd = q.get_nowait()
            if cmd[0:6] == "SELECT":
                if int(cmd[7:]) == self.myid:
                    self.isselected = True
                    print "%d knows its selected" % self.myid
                else: # This was not the intended component, throw the string back
                    self.isselected = False
                    q.put(cmd)
        except:
            pass

    def get_octo(self):
        octo_dict = {
            "type_hints": self.type_hints,
            "color": self.mycolor,
            "source": self.mysource,
            "myid": self.myid,
            "friends": self.myfriends,
            "layers": len(self.layers),
            "neurons_per_layer": 7,
            "x": 8
        }

        octo = Octo(octo_dict)

        return octo

    def neurons_repr(self):
        '''returns a list of (neuronid, state)'''
        l = []
        #print len(self.layers)

        for i in self.layers:
            l.append((i.get_id(), i.get_state()))

        return l

    def connections_repr(self):
        '''returns a list of tuples representing neuron connections'''

        l = [(1, 2, 3), (3, 2), (4, 5) ]
        return l 

    def sendlayers_if_selected(self, p):
        if self.isselected :    
            p.send(self.neurons_repr())
            p.send(self.connections_repr())
            sleep(1)
            # self.isselected = 0; # only send it once per SELECT command
            # print("id %d sent " % self.myid)


    def send_output(self, data_to_work_on=None, octo_q=None):
        try:
            octo_q.put(self.get_octo())  # just send an octo for now
            
        except Exception as e:
            print e
            log.warn("component %d unable to send octo!", self.get_id())

            print "put asn object"

    def live_loop(self, break_flag, q, cmd_q, main_pipe):
        '''loop repeatedly until breakflag is not 1 \
        (breakflag comes from the parent process, in\
        this case, sid...)'''

        while True:
            # 64 of these loops!

            if break_flag.value == -1:
                # print "process %d waiting for job flag... " % self.myid
                sleep(2)
                continue

            if break_flag.value == 0:
                # print "process %d told to break out of live_loop" % self.myid
                main_pipe.close()
                return

            if break_flag.value == 1:  # 1 signals "work"
                try:
                    self.proc_cmd_q(cmd_q)
                    self.sendlayers_if_selected(main_pipe)

                    inn = self.get_input()

                    self.do_work_on_input(inn)  # todo: do actual work
                    self.send_output(inn, q)

                except Exception as E:
                    m = "Component %d couldn't do work, exitted" % self.myid
                    print m
                    raise E
                    exit(1)
                finally:
                    sleep(0.5) # Careful!
        return

    def signal_death(self):
        # = 0
        pass

    def read_user_input(self):
        pass

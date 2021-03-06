'''
An atom in the sid system...
'''

try:
    from multiprocessing import Lock
    import random
except:
    print "Could not load main dependencies for neuron"

try :
    from helpers.getmylogger import silent_logger, loud_logger

except ImportError as e:
    print "Could not load internal helpers for neuron..."
    print e
    exit(1)

def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile):
      if random.randrange(num + 2): continue
      line = aline
    return line


def get_molecule_list():
    # todo: return real stuff from file

    return ["dopamine", "bacon", "tomato"]

log = loud_logger("neuron_stim")

# -class*
# -communicate with neighbours (?)

#       -in/out pipe


class Neuron:
    '''an atom in the sid system'''

    def __init__(self, parent_id = None, n={"dopamine":10, "serotonin":10}):
        '''
        n is a dict of moleculename:molecule_concentration,molecule_lock
        parent_layer is a list of "friend" neurons (could include self!)
        '''
        self.mymolecules = n
        self.parent_id = parent_id
        self.mystate = 0

        #self.myfriends = parent_layer
        #self.friends = parent_layer # a list of friend neurons

    def dopamine_response(self, value):
        log.info("responding to dopamine value %d", value)
        pass

    def update_state(self): ## update the state and output value of neuron
        moles = self.mymolecules
        self.mystate = 1

        for i in moles.iteritems():
            name = i[0]
            lock = i[1][0]
            val = i[1][1]

            if name == "dopamine" :
                lock.acquire()
                log.info("dopamine is at %d", val)
                self.dopamine_response(val)
                lock.release()

        
        pass
    
    def get_id(self):
        return int(str(id(self))[-4:]) 

    def get_state(self):
        return random.randint(1, 255)

if __name__ == '__main__':
    a=b=c=1092148 # the concentrationof the molecules in the layer pool...
    #molecules = dict(  dopamine=[a,Lock()] )
    #d = {key: value for (key, value) in iterable} {}

    molecules = {}

    for name in get_molecule_list():
        molecules[name] = (Lock(), random.randint(40, 100000))


    test_neuron = Neuron(molecules, [] )
    test_neuron.update_state()

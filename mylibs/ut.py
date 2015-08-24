''' ut: universal tweener with asynch locks for python ~ gbdu'''

try:
    from helpers.getmylogger import silent_logger,loud_logger
    from multiprocessing import Lock, Value
    import exceptions
except Exception as e:
    print "Could not load ut dependencies: "
    print e
    exit(1)

logger = loud_logger("tweener")
llog = silent_logger("silent_tweener")

DEFAULT_TWEEN_TO = 0
DEFAULT_TWEEN_MIN = 0
DEFAULT_TWEEN_VALUE = 0


   # def add_tweener(self, name, init_val=20, tween_to=20):
        # '''adds a tweener to this ut list, does nothing if it already exists'''
        # if name in self._itl:
        #     llog.warning("adding a tweener that already exists... ")
        #     llog.warning("adding tweener that already exists..., did nothing")
        #     return
        # 
        # tween_to = DEFAULT_TWEEN_TO
        # val = init_val
        # # adding an inner list
        # inner_dict = {
        #     'name':name,
        #     'lock':Lock(),
        #     'value':val,
        #     'type':"up", # up, down, rand, or cycle
        #     'cycle_state':"up", # only used for cycle state
        #     'to':tween_to,
        #     "min": DEFAULT_TWEEN_MIN
        # }
        # #llog.info("%s about to be appended....", inner_dict)
        # # appended
        # 
        # self._itl.append(inner_dict)
        
class TinyTween:
    name=None
    lock=None
    value=None
    mytype = "cycle"  # up, down, rand, or cycle
    cycle_state = "up" # only used for cycle state
    tween_to = None
    mymin = None

    def __init__(self, name, value=0, mytype="cycle", tween_to=200, mymin=10):
        '''
        name -- the name of the value (to be used to retrieve later)
        value -- init value for tween
        mytype -- Either: up, down, cycle, rand, or constant
        tween_to -- max value to tween up to (maxima in sin/cycle mode)
        mymin -- min value to tween down to (minimum in sin/cycle mode)
        '''
        self.name = name
        self.lock = Lock()
        self.value = value
        self.tween_to = tween_to
        self.mytype = mytype
        self.cycle_state = "up"
        self.mymin = mymin
        pass
        
class Ut:
    '''universal tweener for python -- with locks'''
    
    tinytweens = []
    
    def add_tweener(self, name, mytype, mymin=0, tween_to=0):
        nt = TinyTween(name, 0, mytype, tween_to, mymin)
        self.tinytweens.append(nt)
    
    def find_tweener(self, name):
        '''returns an internal dict if a tweener exists in internal list'''
        for t in self.tinytweens:
            if t.name == name:
                return t
        return False #couldn't find it 

    def __init__(self, num_starting_vals=0):
        '''returns a ut object with internal tweens'''
        
        pass

    def tween_cycle(self, name, tween_to, tween_from):
        i = self.find_tweener(name)
        if i :
            i.lock.acquire()
            i.tween_to = tween_to
            i.tween = tween_from
            i.value = tween_from
            i.mytype = 'cycle'
            i.cycle_state = 'up'
            i.lock.release()
        elif down > top:
            raise ValueError("tween cycle: top is bigger than down")
        else :
            raise ValueError("could not find tweener to cycle %s" % name)

    def tween_to_up(self, name, tween_to):
        '''increases the value of the tween with called to tween_to'''
        i = self.find_tweener(name)
        if i:
            i.lock.acquire()
            i.tween_to = tween_to
            i.mytype = "up"
            i.lock.release()
        else:
            print i
            print name, tween_to
            raise Exception("unable to find value for tween_to_up")
            
    def print_all_tweens(self):
        ''' prints all tweens (for debug)'''
        for i in self.tinytweens:
            print i
        
    def constant(self, name, constant):
        '''set this tween to a constant that does not change'''
        i = self.find_tweener(name)
        if i:
            i.lock.acquire()
            i.value = i.tween_to = i.mymin = constant
            i.mytype = "constant"
            i.lock.release()
            llog.info("lock rlsd")
        else:
            raise ValueError("ut constant: name: %s constant %d" % (name, constant))

    def get_tween_value(self, name):
        '''returns the current value of the tween'''
        i = self.find_tweener(name)
        if i:
            return i.value
        else:
            print "the name is : %s " % name 
            raise Exception("get_tween_value called with improper name")
            return 200

    def update_frame(self, increase_by=1, decrease_by=1):
        '''updates internal values, fuzz is not implemented yet'''
        # llog.info("updating tween")
        for idict in self.tinytweens:
            if idict.mytype == "constant":
                continue

            if idict.mytype == "up": ## increase up tweeners
                if idict.value < idict.tween_to:
                    idict.lock.acquire()
                    idict.value += increase_by
                    idict.lock.release()
                    continue
            elif idict.mytype == "down": ## decrease down tweeners
                if idict.value > idict.tween_to:
                    idict.lock.acquire()
                    idict.value -= decrease_by
                    idict.lock.release()
                    continue
            elif idict.mytype == "cycle":
                ## handle cycle:
                llog.info("cycling " + str(idict))
                if idict.cycle_state == "up":
                    if idict.value < idict.tween_to:
                        idict.lock.acquire()
                        idict.value += increase_by
                        idict.lock.release()
                    elif idict.value >= idict.tween_to:
                        idict.lock.acquire()
                        idict.cycle_state = "down"
                        idict.lock.release()
                if idict.cycle_state == "down":
                    if idict.value > idict.mymin:
                        idict.lock.acquire()
                        idict.value -= decrease_by
                        idict.lock.release()
                    elif idict.value <= idict.mymin:
                        idict.lock.acquire()
                        idict.cycle_state = "up"
                        idict.lock.release()

        llog.info("update frame exist")
        return 10
    
''' ut: universal tweener with asynch locks for python ~ gbdu'''

try:
    from helpers.getmylogger import silent_logger,loud_logger
    from multiprocessing import Lock
    import exceptions
except Exception as e:
    print "Could not load ut dependencies: "
    print e
    exit(1)
    
logger = loud_logger("gui_helpers")
    
llog = silent_logger("tweener")
DEFAULT_TWEEN_TO = 0
DEFAULT_TWEEN_MIN = 0
DEFAULT_TWEEN_VALUE = 0

class Ut:
    '''universal tweener for python -- with locks'''
    _itl = []

    def find_tweener(self, name):
        '''returns an internal dict if a tweener exists in internal list'''
        if len(self._itl) == 0:
            llog.warning("list not initd eyet and youre trying to find %s ", name)
            return False
        
        for i in self._itl :
            if i['name'] == name:
                llog.info("returning %s as found ", name)
                return i
            
        return False

    def add_tweener(self, name, init_val=20, tween_to=20):
        '''adds a tweener to this ut list, does nothing if it already exists'''
        
        if self.find_tweener(name):
            llog.warning("adding tweener that already exists..., did nothing")
            return
        
        tween_to = DEFAULT_TWEEN_TO
        val = init_val
        # adding an inner list
        inner_dict = {
            'name':name,
            'lock':Lock(),
            'value':val,
            'type':"up", # up, down, rand, or cycle
            'cycle_state':"up", # only used for cycle state
            'to':tween_to,
            "min": DEFAULT_TWEEN_MIN
        }
        #llog.info("%s about to be appended....", inner_dict)
        # appended
        
        self._itl.append(inner_dict)

    def __init__(self, num_starting_vals):
        '''returns a ut object with internal tweens'''
        for i in range(num_starting_vals):
            self.add_tweener(i)
    
    def tween_cycle(self, name, tween_to, tween_from):
        i = self.find_tweener(name)
        if i :
            i['lock'].acquire()
            i['to'] = tween_to
            i['from'] = tween_from
            i['value'] = tween_from
            i['type'] = 'cycle'
            i['cycle_state'] = 'up'
            i['lock'].release()
        elif down > top:
            raise ValueError("tween cycle: top is bigger than down")
        else :
            raise ValueError("could not find tweener to cycle %s" % name) 
    
    def tween_to_up(self, name, tween_to):
        '''increases the value of the tween with called to tween_to'''
        i = self.find_tweener(name)
        if i:
            i["lock"].acquire()
            i["to"] = tween_to
            i["type"] = "up"
            i["lock"].release()
    
    def constant(self, name, constant):
        '''set this tween to a constant that does not change'''
        i = self.find_tweener(name)
        if i:
            i["lock"].acquire()
            i["value"] = i["to"] = i["from"] = constant
            i["type"] = "constant"
            i["lock"].release()
            llog.info("lock rlsd")
        else:
            raise ValueError("bad value to constant")
        
    def get_tween_value(self, name):
        '''returns the current value of the tween'''
        i = self.find_tweener(name)
        if i:
            i['lock'].acquire()
            val = i["value"] # return the current val
            i['lock'].release()
            return val
        else :
            llog.warning("not found '%s'" , name)
            raise ValueError("bad value")
            return 10 # return the default guy
    
    def _handle_cycle_update(self, name, increase_by, decrease_by):
        internal_dict = self.find_tweener(name)
        

    pass

    def update_frame(self, increase_by=1, decrease_by=1):
        '''updates internal values, fuzz is not implemented yet'''
        
        # llog.info("updating tween")
        for idict in self._itl:
            if idict["type"] == "constant":
                continue
            
            if idict["type"] == "up": ## increase up tweeners
                if idict['value'] < idict['to']:
                    idict['lock'].acquire()
                    idict['value'] += increase_by
                    idict['lock'].release()
                    continue
            elif idict["type"] == "down": ## decrease down tweeners
                if idict['value'] > idict['to']:
                    idict['lock'].acquire()
                    idict['value'] -= decrease_by
                    idict['lock'].release()
                    continue
            elif idict["type"] == "cycle":
                ## handle cycle:
                if idict['cycle_state'] == "up":
                    if idict['value'] < idict['to']:
                        idict['lock'].acquire()
                        idict['value'] += increase_by
                        idict['lock'].release()
                    elif idict['value'] >= idict['to']:
                        idict['lock'].acquire()
                        idict['cycle_state'] = "down"
                        idict['lock'].release()
                if idict['cycle_state'] == "down":
                    if idict['value'] > idict['from']:
                        idict['lock'].acquire()
                        idict['value'] -= decrease_by
                        idict['lock'].release()
                    elif idict['value'] <= idict['from']:
                        idict['lock'].acquire()
                        idict['cycle_state'] = "up"
                        idict['lock'].release()  
                        
        llog.info("update frame exist")
        return 10

''' ut: universal tweener with asynch locks for python ~ gbdu'''

from getmylogger import silent_logger,loud_logger
from multiprocessing import Lock

llog = silent_logger("tweener")
DEFAULT_TWEEN_TO = 0
DEFAULT_TWEEN_MIN = 0
DEFAULT_TWEEN_VALUE = 0

class Ut:
    '''universal tweener for python -- with locks'''
    _itl = []

    def does_exist(self, name):
        '''returns True if a tweener exists in internal list'''
        if len(self._itl) == 0:
            return False
        
        for i in self._itl :
            if i['name'] == name:
                return True
        
        return False

    def add_tweener(self, name, init_val=20, tween_to=20):
        '''adds a tweener to this ut list, does nothing if it already exists'''
        
        if self.does_exist(name):
            llog.warning("adding tweener that already exists..., did nothing")
            return
        
        tween_to = DEFAULT_TWEEN_TO
        val = init_val
        # adding an inner list
        inner_dict = {
            'name':name,
            'lock':Lock(),
            'value':val,
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

    def tween_to_up(self, name, tween_to):
        '''increases the value of the tween with called to tween_to'''
        if self.does_exist(name):
            llog.info("I will tween %s up by %d every update frame ", name, tween_to)
            for i in self._itl:
                if i["name"] == name:
                    i["lock"].acquire()
                    i["to"] = tween_to
                    i["lock"].release()
                    llog.info("lock rlsd")
            
        else:
            pass
            #llog.error("%s not found, cant tween up", name)
            #raise exception.BadValue("aaaa")

    def constant(self, name, constant):
        '''set this tween to a constant that does not change'''
        if self.does_exist(name):
            llog.info("%s set to constant", name)
            for i in self._itl:
                if i['name'] == name:
                    i["lock"].acquire()
                    i["value"] = i["to"] = constant
                    i["lock"].release()
                    llog.info("lock rlsd")
                
        else:
            llog.error("%s not found, cant constant the tween", name)
            raise exception.BadValue("aaaa")
        
    def get_tween_value(self, name):
        '''returns the current value of the tween'''
        
        for i in self._itl:
            if i['name'] == name:
                i['lock'].acquire()
                val = i["value"] # return the current val
                i['lock'].release()
                return val
           
        llog.warning("not found '%s'" , name)
        raise
        return 10 # return the default guy
    
        
    def update_frame(self, increase_by=1, decrease_by=1):
        '''updates internal values, fuzz is not implemented yet'''
        
        # llog.info("updating tween")
        for internal_dict in self._itl:
            if internal_dict['value'] == internal_dict['to']:
                continue
            
            if internal_dict['value'] < internal_dict['to']:
                internal_dict['lock'].acquire()
                internal_dict['value'] += increase_by
                internal_dict['lock'].release()
                
            if internal_dict['value'] >= internal_dict['to']:
                internal_dict['lock'].acquire()
                internal_dict['value'] = 0
                internal_dict['lock'].release()
                

        return 10

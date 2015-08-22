# ut: universal tweener with asynch locks for python
# ~ gbdu

from getmylogger import silent_logger
from multiprocessing import Lock

log = silent_logger("tweener")
DEFAULT_TWEEN_TO = 0
DEFAULT_TWEEN_MIN = 0
DEFAULT_TWEEN_VALUE = 0

class ut:
    '''universal tweener for python -- with locks'''
    _itl = []
    def add_tweener(self, name):
        '''adds a tweener to this ut list'''
        TweenTo = DEFAULT_TWEEN_TO
        v = DEFAULT_TWEEN_VALUE
        inner_dict = {}
        inner_dict[name] = { 'lock':Lock(), 'value':v, 'to':TweenTo, "min": DEFAULT_TWEEN_MIN }
        _itl.append(inner_dict)
    
    def __init__(self, num_starting_vals):
        '''returns a ut object with internal tweens'''
        for i in range(starting_vals):
            self.add_tweener(i)
    
    def tween_to_up(self, name, tween_to):
        '''increases the value of the tween with called to tween_to'''
        for i in self._itl:
            if i[name] == name: #found our internal_tween
                i["lock"].acquire()
                i["to"] = tweento()
                i["lock"].release()
                
    def get_tween_value(self, name):
        '''returns the current value of the tween'''
        for i in self._itl:
            if i[name] == name :
                i["lock"].acquire()
                i["value"] = name[1] # return the current val
                i["lock"].release()
    
    def update_frame(self, increase_by=1, decrease_by=1):
        for internal_dict in self._itl:
            if internal_dict["value"] < internal_dict["to"]:
                internal_dict["lock"].acquire()
                internal_dict["value"] += increase_by
                internal_dict["lock"].release()
                
            elif internal_dict["value"] > internal_dict["to"]:
                internal_dict["lock"].acquire()
                internal_dict["value"] -= increase_by
                internal_dict["lock"].release()
            
            else: # The values match, do nothing and check next tween
                pass
            
        return time_it_took

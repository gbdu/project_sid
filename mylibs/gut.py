"""
gut is a simple python gui library with tweening support ( color fade, etc... )
gut stands for Global Universal Tweener

"""

__author__ = 'gbdu'
__copyright__ = "Copyright 2015, gbdu"
__credits__ = ["gbdu"]
__email__ = "ogrum@live.com"

import random
from time import sleep
import ut

class Gut:
    internal_ut = None

    def add_random_tweens(self, n=256):
        '''
        Add n tweens of type int and cycle to the internal ut,
        named as such: 1,2,3...

        n -- The number of tweeners to add, defaults to 256
        '''
        for i in range(n):
                st = random.randint(40, 90)
                self.internal_ut.add_tweener(str(i), "cycle", 0, st)

        return self.internal_ut

    def add_default_color_tweens(self):
        self.internal_ut.add_tweener("rotation_angle", "cycle", 0, 360)
        self.internal_ut.add_tweener("default_box", "constant", 50)
        self.internal_ut.add_tweener("selected_line", "cycle", 200, 250)
        self.internal_ut.add_tweener("linesr", "cycle", 50,200)
        self.internal_ut.add_tweener("default_box_text", "cycle",
                                     random.randint(0,50),
                                     random.randint(50, 200))

        self.internal_ut.add_tweener("active_box", "cycle", 0, 100)
        self.internal_ut.add_tweener("nearbox_1", "cycle", 0, 40)
        self.internal_ut.add_tweener("nearbox_2", "cycle", 0, 30)

    def get_color_inverse(self,color):
            inverse = [abs(250-color[0]), abs(250-color[1]), abs(250-color[2])]
            return inverse

    def get_color_dimmer(self,color,a=20):
            inverse = [color[0]-a, color[1]-a, color[2]-a]
            return inverse

    def update_frame(self, by=1):
        self.internal_ut.update_frame(by)

    def update_frame_loop(self, live_flag_ref):
        '''
        Loops and updates internal state indefinitely as long as main_breakout
        value is 1.

        live_flag_ref is a reference to a Value("d", [1/0] ) object, where 1
        indicates "live" state and 0 indicates "dead/killed/exit"

        '''

        while 1:
            if(live_flag_ref.value == -1):
                sleep(2)
                continue

            if(live_flag_ref.value == 0):
                break ;

            self.update_frame(1)

        print "out of frame loop..."



    def get_tween_value(self, name):
        i = self.internal_ut.get_tween_value(name)
        return i

    def __init__(self):
        try:
            self.internal_ut = ut.Ut(256)
        except:
            print "unable to init a ut"
            raise
        ####
        try:
            self.add_default_color_tweens()
        except:
            print "unable to add default colors"
            raise
        ####
        try:
            self.add_random_tweens()
        except:
            print "unable to add random tweens"
            raise
        ###

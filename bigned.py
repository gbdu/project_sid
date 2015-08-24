"""
A visual representation of a Sid
This has the following asynch processes running:
        - sid.live
        - drawing
        - universal tweener updater
"""

__author__ = 'gbdu'
__copyright__ = "Copyright 2015, gbdu"
__credits__ = ["gbdu"]
__license__ = "GPL"
__version__ = "1.5-alpha"
__email__ = "ogrum@live.com"
__status__ = "dev"

# Import main dependencies:
try:
        import os,sys
        import pygame
        import time
        from multiprocessing import Process, Value
        from time import sleep
        import random
except ImportError as e:
        print "failed to import main dependencies... "
        print e
        exit(1)
# Import my dependencies:
try:
        from helpers import getmylogger
        from ai import sid
        from mylibs import ut
        from mylibs import gut
        from gui import gui_helpers,pyconsole
except ImportError as e:
        print "failed to import bigned dependencies... "
        print e
        exit (1)

all_live_loops = Value("d", 0)

selected_component_id = 0

dlog = getmylogger.silent_logger("silent_bigned") #silent drawing logger
llog = getmylogger.loud_logger("bigned") #silent drawing logger

llog.info("set up all the globals... ")

class BigNed:
        
        internal_sid = None
        screen = None
        myfont = None
        user_console = None
        mygut = None 
        
        global dlog
        global llog
        
        def init_console(self, key_calls):
                try:
                        r = pygame.Rect(300, 20, 320, 256)
                        uc = pyconsole.Console(self.screen, r, key_calls=key_calls  )
                        return uc
                except:
                        llog.error("unable to init console %s" % sys.exc_info()[0])
                        exit(1)
        
        def extinguish_and_deload():
                llog.info("      ABOUT TO EXTINGUISH AND DELOAD")
                self.all_loops_live = False
                self.internal_sid.signal_extinguish()
                llog.info("signaled extinguish  [ SUCCESS ]")

        def __init__(self):
                '''inits big ned and draws a visual representation of its state'''
                try:
                        try:
                                self.mygut = gut.Gut()
                        except Exception as e:
                                print "Unable to init a gut"
                                print e
                                exit(1)
                                
                        self.internal_sid = sid.Sid()
                        self.internal_sid.setname("BigNed")
                        self.all_loops_live = True
                        self.screen = gui_helpers.init_pygame()
                        self.myfont = gui_helpers.create_font()
                        key_calls={"d": self.extinguish_and_deload}
                        
                        self.user_console = self.init_console(key_calls)
                        
                        llog.info("The sid %s was created successfully, he's not alive yet though [ SUCCESS ] " % self.internal_sid.getname() )
        
                except Exception as e:
                        llog.info("failed to init a bigned ... [ FAIL ] ")
                        print e
                        exit(1)
                        
        def draw_version_label(self, surf,color=(200,200,200)):
                '''draws the version info on the top of the main screen'''
                surf.fill((40,40,40))
                text = self.myfont.render("bigned " + __version__, 1, color)
                r=pygame.Rect(0,0,100,20)
                surf.blit(text, r)
        def draw_panel_label(self, surf):
                '''draw the bottom panel label'''
                global selected_component_id

                surf.fill((40,40,40))
                info_paragraph = []

                info_paragraph.append("Currently selected component: %d " % selected_component_id)
                c_dict = self.internal_sid.get_component_by_id(selected_component_id)

                c_dict['lock'].acquire()
                octo = c_dict['component'].get_octo()
                c_dict['lock'].release()

                #info_paragraph.append("Internal octo: ")

                info_paragraph.append("    component type : %s" % octo["type_hints"])
                info_paragraph.append("    source : %s" % octo["source"])

                info_paragraph.append("")

                for number,line in enumerate(info_paragraph):
                        rpos = pygame.Rect(0, (number*self.myfont.get_height()), 20,20) # location of text
                        text = self.myfont.render(line, 1, (100,200,100))
                        surf.blit(text, rpos)
                        
        def draw_box_label(self, surf, color, component_counter, boxrect):
                # Display some text
                text = self.myfont.render(str(component_counter), 1, color)
                textpos = boxrect
                surf.blit(text, textpos)
        
        def draw_box(self, surf, i, inrow, color, width, height, component_counter):
                '''draw a single box'''
                
                pos = pygame.mouse.get_pos()
                boxrect = pygame.Rect(inrow*width, i*height, width, height)
                a = b = c = 0
                
                boxrect_big = pygame.Rect(inrow*width - width*1, i*height - height*1, width*3, height*3)
                t = self.mygut.get_tween_value(str(component_counter))
                
                if boxrect.collidepoint(pos): # this is an active box
                        a = self.mygut.get_tween_value("active_box")
                        global selected_component_id
                        selected_component_id = component_counter
                        color = [200, 200 , 200+(t/2)]
                elif boxrect_big.collidepoint(pos):
                        b = self.mygut.get_tween_value("nearbox_1")
                        color=[a+b+t + 20, a+b+t + 20 , t/2 + 40]
                else: # This is a regular component, draw it using its tween
                        color = [a+b+t, a+b+t, 20+ (t/2)]

                if(selected_component_id != component_counter):
                        c_dict = self.internal_sid.get_component_by_id(component_counter)
                        c_dict['lock'].acquire()
                        octo = c_dict['component'].get_octo()
                        c_dict['lock'].release()

                        if(octo["type_hints"] == "audio"):
                                color = (color[0], color[1]+15, color[2]+10)
                        if(octo["type_hints"] == "video"):
                                color = (color[0]+15, color[1]+10, color[2])
                        if(octo["type_hints"] == "langu"):
                                color = (color[0]+15, color[1]+5, color[2]+20)

                pygame.draw.rect(surf, color, boxrect , 0)
                self.draw_box_label(surf, color, component_counter, boxrect)
                
        def draw_components_on_surf(self, surf):
                '''Draw a grid of 16x16 boxes representing our components'''
                c_r = pygame.Rect(0, 0, 256, 256)
                # hide the cursor if we're in here
                pos = (pygame.mouse.get_pos()[0] - 20 ,
                       pygame.mouse.get_pos()[1] - 20)
        
                if(c_r.collidepoint(pos)):
                        pygame.mouse.set_visible(0)
                else:
                        pygame.mouse.set_visible(1)
        
                pygame.draw.rect(surf, (45, 45, 45), c_r, 0 )
                width = 32
                height= 32

                component_counter = 0
                for i in range(8):
                        for inrow in range(8):
                                d = self.mygut.get_tween_value("default_box")
                                color = [d,d,d]
                                self.draw_box(surf, i, inrow, color, width, height, component_counter)
                                component_counter += 1
        
        #XXX : INFINITE/BREAKABLE LOOP 1 (DRAW)
        def draw_loop(self):
                """
                draw the given Ned on INIT'd scr
                """
                
                llog.info("* PROCESS: Draw process started")
        
                
                ## Actual Draw() starts here
        
                
                self.screen.fill((35, 35, 35))
        
        
                panel_label_surf = pygame.Surface((256, 170))
                component_surf = pygame.Surface((256, 256))
                version_label_surf = pygame.Surface((100, self.myfont.get_height()))
        
                component_box_where= (20,20)
                panel_label_where = (20, 300)
                version_label_where = (5,5)
        
                global user_console
        
        
                llog.info("entering main draw loop")
                
                frame_counter = 0
                frame_counter_start_time = time.time()
                
                while all_loops_live.value == 1 :
                        ## This is our main loop, draw input screen and update tweener
                        self.user_console.process_input()
                        self.user_console.draw()
                        
                        self.mygut.update_frame() # TODO move this to independent process...
                        
                        self.draw_version_label(version_label_surf)
                        self.draw_panel_label(panel_label_surf)
                        self.draw_components_on_surf(component_surf)
                        
                        self.screen.blit(version_label_surf, version_label_where)
                        self.screen.blit(component_surf, component_box_where)
                        self.screen.blit(component_surf, component_box_where)
                        self.screen.blit(panel_label_surf, panel_label_where)
                        
                        pygame.display.flip()
                        elapsed_time = time.time() - frame_counter_start_time
                        
                        if(elapsed_time >= 10): # updates every 10 seconds
                                ## Calculate fps
                                fps = frame_counter / 10 ## number of frames / 10 secs...
                                frame_counter_start_time = time.time() # set time again...
                                frame_counter = 0 # set starting frame again
                        else:
                                frame_counter += 1
                        
                llog.info("exiting main draw loop...")
                
        def create_sid_process(self, global):
                ''' start the sid loop process '''
                SidProcess = Process(target=self.internal_sid.live) # sid process
                llog.info("started sid process...")
                SidProcess.start()
                return SidProcess
        
        def create_draw_process(self):
                ''' start the draw loop process '''
                drawp = Process(target=self.draw_loop) # sid process
                llog.info("started draw process...")
                drawp.start()
                return drawp
        
        def create_tween_process(self):
                ''' start the draw loop process '''
                tweenp = Process(target=self.mygut.update_frame_loop) # sid process
                llog.info("started draw process...")
                tweenp.start()
                return tweenp
        
if __name__ == '__main__':
        llog.info("Here we go!!!")
        bn = BigNed()
        
        p1=bn.create_sid_process()
        p2=bn.create_draw_process()
        p3=bn.create_tween_process()
        
        p1.join();
        p2.join();
        p3.join();
        
        # 
        # 
        # ## Only tweening:
        # # globals()['gut'] = ut.Ut()
        # # add_color_tweeners()
        # # setup_color_tweens()
        # # TweenerProcess = Process(target=update_gut)
        # # llog.info("---> init ut in main process")
        # # TweenerProcess.start()
        # # 
        # SidProcess.start()
        # llog.info("[2/3] : sid process was started ")
        # 
        # DrawProcess.start()
        # llog.info("[3/3] : draw process was started")
        # 
        # 
        # 
        # # Important: start tweener updater before everything else?
        # DrawProcess.join()
        # llog.info("      -> joined draw process [ SUCCESS ] ")
        # 
        # SidProcess.join()
        # llog.info("      -> joined ned [ SUCCESS ] ")
        # 
        # 
        # TweenerProcess.join()
        # llog.info("      -> joined tween process [ SUCCESS ] ")
        # 
        # 
        # llog.info("All done, bye!")
        pass
#!/usr/bin/python2.7

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

GLOBAL_LIVE_FLAG = Value("d", 0)

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
        myboxes = []  # A list of tuples (component_id,boxrect)
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

        def extinguish_and_deload(self):
                llog.info(" EXIT -> extinguish_and_deload called" )
                global GLOBAL_LIVE_FLAG
                GLOBAL_LIVE_FLAG.value = 0
                self.internal_sid.signal_extinguish()

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
                        self.screen = gui_helpers.init_pygame()
                        self.myfont = gui_helpers.create_font()
                        key_calls={"d": self.extinguish_and_deload}

                        self.user_console = self.init_console(key_calls)

                        llog.info("The sid %s was created successfully, he's not alive yet though [ SUCCESS ] " % self.internal_sid.getname() )

                except Exception as e:
                        llog.info("failed to init a bigned ... [ FAIL ] ")
                        print e
                        exit(1)

        def draw_version_label(self, surf, fps , color=(200,200,200)):
                '''draws the version info and fps on the top of the main screen'''
                surf.fill((40,40,40))

                text = self.myfont.render("bigned " + __version__ + " " + str(fps) + " fps", 1, color)
                r=pygame.Rect(0,0,150,20)
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

                self.myboxes.append((component_counter, boxrect ))

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

                selected = selected_component_id == component_counter
                bordered = 1 if selected else 0
                pygame.draw.rect(surf, color, boxrect , bordered)
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

                                dlog.info("drew box")

        def draw_a_link(self, surf, c1, c2):
            '''c1 c2 are ids'''

            line_pos1_x = line_pos1_y= 10;
            line_pos2_y = line_pos2_x= 40;


            for c in self.myboxes:

                startp = (0,0)
                endp = (100,100)

                if c[0] == c1: ## We found the first box in our box list
                    startp = (c[1][0], c[1][1])

                if c[0] == c2: ## We found the first box in our box list
                    endp = (c[1][0], c[1][1])

                pygame.draw.line(surf, (200,0,0), startp, endp)


        def draw_links_on_surf(self, surf):
            friend_list = self.internal_sid.get_component_friends()
            #friend_list.append((5,15))
            for f in friend_list :
                c1_id = f[0]
                c2_id = f[1]

                self.draw_a_link(surf, c1_id, c2_id)

            #llog.info("drew component links... on %d " % len(friend_list))
            #dlog.warn("drew links")
            pass

        #XXX : INFINITE/BREAKABLE LOOP 1 (DRAW)
        def draw_loop(self, break_flag):
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

                frame_counter = 0.0
                frame_counter_start_time = time.time()
                fps = 0.0
                FPS_AVG = 10.0

                while True :




                    ## This is our main loop, draw input screen and update tweener

                    if(break_flag.value == -1): # -1 means "pause a bit..."
                            sleep(2) # sleep for two seconds then try again
                            continue;
                    elif(break_flag.value == 0): # 0 means stop
                            self.internal_sid.signal_extinguish()
                            break ;

                    self.user_console.process_input()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.extinguish_and_deload()

                            pygame.quit(); sys.exit();
                    self.user_console.draw()

                    self.mygut.update_frame() # TODO move this to independent process...

                    self.draw_version_label(version_label_surf, fps)

                    self.draw_panel_label(panel_label_surf)
                    self.draw_components_on_surf(component_surf)

                    self.draw_links_on_surf(component_surf)
                    self.screen.blit(version_label_surf
                    ,  version_label_where)
                    self.screen.blit(component_surf, component_box_where)
                    self.screen.blit(component_surf, component_box_where)
                    self.screen.blit(panel_label_surf, panel_label_where)

                    pygame.display.flip()
                    elapsed_time = time.time() - frame_counter_start_time

                    if(elapsed_time >= FPS_AVG):  # FPS_AVG is how many seconds fps is averaged over...
                            ## Calculate fps
                            fps = frame_counter / FPS_AVG
                            frame_counter_start_time = time.time() # set time again...
                            frame_counter = 0.0 # set starting frame again
                    else:
                            frame_counter += 1.0

                llog.info("exiting main draw loop...")

        def create_sid_process(self, break_flag):
                '''
                start the sid loop process
                break_flag -- a value indicating live loop exit state
                '''
                SidProcess = Process(target=self.internal_sid.live_loop, args=(break_flag,)) # sid process
                llog.info("started sid process...")
                SidProcess.start()
                return SidProcess

        def create_draw_process(self, break_flag):
                ''' start the draw loop process '''
                drawp = Process(target=self.draw_loop, args=(break_flag,)) # sid process
                llog.info("started draw process...")
                drawp.start()
                return drawp

        def create_tween_process(self, break_flag):
                ''' start the gut process '''
                tweenp = Process(target=self.mygut.update_frame_loop, args=(break_flag,)) # sid process
                llog.info("started tween process...")
                tweenp.start()
                return tweenp

if __name__ == '__main__':
        llog.info("Here we go!!!")
        bn = BigNed()

        p1=bn.create_sid_process(GLOBAL_LIVE_FLAG)
        p2=bn.create_draw_process(GLOBAL_LIVE_FLAG)
        p3=bn.create_tween_process(GLOBAL_LIVE_FLAG)

        ## all processes are now ready to start.

        GLOBAL_LIVE_FLAG.value = -1

        bn.internal_sid.make_components_friends(2,16)

        # This gives around 2 seconds of synchronization
        # time for all processes to start.


        time.sleep(2)

        GLOBAL_LIVE_FLAG.value = 1

        p1.join();
        llog.info("p1  -> sid process is done")
        p2.join();
        llog.info("p2  -> draw process is done")
        p3.join();
        llog.info("p3  -> tween process is done")

        llog.info("All done, bye!")

        pygame.quit()
        pass

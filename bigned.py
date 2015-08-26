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

GLOBAL_LIVE_FLAG = Value("d", -1)

selected_component_id = 0

dlog = getmylogger.silent_logger("silent_bigned") #silent drawing logger
llog = getmylogger.loud_logger("bigned") #silent drawing logger

llog.info("set up all the globals... ")

class BigNed:

        _mysid = None
        screen = None
        myfont = None
        user_console = None
        mygut = None
        myboxes = []  # A list of tuples (component_id,boxrect)
        global dlog
        global llog

        clicked_components = () # whenever this reaches two, they get added
                                # and the list gets emptied

        def lg(self, msg="defaultmsg"):
            '''drawn log output'''
            self.user_console.output(msg)
            llog.info(msg)

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
                self._mysid.signal_extinguish()

        def __init__(self):
                '''inits big ned and draws a visual representation of its state'''
                try:
                    self.mygut = gut.Gut()
                    self._mysid = sid.Sid()
                    self._mysid.make_components_friends(10, 20)
                    self._mysid.setname("BigNed")
                    self.screen = gui_helpers.init_pygame()
                    self.myfont = gui_helpers.create_font()

                    key_calls={"d": self.extinguish_and_deload}
                    self.user_console = self.init_console(key_calls)

                    llog.info("The sid %s was created successfully, he's not alive yet though [ SUCCESS ] " % self._mysid.getname() )

                except Exception as e:
                        llog.info("failed to init a bigned ... [ FAIL ] ")
                        print e
                        exit(1)
        # Processing

        def process_mouse(self, event):
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                self.lg("processed up")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.lg("processed down")


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
                linfo = []

                linfo.append("Currently selected component: %d " % selected_component_id)
                c_dict = self._mysid.get_component_by_id(selected_component_id)

                #c_dict['component'].add_friend(10)
                octo = c_dict['component'].get_octo()


                #linfo.append("Internal octo: ")

                linfo.append("    octo-hints : %s" % octo["type_hints"])
                linfo.append("    octo-color : %s %s %s" % octo["mycolor"])
                linfo.append("    octo-source : %s" % octo["source"])
                linfo.append("    octo-id : %s" % octo["id"])
                linfo.append("    octo-friends : %s" % octo["friends"])
                linfo.append("")


                for number,line in enumerate(linfo):
                        rpos = pygame.Rect(0, (number*self.myfont.get_height()), 20,20) # location of text
                        text = self.myfont.render(line, 1, (150+number*10,100,100+number*10))
                        surf.blit(text, rpos)

        def draw_box_label(self, surf, color, bc, boxrect):
                # Display some text
                text = self.myfont.render(str(bc), 1, color)
                textpos = boxrect
                surf.blit(text, textpos)

        def draw_box(self, surf, i, inrow, color, width, height, bc):
                '''draw a single box'''
                c_dict = self._mysid.get_component_by_id(bc)
                c_dict['lock'].acquire()
                octo = c_dict['component'].get_octo()
                c_dict['lock'].release()

                pos = pygame.mouse.get_pos()
                boxrect = pygame.Rect(inrow*width, i*height, width, height)
                a = b = c = 0

                boxrect_big = pygame.Rect(inrow*width - width*1, i*height - height*1, width*3, height*3)
                t = self.mygut.get_tween_value(str(bc))

                if boxrect.collidepoint(pos): # affect for active box
                        a = self.mygut.get_tween_value("active_box")
                        global selected_component_id
                        selected_component_id = bc
                        color = [180, 180 , 200+(t/2)]
                elif boxrect_big.collidepoint(pos): # affect color by near
                        b = self.mygut.get_tween_value("nearbox_1")
                        color=[a+b+t + 30, a+b+t + 30 , t/2 + 40]
                else: # This is a regular component, draw it using its tween
                        color = [a+b+t, a+b+t, 20+ (t/2)]

                if(selected_component_id != bc): ## Affect color by hint type
                        if(octo["type_hints"] == "audio"):
                                color = (color[0], color[1]+15, color[2]+10)
                        if(octo["type_hints"] == "video"):
                                color = (color[0]+15, color[1]+10, color[2])
                        if(octo["type_hints"] == "langu"):
                                color = (color[0]+15, color[1]+5, color[2]+20)

                pygame.draw.rect(surf, color, boxrect , 0)
                self.draw_box_label(surf, color, bc, boxrect)

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

                bc = 0

                linesps = []
                linescl = []

                f_flag = 0

                for i in range(8):
                        for inrow in range(8):
                            d = self.mygut.get_tween_value("default_box")
                            color = [d,d,d]
                            self.draw_box(surf, i, inrow, color, width, height, bc)


                            c_dict = self._mysid.get_component_by_id(bc)
                            c_dict['lock'].acquire()
                            octo = c_dict['component'].get_octo()
                            c_dict['lock'].release()

                            for p in octo["friends"]:
                                linesps.append( (inrow*width+width/2, i*height+height/2) )
                                linesps.append( (inrow*width+15, i*height+3+height/2) )
                                linescl.append(octo["mycolor"][0])
                                linescl.append(octo["mycolor"][1])
                                linescl.append(octo["mycolor"][2])



                            bc += 1

                s = sum(linescl)
                avg = s/len(linescl)

                pygame.draw.lines(surf, (avg,avg,avg), False, linesps, 2)

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


                self.lg("entering main draw loop")

                frame_counter = 0.0
                frame_counter_start_time = time.time()
                fps = 0.0
                FPS_AVG = 10.0

                while True :
                    ## This is our main loop, draw input screen and update tweener

                    self.user_console.process_input()

                    if(break_flag.value == -1): # -1 means "pause a bit..."
                            sleep(2) # sleep for two seconds then try again
                            continue;
                    elif(break_flag.value == 0): # 0 means stop
                            self.extinguish_and_deload
                            break ;


                    event = pygame.event.poll()
                    if event.type == pygame.QUIT:
                        self.extinguish_and_deload()
                        exit(0)


                    if event.type == pygame.MOUSEBUTTONUP:
                        self.process_mouse(event)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.process_mouse(event)
                    elif event.type == pygame.MOUSEMOTION:
                        x, y = event.pos
                    else:
                        x,y=0,0


                    self.user_console.draw()

                    self.mygut.update_frame() # TODO move this to independent process...

                    self.draw_version_label(version_label_surf, fps)

                    self.draw_panel_label(panel_label_surf)
                    self.draw_components_on_surf(component_surf)

                    #self.draw_links_on_surf(component_surf)
                    self.screen.blit(version_label_surf
                    ,  version_label_where)
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
                SidProcess = Process(target=self._mysid.live_loop, args=(break_flag,)) # sid process
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

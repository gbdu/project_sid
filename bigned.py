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
__version__ = "1.4-alpha"
__email__ = "ogrum@live.com"
__status__ = "dev"

#from dbgp.client import brkOnExcept
#brkOnExcept(host='mybox', port=9000)

# Import main dependencies:
try:
        import os,sys
        import pygame
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
        from gui import gui_helpers,pyconsole

except ImportError as e:
        print "failed to import bigned dependencies... "
        print e
        exit (1)


USER_CONSOLE_ENABLED = True #only checked when drawing


globals()["dlog"] =  getmylogger.silent_logger("drawing") #silent drawing logger
globals()["llog"] =  getmylogger.loud_logger("drawing") #silent drawing logger

try:
        globals()["screen"] = gui_helpers.init_pygame()
        globals()["gfont"] = gui_helpers.create_font()
        globals()["gselected_component"] = 1
        globals()["main_breakout"] = Value("d", 1)
        globals()["color_ut"] = None
except Exception as e:
        llog.error("error while init  [ FAIL ] ")
        print e
        exit(1)

def extinguish_and_deload():
        llog.info("---> ABOUT TO DELOAD")
        globals()["main_breakout"].value = 0
        globals()["llog"].info("extinguished")
        globals()["bigned"].signal_extinguish()
        llog.info("signaled extinguish  [ SUCCESS ]")

def init_console(screen, key_calls):
        try:
                r = pygame.Rect(300, 20, 320, 256)
                uc = pyconsole.Console(screen, r, key_calls=key_calls  )
                return uc
        except:
                llog.error("unable to init console %s" % sys.exc_info()[0])
                exit(1)

globals()["user_console"] = init_console(globals()["screen"],
        key_calls={"d": extinguish_and_deload})
globals()["selected_component_id"] = 0

#### Start here

def setup_color_tweens(): ## This is a list of tweens set up by default...

        for i in range(256):
                st = random.randint(40, 90)
                color_ut.add_tweener(str(i))
                color_ut.tween_cycle(str(i), st, 0)
                #llog.info("set up '%s' with %d and %d", str(i), st, 100)
        pass

def add_color_tweeners(ut_obj):
        ut_obj.add_tweener("rotation_angle")
        ut_obj.tween_to_up("rotation_angle", 360)

        ut_obj.add_tweener("default_box")
        ut_obj.constant("default_box", 50)

        ut_obj.add_tweener("default_box_text")
        ut_obj.tween_cycle("default_box_text",
                             random.randint(0,50),
                             random.randint(50, 200))

        ut_obj.add_tweener("active_box")
        ut_obj.tween_cycle("active_box", 0, 100)

        ut_obj.add_tweener("nearbox_1")
        ut_obj.tween_cycle("nearbox_1", 0, 40)

        ut_obj.add_tweener("nearbox_2")
        ut_obj.tween_cycle("nearbox_2", 0, 20)

        try:
                setup_color_tweens()
        except Exception as e :
                llog.error("Couldnt setup color tweens for components...")
                print e
                exit(1)
        return ut_obj

def get_color_inverse(color):
        inverse = [abs(250-color[0]), abs(250-color[1]), abs(250-color[2])]
        return inverse

def get_color_dimmer(color,a=20):
        inverse = [color[0]-a, color[1]-a, color[2]-a]
        return inverse


## Innit is done

def Draw(theNed, color_ut):
        """draw the given Ned on global scr"""

        global llog

        llog.info("* PROCESS: Draw")

        def get_component_color(component_pipe):
                '''get the color of the box that represents the component'''
                #return component.get_color_dim()
                return component_pipe.recv()

        def draw_component_info_on_surf(surf, where):
                global dlogs
                dlog.log("draw component info")
                c_r = pygame.Rect(0,0, 256, 100)
                pygame.draw.rect(surf, (30, 40, 80), c_r, 0)

        def draw_components_on_surf(surf):
                '''Draw a grid of 16x16 boxes representing our components'''
                c_r = pygame.Rect(0, 0, 256, 256)
                # hide the cursor if we're in here
                pos = (pygame.mouse.get_pos()[0] - 20 , pygame.mouse.get_pos()[1] - 20)

                if(c_r.collidepoint(pos)):
                        pygame.mouse.set_visible(0)
                else:
                        pygame.mouse.set_visible(1)

                # left, top, width, height
                ## draw the border
                pygame.draw.rect(surf, (45, 45, 45), c_r, 0 )

                width = 32
                height= 32

                def draw_box_label(i, inrow, color, component_counter):
                        boxrect = pygame.Rect(inrow*width, i*height, width, height)
                        # Display some text
                        global gfont
                        text = gfont.render(str(component_counter), 1, color)
                        textpos = boxrect
                        surf.blit(text, textpos)

                def draw_box(i, inrow, color, component_counter):
                        '''draw a single box'''
                        boxrect = pygame.Rect(inrow*width, i*height, width, height)
                        a = b = c = 0
                        global bigned
                        boxrect_big = pygame.Rect(inrow*width - width*1, i*height - height*1, width*3, height*3)
                        t = color_ut.get_tween_value(str(component_counter))

                        if boxrect.collidepoint(pos): # this is an active box
                                a = color_ut.get_tween_value("active_box")
                                global selected_component_id
                                selected_component_id = component_counter
                                color = [200, 200 , 200+(t/2)]
                        elif boxrect_big.collidepoint(pos):
                                b = color_ut.get_tween_value("nearbox_1")
                                color=[a+b+t + 20, a+b+t + 20 , t/2 + 40]
                        else: # This is a regular component, draw it using its tween
                                color = [a+b+t, a+b+t, 20+ (t/2)]

                        if(selected_component_id != component_counter):
                                c_dict = bigned.get_component_by_id(component_counter)
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
                        draw_box_label(i, inrow, get_color_inverse(color), component_counter)

                component_counter = 0
                for i in range(8):
                        for inrow in range(8):
                                d = color_ut.get_tween_value("default_box")
                                color = [d,d,d]
                                draw_box(i, inrow, color, component_counter)
                                component_counter += 1

                #dlog.info("drew component grid....")

                return ## Draw components

        def draw_version_label(surf,color=(200,200,200)):
                global gfont
                surf.fill((40,40,40))
                text = gfont.render("bigned " + __version__, 1, color)
                r=pygame.Rect(0,0,100,20)
                surf.blit(text, r)

        def draw_panel_label(surf):
                '''draw the bottom panel label'''
                global selected_component_id
                global gfont

                surf.fill((40,40,40))
                info_paragraph = []

                info_paragraph.append("Currently selected component: %d " % selected_component_id)
                c_dict = bigned.get_component_by_id(selected_component_id)

                c_dict['lock'].acquire()
                octo = c_dict['component'].get_octo()
                c_dict['lock'].release()

                #info_paragraph.append("Internal octo: ")

                info_paragraph.append("    component type : %s" % octo["type_hints"])
                info_paragraph.append("    source : %s" % octo["source"])

                info_paragraph.append("")

                for number,line in enumerate(info_paragraph):
                        rpos = pygame.Rect(0, (number*gfont.get_height()), 20,20) # location of text
                        text = gfont.render(line, 1, (100,200,100))
                        surf.blit(text, rpos)

        def draw_info_about_component_from_id(where):
                pass

        ## Actual Draw() starts here

        global screen
        screen.fill((35, 35, 35))


        panel_label_surf = pygame.Surface((256, 170))
        component_surf = pygame.Surface((256, 256))
        version_label_surf = pygame.Surface((100, gfont.get_height()))

        component_box_where= (20,20)
        panel_label_where = (20, 300)
        version_label_where = (5,5)

        global main_breakout
        global user_console


        llog.info("entering main draw loop")
        while main_breakout.value == 1:
                ## This is our main loop, draw input screen and update tweener
                user_console.process_input()
                user_console.draw()
                #
                # color_ut.update_frame()
                #
                draw_version_label(version_label_surf)

                draw_panel_label(panel_label_surf)
                draw_components_on_surf(component_surf)

                #deg = color_ut.get_tween_value("rotation_angle");
                #rotated_component_surf = pygame.transform.rotate(component_surf,  deg)
                #print deg

                screen.blit(version_label_surf, version_label_where)
                screen.blit(component_surf, component_box_where)
                screen.blit(component_surf, component_box_where)

                screen.blit(panel_label_surf, panel_label_where)

                pygame.display.flip()


        llog.info("exiting main draw loop...")


        return
        ## Draw() ends here


def update_frame_loop(ut, update_by=1):
    while main_breakout.value == 1:
        llog.info("ran frame updater on %s ", ut)
        ut.update_frame(update_by)
        sleep(1)
    llog.info("out of frame loop...")

if __name__ == '__main__':
        global dlog
        global bigned

        llog.info("Here we go!!!")

        bigned = sid.Sid()
        bigned.setname("BigNed")

        llog.info("The sid %s was created successfully, he's not alive yet though [ SUCCESS ] " % bigned.getname() )

        color_ut = ut.Ut()

        if not color_ut :
                raise Exception("error init ut")
                exit(1)


        llog.info("init ut in main process")

        try:
                color_ut = add_color_tweeners(color_ut)
        except :
                llog.error("failed to init tweeners: %s", e)
                exit(1)

        SidProcess = Process(target=bigned.live) # sid process
        DrawProcess = Process(target=Draw, args=(bigned,color_ut)) # draw
        TweenerProcess = Process(target=update_frame_loop,args=(color_ut, 1))


        global main_breakout
        main_breakout.value = 1

        TweenerProcess.start()
        llog.info("[1/3] : tweener process was started")

        SidProcess.start()
        llog.info("[2/3] : sid process was started ")

        DrawProcess.start()
        llog.info("[3/3] : draw process was started")


        # Important: start tweener updater before everything else?
        DrawProcess.join()
        llog.info("      -> joined draw process [ SUCCESS ] ")

        SidProcess.join()
        llog.info("      -> joined ned [ SUCCESS ] ")


        TweenerProcess.join()
        llog.info("      -> joined tween process [ SUCCESS ] ")


        llog.info("All done, bye!")

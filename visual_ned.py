"""draw a visual AI window"""
"""Three  processes: NedProcess, DrawProcess, UpdateDataProcess"""

import os,sys
import pygame,pyconsole
import gui_helpers as g
from ned import Ned
from multiprocessing import Process, Value
from Text import Text
from getmylogger import silent_logger,loud_logger
import random

from time import sleep
import exceptions
import ut

__version__ = "base"

USER_CONSOLE_ENABLED = True #only checked when drawing


globals()["dlog"] = silent_logger("drawing") #silent drawing logger
globals()["llog"] = loud_logger("visual_ned") #loud logger (shows in console)

globals()["llog"].info("log setup! [ SUCCESS ] ")

globals()["bigned"] = None

try:
        global llog
        globals()["screen"] = g.init_pygame()
        llog.info("init'd screen [ SUCCESS ]")
        globals()["gfont"] = g.create_font()
        llog.info("init'd font successful [ SUCCESS ] ")
        
        globals()["gselected_component"] = 1
        globals()["main_breakout"] = Value("d", 0)

        llog.info("ut init'd successfully...  [ SUCCESS ] ")
        
        globals()["color_ut"] = None
        
except TypeError as e:
        llog.error("type error while init %s  [ FAIL ] ", e)
        exit(1)
except:
        llog.error("error while init  [ FAIL ] ")
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

globals()["user_console"] = init_console(globals()["screen"], key_calls={"d": extinguish_and_deload})

#### Start here

def setup_color_tweens():
        for i in range(256):
                st = random.randint(0, 90)
                color_ut.add_tweener(str(i), st, 100)
                color_ut.tween_to_up(str(i), 100)
                llog.info("set up '%s' with %d and %d", str(i), st, 100)
        pass

def init_color_tweeners():
        global color_ut
        color_ut = ut.Ut(1)
        
        color_ut.add_tweener("default_box")
        color_ut.constant("default_box", 50)
        
        color_ut.add_tweener("active_box")
        color_ut.tween_to_up("active_box", 100)
        
        color_ut.add_tweener("nearbox_1")
        color_ut.tween_to_up("nearbox_1", 50)
        
        color_ut.add_tweener("nearbox_2")
        color_ut.tween_to_up("nearbox_2", 20)
        
        try:
                setup_color_tweens()
        except Exception as e :
                llog.error("Couldnt setup color tweens for components...")
                print e
                exit(1)
        return


try:
        init_color_tweeners()
except ValueError as e:
        llog.error("failed to init tweeners: %s", e)
        exit(1)
except Exception as e:
        print e
        llog.error("unknown error 1")
        exit(1)
        
def octo_getcolor(octo):
        return octo[0]

def Draw(theNed):
        """draw the given Ned on global scr"""
        # TODO:
        # Things to draw on main screen:
        #       - What sid thinks it looks like (as a person)
        #       - output from one of the text components
        # Things to input:
        #       - Right-click menu
        #       - components that fire together wire together
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

                width = 16
                height= 16


                def draw_box(i, inrow, color, component_counter):
                        '''draw a single box'''
                        boxrect = pygame.Rect(inrow*width, i*height, width, height)
                        a = b = c = 0
                                                       
                               
                        global color_ut
                        # left, top, width, height

                        boxrect_big = pygame.Rect(inrow*width - width*1, i*height - height*1, width*3, height*3)
                        t = color_ut.get_tween_value(str(component_counter))
                        if boxrect.collidepoint(pos): # this is an active box
                                a = color_ut.get_tween_value("active_box")
                                color = [a,200,random.randint(0,100)]
                        elif boxrect_big.collidepoint(pos):
                                b = color_ut.get_tween_value("nearbox_1")
                                color=[a+b+t*2, a+b+t, 40]
                        else: # This is a regular component, draw it using its tween
                                color = [a+b+t, a+b+t, t/2]
                        try:
                                pygame.draw.rect(surf, color, boxrect , 0)
                        except:
                                llog.warning("bad color?")
                        
                component_counter = 0
                for i in range(16):
                        for inrow in range(16):
                                d = color_ut.get_tween_value("default_box")
                                color = [d,d,d]
                                draw_box(i, inrow, color, component_counter)
                                component_counter += 1

                dlog.info("drew component grid....")

                return ## Draw components

        def draw_version_label(screen):
                version_text=Text(screen, globals()["gfont"], pygame.Rect(0,0,0,0) ,
                                 "sid simulator " + __version__)
                version_text.draw()
                dlog.info("drew version label")

        def draw_panel_label(screen, label):
                '''draw the bottom panel label'''
                sc.fill((35, 35, 35))
                panel_text = Text(screen,  globals()["gfont"], pygame.Rect(30, 300, 0, 0), label)
                panel_text.draw();
                dlog.info("drew panel label")

        ## Actual Draw() starts here

        global screen
        screen.fill((35, 35, 35))

        llog.info("entering main draw loop")

        global main_breakout
        global color_ut
        
        while main_breakout.value == 1:
                ## This is our main loop, draw input screen and update tweener
                
                globals()['color_ut'].update_frame(increase_by=1)
                
                global user_console
                user_console.process_input()
                user_console.draw()

                
                
                try:
                        color_ut.update_frame()
                except ValueError as e:
                        llog.error("update frame error? %s ", e)
                        exit(1)
                draw_version_label(screen)
                component_surf = pygame.Surface((256, 256))
                draw_components_on_surf(component_surf)

                
                component_box_where= (20,20)
                screen.blit(component_surf, component_box_where)

                pygame.display.flip()

        llog.info("exiting main draw loop...")


        return
        ## Draw() ends here

def UpdateData(n):
        #Current component duplex pipe::
        llog.info("* PROCESS updatedata started")

        while main_breakout.value == 1:
                try:
                        a = n.get_component_tuples()
                except RuntimeError as e:
                        llog.warning("unable to get component tuples")
                        sleep(1)
                        continue
                
                
                for t in a:
                        exit(1)
                sleep(1)

        llog.info("exiting updatedata loop")

if __name__ == '__main__':
        global llog
        global dlog
        global bigned
        
        llog.info("here we go")
        dlog.info('create console')

        # Create ned process

        llog.info("creating processes")

        bigned = Ned()
        bigned.setname("bigned-"+__version__)

        llog.info("this is ned %s" % __version__)
        # log("creating processes")
        NedProcess = Process(target=bigned.live)

        # Create draw process
        DrawProcess = Process(target=Draw, args=(bigned,))

        # Create UpdateDataProcess
        UpdateDataProcess = Process(target=UpdateData, args=(bigned,))

        global main_breakout
        main_breakout.value = 1

        NedProcess.start()
        llog.info("created ned process")

        DrawProcess.start()
        llog.info("created draw process")

        UpdateDataProcess.start()
        llog.info("created updatedata process")

        llog.info("********* in main process... ")

        DrawProcess.join()
        llog.info("      -> joined draw process [ SUCCESS ] ")

        NedProcess.join()
        llog.info("      -> joined ned [ SUCCESS ] ")

        UpdateDataProcess.join()
        llog.info("      -> joined update [ SUCCESS ] ")

        llog.info("All done bye")

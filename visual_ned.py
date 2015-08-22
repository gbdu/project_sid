import os,sys
import pygame
from ned import Ned
from pyconsole import Console
from multiprocessing import Process, Lock, Value
from Text import Text
from getmylogger import silent_logger,loud_logger
import random
from time import sleep

current_view_component = 1
big_counter = 0 # between 0-255
processes = []
user_console = None
TheBigNed = 0

dlog = silent_logger("drawing")
log = loud_logger("visual_ned")

#       Three  processes:
#       NedProcess                                      DrawProcess(Ned Object)                 UpdateDataProcess
#        |                                                                                |                                                     |
#       Runs a regular ned          Repeatedly draws info on screen      (Updates data recv'd from pipes)
#

__version__ = "1.1-alpha"

font = None
main_breakout = Value("d", 0)

octos_snapshot = [] # should be 64
octos_locks = [Lock() for i in range(64)]

def init_pygame():
        '''init pygame and return a screen object'''
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        dlog.info("init pygame")
        #hide the mouse

        return screen

def extinguish_and_deload():
        main_breakout.Value = 0
        log.info("extinguished")
        TheBigNed.signal_extinguish()
        

def init_console(screen):
        r = pygame.Rect(300, 20, 320, 256)
        user_console = Console(screen, r, key_calls={"d": extinguish_and_deload } )
        log.info("init user console")
        return user_console

sc = init_pygame()

def octo_getcolor(octo):
        return octo[0]

def Draw(theNed):
        """Initialize pygame then draw the given Ned"""


        def get_component_color(component_pipe):
                '''get the color of the box that represents the component'''
                #return component.get_color_dim()
                return component_pipe.recv()

        def draw_component_info_on_surf(surf, where):
                dlog.info("draw component info")
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
                        global big_counter
                        boxrect = pygame.Rect(inrow*width, i*height, width, height)

                        if boxrect.collidepoint(pos):
                                color = (color[0]+10,color[1]+20,color[2]+80)
                                if(pygame.mouse.get_pressed()[0]):
                                        global current_view_component
                                        current_view_component = component_counter
                                        user_console.output("Switched to current: %d " % current_view_component)
                        # left, top, width, height

                        # Near values for nice mouse gradient:

                        boxrect_bigger = pygame.Rect(inrow*width - width*1, i*height - height*1, width*3, height*3)
                        if boxrect_bigger.collidepoint(pos):
                                color = (big_counter/2,color[1]+10+3*random.randint(1,4),color[2]+10)

                        # Near values for nice mouse gradient:
                        boxrect_bigger2 = pygame.Rect(inrow*width-3*width, i*height-3*height, width*7, height*7)
                        if boxrect_bigger2.collidepoint(pos):
                                color = (color[0]+10+3*random.randint(1,2),color[1]+10+3*random.randint(1,4),color[2]+10)

                                #self.current_component_info = "AAAAAAAAAA component info!!!"
                        pygame.draw.rect(surf, color, boxrect , 0)

                        big_counter += 1
                        if(big_counter >= 256):
                                big_counter = 0

                component_counter = 0
                for i in range(0, 16):
                        for inrow in range(16):
                                color = (inrow,i,i*inrow/10)
                                draw_box(i, inrow, color, component_counter)
                                component_counter += 1

                dlog.info("drew component grid....")

                return ## Draw components

        def draw_version_label(screen):
                version_text=Text(screen, font, pygame.Rect(0,0,0,0) ,
                                 "sid simulator " + __version__)
                version_text.draw()
                dlog.info("drew version label")

        def draw_panel_label(screen, label):
                '''draw the bottom panel label'''
                sc.fill((35, 35, 35))
                panel_text = Text(screen, font, pygame.Rect(30, 300, 0, 0), label)
                panel_text.draw();
                dlog.info("drew panel label")

        def init_fonts():
                global font

                wk_dir = os.path.dirname(os.path.realpath('__file__'))
                font_dir = os.path.join(wk_dir, "fonts")

                font = pygame.font.Font(os.path.join(font_dir, "forb.ttf"), 8)
                return

        ## Actual Draw() starts here

        sc.fill((35, 35, 35))
        init_fonts()


        log.info("entering main draw loop")
        user_console.output("hello")
        
        while main_breakout.Value == 1:
                user_console.process_input()
                user_console.draw()
                draw_version_label(sc)
                component_surf = pygame.Surface((256, 256))
                draw_components_on_surf(component_surf)
        
                component_box_where= (20,20)
                sc.blit(component_surf, component_box_where)
        
                #component_info_surf = pygame.Surface((256,100))
                #component_info_where = (256+60,256+60)
                #draw_component_info_on_surf(component_info_surf, component_info_where)
        
               # sc.blit(component_info_surf, component_info_where)
                pygame.display.flip()

        log.info("exiting main draw loop...")
       
        
        return
        ## Draw() ends here

def UpdateData(n):
        #Current component duplex pipe::
        log.info("updatedata started")
        while main_breakout.Value == 1:
                
                sleep(1)
                
                a = n.get_component_tuples()[2]
                b = n.get_component_tuples()[3]
                
        log.info("exiting updatedata loop")

if __name__ == '__main__':
        # Create the three processes:
        # -----
        log.info("here we go")

        user_console = init_console(sc)
        user_console.output("info:Created console")
        log.info('create console')
        
        # Create ned process
        n = Ned()
        
        global TheBigNed
        TheBigNed = n

        log.info("creating processes")

        n.setname("ned-"+__version__)

        log.info ("this is ned %s" % __version__)
        # log.info("creating processes")
        NedProcess = Process(target=n.live)

        # Create draw process
        DrawProcess = Process(target=Draw, args=(n,))

        # Create UpdateDataProcess
        UpdateDataProcess = Process(target=UpdateData, args=(n,))

        main_breakout.Value=1
        
        NedProcess.start()
        log.info("created ned process")

        DrawProcess.start()
        log.info("created draw process")

        #UpdateDataProcess.start()
        log.info("created updatedata process")

        log.info("********* in main process... ")
        
        DrawProcess.join()
        log.info("      -> joined draw process")
        
        NedProcess.join()
        log.info("      -> joined ned")
        
        # UpdateDataProcess.join()
        log.info("      -> joined update")
        
        log.info("All done!")
        
#!/usr/bin/python2.7

"""
A visual representation of a Sid
This has the following asynch processes running:
        - sid.live
        - drawing
        - universal tweener updater
"""

__author__ = 'gbdu'
__license__ = "GPL"
__version__ = "1.6-alpha"
__email__ = "ogrum@live.com"

# Import main dependencies:
try:
    import sys
    import pygame
    import time
    from multiprocessing import * 
    import traceback
    from time import sleep

except ImportError as e:
        print("failed to import main dependencies...")
        print(e)
        exit(1)
# Import my dependencies:
try:
    from helpers import getmylogger

    from ai import sid
    from mylibs import gut
    from gui import gui_helpers
    from gui import pyconsole
    from helpers import octo

except ImportError as e:
    print("failed to import bigned dependencies... ")
    print(e)
    exit(1)

GLOBAL_LIVE_FLAG = Value("d", 0)

selected_component_id = 0
clicked_component_id = None

dlog = getmylogger.silent_logger("silent_bigned")  # silent drawing logger
llog = getmylogger.loud_logger("bigned")  # silent drawing logger
zoom = 1

class BigNed:
    _mysid = None
    _layercache = None
    screen = None
    myfont = None
    mygut = None
    click = []  # clearead every two points...
    user_msg_q = None
    latest_octos = None
    layer_pipe = None

    global dlog
    global llog
    clicked_components = ()
    # whenever this reaches two, they get added and the list gets emptied

    def init_console(self, key_calls):
        try:
            r = pygame.Rect(300, 20, 300, 256)
            uc = pyconsole.Console(self.screen, r, key_calls=key_calls)
            return uc
        except:
            llog.error("unable to init console %s" % sys.exc_info()[0])
            exit(1)
            
    def lg(self, msg="defaultmsg"):
        '''drawn log output'''
        self.user_msg_q.put(msg)
        llog.info (msg)
        pass

    def extinguish_and_deload(self):
        llog.info("extinguish_and_deload called")
        GLOBAL_LIVE_FLAG.value = 0

    def __init__(self, user_msg_q, latest_octos, cmd_q, p):
        try:
            self.mygut = gut.Gut()
            self._mysid = sid.Sid()
            self._mysid.setname("BigNed")
            self.screen = gui_helpers.init_pygame()
            self.myfont = gui_helpers.create_font()
            self.latest_octos = latest_octos
            self.cmd_q = cmd_q
            self.layer_pipe = p
            #self.octo_q = octo_q
            self.user_msg_q = user_msg_q
        
        except Exception as e:
                llog.info("failed to init a bigned ... [ FAIL ] ")
                print traceback.print_exc()
                exit(1)

    def change_clicked(self, i):
        global clicked_component_id

        if(clicked_component_id == i):
            # This is to avoid putting multiple SELECTs in the queue
            # for the same ID.
            return

        if clicked_component_id: # Deselect the old one
            self.cmd_q.put("DESELECT %d" % clicked_component_id)

        clicked_component_id = i
        self.cmd_q.put("SELECT " + str(i) )

    def get_component_box(self, cid):
        width = 32
        height = 32
        counter = 0
        for row in range(8):
            for col in range(8):
                if counter == cid:
                    return pygame.Rect(col*width, row*height, width, height)
                counter += 1
        return pygame.Rect(col*width+cid,col*width+cid,width,height)

    def process_mouse(self, event):
        if (len(self.click)) == 2:
            self._mysid.make_components_friends(self.click[0], self.click[1])
            self.click = [ ] 

        #pos = pygame.mouse.get_pos()
        pos = event.pos
        pos = pos[0]-20,pos[1]-20

        # First, check if this is a mousewheel op
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                global zoom
                if zoom < 2: zoom += 0.01
            elif event.button == 5:
                global zoom
                if zoom > 0.5: zoom -= 0.01

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for i in range(64):
                box = self.get_component_box(i)
                if box.collidepoint(pos):
                    self.click.append(i)
                    self.change_clicked(i)
                    if (len(self.click)) == 2:
                        self._mysid.make_components_friends(self.click[0],
                            self.click[1])
                        self.click = [ ]

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (event.button == 3):
                self.click = []
            elif (len(self.click)) == 2:
                self._mysid.make_components_friends(self.click[0], self.click[1])
                self.click = [ ]

    def draw_version_label(self, surf, fps , color=(200,200,200)):
            '''draws the version info and fps on the top of the main screen'''
            surf.fill((40,40,40))

            text = self.myfont.render("bigned " + __version__ + " " + str(fps) + " fps", 1, color)
            r=pygame.Rect(0,0,150,20)
            surf.blit(text, r)

    def draw_paragraph(self, surf, para):
        for number,line in enumerate(para):
            rpos = pygame.Rect( 5, 5+(number*self.myfont.get_height()), 20,20)
            text = self.myfont.render(line, 1, (150,150,160))
            surf.blit(text, rpos)

    def draw_panel_label(self, surf):
        '''draw the bottom panel label'''
        global selected_component_id

        surf.fill((40,40,40))
        linfo = []
        linfo.append("Currently selected: %d " % selected_component_id)

        octo = self.get_latest_octo_from(selected_component_id)

        if octo is not None:
            linfo.append("*---- OCTO PACK ----*")
            linfo.append("    octo-hints : %s" % octo.type_hints)
            linfo.append("    octo-color : " + str(octo.color))
            linfo.append("    octo-source : %s" % octo.source)
            linfo.append("    octo-id : %s" % octo.myid)
            linfo.append("    octo-friends : %s" % octo.friends)
        else:
            linfo.append("{ This component has not queued an octo state\
             yet...}")

        linfo.append("*---- OCTO PACK ----*")

        self.draw_paragraph(surf, linfo)

    def draw_box_label(self, surf, color, bc, boxrect):
            text = self.myfont.render(str(bc), 1, color)
            textpos = (boxrect[0],boxrect[1])
            surf.blit(text, textpos)

    def get_neuron_box(self, surf, idx):
        sz = surf.get_size()
        n_width = 10
        n_height = 10
        padding=5
        rows = (sz[0] / n_width)-1
        cols = (sz[1] / n_height)-1
        counter = 0
        for r in range(rows):
            for c in range(cols):
                if counter == idx :
                    return (r*10 + 10, c*10 + 10, n_width-padding, n_height-padding)
                counter += 1

    def draw_neurons(self, surf, n, connections):
        ''' draws a representation of the connections between the neurons
        n and their connections '''

        # Draw neurons
        for counter,i in enumerate(n):
            # First draw the neurons
            color = (100, 50, i[1])
            rect = self.get_neuron_box(surf, counter)
            pygame.draw.rect(surf, color, rect, 0)
        
        # Draw connections
        for counter,i in enumerate(connections):
            p1 = (self.get_neuron_box(surf, i[0]))[0:2]
            p1 = p1[0]+2, p1[1]+2

            p2 = (self.get_neuron_box(surf, i[1]))[0:2]

            p2 = p2[0]+2, p2[1]+2

            pygame.draw.aaline(surf, (200,200,200), p1, p2, 1)

    def draw_layer_panel_on_surf(self, surf):
            '''draw the bottom panel label'''
            global selected_component_id

            # surf.fill((40,40,40))

            global clicked_component_id
            if clicked_component_id :
                self._layercache = self.layer_pipe.recv()
                
                n = []
                for i in self._layercache :
                    n.append(i)

                # get connections
                self._layercache = self.layer_pipe.recv()
                
                connections = []
                for i in self._layercache :
                    connections.append(i)

                self.draw_neurons(surf, n, connections)

            else:
                pass


    def draw_smaller_boxes(self, surf, boxrect, bc, bgcolor):
        width = boxrect[2] / 6
        height = boxrect[3] / 8
        top = boxrect[0] + 32 - width
        left = boxrect[1] + 32 - height

        o = self.get_latest_octo_from(bc)
        oc = o.color

        c = (bgcolor[0]+oc[0])/2,(oc[1]+bgcolor[1])/2,(oc[1]+bgcolor[2])/2
        r = pygame.Rect(top,left,width,height)

        pygame.draw.rect(surf, c, r, 0)

        # Right most minbox just shows the color avg between oct color from
        # process and the background color1
        r2 = pygame.Rect(top-8, left, boxrect[2]/5, boxrect[3]/5)
        pygame.draw.rect(surf, oc, r2, 0)

        # The next box shows the color straight from the octo
        r3 = pygame.Rect(top-16, left, boxrect[2]/5, boxrect[3]/5)
        # pygame.draw.rect(surf, oc, r3, 0)

        # The next box is todo
        r4 = pygame.Rect(top-24, left, boxrect[2]/5, boxrect[3]/5)
        # pygame.draw.rect(surf, (50,50,50), r4, 0 )

    def draw_box(self, surf, boxrect, bc):
            a = b = c = 0 # used for fancy tweening
            
            octo = self.get_latest_octo_from(bc)

            width = boxrect[2]
            height = boxrect[3]
            #self.lg(str(boxrect))
            i = boxrect[1]/width
            col = boxrect[0]/height
            pos = pygame.mouse.get_pos()
            pos = pos[0]-20,pos[1]-20

            boxrect_big = pygame.Rect(col*width - width*1, i*height -
                height*1, width*3, height*3)
            t = self.mygut.get_tween_value(str(bc))
            color = (0,0,0)

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

            clicked = 0
            if bc in self.click:
                clicked = 1

            if len(self.click) == 1:
                p1_rect = self.get_component_box(self.click[0])
                p1 = p1_rect[0]+16,p1_rect[1]+16

                p2 = pos

                st = self.mygut.get_tween_value("selected_line")
                pygame.draw.aaline(surf, (st,st,st), p1, p2, 5)

            if(selected_component_id != bc): ## Affect color by hint type
                    if(octo.type_hints == "audio"):
                            color = (color[0], color[1]+15, color[2]+10)
                    if(octo.type_hints == "video"):
                            color = (color[0]+15, color[1]+10, color[2])
                    if(octo.type_hints == "langu"):
                            color = (color[0]+15, color[1]+5, color[2]+20)

            pygame.draw.rect(surf, color, boxrect , 1 if clicked else 0)

            self.draw_smaller_boxes(surf, boxrect, bc, color)
            self.draw_box_label(surf, gui_helpers.get_color_inverse(color), bc, boxrect)

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

            pygame.draw.rect(surf, (150, 150, 150), c_r, 0 )
            width = 32
            height= 32


            for b in range(64): ## first draw the boxes
                brect = self.get_component_box(b)
                self.draw_box(surf, brect, b)

            # for b in range(64): ## draw the connection
            #     #[b, width,height]
            #     brect = self.get_component_box(b)
            #     octo = self.get_latest_octo_from(b)

            #     for p in octo.friends:
            #         frect = self.get_component_box(p)

            #         p1 = brect[0] + (width/2),brect[1] + (height/2)
            #         p2 = frect[0] + (width/2),frect[1] + (width/2)
                    
            #         pygame.draw.aaline(surf, (200,200,200), p1, p2, 2)

    #XXX : INFINITE/BREAKABLE LOOP 1 (DRAW)
    def draw_loop(self, break_flag):
        """\
        draw the given Ned on INIT'd scr
        """
        self.screen.fill((35, 35, 35))
        panel_label_surf = pygame.Surface((256, 120))
        component_surf = pygame.Surface((256, 256))
        version_surf = pygame.Surface( (150,
            self.myfont.get_height()) )
        layer_panel_surf = pygame.Surface((256, 120))

        component_box_where = (20, 20)
        panel_label_where = (20, 300)
        version_label_where = (5, 5)
        layer_panel_where = (300, 300)

        frame_counter = 0.0

        frame_counter_start_time = time.time()
        fps = 0.0
        FPS_AVG = 10.0
        # Main process blocks here
        while True:
            if break_flag.value == -1:
                # -1 means "pause a bit..."
                sleep(2)  # sleep for two seconds then try again
                continue
            elif break_flag.value == 0:  # 0 means stop
                self.extinguish_and_deload()
                self.lg("broke out of draw loop")
                break

            user_console.process_input()

            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                self.extinguish_and_deload()
                break 

            if event.type == pygame.MOUSEBUTTONUP:
                self.process_mouse(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.process_mouse(event)
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            else:
                x, y = 0, 0

            if not self.user_msg_q.empty():
                msg = self.user_msg_q.get_nowait()
                user_console.output(msg)

            user_console.draw()

            self.mygut.update_frame()  #TODO move this to independent process...

            self.draw_version_label(version_surf, fps)
            self.draw_layer_panel_on_surf(layer_panel_surf)
            self.draw_panel_label(panel_label_surf)
            self.draw_components_on_surf(component_surf)

            
            rod = pygame.transform.rotozoom(component_surf, 0, zoom) \
                if zoom != 1 else component_surf

            #self.draw_links_on_surf(component_surf)
            self.screen.blit(version_surf, version_label_where)
            self.screen.blit(rod, component_box_where)
            self.screen.blit(panel_label_surf, panel_label_where)
            self.screen.blit(layer_panel_surf, layer_panel_where)
            pygame.display.flip()
            elapsed_time = time.time() - frame_counter_start_time


            if(elapsed_time >= FPS_AVG):  # FPS_AVG is how many seconds fps
            # is averaged over...
                    ## Calculate fps
                    fps = frame_counter / FPS_AVG
                    frame_counter_start_time = time.time() # set time again...
                    frame_counter = 0.0 # set starting frame again
            else:
                    frame_counter += 1.0

    def create_sid_process(self, break_flag, msg_q, octo_q, octo_d, p):
            '''
            start the sid loop process
            break_flag -- a value indicating live loop exit state
            '''
            SidProcess = Process(target=self._mysid.start_and_block,args=
                (break_flag, msg_q, octo_q, octo_d, p))
            SidProcess.start()
            return SidProcess

    def create_draw_process(self, break_flag, uc):
            ''' start the draw loop process '''
            drawp = Process(target=self.draw_loop, args=(break_flag,))
            #  sid process
            drawp.start()
            return drawp

    def info_loop(self, breakflag, q, m):
        import datetime
        while breakflag.value :
            pass
            # msg = str( datetime.datetime.now() )
            # try:
            #     msg += m.recv()
            #     q.put(str(msg))
            # except:
            #     traceback.print_exc()


    def create_info_process(self, break_flag, msg_queue, m):
            ''' start the info process, sends useful hints to user'''
            infop = Process(
                target=self.info_loop,
                args=(break_flag, msg_queue, m, )
                )

            infop.start()
            return infop

    def get_latest_octo_from(self, cid):
        if str(cid) in self.latest_octos:
            o = self.latest_octos[str(cid)]
            return o.get_a_copy() # Get a copy so we dont accidentally write it over 
        else:
            return octo.Octo()


if __name__ == '__main__':
    global user_console
    global llog
    component_num = 64

    llog.info("Here we go!!!")
    octo_q = Queue()  # a list of (componentid,(lockparent,lockchild))
    user_msg_q = Queue()
    cmd_q = Queue()
    manager = Manager()
    latest_octos = manager.dict()
    pa1,pa2 = Pipe()
    

    try:
        bn = BigNed(user_msg_q, latest_octos, cmd_q, pa1)
        key_calls = {
            "d": bn.extinguish_and_deload
        }
        user_console = bn.init_console(key_calls)

    except Exception as e:
        llog.error("could not create bigned or console")
        print e
        exit(1)

    try:
        GLOBAL_LIVE_FLAG.value = -1
        p1 = bn.create_sid_process(GLOBAL_LIVE_FLAG, cmd_q,
         octo_q, latest_octos, pa2)
        p2 = bn.create_draw_process(GLOBAL_LIVE_FLAG, user_console)
        p3 = bn.create_info_process(GLOBAL_LIVE_FLAG, user_msg_q, pa1)
       # p4 = bn.create_octo_process(GLOBAL_LIVE_FLAG)
    except Exception as e:
        llog.error("could not create processes")
        print e
        exit(1)

    # pl = []
    # c = 0
    # while c != 63:
    #     pl.append(pipelist_p.get())
    #     print c 
    #     c += 1
    # llog.info("%d pipes received -- waiting for main processes" % c)


    GLOBAL_LIVE_FLAG.value = 1

    bn.lg("Started processes - filling cache/main loop")

    bn.lg("now waiting to join")
    
    p2.join()
    llog.info("p2  -> draw process is done")
    GLOBAL_LIVE_FLAG.value = 0
    p1.join()
    llog.info("p1  -> sid process is done")

    p3.join()
    llog.info("p3  -> user info process is done")
    llog.info("p4  -> snapper process is done")


    llog.info("All done, bye!")

    pygame.quit()
    pass

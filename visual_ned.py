import pygame
import time
from ned import Ned
from pyconsole import Console
from multiprocessing import Process, Lock, Value, Array
import os,sys
from Text import Text

import logging

formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(name)s:%(lineno)d} %(levelname)s - %(message)s','%H:%M:%S')

drawlogger = logging.getLogger("drawing")
hdlr = logging.FileHandler('logs/drawing')
hdlr.setFormatter(formatter)
drawlogger.addHandler(hdlr)

logger = logging.getLogger("visual_ned")
hdlr = logging.FileHandler('logs/visual_ned')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

#	Three  processes:
#	NedProcess					DrawProcess(Ned Object)			UpdateDataProcess
#	 |										  |							|
#	Runs a regular ned	    Repeatedly draws info on screen	 (Updates data recv'd from pipes)
#

__version__ = "1.0-alpha"

font = None
main_breakout = Value("d", 0)

octos_snapshot = [] # should be 64
octos_locks = [Lock() for i in range(64)]

def octo_getcolor(octo):
	return octo[0]

def Draw(theNed):
	"""Initialize pygame then draw the given Ned"""
	
	def init_pygame():
		'''init pygame and return a screen object'''
		pygame.init()
		screen = pygame.display.set_mode((640, 480))
		drawlogger.info("init pygame")
		return screen

	def get_component_color(component_pipe):
		'''get the color of the box that represents the component'''
		#return component.get_color_dim()
		return component_pipe.recv()
		
	def draw_components(surf):
		'''Draw a grid of 16x16 boxes representing our components'''
		# left, top, width, height
		## draw the border
		pygame.draw.rect(surf, (45, 45, 45), pygame.Rect(0, 0, 256, 256), 0 )

		width = 16
		height= 16

		def draw_box(i, inrow, color):
			'''draw a single box'''
			r = pygame.Rect(inrow*width, i*height, width, height)
			pygame.draw.rect(surf, color, r , 0)
					
		for i in range(0, 16):
			for inrow in range(16):
				# x = iter(color_list)
				
				octos_locks[i+inrow].acquire()
				color=octo_getcolor(octos_snapshot[i+inrow])
				octos_locks[i+inrow].release()
				
				#color = (inrow,i*10,i*inrow/10)
				draw_box(i, inrow, color)
				
		drawlogger.info("drew component grid....")
		return ## Draw components
	
	def draw_version_label(screen):
		version_text=Text(screen, font, pygame.Rect(0,0,0,0) ,
				 "sid simulator " + __version__)
		version_text.draw()
		logging.info("drew version label")

	def draw_panel_label(screen, label):
		'''draw the bottom panel label'''
		panel_text = Text(screen, font, pygame.Rect(30, 300, 0, 0), label)
		panel_text.draw();
		drawlogger.info("drew panel label")
	
	def init_fonts():
		global font
		
		wk_dir = os.path.dirname(os.path.realpath('__file__'))
		font_dir = os.path.join(wk_dir, "fonts")
		
		font = pygame.font.Font(os.path.join(font_dir, "forb.ttf"), 8)
		return

	def extinguish_and_deload():
		logger.info("extinguished")
		theNed.signal_extinguish()		
		pygame.display.quit()
		pygame.quit()
		logging.info("really extinguished")

	def init_console(screen):
		global user_console
		r = pygame.Rect(300, 20, 320, 256)
		user_console = Console(screen, r, key_calls={"d": extinguish_and_deload} )
		logger.info("init user console")
		return user_console
	
	## Actual Draw() starts here
	
	sc = init_pygame()
	sc.fill((35, 35, 35))
	init_fonts()
	user_console = init_console(sc)
	pipe_list = theNed.get_component_pipes()
	
	logger.info("entering main draw loop")
	while main_breakout.value == 1: # main loop
		user_console.process_input()
		surf = pygame.Surface((256, 256))
		
		user_console.draw()
		
		draw_components(surf)
		
		draw_panel_label(sc, "aaaaaa")
		
		where = (20,20)
		blittedRect = sc.blit(surf, where)
		pygame.display.flip()
		

	## Draw() ends here

def UpdateData(n):
	l = n.get_component_pipes()
	
	while main_breakout.value == 1:
		logger.info("updated")
		
		for idx, val in enumerate(l):
			octos_locks[idx].acquire()
			octos_snapshot[idx] = val.recv()
			octos_locks[idx].release()
			
			
			#octos[1]=[12,12,12]

if __name__ == '__main__':	
	# Create the three processes:
	# -----
	
	# Create ned process
	n = Ned()
	n.setname("ned-"+__version__)
	NedProcess = Process(target=n.live)
	
	
	
	# Create UpdateDataProcess
	UpdateDataProcess = Process(target=UpdateData, args=(n,))

	# Create draw process
	DrawProcess = Process(target=Draw, args=(n,))
	
	main_breakout.value=1
	
	NedProcess.start()
	UpdateDataProcess.start()
	DrawProcess.start()
	
	NedProcess.join()
	UpdateDataProcess.join()
	DrawProcess.join()

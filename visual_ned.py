import pygame
import time
import ned
import threading
import pygame
import pyconsole
import os, sys
import trunc
from Text import Text


__version__ = "1.0-alpha"

def Rest():
	MyComponents = MyNed.get_components();


	def get_component_color(component):
		return component.get_color_dim()

	def die():
		for i in MyComponents:
			i.die()

		pygame.display.quit()
		pygame.quit()
		sys.exit(0)

	def draw_everything_to_surf(surf):
		# left, top, width, height
		pygame.draw.rect(surf, (45, 45, 45), pygame.Rect(0, 0, 256, 256), 0) # draw background

		width = 16
		height= 16

		counter = 0
		for i in range(0,16):
			for box_num_in_row in range(16):
				x = iter(MyComponents)
				color = get_component_color(x.next())
				pygame.draw.rect(surf, color, pygame.Rect(box_num_in_row*width, i*height, width, height), 0)

	########################


	screen.fill((35, 35, 35))

	user_console = pyconsole.Console(screen, pygame.Rect(300, 20, 320, 256), key_calls={"d": die})

	wk_dir = os.path.dirname(os.path.realpath('__file__'))
	font = pygame.font.Font(os.path.join(os.path.join(wk_dir, "fonts"), "forb.ttf"), 8)

	version_text = Text(screen, font, pygame.Rect(0,0,0,0) , "sid simulator " + __version__)
	version_text.draw()


	panel_text = Text(screen, font, pygame.Rect(30, 300, 0, 0), MyNed.get_panel())
	panel_text.draw();

	break_out = False
	while break_out == False :
		# clear screen at the start of every frame
		user_console.process_input()

		# process console:
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				print "out"
				break_out = True
				die()
				break


		user_console.draw()
		panel_text.draw()


		surf = pygame.Surface((256, 256))

		draw_everything_to_surf(surf)

		where = 20,20
		blittedRect = screen.blit(surf, where)
		#oldCenter = blittedRect.center
		pygame.display.flip()


pygame.init()
degree = 0

screen = pygame.display.set_mode((640, 480))

MyNed = ned.Ned()
MyNed.setname("ned")


ta = threading.Thread(target=Rest)
ta.daemon=True

ta.start()
tx = threading.Thread(target=MyNed.live, args=(42,))
tx.start()

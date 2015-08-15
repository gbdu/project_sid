import pygame
import sys
import time
import ned

import pygame
from pygame import gfxdraw

# necessary pygame initializing
pygame.init()
degree = 0

screen = pygame.display.set_mode((640, 480))

MyNed = ned.Ned()
MyComponents = MyNed.get_components();

def get_component_color(component):
	return component.get_color_dim()

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



while True:
	# clear screen at the start of every frame
	screen.fill((35,35,35))
	surf = pygame.Surface((256, 256))


	draw_everything_to_surf(surf)

	where = 20,20
	blittedRect = screen.blit(surf, where)
	oldCenter = blittedRect.center
	pygame.display.flip()
	pygame.time.wait(1)




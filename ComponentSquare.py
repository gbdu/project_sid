import pygame
import sys

class CompnentSquare:
	def __init__(self, color):
		self.mycolor = color

	def set_color(self, color):
		pass

	def draw_on_grid(self, screen, row, column):
		pygame.draw.rect(screen, self.mycolor, ((10 + (row * 10), 10 + (column * 10), 10, 10)), 0)



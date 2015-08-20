import os
import pygame


__author__ = 'gargantua'
__doc__ = """
    descript
"""

wk_dir = os.path.dirname(os.path.realpath('__file__'))
font = pygame.font.Font(os.path.join(os.path.join(wk_dir, "fonts"), "forb.ttf"), 8)


class Text():
	"""spartan text class. Does not cache surface."""

	def __init__(self, font, posy, text=None):
		if text is None: text = "default text"
		self._text = text
		self.rect = posy
		self.render()

	def text(self, text):
		"""change text"""
		self.render(text)

	def render(self, text=None):
		if text is None: text = self._text
		self._text = text
		self.surface = self.font.render(self._text, True, (160, 120, 160))
		self.rect.size = self.surface.get_rect().size

	def draw(self):
		screen.blit(self.surface, self.rect)


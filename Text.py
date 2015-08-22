import os
import pygame
from itertools import chain

__author__ = 'gargantua'


class trunc:
	@staticmethod
	def truncline(text, font, maxwidth):
		real = len(text)
		stext = text
		l = font.size(text)[0]
		cut = 0
		a = 0
		done = 1
		old = None
		while l > maxwidth:
			a = a + 1
			n = text.rsplit(None, a)[0]
			if stext == n:
				cut += 1
				stext = n[:-cut]
			else:
				stext = n
			l = font.size(stext)[0]
			real = len(stext)
			done = 0
		return real, done, stext

	@staticmethod
	def wrapline(text, font, maxwidth):
		done = 0
		wrapped = []
		while not done:
			nl, done, stext = trunc.truncline(text, font, maxwidth)
			wrapped.append(stext.strip())
			text = text[nl:]
		return wrapped

	@staticmethod
	def wrap_multi_line(text, font, maxwidth):
		""" returns text taking new lines into account.
		"""
		lines = chain(*(trunc.wrapline(line, font, maxwidth) for line in text.splitlines()))
		return list(lines)


wk_dir = os.path.dirname(os.path.realpath('__file__'))

class Text():
	"""spartan text class. Does not cache surface."""

	def __init__(self, screen, font, rec, text=None):
		if text is None: text = "default text"
		self._text = text
		self.rect = rec
		self.font = pygame.font.Font(os.path.join(os.path.join(wk_dir, "fonts"), "forb.ttf"), 8)
		self.screen = screen
		self.render()

	def text(self, text):
		"""change text"""
		self.render(text)

	def render(self, text=None):
		if text is None: text = self._text
		
		wrapped = trunc.wrapline(unicode(text), self.font, 200)

		self.lines = []
		for i in wrapped :
			self.lines.append(self.font.render(i, True, (160, 120, 160)))

		#self.rect.size = self.surface.get_rect().size

		self.draw();


	def draw(self):
		j=0
		for i in self.lines:
			self.screen.blit(i, (int(self.rect.left), int(self.rect.bottom) + j* 8 ))
			j += 1

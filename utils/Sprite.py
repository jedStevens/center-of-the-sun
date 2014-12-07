import os
import pygame
from App import App
from Vector import Vector

class Sprite(pygame.sprite.DirtySprite):
	DEFAULT = pygame.image.load("assets/noImage.png")
	def __init__(self, x, y, path="", imgX=1, imgY=1, ext=".png"):
		pygame.sprite.Sprite.__init__(self)

		self.animated = False
		self.sheet = None
		self.image = None
		self.frame = 0
		self._subImgs = (imgX, imgY)
		self._sliceSize = (0,0)

		if path != "":
			if self._subImgs != (1,1):
				self.sheet = pygame.image.load(path+ext)
				self._sliceSize = (self.sheet.width  / self._subImgs[0],
						   self.sheet.height / self._subImgs[1])
				self.image = self.getSubImage(0)
			else:
				self.image = pygame.image.load(path+ext)
		else:
			self.image = Sprite.DEFAULT
		

		self.rect = self.image.get_rect()
		self.position = Vector(x,y)
		self.center = Vector(x + self.image.get_width() /2, y + self.image.get_width() / 2)

	"""

	INHERITED METHODS

	update(*args)	-> None
		updates the sprite

	add(*groups)	-> None
		adds the sprite to *groups

	remove(*groups)	-> None
		removes the sprite from *groups
	
	kill()		-> None
		removes the sprite from every group

	alive()		-> bool
		tests if this sprite is in 1 or more groups
	
	groups()	-> group_list
		returns the groups this sprite is in

	"""

	def preUpdate(self):
		pass
	
	def postUpdate(self):
		self.rect.x = self.position.x
		self.rect.y = self.position.y
		self.center = Vector.FromTuple(self.rect.center)
		if self.animated:	
			self.image = getSubImage(self.frame)

	def getSubImage(self, i):
		""" Gets sub Image at frame number i"""
		x =    (i % self._subImgs[0]) * self._sliceSize[0]
		y = int(i / self._subImgs[1]) * self._sliceSize[1]
		rect = pygame.Rect((x,y),self._sliceSize)
		return self.sheet.subsurface(rect)


import pygame
from App import App

class State(pygame.sprite.OrderedUpdates):
	def __init__(self, bgColor=None):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.bgColor = bgColor

	"""
	INHERITED METHODS

	sprites()	-> sprite list
		gets the sprites in the group
	
	copy()		-> Group
		copies the group

	add(*sprites)	-> None
		adds *sprites to the group

	remove(*sprites)-> None
		removes *sprites from the group
	
	has(*sprites)	-> Boolean
		tests if *sprites are in the group
	
	update(*args)	-> None
		updates the sprites in the group

	draw(Surface)	-> None
		draws the sprites to Surface

	empty()		-> None
		empties the group of all sprites

	"""
	def preUpdate(self):
		for obj in self.sprites():
			obj.preUpdate()
	
	def postUpdate(self):
		for obj in self.sprites():
			obj.postUpdate()
	
	def draw(self):
		return pygame.sprite.OrderedUpdates.draw(self, App.Screen)
	
	def quit(self):
		pass # To be overidden

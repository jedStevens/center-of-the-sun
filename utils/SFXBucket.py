import pygame
pygame.init()

class SFXBucket:
	def __init__(self):
		self.map = {}
		self.flags = {}

	def load(self, path, name, ext=".wav"):
		self.flags[name] = False
		self.map[name] = pygame.mixer.Sound(path+ext)
	
	def __getitem__(self, i):
		return self.map[i]

	def play(self, name):
		self.flags[name] = False			
		return self.map[name].play()

	def playAllFlagged(self):
		for key in self.flags:
			if self.flags[key]:
				self.play(key)
	
	def flag(self, name):
		self.flags[name] = True

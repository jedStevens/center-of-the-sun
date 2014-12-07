import pygame
from App import App
from Sprite import Sprite
pygame.init()
Scorefont = pygame.font.Font("assets/game/Circo.ttf", 32)

class Ball(Sprite):
	def __init__(self):
		Sprite.__init__(self, 0, 0, "assets/game/ball")
		self.source = self.image.copy()

	def updateScore(self, score):
		self.image = self.source.copy()
		scoreText = Scorefont.render(str(int(score)), True, (255,255,255))
		dest = (self.image.get_width() / 2 - scoreText.get_width() / 2,
			self.image.get_height()/ 2 - scoreText.get_height()/ 2)
		self.image.blit(self.source, (0,0))
		self.image.blit(scoreText, dest)
		
	def update(self):
		Sprite.update(self)
		self.position.x = (App.Width / 2) - (self.image.get_width() / 2)
		self.position.y = (App.Height / 2) - (self.image.get_height() / 2)

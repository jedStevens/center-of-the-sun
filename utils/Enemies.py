import random
import pygame, math
from Sprite import Sprite
from App import App
from Vector import Vector

class BaseObject(Sprite):
	SpawnDist = 530
	def __init__(self, angle, speed=100, path="", mod=0.0, level=1):
		Sprite.__init__(self, 0, 0, path)
		self.position = Vector.FromAngle(angle, BaseObject.SpawnDist)
		self.position += App.Center

		self.angle = angle
		self.speed = speed + (random.random()* mod)
		self.dist = BaseObject.SpawnDist
		self.level = level

	def update(self):
		Sprite.update(self)

		if (self.level == 1):
			pass
		elif (self.level == 2):
			self.angle += 0.25
		elif (self.level >= 3):
			self.angle += math.sin(pygame.time.get_ticks() / 250.0)

		self.dist -= self.speed * App.Elapsed
		self.position = Vector.FromAngle(self.angle, self.dist)
		self.position = self.position + App.Center
		if (Vector.Distance(self.center, App.Center) < 50):
			self.kill()

class ToShoot(BaseObject):
	def __init__(self, angle, speed=125, mod=0.0, level=1):
		BaseObject.__init__(self, angle, speed, "assets/game/toShoot", mod, level)

class ToAvoid(BaseObject):
	def __init__(self, angle, speed=125, mod=0.0, level=1):
		BaseObject.__init__(self, angle, speed, "assets/game/toAvoid", mod, level)

class ToGet(BaseObject):
	def __init__(self, angle, speed=125, mod=0.0, level=1):
		BaseObject.__init__(self, angle, speed, "assets/game/toGet", mod, level)


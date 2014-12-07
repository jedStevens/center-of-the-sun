import pygame
import math
from Sprite import Sprite
from Vector import Vector
from App import App

class Player(Sprite):
	def __init__(self):
		Sprite.__init__(self, 0, 0, "assets/game/player")
		self.angle = 0
		self.distance = 100
		self.velocity = 0
		self.accel = 17.0
		self.maxVelocity = 450.0
		self.bullets = pygame.sprite.Group()
		self.shootTimer = 0
		self.shootRate = 0.35
		self.shootSound = pygame.mixer.Sound("assets/game/shoot.wav")
	
	def update(self):
		Sprite.update(self)

		# Keyboard Input
		
		if (App.Keys[pygame.K_LEFT] or App.Keys[pygame.K_a] or 
		    App.Keys[pygame.K_RIGHT] or App.Keys[pygame.K_d]):
			if (App.Keys[pygame.K_LEFT] or App.Keys[pygame.K_a]):
				self.velocity -= self.accel
			if (App.Keys[pygame.K_RIGHT] or App.Keys[pygame.K_d]):
				self.velocity += self.accel
			if (abs(self.velocity) > self.maxVelocity):
				self.velocity = self.maxVelocity * math.copysign(1, self.velocity)
		
		else:
			self.velocity *= 0.80
			if (abs(self.velocity) < 0.1):
				self.velocity = 0.0
		
		self.shootTimer += App.Elapsed
		if (App.Keys[pygame.K_UP] or App.Keys[pygame.K_w] or App.Keys[pygame.K_SPACE]):
			self.shoot()

		# Move the player
		self.angle += self.velocity * App.Elapsed

		# Set Position
		self.position = Vector.FromAngle(self.angle, self.distance)
		self.position.x += (App.Width / 2) - (self.image.get_width() / 2)
		self.position.y += (App.Height / 2) - (self.image.get_height() / 2)

	def shoot(self):
		if self.shootTimer > self.shootRate:
			newBullet = Bullet(self.angle, self.distance)
			self.bullets.add(newBullet)
			for g in self.groups():
				g.add(newBullet)
			self.shootTimer = 0
			self.shootSound.play()

class Bullet(Sprite):
	def __init__(self, angle, playerDist, speed=100):
		Sprite.__init__(self, 0, 0, "assets/game/bullet")
		self.distance = playerDist + self.image.get_width()
		self.angle = angle
		self.speed = speed
		self.position = Vector.FromAngle(self.angle, self.distance)
		self.position.x += (App.Width / 2) - (self.image.get_width() / 2)
		self.position.y += (App.Height / 2) - (self.image.get_height() / 2)
	
	def update(self):
		Sprite.update(self)
		self.distance += self.speed * App.Elapsed
		self.speed += 3
		if self.distance > 600:
			self.kill()
		self.position = Vector.FromAngle(self.angle, self.distance)
		self.position.x += (App.Width / 2) - (self.image.get_width() / 2)
		self.position.y += (App.Height / 2) - (self.image.get_height() / 2)

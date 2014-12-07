import random
from Sprite import Sprite
from Enemies import *
from App import App

RANDOM		= 0
CWSPIRAL	= 1
CCWSPIRAL	= 2
BURST		= 3
ALT		= 4

Objects = [ToShoot, ToAvoid, ToGet]
Modes = [RANDOM, CWSPIRAL, CCWSPIRAL, BURST, ALT]

class ObjectHandler:
	def __init__(self, group, toShoot, toAvoid, toGet):
		self.group = group
		self.toShoot = toShoot
		self.toAvoid = toAvoid
		self.toGet = toGet

		self.mode = RANDOM
		self.modeTimer = 0
		self.modeRate = 5 + random.random()*2

		self.spawnTimer = 0
		self.spawnRate = 1.5
		self.spawnMulti = 1.0

		self.speed = 100
		self.angle = 0
		self.level = 1
		self.mod = 0.0 # THIS IS NOT self.mode
		self.enemy = None
		self.lastEnemy = None

		self.on = False


	def update(self):
		if self.on:
			self.spawnTimer += App.Elapsed
			self.modeTimer += App.Elapsed

			if (self.modeTimer > self.modeRate):
				self.mode = self.setUpMode(random.choice(Modes))

			if (self.spawnTimer > self.spawnRate):
				self.spawnEnemy()

	def spawnEnemy(self):
		if(self.mode == RANDOM):
			self.enemy = random.choice(Objects)
			self.angle = random.random()*270 - 135
			self.addObj()
		elif (self.mode == CWSPIRAL):
			self.enemy = random.choice(Objects)
			self.angle += 40
			self.addObj()
		elif (self.mode == CCWSPIRAL):
			self.enemy = random.choice(Objects)
			self.angle -= 40
			self.addObj()
		elif (self.mode == BURST):
			for i in range(3):
				self.enemy = Objects[i]
				self.angle += random.random()*60 + 10
				self.addObj()
		elif (self.mode == ALT):
			self.enemy = random.choice(Objects)
			if self.lastEnemy == ToShoot:
				self.enemy = ToAvoid
			self.angle += 180
			self.addObj()

	def addObj(self):
		obj = self.enemy(self.angle, self.speed, self.mod, self.level)
		if (self.enemy == ToShoot):
			self.toShoot.add(obj)
		elif (self.enemy == ToAvoid):
			self.toAvoid.add(obj)
		elif (self.enemy == ToGet):
			self.toGet.add(obj)
		
		self.group.add(obj)
		self.spawnTimer = 0
		self.lastEnemy = self.enemy

	def setDifficulty(self, score):
		diff = score / 10
		self.spawnRate = (1.5 - (float(diff) / 10.0)) * self.spawnMulti
		self.speed = 100 + (diff * 10)

	def setUpMode(self, mode):
		if mode == RANDOM:
			self.spawnMulti = 1.0
			self.mod = 0
		elif mode == CWSPIRAL or mode == CCWSPIRAL:
			self.enemy = random.choice(Objects)
			self.angle = random.randint(0,360)
			self.spawnMulti = 0.75
			self.mod = 0
		elif mode == BURST:
			self.spawnMulti = 2.0
			self.mod = 15
		elif mode == ALT:
			self.spawnMulti = 1.0
			self.mod = 0
			self.angle = random.randint(0,360)
		self.modeTimer = 0
		self.modeRate = 5 + random.random()*2
		return mode

	def start(self):
		self.on = True

	def stop(self):
		self.on = False

	def setLevel(self, level):
		self.level = level

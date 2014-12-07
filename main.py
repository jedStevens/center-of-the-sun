import pygame
import random
from pygame.sprite import *
from utils.App import App
from utils.State import State
from utils.Sprite import Sprite
from utils.Player import Player
from utils.Ball import Ball
from utils.ObjectHandler import ObjectHandler
from utils.SFXBucket import SFXBucket
pygame.init()
pygame.mixer.init()

Gamefont = pygame.font.Font("assets/game/Circo.ttf", 24)

class MainMenuState(State):
	def __init__(self):
		State.__init__(self)
		self.add(Sprite(0,0,"assets/menu/bg"))

	def update(self):
		if (App.justDown(pygame.K_SPACE)):
			App.switchState(ControlsState())

class ControlsState(State):
	def __init__(self):
		State.__init__(self, (0,0,0))
		self.add(Sprite(0,0, "assets/controls/bg"))

	def update(self):		
		if (App.justDown(pygame.K_SPACE)):
			App.switchState(GameState())

class GameState(State):
	def __init__(self):
		State.__init__(self, (12, 8, 116))
		self.player = Player()
		self.ball = Ball()
		self.toShoot = pygame.sprite.Group()
		self.toAvoid = pygame.sprite.Group()
		self.toGet = pygame.sprite.Group()
		self.objectHandler = ObjectHandler(self, self.toShoot, self.toAvoid, self.toGet)
		self.objectHandler.start()

		self.add(self.player)
		self.add(self.ball)

		self.score = 0
		self.scoreTotal = 0 #total from previous levels
		self.combo = 0
		self.timer = 100
		self.timeAddedFlag = 0.0
		self.level = 1
		
		self.sounds = SFXBucket()
		self.sounds.load("assets/game/bad", "bad")
		for i in range(11):
			self.sounds.load("assets/game/good"+str(i), "good"+str(i))
		self.sounds.load("assets/game/explosion", "shot")
		self.sounds.load("assets/game/countdown", "countdown")
		self.sounds.load("assets/game/time", "time")
		self.sounds.load("assets/game/levelUp", "levelUp")

		self.countDownPlayed = False
	
	def update(self):
		State.update(self)
		if self.timer > 0:
			self.timer -= App.Elapsed
		else:
			self.timer = 0
		
		if self.timer == 0:
			App.switchState(ScoreState(self.scoreTotal + self.score))

		if self.timer < 5.0:
			self.objectHandler.stop()
			if self.countDownPlayed == False:
				self.countDownPlayed = True
				self.sounds.flag("countdown")
				self.objectHandler.stop()

		if self.score > 100:
			self.levelUp()

		self.objectHandler.update()

		prevScore = self.score

		# handle player collisions
		shootList = spritecollide(self.player, self.toShoot, False, collide_circle)
		for obj in shootList:
			self.score -= 1
			self.combo = 0
			self.sounds.flag("bad")
			obj.kill()

		avoidList = spritecollide(self.player, self.toAvoid, False, collide_circle)
		for obj in avoidList:
			self.score -= 1
			self.combo = 0
			self.sounds.flag("bad")
			obj.kill()

		getList = spritecollide(self.player, self.toGet, False, collide_circle)
		for obj in getList:
			self.score += 1
			self.combo += 1
			self.combo = min(10, self.combo)
			self.sounds.flag("good"+str(self.combo))
			obj.kill()
		
		# handle bullet collisions		
		shootList = groupcollide(self.player.bullets, self.toShoot, True, True, collide_circle)
		for obj in shootList:
			self.combo += 1
			self.score += 1
			self.sounds.flag("shot")
		
		avoidList = groupcollide(self.player.bullets, self.toAvoid, True, True, collide_circle)
		for obj in avoidList:
			self.score -= 1
			self.combo = 0
			self.sounds.flag("bad")
		
		getList = groupcollide(self.player.bullets, self.toGet, True, True, collide_circle)
		for obj in getList:
			self.score -= 1
			self.combo = 0
			self.sounds.flag("bad")

		# handle ball collisions
		shootList = spritecollide(self.ball, self.toShoot, False, collide_circle)
		for obj in shootList:
			self.score -= 1
			self.combo = 0
			App.shake(0.5)
			self.sounds.flag("bad")
			obj.kill()

		avoidList = spritecollide(self.ball, self.toAvoid, False, collide_circle)
		for obj in avoidList:
			self.score += 1
			self.combo += 1
			self.combo = min(10, self.combo)
			self.sounds.flag("good"+str(self.combo))
			obj.kill()

		getList = spritecollide(self.ball, self.toGet, False, collide_circle)
		for obj in getList:
			self.score -= 1
			self.combo = 0
			App.shake(0.5)
			self.sounds.flag("bad")
			obj.kill()

		if (self.combo == 10):
			self.timer += 10
			self.timeAddedFlag = 3.0
			self.combo = 0
			self.sounds.flag("time")

		# SFX
		self.sounds.playAllFlagged()

		# Handle Leveling System
		self.score = max(0,self.score)
		self.ball.updateScore(self.score)
		self.objectHandler.setDifficulty(self.score)

	def draw(self):
		State.draw(self)
		App.Screen.blit(Gamefont.render(str(round(self.timer, 1)), True, (255,255,255)), (20,0))
		text = Gamefont.render("x"+str(self.combo), True, (255,255,255))
		dest = (App.Width - text.get_width() - 20,0)
		App.Screen.blit(text, dest)

		if self.timeAddedFlag:
			text = Gamefont.render("+10 Seconds", True, (255,255,255))
			dest = (App.Width / 2 - text.get_width() / 2, App.Height / 2 - 200)
			App.Screen.blit(text, dest)
			self.timeAddedFlag -= App.Elapsed
			if self.timeAddedFlag < 0:
				self.timeAddedFlag = 0

	def levelUp(self):
		self.scoreTotal += 100
		self.score = 0
		self.timer = 100
		self.level += 1
		self.objectHandler.setLevel(self.level)
		self.sounds.flag("levelUp")

		# clear all enemies
		self.remove(self.toShoot)
		self.remove(self.toAvoid)
		self.remove(self.toGet)
		self.toShoot.empty()
		self.toAvoid.empty()
		self.toGet.empty()
		
		App.Flash(0.5)
		#maybe change bg?

class ScoreState(State):
	def __init__(self, score):
		State.__init__(self, (255,0,0))
		self.bg = Sprite(0,0,"assets/scores/bg")
		self.add(self.bg)

		self.hsFile = open("assets/scores/scores.txt", "a+")
		self.scores = [int(x.strip('\n')) for x in self.hsFile.readlines()]
		self.scores.append(score)
		self.scores.sort(None, None, True)
		
		self.hsFile.write(str(score)+"\n")

		self.createBg(score)

	def update(self):
		if App.justDown(pygame.K_SPACE):
			App.switchState(ControlsState())

	def createBg(self, newScore):
		i = 0
		index = self.scores.index(newScore)
 		for s in self.scores:
			if i >= 5:
				break
			bg = (0,0,0,255)
			text = str(s)
			if index == i:
				text = "[ "+text+" ]"
			scoreSurf = Gamefont.render(text, True, (255,255,255), bg)
			dest = ((App.Width / 2) - (scoreSurf.get_width() / 2),
				(App.Height / 2) - (scoreSurf.get_height() / 2) + (50 * i) - 150)
			self.bg.image.blit(scoreSurf, dest)
			i += 1

	def quit(self):
		self.hsFile.close()

def main():
	info = pygame.display.Info()
	app = App(750, 750, MainMenuState(), False)

	app.run()

if __name__ == "__main__": main()

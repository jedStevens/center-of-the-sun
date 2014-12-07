import pygame
import random
from Vector import Vector

class App(object):
	#Python Literals
	Width = 0
	Height = 0
	Size = (0,0)
	BgColor = (101,156,239)
	Running = False
	Fps = 0
	FullScreen = False
	Scale = 0.0
	Keys = []
	_prevKeys = []
	Elapsed = 0.0
	Total = 0.0
	
	_shakeVec = (0,0)
	_shakeMag = 0
	_shakeTimer = 0
	
	#Pygame Vars
	Window = None
	Screen = None
	Clock = None

	#Game Engine Vars
	Center = None
	State = None
	Stack = []
	_newState = None
	
	def __init__(self, w, h, state, full=False, scale=1, fps=60, bg=(101,156,239)):

		App.Width = w
		App.Height = h
		App.Size = (App.Width, App.Height)
		App.WindowSize = (App.Width * scale, App.Height * scale)
		App.BgColor = bg
		App.Running = False
		App.Fps = fps
		App.FullScreen = full
		App.Scale = scale
		App.Center = Vector(w / 2, h / 2)
		
		pygame.init()
		pygame.mixer.init()
		
		if (full):
			App.Window = pygame.display.set_mode(App.WindowSize, pygame.FULLSCREEN)
		else:
			App.Window = pygame.display.set_mode(App.WindowSize)

		App.Screen = pygame.Surface((w,h))
		App.Clock = pygame.time.Clock()

		App.Stack.append(state)
		App.State = state
	
	def run(self):
		App.Running = True
		App.Keys = pygame.key.get_pressed()

		while App.Running:
			for e in pygame.event.get():
				if e.type == pygame.QUIT:
					App.Running = False
				elif e.type == pygame.KEYUP:
					if e.key == pygame.K_ESCAPE:
						App.Running = False
			App.handleStates()
			
			App.Elapsed = App.Clock.tick(App.Fps)
			App.Elapsed /= 1000.0

			App._prevKeys = App.Keys
			App.Keys = pygame.key.get_pressed()

			App.State.preUpdate()

			App.State.update()
			
			App.State.postUpdate()

			App.draw()

		pygame.quit()

	@staticmethod
	def draw():
		if App._shakeTimer > 0:
			App._shakeTimer -= App.Elapsed
			App._shakeVec = Vector.FromAngle(random.random()*360, App._shakeMag).toTuple()
		else:
			App._shakeVec = (0,0)

		if App.State.bgColor:
			App.Screen.set_alpha(50)
			App.Screen.fill(App.State.bgColor, None, pygame.BLEND_RGBA_MULT)
		else:
			App.Screen.fill(App.BgColor)
		
		App.State.draw()

		if App.Scale != 1.0:
			pygame.transform.scale(App.Screen, App.WindowSize, App.Window)
		else:
			App.Window.blit(App.Screen, App._shakeVec)
		
		
		pygame.display.update()

	@staticmethod
	def switchState(newState):
		App._newState = newState

	@staticmethod
	def handleStates():
		if App._newState:
			App.State.quit()
			App.State = App._newState
			App._newState = None
	
	@staticmethod
	def shake(duration, magnitude=5.0):
		App._shakeTimer = duration
		App._shakeMag = magnitude

	@staticmethod
	def anyKey():
		for key in App.Keys:
			if (key):
				return True
		return False

	@staticmethod
	def justDown(key):
		if App.Keys[key] and not App._prevKeys[key]:
			return True
		return False

	@staticmethod
	def Flash(d):
		App.Window.fill((255,255,255))

	def GlitchEffect(duration, magnitude):
		pass

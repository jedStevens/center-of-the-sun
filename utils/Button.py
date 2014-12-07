from Sprite import Sprite
from App import App

NONE	= 0
HOVER	= 1
PRESSED	= 2

class Button(Sprite):
	def __init__(self, x, y, path=""):
		Sprite.__init__(self, x, y, path, 3)
		self.state = NONE
		self.down = False
		self.justPressed = False

	"""
	INHERITED METHODS

		See Sprite Class

	"""
	
	def update(self):
		
		if self.state == PRESSED and App.Mouse.Up:
			self.state = NONE
			self.justPressed = True	
			
		elif self.state == HOVER and App.Mouse.Down:
			self.state = PRESSED
			self.down = True
			self.justPressed = False

		elif self.rect.collidepoint(App.Mouse.X, App.Mouse.Y):
			self.state = HOVER
			self.down = False
			self.justPressed = False
			
		else:
			self.state = NONE

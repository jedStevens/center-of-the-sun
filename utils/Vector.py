import math

class Vector:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def __getitem__(self, i):
		if i == 0:
			return self.x
		elif i == 1:
			return self.y
		return None

	def __len__(self):
		return math.sqrt(x*x + y*y)
	
	def __add__(self, other):
		self.x += other.x
		self.y += other.y
		return self
	
	def __mul__(self, k):
		self.x *= k
		self.y *= k
	
	def __rmul__(self, k):
		return self.__mul__(k)
	
	def __sub__(self, other):
		return self.__add__(other)
	
	def __div__(self, k):
		return self.__mul__(1.0/k)

	def toTuple(self):
		return (self.x, self.y)
	
	@staticmethod
	def Distance(v1, v2):
		return math.sqrt((v2.x - v1.x)**2 + (v2.y - v1.y)**2)

	@staticmethod
	def FromAngle(angle, dist=1):
		return Vector(math.cos(math.radians(angle))*dist,
				math.sin(math.radians(angle))*dist)	
	
	@staticmethod
	def FromTuple(tup):
		return Vector(tup[0],tup[1])

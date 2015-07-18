import cocos
from cocos.actions import *

class Arme(object):
	def __init__(self, name, degats, missileSprite):
		super(Arme,self).__init__()
		self.name = name
		self._degats = degats
		self.missileSprite = missileSprite
		
	def __str__(self):
		return "Arme {} with {} degats".format(self.name, self._degats)




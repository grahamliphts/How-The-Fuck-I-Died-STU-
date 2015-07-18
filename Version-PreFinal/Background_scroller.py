import cocos
from cocos import actions
from cocos.actions import *
from random import randint

class BackgroundStar(cocos.layer.Layer):
	def __init__(self,StarNum,Speed):
		super(BackgroundStar, self).__init__()
		self.speed = Speed
		Star = []
		i = 0
		scale = ScaleBy(1.1, duration=0.5)
		while i < StarNum :
			X = randint(-10, 1800)
			Y = randint( -10, 800)
			Star.append(cocos.sprite.Sprite('Sprites/Background/Star.png'))
			Star[i].position = (X,Y)
			Star[i].scale = 0.1
			self.add(Star[i])

			duration = Star[i].position[0] / self.speed

			moveToLeft = MoveTo((-10,Star[i].position[1]),duration = duration)
			Star[i].do( Repeat( Reverse(scale) + scale ) )
			Star[i].do( moveToLeft )
			i += 1;

		self.Star = Star
		self.schedule_interval(self.step, 1)
		#Star = cocos.sprite.Sprite('Sprites/Background/Star.png')
		#Star.position = (30,30)
		#Star.scale = 1
		#self.add(Star)
	def step(self, dt):
		for star in self.Star :
			if star.position[0] <= 0 :
				star.position = (2000,star.position[1])
				duration = star.position[0] / self.speed
				moveToLeft = MoveTo((-10,star.position[1]),duration = duration)
				star.do( moveToLeft )
import cocos
from cocos import actions
from cocos.actions import *
from random import randint

class Ennemi_wave(cocos.layer.Layer):
	def __init__(self,StarNum,Speed,scene):
		super(Ennemi_wave, self).__init__()
		self.speed = Speed
		Ennemi_list = []
		i = 0
		scale = ScaleBy(1.1, duration=0.5)

		while i < StarNum :
			X = randint(1700,2200)
			Y = randint(0,800)
			Ennemi_list.append(Ennemi('Sprites/ennemi_moche.PNG',self.speed,X,Y))
			scene.add(Ennemi_list[i], z = 2)
			i += 1;

		self.Ennemi_list = Ennemi_list
		self.linkedScene = scene
		self.schedule_interval(self.New_Wave, 5)
	def step(self, dt):
		print("Nothing")

	def New_Wave(self,dt):
		print("New_Wave")
		StarNum = randint(10,15)
		i = 0
		Ennemi_list = []
		scale = ScaleBy(1.1, duration=0.5)
		while i < StarNum :
			X = randint(1700,2200)
			Y = randint(0,800)
			Ennemi_list.append(Ennemi('Sprites/ennemi_moche.PNG',self.speed,X,Y))
			self.linkedScene.add(Ennemi_list[i],z = 3)
			i += 1;

class Ennemi(cocos.layer.Layer):
	def __init__(self,spritePath,speed,posX,posY):
		super(Ennemi, self).__init__()
		scale = ScaleBy(1.1, duration=0.5)
		sprite = cocos.sprite.Sprite (spritePath)
		sprite.position = (posX,posY)
		sprite.scale = 0.15
		self.add(sprite)
		duration = sprite.position[0] / speed
		moveToLeft = MoveTo((-30,sprite.position[1]),duration = duration)
		sprite.do( Repeat( Reverse(scale) + scale ) )
		sprite.do( moveToLeft )
import cocos
from cocos import actions
from cocos.actions import *
from random import randint
import cocos.euclid as eu
import cocos.collision_model as cm

class Ennemi_wave(cocos.layer.Layer):
	def __init__(self,StarNum,Speed,scene,CollisionManager):
		super(Ennemi_wave, self).__init__()
		self.speed = Speed
		self.collision = CollisionManager
		Ennemi_list = []
		i = 0
		scale = ScaleBy(1.1, duration=0.5)

		while i < StarNum :
			X = randint(1700,2200)
			Y = randint(0,800)
			Ennemi_list.append(Ennemi('Sprites/ennemi_moche.PNG',self.speed,X,Y,self.collision))
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
			Ennemi_list.append(Ennemi('Sprites/ennemi_moche.PNG',self.speed,X,Y,self.collision))
			self.linkedScene.add(Ennemi_list[i],z = 3)
			i += 1;

class Ennemi(cocos.layer.Layer):
	def __init__(self,spritePath,speed,posX,posY,collisionManager):
		super(Ennemi, self).__init__()
		scale = ScaleBy(1.1, duration=0.5)
		self.sprite = cocos.sprite.Sprite (spritePath)
		self.sprite.position = (posX,posY)
		self.sprite.scale = 0.15
		radius = 0.5
		self.sprite.cshape = cm.CircleShape(eu.Vector2(posX, posY), radius)
		self.add(self.sprite)
		duration = self.sprite.position[0] / speed
		moveToLeft = MoveTo((-30,self.sprite.position[1]),duration = duration)
		self.sprite.do( Repeat( Reverse(scale) + scale ) )
		self.sprite.do( moveToLeft )
		self.collision_manager = collisionManager

		#----------------------- COLLIDER---------------------------		
		collisionManager.add(self.sprite)
		self.schedule_interval(self.update, 0.1)

	def update(self,dt):
		self.sprite.cshape.center = eu.Vector2(self.sprite.position[0], self.sprite.position[1])
		collision = self.collision_manager.objs_colliding(self.sprite)
		if collision : 
			#if collision not in self.vaisseau.get_children():
			#self.remove(self.sprite)
			#print(collision)
			print("Collide ennemi")
		#print("Plouf")
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
		self.linkedScene = scene
		self.starnum = StarNum
		Ennemi_list = []
		i = 0
		scale = ScaleBy(1.1, duration=0.5)

		while i < StarNum :
			X = randint(1700,1900)
			Y = randint(0,800)
			Ennemi_list.append(Ennemi('Sprites/ennemi_moche.PNG',self.speed,X,Y,self.collision,self.linkedScene))
			scene.add(Ennemi_list[i], z = 2)
			i += 1;

		self.Ennemi_list = Ennemi_list		
		self.schedule_interval(self.New_Wave, 5)
	def step(self, dt):
		print("Nothing")

	def New_Wave(self,dt):
		print("New_Wave")
		StarNum = self.starnum + randint(0,5)
		i = 0
		Ennemi_list = []
		scale = ScaleBy(1.1, duration=0.5)
		while i < StarNum :
			X = randint(1700,1900)
			Y = randint(0,800)
			Ennemi_list.append(Ennemi('Sprites/ennemi_moche.PNG',self.speed,X,Y,self.collision,self.linkedScene))
			self.linkedScene.add(Ennemi_list[i],z = 3)
			i += 1;

class Ennemi(cocos.layer.Layer):
	def __init__(self,spritePath,speed,posX,posY,collisionManager,scene):
		super(Ennemi, self).__init__()
		scale = ScaleBy(1.1, duration=0.5)
		self.sprite = cocos.sprite.Sprite (spritePath)
		self.sprite.position = (posX,posY)
		self.sprite.scale = 0.15
		self.linkedScene = scene
		radius = 0.5
		self.sprite.cshape = cm.CircleShape(eu.Vector2(posX, posY), radius)
		self.add(self.sprite)
		duration = self.sprite.position[0] / speed
		#moveToLeft = MoveTo((-30,self.sprite.position[1]),duration = duration)
		#self.sprite.do( Repeat( Reverse(scale) + scale ) )
		#self.sprite.do( moveToLeft )

		move = MoveTo((-30,self.sprite.position[1]),duration = duration)
		move_complex = (AccelDeccel(MoveBy((randint(-150, -100), randint(100, 300)), 1)) +  AccelDeccel( (MoveBy((-150, -300), 1) ) ) )
		movementIndex = randint(0, 5);
		if movementIndex == 4 :
			move = self.move_straight(duration)
		if movementIndex == 3:
			move = self.move_diagonal(duration)
		if movementIndex == 2:
			move_complex = (AccelDeccel(MoveBy((randint(-150, -100), randint(100, 300)), 1)) +  AccelDeccel( (MoveBy((-150, -300), 1) ) ) )
		if movementIndex == 1:
			move_complex = (AccelDeccel(MoveBy((randint(-150, -100), randint(-300, 300)), 1)) +  AccelDeccel( (MoveBy((-150, randint(-300, 300)), 1) ) ) )
		if movementIndex == 0:
			move_complex = (AccelDeccel(MoveBy( (randint(-150, -100), randint(-300, 300)), 1) ) )

		
		if movementIndex < 3:
			self.sprite.do(Repeat(move_complex))
		else:
			self.sprite.do( move )
		self.sprite.do( Repeat( Reverse(scale) + scale ) )
		self.collision_manager = collisionManager
		self.schedule_interval(self.fire,1)
		self.schedule_interval(self.update,0.2)

	def update(self,dt):
		self.sprite.cshape.center = eu.Vector2(self.sprite.position[0], self.sprite.position[1])
		collision = self.collision_manager.objs_colliding(self.sprite)
		#if collision : 
			#print("Collide ennemi")
			#self.sprite.kill()
		#print("Plouf")
	def fire(self,dt):
		Bullet = bullet(self.sprite.position[0],self.sprite.position[1],500,self.collision_manager)
		self.linkedScene.add(Bullet, z = 3)

	def move_straight(self, dura):

		return MoveTo((-30,self.sprite.position[1]),dura)
	
	def move_diagonal(self, dura):
		
		return MoveTo((-30,self.sprite.position[1]+randint(0, 200)),dura)

class bullet(cocos.layer.Layer):
	def __init__(self,posX,posY,speed,collisionManager):
		super(bullet,self).__init__()
		self.sprite = cocos.sprite.Sprite ('Sprites/Armes/missile1.png')
		self.sprite.position = (posX,posY)
		self.sprite.scale = 1
		radius = 0.1
		self.sprite.cshape = cm.CircleShape(eu.Vector2(posX, posY), radius)
		self.add(self.sprite)
		
		collisionManager.add(self.sprite)

		duration = self.sprite.position[0] / speed
		moveToLeft = MoveTo((-30,self.sprite.position[1]),duration = duration)
		self.sprite.do(moveToLeft)
		self.collision_manager = collisionManager
		self.schedule_interval(self.bulletUpdate,0.5)

	def bulletUpdate(self,dt):
		#self.sprite.position = (self.sprite.position[0] - 2,self.sprite.position[1])
		self.sprite.cshape.center = eu.Vector2(self.sprite.position[0], self.sprite.position[1])

	

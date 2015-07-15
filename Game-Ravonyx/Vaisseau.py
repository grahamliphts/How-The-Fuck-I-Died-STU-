from cocos.director import director
from cocos.layer import Layer
from cocos.actions import *
import cocos
import cocos.collision_model as cm

class Vaisseau(Layer):
	def __init__(self, name, life, sprite, arme, collision_m):
		super(Vaisseau,self).__init__()
		
		width, height = director.get_window_size()
		
		self.sprite = sprite
		self.sprite.scale = 0.2
		self.sprite.position = (width//2, height//2)
		self.sprite.cshape = cm.AARectShape(
			self.sprite.position,
			self.sprite.width//2,
			self.sprite.height//2
		)
		collision_m.add(self.sprite)
		self.name = name
		self.life = life
		
		self.add(self.sprite)
		self.arme = arme
		self.missileSprites = []
		self.schedule(self.update)
	
	
	def shoot(self):
		x, y = self.sprite.position
		width, height = director.get_window_size()
		if(self.arme.name == "Simple"):
			sprite = cocos.sprite.Sprite(self.arme.missileSprite)
			self.add_collider_missile(sprite)
			self.add_to_layer(x + self.sprite.width//2 + 10, y)
			self.missileSprites[-1].do( MoveByAdditive((width, 0), 1) )
			
		elif(self.arme.name == "Triple"):
			sprite1 = cocos.sprite.Sprite(self.arme.missileSprite)
			self.add_collider_missile(sprite1)
			self.add_to_layer(x + self.sprite.width//2 + 10, y)
			self.missileSprites[-1].do( MoveByAdditive((width, 0), 1))
			
			sprite2 = cocos.sprite.Sprite(self.arme.missileSprite)
			self.add_collider_missile(sprite2)
			self.add_to_layer(x + self.sprite.width//2 + 10, y)
			self.missileSprites[-1].do( MoveBy((width, height//2), 1.5) )
			
			sprite3 = cocos.sprite.Sprite(self.arme.missileSprite)
			self.add_collider_missile(sprite3)
			self.add_to_layer(x + self.sprite.width//2 + 10, y)
			self.missileSprites[-1].do( MoveBy((width, -height//2), 1.5) )
			
		return self.missileSprites[-1]
	
	def add_collider_missile(self, sprite):
		self.missileSprites.append(sprite)
		self.missileSprites[-1].cshape = cm.AARectShape(
			self.missileSprites[-1].position,
			self.missileSprites[-1].width//2,
			self.missileSprites[-1].height//2
		)
	def add_to_layer(self, x, y):
		self.add(self.missileSprites[-1])
		self.missileSprites[-1].position = ( x, y)
		
	def update(self, dt):
		self.sprite.cshape.center = self.sprite.position
		for missile in self.missileSprites:
			missile.cshape.center = missile.position
			w1 = missile.width
			h1 = missile.height
			x, y = missile.position
			width, height = director.get_window_size()
			if(x - w1 <= 0 or x + w1 >= width or y - h1 <= 0 or y + h1 >= height):
				if missile in self.get_children():
					self.remove(missile)
			
	def on_enter(self):
		super(Vaisseau,self).on_enter()
	def on_exit(self):
		super(Vaisseau,self).on_exit()

	def __str__(self):
		return "Vaisseau {} with {} life".format(self.name, self.life)

import cocos.euclid as eu
class MoveByAdditive(Action):
    def init( self, delta_pos, duration ):
        try:
            self.delta_pos = eu.Vector2(*delta_pos)/float(duration)
        except ZeroDivisionError:
            duration = 0.0
            self.delta_pos = eu.Vector2(*delta_pos)
        self.duration = duration

    def start(self):
        if self.duration==0.0:
            self.target.position += self.delta_pos
            self._done = True

    def step(self, dt):
        old_elapsed = self._elapsed
        self._elapsed += dt
        if self._elapsed > self.duration:
            dt = self.duration - old_elapsed
            self._done = True
        self.target.position += dt*self.delta_pos		

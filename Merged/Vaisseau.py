import pyglet
from cocos.director import director
from cocos.layer import Layer
from cocos.actions import *
import cocos
import cocos.collision_model as cm

class Vaisseau(Layer):
	def __init__(self, name, life, sprite, arme, collision_m,special):
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

		self.special = special
		self.special.shield.position = self.sprite.position
	
	
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
		self.special.shield.position = self.sprite.position

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


class Shield(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self,posX,posY):
        super(Shield, self).__init__()
        
        shield_ui100 = cocos.sprite.Sprite('Sprites/shield/shield_100.png')
        shield_ui100.position = posX, posY
        shield_ui100.scale = 0.1
        self.add(shield_ui100, z=0)
        self.shield_ui100 = shield_ui100
        
        shield_ui75 = cocos.sprite.Sprite('Sprites/shield/shield_75.png')
        shield_ui75.position = posX, posY
        shield_ui75.scale = 0.1
        self.add(shield_ui75, z=0)
        self.shield_ui75 = shield_ui75
        self.shield_ui75.do(Hide())
        
        shield_ui50 = cocos.sprite.Sprite('Sprites/shield/shield_50.png')
        shield_ui50.position = posX, posY
        shield_ui50.scale = 0.1
        self.add(shield_ui50, z=0)
        self.shield_ui50 = shield_ui50
        self.shield_ui50.do(Hide())
        
        shield_ui25 = cocos.sprite.Sprite('Sprites/shield/shield_25.png')
        shield_ui25.position = posX, posY
        shield_ui25.scale = 0.1
        self.add(shield_ui25, z=0)
        self.shield_ui25 = shield_ui25
        self.shield_ui25.do(Hide())
        
        shield_ui = cocos.sprite.Sprite('Sprites/shield/shield.png')
        shield_ui.position = posX, posY
        shield_ui.scale = 0.1
        self.add(shield_ui, z=0)
        self.shield_ui = shield_ui
        self.shield_ui.do(Hide())

        shield = cocos.sprite.Sprite('Sprites/shield/shield_ship.png')
        shield.scale = 1
        self.add(shield, z=0)
        self.shield = shield
        self.shield.do(Hide())
        
        self.Reload = 20 # 20 Seconds Reload
        self.ReloadState = 0
        self.Durability = 5 # 5 Seconds Durability
        self.isReload = 1
        
        
    def on_key_press(self, key, modifiers):
        key_pressed = pyglet.window.key.symbol_string(key)
        if key_pressed == 'R' and self.isReload == 1:
            self.isReload = 0
            self.shield.do(Show())
            self.shield_ui100.do(Hide())
            self.shield_ui.do(Show())
            
            self.schedule_interval(self.shieldActivate, self.Durability)
            self.schedule_interval(self.reload, self.Reload/4)
    def reload(self, dt):
        self.ReloadState += self.Reload/4
        
        if self.ReloadState == self.Reload:
            self.isReload = 1
            self.ReloadState = 0
            self.shield_ui75.do(Hide())
            self.shield_ui100.do(Show())
            self.unschedule(self.reload)
        elif self.ReloadState >= self.Reload * 3 / 4:
            self.shield_ui50.do(Hide())
            self.shield_ui75.do(Show())
        elif self.ReloadState >= self.Reload * 2 / 4:
            self.shield_ui25.do(Hide())
            self.shield_ui50.do(Show())
        elif self.ReloadState >= self.Reload * 1 / 4:
            self.shield_ui.do(Hide())
            self.shield_ui25.do(Show())
            
    def shieldActivate(self, dt):
        self.shutDownShield()

    def shutDownShield(self):
        self.shield.do(Hide())
        self.unschedule(self.shieldActivate)
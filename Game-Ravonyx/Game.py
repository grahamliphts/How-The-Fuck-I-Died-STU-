#pyglet
from pyglet.gl import *

# cocos2d related
import cocos
from cocos.layer import Layer, ColorLayer
from cocos.scene import Scene
from cocos.director import director
from cocos.actions import *
import cocos.collision_model as cm

from GameControl import *
from GameModel import *
from GUI import *
from Vaisseau import *
from Armes import *

class GameView( Layer ):
	def __init__(self, hud, vaisseau, col_manager ):
		super(GameView,self).__init__()

		self.vaisseau = vaisseau
		self.hud = hud
		self.hud.show_message( 'GET READY')
		self.col_manager = col_manager
		self.schedule(self.update)
		
	def update_pos_vaisseau(self, x, y):
		w1 = self.vaisseau.sprite.width/2
		h1 = self.vaisseau.sprite.height/2
		width, height = director.get_window_size()
		if(x - w1 >= 0 and x + w1 <= width and y - h1 >= 0 and y + h1 <= height):
			self.vaisseau.sprite.position = (x,y)
			
	def vaisseau_shoot(self):
		sprite = self.vaisseau.shoot()
		self.col_manager.add(sprite)
	
	def update(self,dt):
		for other in self.col_manager.iter_colliding(self.vaisseau.sprite):
			if other not in self.vaisseau.get_children():
				self.vaisseau.remove(other)
				self.vaisseau.missileSprites.remove(other)
		#collide de missile
		"""for missile in self.vaisseau.missileSprites:
			for other in self.col_manager.iter_colliding(missile):
				print("collide")"""
	
	def on_enter(self):
		super(GameView,self).on_enter()
	def on_exit(self):
		super(GameView,self).on_exit()

def get_newgame():
	'''returns the game scene'''
	scene = Scene()
	collision_manager = cm.CollisionManagerBruteForce()
	
	 # view
	arme = Arme("Triple", 20, 'Sprites/Armes/missile1.png')
	sprite = cocos.sprite.Sprite('Sprites/Ship_moche.png')
	vaisseau = Vaisseau("Default", 100, sprite, arme, collision_manager);
	hud = HUD()
	view = GameView(hud, vaisseau, collision_manager)
	
	#model
	model = GameModel()
	# controller
	ctrl = GameCtrl(model, view)
    # set controller in model
	model.set_controller( ctrl )
	
	scene.add( view, z=1, name="view" )
	scene.add( ctrl, z=1, name="controller" )
	scene.add( hud, z=3, name="hud" )
	scene.add( vaisseau , z=2, name="vaisseau" )
	
	scene.add( BackgroundLayer(), z=0, name="background" )
	

	return scene

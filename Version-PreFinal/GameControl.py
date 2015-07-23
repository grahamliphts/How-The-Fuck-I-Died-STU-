# pyglet related
import pyglet
from pyglet.window import key

# cocos2d related
from cocos.layer import Layer
from cocos.scene import Scene
from cocos.euclid import Point2
from cocos.director import director

class GameCtrl( Layer ):

	is_event_handler = True #: enable pyglet's events

	def __init__(self, model, view):
		super(GameCtrl,self).__init__()
		self.used_key = False
		self.paused = False
		self.elapsed = 0
		self.model = model
		self.view = view
		
	def on_key_press(self, k, m ):
		if self.paused:
			return False
		if self.used_key:
			return False
		if k in (key.LEFT, key.RIGHT, key.DOWN, key.UP,key.SPACE, key.V, key.B):
			if k == key.LEFT:
				print("left")
			elif k == key.RIGHT:
				print("right")
			elif k == key.DOWN:
				print("down")
			elif k == key.UP:
				print("up")
			elif k == key.SPACE:
				self.view.vaisseau_shoot()
			elif k == key.V:
                                self.view.vaisseau.ActiveShield()
			elif k == key.B:
                                self.view.vaisseau.ExplodeBomb()
				
	def on_mouse_motion (self, x, y, dx, dy):
		self.view.update_pos_vaisseau(x,y)

	def on_mouse_press (self, x, y, buttons, modifiers):
		self.view.vaisseau_shoot()
	
	
	def pause_controller( self ):
		'''removes the schedule timer and doesn't handler the keys'''
		self.paused = True
		self.unschedule( self.step )

	def resume_controller( self ):
		'''schedules  the timer and handles the keys'''
		self.paused = False
		self.schedule( self.step )

	def step( self, dt ):
		'''updates the engine'''
		self.elapsed += dt
		if self.elapsed > status.level.speed:
			self.elapsed = 0

	def draw( self ):
		'''draw the map and the block'''
		self.used_key = False

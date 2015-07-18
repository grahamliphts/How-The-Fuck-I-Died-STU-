from cocos.layer import *
from cocos.text import *
from cocos.actions import *
import cocos
import pyglet
from pyglet.gl import *

class BackgroundLayer( Layer ):
	def __init__(self):
		super( BackgroundLayer, self ).__init__()
		width, height = director.get_window_size()
		self.img = cocos.sprite.Sprite('Sprites/Background/backgroundMenu.png')
		self.img.position = (width//2,height//2)
		self.img.scale_x = (width/self.img.width)
		self.img.scale_y = (height/self.img.height)
		self.add(self.img)

	def on_enter(self):
		super(BackgroundLayer,self).on_enter()
	def on_exit(self):
		super(BackgroundLayer,self).on_exit()
		
class MessageLayer( Layer ):
    def show_message( self, msg, callback=None ):
        w,h = director.get_window_size()

        self.msg = Label( msg,
            font_size=52,
            font_name='Retro Computer',
            anchor_y='center',
            anchor_x='center' )
        self.msg.position=(w//2.0, h)

        self.add( self.msg )

        actions = Accelerate(MoveBy( (0,-h/2.0), duration=0.5)) + \
                    Delay(1) +  \
                    Accelerate(MoveBy( (0,-h/2.0), duration=0.5)) + \
                    Hide()

        if callback:
            actions += CallFunc( callback )

        self.msg.do( actions )

class HUD( Layer ):
    def __init__( self ):
        super( HUD, self).__init__()
        self.add( MessageLayer(), name='msg' )

    def show_message( self, msg, callback = None ):
        self.get('msg').show_message( msg, callback )
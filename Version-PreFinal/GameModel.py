# stdlib
import copy
import random
import weakref

import pyglet
from cocos.euclid import Point2

from Status import status
from Levels import levels

class GameModel( pyglet.event.EventDispatcher ):

    def __init__(self):
        super(GameModel,self).__init__()
        status.reset()
        status.level = levels[0]

    def start( self ):
        self.set_next_level()

    def set_controller( self, ctrl ):
        self.ctrl = weakref.ref( ctrl )

    def set_next_level( self ):
        self.ctrl().resume_controller()

        if status.level_idx is None:
            status.level_idx = 0
        else:
            status.level_idx += 1

        l = levels[ status.level_idx ]
        status.level = l()
        self.dispatch_event("on_new_level")


GameModel.register_event_type('on_level_complete')
GameModel.register_event_type('on_new_level')
GameModel.register_event_type('on_win')

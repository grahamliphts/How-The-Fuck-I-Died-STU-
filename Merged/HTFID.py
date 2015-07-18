# HOW THE FUCK I DIED !!!

# ------------------------------
# LIBRARIES
# ------------------------------
from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

import cocos
from cocos.director import director
from cocos.actions import *

import pyglet
# ------------------------------


# ------------------------------
# CLASS DEPLACEMENT
# ------------------------------
class SpaceShip(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self, special):
        super(SpaceShip, self).__init__()
        
        spaceship = cocos.sprite.Sprite('Sprites/Ship_moche.png')
        spaceship.position = 320, 240
        spaceship.scale = 0.2
        self.add(spaceship, z=1)
        self.spaceship = spaceship

        self.special = special
        self.special.position = spaceship.position
        
    
    def on_key_press(self, key, modifiers):
        key_pressed = pyglet.window.key.symbol_string(key)
        if key_pressed == "D":
            move = Repeat(MoveBy((10, 0), 0.1))
            self.spaceship.do(move)
            self.special.shield.do(move)
        if key_pressed == "Q":
            move = Repeat(MoveBy((-10, 0), 0.1))
            self.spaceship.do(move)
            self.special.shield.do(move)
        if key_pressed == "Z":
            move = Repeat(MoveBy((0, 10), 0.1))
            self.spaceship.do(move)
            self.special.shield.do(move)
        if key_pressed == "S":
            move = Repeat(MoveBy((0, -10), 0.1))
            self.spaceship.do(move)
            self.special.shield.do(move)

    def on_key_release(self, key, modifiers):
        self.spaceship.stop()
        self.special.shield.stop()

            
# ------------------------------
# CLASS SPECIAL 1 - SHIELD
# ------------------------------
class Shield(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(Shield, self).__init__()
        
        shield_ui100 = cocos.sprite.Sprite('Sprites/shield/shield_100.png')
        shield_ui100.position = 0, 100
        shield_ui100.scale = 0.1
        self.add(shield_ui100, z=0)
        self.shield_ui100 = shield_ui100
        
        shield_ui75 = cocos.sprite.Sprite('Sprites/shield/shield_75.png')
        shield_ui75.position = 0, 100
        shield_ui75.scale = 0.1
        self.add(shield_ui75, z=0)
        self.shield_ui75 = shield_ui75
        self.shield_ui75.do(Hide())
        
        shield_ui50 = cocos.sprite.Sprite('Sprites/shield/shield_50.png')
        shield_ui50.position = 0, 100
        shield_ui50.scale = 0.1
        self.add(shield_ui50, z=0)
        self.shield_ui50 = shield_ui50
        self.shield_ui50.do(Hide())
        
        shield_ui25 = cocos.sprite.Sprite('Sprites/shield/shield_25.png')
        shield_ui25.position = 0, 100
        shield_ui25.scale = 0.1
        self.add(shield_ui25, z=0)
        self.shield_ui25 = shield_ui25
        self.shield_ui25.do(Hide())
        
        shield_ui = cocos.sprite.Sprite('Sprites/shield/shield.png')
        shield_ui.position = 0, 100
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
        if key_pressed == 'SPACE' and self.isReload == 1:
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
        
        
            
    

if __name__ == "__main__":
    director.init(resizable=True)
    
    scene = cocos.scene.Scene()
    
    shield = Shield()
    scene.add(shield, z=2)
    
    spaceship = SpaceShip(shield)
    
    scene.add(spaceship, z=1)
    
    director.run(scene)

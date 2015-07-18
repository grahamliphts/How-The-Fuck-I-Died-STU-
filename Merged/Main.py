import cocos

import pyglet
from pyglet import gl, font
from pyglet.window.key import KeyStateHandler
from pyglet.window import key

from cocos.scene import Scene
from cocos.layer import *
from cocos.menu import *
from cocos.text import *
from cocos.actions import *
from cocos.director import director

from GUI import *
import Game

class MainMenu( Menu ):

    def __init__(self):
        super( MainMenu, self).__init__('How the #(%@ i die') 

        #self.select_sound = soundex.load('move.mp3')

        # you can override the font that will be used for the title and the items
        # you can also override the font size and the colors. see menu.py for
        # more info
        self.font_title['font_name'] = 'Retro Computer'
        self.font_title['font_size'] = 56
        self.font_title['color'] = (94,119,203,255)

        self.font_item['font_name'] = 'Retro Computer'
        self.font_item['color'] = (94,119,203,255)
        self.font_item['font_size'] = 40

        self.font_item_selected['font_name'] = 'Retro Computer'
        self.font_item_selected['color'] = (123,143,208,255)
        self.font_item_selected['font_size'] = 46

        # example: menus can be vertical aligned and horizontal aligned
        self.menu_anchor_y = 'center'
        self.menu_anchor_x = 'center'

        items = []

        items.append( MenuItem('Play', self.on_new_game) )
        items.append( MenuItem('Quit', self.on_quit) )
        
        self.create_menu( items, shake(), shake_back() )
        
    def on_new_game(self):
        import Game
        director.push(Game.get_newgame())
    def on_quit(self):
        pyglet.app.exit()

class EndScreen( Menu ):

    def __init__(self):
        super( EndScreen, self).__init__('How the #(%@ i die') 

        #self.select_sound = soundex.load('move.mp3')

        # you can override the font that will be used for the title and the items
        # you can also override the font size and the colors. see menu.py for
        # more info
        self.font_title['font_name'] = 'Retro Computer'
        self.font_title['font_size'] = 56
        self.font_title['color'] = (94,119,203,255)

        self.font_item['font_name'] = 'Retro Computer'
        self.font_item['color'] = (94,119,203,255)
        self.font_item['font_size'] = 40

        self.font_item_selected['font_name'] = 'Retro Computer'
        self.font_item_selected['color'] = (123,143,208,255)
        self.font_item_selected['font_size'] = 46

        # example: menus can be vertical aligned and horizontal aligned
        self.menu_anchor_y = 'center'
        self.menu_anchor_x = 'center'

        items = []

        val = '65'
        items.append( MenuItem('Score : ' + val,self.on_new_game))

        items.append( MenuItem('Retry', self.on_new_game) )
        items.append( MenuItem('Quit', self.on_quit) )
        
        self.create_menu( items, shake(), shake_back() )
        
    def on_new_game(self):
        scene = Scene()
        scene.add( MultiplexLayer( MainMenu()),z=1 )
        scene.add( BackgroundLayer(), z=0 )
        director.run( scene )

    def on_quit(self):
        pyglet.app.exit()
            
if __name__ == "__main__":
    pyglet.resource.path.append('Sprites')
    pyglet.resource.reindex()
    font.add_directory('Sprites')

    director.init( resizable=False, width=1600, height=800 )
    scene = Scene()
    scene.add( MultiplexLayer( MainMenu()),z=1 )
    scene.add( BackgroundLayer(), z=0 )
    director.run( scene )
    



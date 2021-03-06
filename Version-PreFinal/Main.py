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
import time

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
        self.modesale = 0
        
    def on_key_press(self, k, m ):
        if k == key.P:
            if self.modesale == 0:
                self.modesale = 1
            else:
                self.modesale = 0
                    
    def on_new_game(self):
        import Game
        Score = 0
        director.push(Game.get_newgame(self.modesale))
        
    def on_quit(self):
        pyglet.app.exit()
        
class EndScreen( Menu ):
    def __init__(self, score):
        super( EndScreen, self).__init__('How the #(%@ i die')
        
        self.score = score
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

        val = str(self.score)
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
    global Score

    last_time = time.clock()
    
    pyglet.resource.path.append('Sprites')
    pyglet.resource.reindex()
    font.add_directory('Sprites')

    director.init( resizable=False, width=1600, height=800 )
    scene = Scene()
    scene.add( MultiplexLayer( MainMenu()),z=1 )
    scene.add( BackgroundLayer(), z=0 )
    director.run( scene )
    



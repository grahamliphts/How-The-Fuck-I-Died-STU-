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
from Background_scroller import * 
from Ennemi import *
from Bomb import * 
from Shield import *
from Main import *

class GameView( Layer ):
    """Main Gameviewer """
    def __init__(self, hud, vaisseau, col_manager ):
        """GameView Init"""
        super(GameView,self).__init__()

        self.player = pyglet.media.Player()
        sound = pyglet.media.load('Song/BackSound.wav')
        self.player.queue(sound) 
        self.player.play()

        self.vaisseau = vaisseau
        self.hud = hud
        self.hud.show_message( 'GET READY')
        self.col_manager = col_manager
        self.schedule(self.update)

        self.initHealth = 1
        self.health = 1
        
        healthGUI = cocos.sprite.Sprite('Sprites/GUI/Health_empty.png')
        healthGUI.position = 210, 750
        healthGUI.scale = 1
        self.add(healthGUI, z=0)
        self.healthGUI = healthGUI
        
        healthState = cocos.sprite.Sprite('Sprites/GUI/Health.png')
        healthState.position = 210, 750
        healthState.scale = 1
        self.add(healthState, z=0)
        self.healthState = healthState
                
        self.schedule_interval(self.calculate_time, 0.1)
        self.score = 0
        
    def update_pos_vaisseau(self, x, y):
        """SHip Main update"""
        w1 = self.vaisseau.sprite.width/2
        h1 = self.vaisseau.sprite.height/2
        width, height = director.get_window_size()
        if(x - w1 >= 0 and x + w1 <= width and y - h1 >= 0 and y + h1 <= height):
            self.vaisseau.sprite.position = (x, y)
            
    def vaisseau_shoot(self):
        """Fire ship"""
        sprite = self.vaisseau.shoot()
        self.col_manager.add(sprite)
        
    def calculate_time(self, dt):
        """Timmer"""
        self.score += 1
        pass
    
    def update(self, dt):
        """ Colliders update"""
        for other in self.col_manager.iter_colliding(self.vaisseau.sprite):
            if other not in self.vaisseau.get_children():
                bombactive = self.vaisseau.bombClass.active
                if self.vaisseau.shieldClass.Active == 0 and  bombactive == 0 :
                    self.health -= 1
                    self.healthState.scale = self.health / self.initHealth
                # FIN DE PARTIE
                if self.health <= 0:
                    self.player.pause()
                    music = pyglet.media.load("Song/death.wav")
                    music.play()
                    scene = Scene()
                    scene.add( MultiplexLayer( EndScreen(self.score)), z=1 )
                    scene.add( BackgroundLayer(), z=0 )
                    director.run( scene )
                
    def on_enter(self):
        """On enter event"""
        super(GameView, self).on_enter()
        
    def on_exit(self):
        """ On exit event"""
        super(GameView, self).on_exit()
        
class scoreC( Layer ):
    """ Score Class"""
    def __init__(self, value):
        """ Score init"""
        super(scoreC, self).__init__()
        self.value = value
        
def get_newgame():
    """returns the game scene"""
    scene = Scene()
    collision_manager_Ennemi = cm.CollisionManagerBruteForce()
    collision_manager_Player = cm.CollisionManagerBruteForce()
    
     # view
    arme = Arme("Simple", 20, 'Sprites/Armes/missile3.png')
    sprite = cocos.sprite.Sprite('Sprites/Ship2.png')
    shield = Shield(50, 100)
    bombSpe = Bomb(100, 120, 100, collision_manager_Ennemi)
    vaisseau = Vaisseau("Default", 100, sprite, arme, collision_manager_Player, collision_manager_Ennemi, shield, bombSpe)
    hud = HUD()
    view = GameView(hud, vaisseau, collision_manager_Player)
    Star = Backgroundstar(30, 60)

    ennemi_wave = Ennemi_wave(10,200,scene, collision_manager_Player, collision_manager_Ennemi)
    
    #model
    model = GameModel()
    # controller
    ctrl = GameCtrl(model, view)
    # set controller in model
    model.set_controller( ctrl )
    
    scene.add( view, z=1, name="view" )
    scene.add( ctrl, z=1, name="controller" )
    scene.add( hud, z=3, name="hud" )
    scene.add( shield, z = 3 , name = "Shield")
    scene.add( bombSpe, z = 3 , name = "Bombe")
    scene.add( vaisseau , z=2, name="vaisseau" )
    scene.add( ennemi_wave, z = 2, name = "ennemis")
    scene.add( BackgroundLayer(), z=0, name="background" )
    scene.add( Star,z = 0, name = "Stars")

    


    return scene

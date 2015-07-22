import cocos
from cocos.actions import *
import cocos.collision_model as cm

class Bomb(cocos.layer.Layer):
    """Bomb special attack class"""
    def __init__(self, degats, posx, posy, CollisionManagerEnnemi):
        """Bomb init FUnction"""
        super(Bomb, self).__init__()
        self.name = "BombSpecial"
        self.degats = degats
        self.CollisionManagerEnnemi = CollisionManagerEnnemi
        
        bomb_ui100 = cocos.sprite.Sprite('Sprites/bomb/bomb_100.png')
        bomb_ui100.position = posx, posy
        bomb_ui100.scale = 0.6
        self.add(bomb_ui100, z=0)
        self.bomb_ui100 = bomb_ui100
        
        bomb_ui75 = cocos.sprite.Sprite('Sprites/bomb/bomb_75.png')
        bomb_ui75.position = posx, posy
        bomb_ui75.scale = 0.6
        self.add(bomb_ui75, z=0)
        self.bomb_ui75 = bomb_ui75
        self.bomb_ui75.do(Hide())
        
        bomb_ui50 = cocos.sprite.Sprite('Sprites/bomb/bomb_50.png')
        bomb_ui50.position = posx, posy
        bomb_ui50.scale = 0.6
        self.add(bomb_ui50, z=0)
        self.bomb_ui50 = bomb_ui50
        self.bomb_ui50.do(Hide())
        
        bomb_ui25 = cocos.sprite.Sprite('Sprites/bomb/bomb_25.png')
        bomb_ui25.position = posx, posy
        bomb_ui25.scale = 0.6
        self.add(bomb_ui25, z=0)
        self.bomb_ui25 = bomb_ui25
        self.bomb_ui25.do(Hide())
        
        bomb_ui = cocos.sprite.Sprite('Sprites/bomb/bomb.png')
        bomb_ui.position = posx, posy
        bomb_ui.scale = 0.6
        self.add(bomb_ui, z=0)
        self.bomb_ui = bomb_ui
        self.bomb_ui.do(Hide())
        
        spriteexplode = cocos.sprite.Sprite('Sprites/bomb/shockwave.png')
        self.add(spriteexplode, z=2)
        self.spriteexplode = spriteexplode
        self.spriteexplode.do(Hide())

        self.reloadtime = 20 # 20 Seconds Reload
        self.reloadstate = 0
        self.isreload = 1

        self.active = 0
        
    def __str__(self):
        """ To string function"""
        return "Arme {} with {} degats".format(self.name, self.degats)

    def Explode(self, positionship):
        """Bomb Activation on position argument"""
        if self.isreload == 1:            
            self.spriteexplode.do(Show())
            self.spriteexplode.position = positionship;
            self.spriteexplode.scale = 0.1
            
            self.bomb_ui100.do(Hide())
            self.bomb_ui.do(Show())
            self.isreload = 0
                        
            scale = ScaleBy(100, duration=2)
            self.spriteexplode.do(scale)

            self.schedule_interval(self.reload, self.reloadtime/4)
            self.schedule_interval(self.deactiveshockwave, 2)

            self.active = 1
            self.spriteexplode.cshape = cm.CircleShape(positionship, 10000)
            self.CollisionManagerEnnemi.add(self.spriteexplode)
	  
    def reload(self, dt):
        """ Bomb reload timmer update"""
        self.reloadstate += self.reloadtime/4
        
        if self.reloadstate == self.reloadtime:
            self.isreload = 1
            self.reloadstate = 0
            self.bomb_ui75.do(Hide())
            self.bomb_ui100.do(Show())
            self.unschedule(self.reload)
        elif self.reloadstate >= self.reloadtime * 3 / 4:
            self.bomb_ui50.do(Hide())
            self.bomb_ui75.do(Show())
        elif self.reloadstate >= self.reloadtime * 2 / 4:
            self.bomb_ui25.do(Hide())
            self.bomb_ui50.do(Show())
        elif self.reloadstate >= self.reloadtime * 1 / 4:
            self.bomb_ui.do(Hide())
            self.bomb_ui25.do(Show())

            
    def deactiveshockwave(self, dt):
        """End of shockwave"""
        self.spriteexplode.do(Hide())
        self.CollisionManagerEnnemi.remove_tricky(self.spriteexplode)
        self.active = 0
        self.unschedule(self.deactiveshockwave)




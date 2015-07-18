import cocos
from cocos.actions import *
import cocos.collision_model as cm

class Bomb(cocos.layer.Layer):
    def __init__(self, degats, posX, posY, CollisionManagerEnnemi):
        super(Bomb,self).__init__()
        self.name = "BombSpecial"
        self.degats = degats
        self.CollisionManagerEnnemi = CollisionManagerEnnemi
        
        bomb_ui100 = cocos.sprite.Sprite('Sprites/bomb/bomb_100.png')
        bomb_ui100.position = posX, posY
        bomb_ui100.scale = 0.6
        self.add(bomb_ui100, z=0)
        self.bomb_ui100 = bomb_ui100
        
        bomb_ui75 = cocos.sprite.Sprite('Sprites/bomb/bomb_75.png')
        bomb_ui75.position = posX, posY
        bomb_ui75.scale = 0.6
        self.add(bomb_ui75, z=0)
        self.bomb_ui75 = bomb_ui75
        self.bomb_ui75.do(Hide())
        
        bomb_ui50 = cocos.sprite.Sprite('Sprites/bomb/bomb_50.png')
        bomb_ui50.position = posX, posY
        bomb_ui50.scale = 0.6
        self.add(bomb_ui50, z=0)
        self.bomb_ui50 = bomb_ui50
        self.bomb_ui50.do(Hide())
        
        bomb_ui25 = cocos.sprite.Sprite('Sprites/bomb/bomb_25.png')
        bomb_ui25.position = posX, posY
        bomb_ui25.scale = 0.6
        self.add(bomb_ui25, z=0)
        self.bomb_ui25 = bomb_ui25
        self.bomb_ui25.do(Hide())
        
        bomb_ui = cocos.sprite.Sprite('Sprites/bomb/bomb.png')
        bomb_ui.position = posX, posY
        bomb_ui.scale = 0.6
        self.add(bomb_ui, z=0)
        self.bomb_ui = bomb_ui
        self.bomb_ui.do(Hide())
        
        spriteExplode = cocos.sprite.Sprite('Sprites/bomb/shockwave.png')
        self.add(spriteExplode, z=2)
        self.spriteExplode = spriteExplode
        self.spriteExplode.do(Hide())

        self.Reload = 20 # 20 Seconds Reload
        self.ReloadState = 0
        self.isReload = 1

        self.Active = 0
        
    def __str__(self):
        return "Arme {} with {} degats".format(self.name, self.degats)

    def Explode(self, positionShip):
        if self.isReload == 1:            
            self.spriteExplode.do(Show())
            self.spriteExplode.position = positionShip;
            self.spriteExplode.scale = 0.1
            
            self.bomb_ui100.do(Hide())
            self.bomb_ui.do(Show())
            self.isReload = 0
                        
            scale = ScaleBy(100, duration=2)
            self.spriteExplode.do(scale)

            self.schedule_interval(self.reload, self.Reload/4)
            self.schedule_interval(self.deactiveShockwave, 2)

            self.Active = 1
            self.spriteExplode.cshape = cm.CircleShape(positionShip, 10000)
            self.CollisionManagerEnnemi.add(self.spriteExplode)
	  
    def reload(self, dt):
        self.ReloadState += self.Reload/4
        
        if self.ReloadState == self.Reload:
            self.isReload = 1
            self.ReloadState = 0
            self.bomb_ui75.do(Hide())
            self.bomb_ui100.do(Show())
            self.unschedule(self.reload)
        elif self.ReloadState >= self.Reload * 3 / 4:
            self.bomb_ui50.do(Hide())
            self.bomb_ui75.do(Show())
        elif self.ReloadState >= self.Reload * 2 / 4:
            self.bomb_ui25.do(Hide())
            self.bomb_ui50.do(Show())
        elif self.ReloadState >= self.Reload * 1 / 4:
            self.bomb_ui.do(Hide())
            self.bomb_ui25.do(Show())

            
    def deactiveShockwave(self, dt):
        self.spriteExplode.do(Hide())
        self.CollisionManagerEnnemi.remove_tricky(self.spriteExplode)
        self.Active = 0
        self.unschedule(self.deactiveShockwave)




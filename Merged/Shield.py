import cocos
from cocos.actions import *


class Shield(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self, posX, posY):
        super(Shield, self).__init__()
        
        shield_ui100 = cocos.sprite.Sprite('Sprites/shield/shield_100.png')
        shield_ui100.position = posX, posY
        shield_ui100.scale = 0.6
        self.add(shield_ui100, z=0)
        self.shield_ui100 = shield_ui100
        
        shield_ui75 = cocos.sprite.Sprite('Sprites/shield/shield_75.png')
        shield_ui75.position = posX, posY
        shield_ui75.scale = 0.6
        self.add(shield_ui75, z=0)
        self.shield_ui75 = shield_ui75
        self.shield_ui75.do(Hide())
        
        shield_ui50 = cocos.sprite.Sprite('Sprites/shield/shield_50.png')
        shield_ui50.position = posX, posY
        shield_ui50.scale = 0.6
        self.add(shield_ui50, z=0)
        self.shield_ui50 = shield_ui50
        self.shield_ui50.do(Hide())
        
        shield_ui25 = cocos.sprite.Sprite('Sprites/shield/shield_25.png')
        shield_ui25.position = posX, posY
        shield_ui25.scale = 0.6
        self.add(shield_ui25, z=0)
        self.shield_ui25 = shield_ui25
        self.shield_ui25.do(Hide())
        
        shield_ui = cocos.sprite.Sprite('Sprites/shield/shield.png')
        shield_ui.position = posX, posY
        shield_ui.scale = 0.6
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
        
        
    def ActiveShield(self):
        if self.isReload == 1:
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

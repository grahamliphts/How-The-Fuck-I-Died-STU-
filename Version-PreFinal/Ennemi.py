import cocos
import pyglet

from cocos import actions
from cocos.actions import *
from random import randint
import cocos.euclid as eu
import cocos.collision_model as cm

class Ennemi_wave(cocos.layer.Layer):
    def __init__(self, starnum, speed, scene, colmanplayer, colmanennemi, spritedir):
        super(Ennemi_wave, self).__init__()
        self.speed = speed
        
        self.collp = colmanplayer
        self.colle = colmanennemi

        self.spritedir = spritedir
        
        self.linkedScene = scene
        self.starnum = starnum
        
        scale = ScaleBy(1.1, duration=0.5)

        self.toKill = []
        self.schedule_interval(self.New_Wave, 5)

    def New_Wave(self, dt):
        StarNum = self.starnum + randint(0,5)
        i = 0
        scale = ScaleBy(1.1, duration=0.5)
        while i < StarNum :
            X = randint(1700,1900)
            Y = randint(0,800)
            ennemi = Ennemi(self.spritedir, self.speed, X, Y, self.collp, self.colle, self.linkedScene)
            self.add(ennemi, z = 4)
            self.linkedScene.add(ennemi, z = 4)
            i += 1;


class Ennemi(cocos.layer.Layer):
    def __init__(self, spritedir, speed, posX, posY, colmanplayer, colmanennemi, scene):
        super(Ennemi, self).__init__()
        scale = ScaleBy(1.1, duration=0.5)
        
        self.collp = colmanplayer
        self.colle = colmanennemi
        
        self.spritedir = spritedir
        
        self.sprite = cocos.sprite.Sprite(self.spritedir + '/Ennemi1-1.png')
        self.sprite.position = (posX,posY)
        self.sprite.scale = 0.15

        self.sprite_explosion = cocos.sprite.Sprite('Sprites/explosion.png')
        self.sprite_explosion.position = (posX,posY)
        self.sprite_explosion.scale = 1
        self.sprite_explosion.do(Hide())
        
        self.linkedScene = scene
        self.name = "Ennemi"
        
        radius = 0.5
        self.sprite.cshape = cm.CircleShape(eu.Vector2(posX, posY), radius)
        
        self.add(self.sprite)
        self.add(self.sprite_explosion)
        
        self.colle.add(self.sprite)
        duration = self.sprite.position[0] / speed

        move = MoveTo((-30,self.sprite.position[1]),duration = duration)
        move_complex = (AccelDeccel(MoveBy((randint(-150, -100), randint(100, 300)), 1)) +  AccelDeccel( (MoveBy((-150, -300), 1) ) ) )
        
        movementIndex = randint(0, 5);
        if movementIndex == 4 :
            move = self.move_straight(duration)
        if movementIndex == 3:
            move = self.move_diagonal(duration)
        if movementIndex == 2:
            move_complex = (AccelDeccel(MoveBy((randint(-150, -100), randint(100, 300)), 1)) +  AccelDeccel( (MoveBy((-150, -300), 1) ) ) )
        if movementIndex == 1:
            move_complex = (AccelDeccel(MoveBy((randint(-150, -100), randint(-300, 300)), 1)) +  AccelDeccel( (MoveBy((-150, randint(-300, 300)), 1) ) ) )
        if movementIndex == 0:
            move_complex = (AccelDeccel(MoveBy( (randint(-150, -100), randint(-300, 300)), 1) ) )

        
        if movementIndex < 3:
            self.sprite.do(Repeat(move_complex))
        else:
            self.sprite.do( move )
        self.sprite.do( Repeat( Reverse(scale) + scale ) )
        
        
        self.schedule_interval(self.fire,2)
        self.schedule_interval(self.update,0.1)

    def update(self,dt):
        self.sprite.cshape.center = eu.Vector2(self.sprite.position[0], self.sprite.position[1])
        collision = self.colle.objs_colliding(self.sprite)
        if collision or self.sprite.position[0] <= 0 or self.sprite.position[1] < 0 and self.sprite.position[0] < 1600 :
            music = pyglet.media.load("Song/explosion.wav")
            music.play()
            self.unschedule(self.fire)
            self.sprite.do(Hide())
            self.sprite_explosion.position = self.sprite.position
            self.sprite_explosion.do(Show())
            self.unschedule(self.update)
            self.schedule_interval(self.explode,2)     

    def explode(self, dt):
        self.sprite.stop()
        self.remove(self.sprite)
        self.sprite_explosion.do(Hide())
        self.unschedule(self.explode)
        self.colle.remove_tricky(self.sprite)
        self.kill()
                
    def fire(self,dt):
        Bullet = bullet(self.sprite.position[0],self.sprite.position[1],500,self.collp, self.spritedir)
        self.linkedScene.add(Bullet, z = 3)

    def move_straight(self, dura):
        return MoveTo((-30,self.sprite.position[1]),dura)
    
    def move_diagonal(self, dura):
        return MoveTo((-30,self.sprite.position[1]+randint(0, 200)),dura)

class bullet(cocos.layer.Layer):
    def __init__(self,posX,posY,speed,collisionManager, spritedir):
        super(bullet,self).__init__()
        self.sprite = cocos.sprite.Sprite (spritedir + '/Armes/missile2.png')
        self.sprite.position = (posX,posY)
        self.sprite.scale = 1
        self.name = "EnnemiBullet"
        
        radius = 1
        self.sprite.cshape = cm.CircleShape(eu.Vector2(posX, posY), radius)
        
        self.isdead = 0
        
        self.add(self.sprite)
        collisionManager.add(self.sprite)

        duration = self.sprite.position[0] / speed
        moveToLeft = MoveTo((-30,self.sprite.position[1]),duration = duration)
        self.sprite.do(moveToLeft)
        self.collision_manager = collisionManager
        self.schedule_interval(self.bulletUpdate,0.1)

    def bulletUpdate(self,dt):
        if self.isdead == 1:
            self.sprite.stop()
            self.remove(self.sprite)
            self.unschedule(self.bulletUpdate)
            self.collision_manager.remove_tricky(self.sprite)
            self.kill()
            
        self.sprite.cshape.center = eu.Vector2(self.sprite.position[0], self.sprite.position[1])
        collision = self.collision_manager.objs_colliding(self.sprite)
        if collision or self.sprite.position[0] <= 0:
            self.isdead = 1
    

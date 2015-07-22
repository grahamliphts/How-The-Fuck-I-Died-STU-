import cocos
from cocos import actions
from cocos.actions import *
from random import randint

class Backgroundstar(cocos.layer.Layer):
    """ Parralax Background"""
    def __init__(self, starnum, speed):
        """ Argument of star background paralaxx nbetoiles, vitesseEtoiles"""
        super(Backgroundstar, self).__init__()
        self.speed = speed
        star = []
        i = 0
        scale = ScaleBy(1.1, duration=0.5)
        while i < starnum :
            x = randint(-10, 1800)
            y = randint( -10, 800)
            star.append(cocos.sprite.Sprite('Sprites/Background/Star.png'))
            star[i].position = (x, y)
            star[i].scale = 0.1
            self.add(star[i])

            duration = star[i].position[0] / self.speed

            movetoleft = MoveTo((-10, star[i].position[1]), duration = duration)
            star[i].do( Repeat( Reverse(scale) + scale ) )
            star[i].do( movetoleft )
            i += 1

        self.star = star
        self.schedule_interval(self.step, 1)
    def step(self, dt):
        """ backgroundstar Update"""
        for star in self.star :
            if star.position[0] <= 0 :
                star.position = (2000, star.position[1])
                duration = star.position[0] / self.speed
                position = star.position[1]
                movetoleft = MoveTo((-10, position), duration = duration)
                star.do( movetoleft )
class Level( object ):
    pass

class LevelLens( Level ):
    speed = 0.5
    lines = 10
    prob = 0.07

class LevelScale( Level ):
    speed = 0.5
    lines = 10
    prob = 0.07

class LevelLiquid( Level ):
    speed = 0.45
    lines = 12
    prob = 0.07


levels = [ LevelLens, LevelScale, LevelLiquid ]

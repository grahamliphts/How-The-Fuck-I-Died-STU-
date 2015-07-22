class Arme(object):
    """Weapon class"""
    def __init__(self, name, degats, missilesprite):
        """Init Fuction"""
        super(Arme, self).__init__()
        self.name = name
        self._degats = degats
        self.missileSprite = missilesprite
		
        def __str__(self):
            """To String function"""
            return "Arme {} with {} degats".format(self.name, self._degats)




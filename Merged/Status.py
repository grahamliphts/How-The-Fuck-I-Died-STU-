class Status( object ):
    def __init__( self ):

        # current score
        self.score = 0
        # current level
        self.level = None
        # current level idx
        self.level_idx = None
		
    def reset( self ):
        self.score = 0
        self.level = None
        self.level_idx = None

status = Status()

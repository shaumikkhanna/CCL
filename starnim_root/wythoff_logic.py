
class Wythoff:
    def __init__(self, piece='queen'):
        self.piece = piece
        self.grid = self.get_grid()
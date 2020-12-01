class Piece:
    def __init__(self, row, col, color, colorShort, colorKing):
        self.row = row
        self.col = col
        self.color = color
        self.colorShort = colorShort
        self.colorKing = colorKing
        self.king = False
        self.captured = False
    
    def move(self, row,col):
        self.row = row
        self.col = col

    def can_move(self):
        return not self.captured

    def capture(self):
        self.captured = True

    def make_king(self):
        self.king = True

    def __repr__(self):
        return str(self.color) + ": (" +str(self.row) + ", " + str(self.col) + ")"

class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position
    def move(self, destination):
        if destination in self.get_valid_moves():
            self.position = destination
        else:
            raise ValueError("Invalid move")

def pathIsClear(self, destination):
    dx = 1 if destination[0] > self.position[0] else -1 if destination[0] < self.position[0] else 0
    dy = 1 if destination[1] > self.position[1] else -1 if destination[1] < self.position[1] else 0
    x, y = self.position[0], self.position[1]
    while x != destination[0] or y != destination[1]:
        x += dx
        y += dy
        if x == destination[0] and y == destination[1]:
            break
        if self.board[x][y] is not None:
            return False
    return True

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.name = 'Pawn'

    def get_valid_moves(self):
        x , y = self.position
        # Implement the rules for pawn movement
        if self.color == 'white' and x == 1:
            return [(x+1, y), (x+2, y)]
            

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'Rook'

    def get_valid_moves(self):
        # Implement the rules for rook movement
        pass

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'Bishop'

    def get_valid_moves(self):
        # Implement the rules for bishop movement
        pass
class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'Knight'

    def get_valid_moves(self):
        # Implement the rules for knight movement
        pass
class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'Queen'

    def get_valid_moves(self):
        # Implement the rules for queen movement
        pass

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'King'

    def get_valid_moves(self):
        # Implement the rules for king movement
        pass

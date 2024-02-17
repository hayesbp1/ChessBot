class Piece:
    def __init__(self, color, position, board):
        self.color = color
        self.position = position
        self.board = board

    def move(self, destination):
        if destination in self.get_valid_moves():
            # If there's a piece at the destination square
            if self.board[destination[0]][destination[1]] is not None:
                # And the piece is the opponent's
                if self.board[destination[0]][destination[1]].color != self.color:
                    # Remove the opponent's piece from the board
                    self.board[destination[0]][destination[1]] = None
            # Move the piece to the destination square
            self.position = destination
        else:
            raise ValueError("Invalid move")
        
    def path_is_clear(self, destination):
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
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'Pawn'

    def get_valid_moves(self):
        valid_moves = []
        x , y = self.position
        # Implement the rules for pawn movement
        if self.color == 'black' and x == 6:
            if self.path_is_clear(self, (x-2, y)):
                valid_moves.append((x-2, y))
            elif self.path_is_clear(self, (x-1, y)):
                valid_moves.append((x-1, y))
        elif self.color == 'white' and x == 1:
            if self.path_is_clear(self, (x+2, y)):
                valid_moves.append((x+2, y))
            elif self.path_is_clear(self, (x+1, y)):
                valid_moves.append((x+1, y))
        elif self.color == 'black':
            if self.path_is_clear(self, (x-1, y)):
                valid_moves.append((x-1, y))
        elif self.color == 'white':
            if self.path_is_clear(self, (x+1, y)):
                valid_moves.append((x+1, y))
        
        # Pawn captures
        if self.color == 'white':
            if self.board[x+1][y-1] is not None and self.board[x+1][y-1].color != self.color:
                valid_moves.append((x+1, y-1))
            if self.board[x+1][y+1] is not None and self.board[x+1][y+1].color != self.color:
                valid_moves.append((x+1, y+1))
        elif self.color == 'black':
            if self.board[x-1][y-1] is not None and self.board[x-1][y-1].color != self.color:
                valid_moves.append((x-1, y-1))
            if self.board[x-1][y+1] is not None and self.board[x-1][y+1].color != self.color:
                valid_moves.append((x-1, y+1))
        return valid_moves   
    
class Rook(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'Rook'

    def get_valid_moves(self):
        # Initialize an empty list to store the legal moves
        valid_moves = []

        # Define the directions in which the rook can move
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            for step in range(1, 8):
                new_x = self.position[0] + step * dx
                new_y = self.position[1] + step * dy

                # Check if the new position is within the board boundaries
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    # If the new position is occupied by an opponent's piece, capture it
                    if self.board[new_x][new_y] is not None:
                        if self.board[new_x][new_y].color != self.color:
                            valid_moves.append((new_x, new_y))
                        break
                    else:
                        valid_moves.append((new_x, new_y))

        return valid_moves

class Bishop(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'Bishop'

    # Implement the rules for bishop movement
    def get_valid_moves(self):
        valid_moves = []
         # Define the directions in which the bishop can move
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            for step in range(1, 8):
                new_x = self.position[0] + step * dx
                new_y = self.position[1] + step * dy

                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    if self.board[new_x][new_y] is None:
                        valid_moves.append((new_x, new_y))
                    elif self.board[new_x][new_y].color != self.color:
                        valid_moves.append((new_x, new_y))
                        break
                    else:
                        break

class Knight(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'Knight'

    def get_valid_moves(self):
        valid_moves = []
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dx, dy in directions:
            x, y = self.position[0] + dx, self.position[1] + dy
            if 0 <= x < 8 and 0 <= y < 8:  # Check if the move is within the board
                if self.board[x][y] is None or self.board[x][y].color != self.color:  # Check if the square is empty or contains an opponent's piece
                    valid_moves.append((x, y))
        return valid_moves

class Queen(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'Queen'

    def get_valid_moves(self):
        valid_moves = []
        # Implement the rules for queen movement
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            for step in range(1, 8):
                new_x = self.position[0] + step * dx
                new_y = self.position[1] + step * dy

                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    if self.board[new_x][new_y] is None:
                        valid_moves.append((new_x, new_y))
                    elif self.board[new_x][new_y].color != self.color:
                        valid_moves.append((new_x, new_y))
                        break
                    else:
                        break

class King(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'King'

    def get_valid_moves(self):
        valid_moves = []
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        # Implement the rules for king movement
        for dx, dy in directions:
            x, y = self.position[0] + dx, self.position[1] + dy
            if 0 <= x < 8 and 0 <= y < 8:  # Check if the move is within the board
                if self.board[x][y] is None or self.board[x][y].color != self.color:  # Check if the square is empty or contains an opponent's piece
                    valid_moves.append((x, y))

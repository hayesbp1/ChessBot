import pygame

class Piece:
    def __init__(self, color, position, board):
        self.color = color
        self.position = position
        self.board = board
        self.en_passant_target = None
        self.hasMoved = False
        # Load the image
        image = pygame.image.load(f"Image/{color}-{self.__class__.__name__}.png")

        # Get the current size
        width, height = image.get_size()

        # Scale the image to 75% of its original size
        self.image = pygame.transform.scale(image, (int(width * 0.75), int(height * 0.75)))

    def draw(self, win):
        x, y = self.position
        win.blit(self.image, (y * 100+2, x * 100))  # Draw the image at the correct position

    def move(self, piece, destination):

        if isinstance(piece, Pawn) and abs(destination[0] - piece.position[0]) == 2:
            self.en_passant_target = (piece.position[0] + (destination[0] - piece.position[0]) // 2, piece.position[1])
        elif isinstance(piece, King):
            if piece.canCastle() and destination[1] in [2, 6]:
                    piece.castle(destination)
            piece.hasMoved = True
        elif isinstance(piece, Rook):
            piece.hasMoved = True
        else:
            self.en_passant_target = None

        if destination in piece.get_valid_moves():
            # If there's a piece at the destination square
            if self.board[destination[0]][destination[1]] is not None:
                # And the piece is the opponent's
                if self.board[destination[0]][destination[1]].color != piece.color:
                    # Remove the opponent's piece from the board
                    self.board[destination[0]][destination[1]] = None
            
             # Save the current state of the board and piece
            old_position = piece.position
            old_square = self.board[destination[0]][destination[1]]

            # Move the piece to the destination square
            self.board[piece.position[0]][piece.position[1]] = None
            self.board[destination[0]][destination[1]] = piece
            piece.position = destination
        else:
            raise ValueError("Invalid move")
            
         # Check if the king is in check
        king = self.board.getKing(piece.color)
        if king.isInCheck():
            # If the king is in check, undo the move and raise an error
            self.board[piece.position[0]][piece.position[1]] = None
            self.board[old_position[0]][old_position[1]] = piece
            piece.position = old_position
            self.board[destination[0]][destination[1]] = old_square
            raise ValueError("Invalid move: King is in check")


        
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
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'Pawn'
    
    # Pawn promotion
    def move(self, destination):
        super().move(destination)
        # Check for pawn promotion
        if (self.color == 'white' and self.position[0] == 7) or (self.color == 'black' and self.position[0] == 0):
            self.promote()

    def promote(self):
        # Ask the player for the type of piece they want
        piece_type = input("Promote pawn to (Q/R/B/N): ")
        if piece_type.upper() == 'Q':
            self.board[self.position[0]][self.position[1]] = Queen(self.color, self.position, self.board)
        elif piece_type.upper() == 'R':
            self.board[self.position[0]][self.position[1]] = Rook(self.color, self.position, self.board)
        elif piece_type.upper() == 'B':
            self.board[self.position[0]][self.position[1]] = Bishop(self.color, self.position, self.board)
        elif piece_type.upper() == 'N':
            self.board[self.position[0]][self.position[1]] = Knight(self.color, self.position, self.board)      

    def get_valid_moves(self):
        legal_moves = []
        x , y = self.position
        # Implement the rules for pawn movement
        if self.color == 'black' and x == 6:
            if self.pathIsClear(self, (x-2, y)):
                legal_moves.append((x-2, y))
            elif self.pathIsClear(self, (x-1, y)):
                legal_moves.append((x-1, y))
        elif self.color == 'white' and x == 1:
            if self.pathIsClear(self, (x+2, y)):
                legal_moves.append((x+2, y))
            elif self.pathIsClear(self, (x+1, y)):
                legal_moves.append((x+1, y))
        elif self.color == 'black':
            if self.pathIsClear(self, (x-1, y)):
                legal_moves.append((x-1, y))
        elif self.color == 'white':
            if self.pathIsClear(self, (x+1, y)):
                legal_moves.append((x+1, y))
        
        # Pawn captures
        if self.color == 'white':
            if self.board[x+1][y-1] is not None and self.board[x+1][y-1].color != self.color:
                legal_moves.append((x+1, y-1))
            if self.board[x+1][y+1] is not None and self.board[x+1][y+1].color != self.color:
                legal_moves.append((x+1, y+1))
        elif self.color == 'black':
            if self.board[x-1][y-1] is not None and self.board[x-1][y-1].color != self.color:
                legal_moves.append((x-1, y-1))
            if self.board[x-1][y+1] is not None and self.board[x-1][y+1].color != self.color:
                legal_moves.append((x-1, y+1))

        # En passant
        if self.board.en_passant_target is not None:
            if self.color == 'white' and x == 3:
                if self.position[1] - 1 == self.board.en_passant_target[1] or self.position[1] + 1 == self.board.en_passant_target[1]:
                    legal_moves.append((self.position[0] + 1, self.board.en_passant_target[1]))
            elif self.color == 'black' and x == 6:
                if self.position[1] - 1 == self.board.en_passant_target[1] or self.position[1] + 1 == self.board.en_passant_target[1]:
                    legal_moves.append((self.position[0] - 1, self.board.en_passant_target[1]))      
        return legal_moves   
    
    
    
class Rook(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'Rook'

    def get_valid_moves(self):
        # Initialize an empty list to store the legal moves
        legal_moves = []

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
                            legal_moves.append((new_x, new_y))
                        break
                    else:
                        legal_moves.append((new_x, new_y))

        return legal_moves

class Bishop(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'Bishop'

    # Implement the rules for bishop movement
    def get_valid_moves(self):
        legal_moves = []
         # Define the directions in which the bishop can move
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            for step in range(1, 8):
                new_x = self.position[0] + step * dx
                new_y = self.position[1] + step * dy

                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    if self.board[new_x][new_y] is None:
                        legal_moves.append((new_x, new_y))
                    elif self.board[new_x][new_y].color != self.color:
                        legal_moves.append((new_x, new_y))
                        break
                    else:
                        break

class Knight(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'Knight'

    def get_valid_moves(self):
        legal_moves = []
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dx, dy in directions:
            x, y = self.position[0] + dx, self.position[1] + dy
            if 0 <= x < 8 and 0 <= y < 8:  # Check if the move is within the board
                if self.board[x][y] is None or self.board[x][y].color != self.color:  # Check if the square is empty or contains an opponent's piece
                    legal_moves.append((x, y))
        return legal_moves

class Queen(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'Queen'

    def get_valid_moves(self):
        legal_moves = []
        # Implement the rules for queen movement
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            for step in range(1, 8):
                new_x = self.position[0] + step * dx
                new_y = self.position[1] + step * dy

                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    if self.board[new_x][new_y] is None:
                        legal_moves.append((new_x, new_y))
                    elif self.board[new_x][new_y].color != self.color:
                        legal_moves.append((new_x, new_y))
                        break
                    else:
                        break

class King(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'King'
        self.hasMoved = False
    
    def canCastle(self, destination):
        opponent_moves = self.board.get_all_opponent_moves()
        if self.hasMoved:
            return False
        if self.color == 'white':
            if self.position == (0, 4):
                if destination == (0,2):
                    if self.board[0][0].name == 'Rook' and self.board[0][0].color == 'white' and not self.board[0][0].hasMoved:
                        if self.pathIsClear(destination) and self.position not in opponent_moves and (0,3) not in opponent_moves and (0,2) not in opponent_moves:
                            return True
                elif destination == (0,6):
                    if self.board[0][7].name == 'Rook' and self.board[0][7].color == 'white' and not self.board[0][7].hasMoved:
                        if self.pathIsClear(destination) and self.position not in opponent_moves and (0,5) not in opponent_moves and (0,6) not in opponent_moves:
                            return True
            return False
        else:
            if self.position == (7, 4):
                if destination == (7,2):
                    if self.board[7][0].name == 'Rook'and self.board[7][0].color == 'black' and not self.board[7][0].hasMoved:
                        if self.pathIsClear(destination) and self.position not in opponent_moves and (7,3) not in opponent_moves and (7,2) not in opponent_moves:
                            return True
                elif destination == (7,6):
                    if self.board[7][7].name == 'Rook' and self.board[7][7].color == 'black' and not self.board[7][7].hasMoved:
                        if self.pathIsClear(destination) and self.position not in opponent_moves and (7,5) not in opponent_moves and (7,6) not in opponent_moves:
                            return True
            return False
            
    def isInCheck(self):
        opponent_moves = self.board.get_all_opponent_moves()
        return self.position in opponent_moves
            
    def castle(self, destination):
        super().move(destination)
        x, y = self.position[0], self.position[1]

        if destination[1] == 2:
            self.board[self.position[0]][0].move((self.position[0], 3))
        elif destination[1] == 6:
            self.board[self.position[0]][7].move((self.position[0], 5))
        Piece.hasMoved = True     
        
    def get_valid_moves(self):
        legal_moves = []
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        # Implement the rules for king movement
        for dx, dy in directions:
            x, y = self.position[0] + dx, self.position[1] + dy
            if 0 <= x < 8 and 0 <= y < 8:  # Check if the move is within the board
                if self.board[x][y] is None or self.board[x][y].color != self.color:  # Check if the square is empty or contains an opponent's piece
                    legal_moves.append((x, y))
        # Remove squares that would put the king in check
        opponent_moves = self.get_all_opponent_moves()
        legal_moves = [move for move in legal_moves if move not in opponent_moves]

        return legal_moves
    
    
    def get_all_opponent_moves(self):
        opponent_moves = []
        for row in self.board:
            for piece in row:
                if piece is not None and piece.color != self.color:
                    opponent_moves.extend(piece.get_valid_moves())
        return opponent_moves
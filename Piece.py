import pygame

class Piece:
    def __init__(self, color, position, board):
        self.color = color
        self.position = position
        self.board = board
        self.hasMoved = False
        # Load the image
        image = pygame.image.load(f"Image/{color}-{self.__class__.__name__}.png")

        # Get the current size
        width, height = image.get_size()

        # Scale the image to 75% of its original size
        self.image = pygame.transform.scale(image, (int(width * 0.75), int(height * 0.75)))

    def draw(self, win):
        x, y = self.position
        win.blit(self.image, (y * 100, x * 100))  # Draw the image at the correct position

    def get_name(self):
        return self.name
    
    def move(self, destination, board):
        if isinstance(self, Pawn) and abs(destination[0] - self.position[0]) == 2:
            board.en_passant_target = (self.position[0] + (destination[0] - self.position[0]) // 2, self.position[1])
        elif isinstance(self, King):
            if self.canCastle() and destination[1] in [2, 6]:
                self.castle(destination)
            self.hasMoved = True
        elif isinstance(self, Rook):
            self.hasMoved = True
        else:
            self.en_passant_target = None

        if destination in self.get_valid_moves():
            # If there's a piece at the destination square
            piece = self.board.get_piece(destination[0], destination[1])
            if piece is not None:
                # And the piece is the opponent's
                if piece.color != self.color:
                    # Remove the opponent's piece from the board
                    piece = self.board.get_piece(destination[0], destination[1])
                    piece = None

            # Save the current state of the board and piece
            old_position = self.position
            old_square = self.board.get_piece(destination[0], destination[1])

            # Move the piece to the destination square
            self.board.set_piece(None, self.position[0], self.position[1])
            board.set_piece(self, destination[0], destination[1])
            self.position = destination
            board.turn += 1
        else:
            raise ValueError("Invalid move")


        
    def path_is_clear(self, destination):
        dx = 1 if destination[0] > self.position[0] else -1 if destination[0] < self.position[0] else 0
        dy = 1 if destination[1] > self.position[1] else -1 if destination[1] < self.position[1] else 0
        x, y = self.position[0], self.position[1]
        while x != destination[0] or y != destination[1]:
            x += dx
            y += dy
            piece = self.board.get_piece(x,y)
            if x == destination[0] and y == destination[1]:
                break
            if piece is not None:
                return False
        return True

class Pawn(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'Pawn'
    
    # Pawn promotion
    def move(self, destination, board):
        super().move(destination, board)
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
        valid_moves = []
        x , y = self.position
        # Implement the rules for pawn movement

        if self.color == 'black':
            if x == 6:
                if self.path_is_clear((x-2, y)):
                    valid_moves.append((x-2, y))
            elif self.path_is_clear((x-1, y)):
                valid_moves.append((x-1, y))
            if self.path_is_clear((x-1, y)):
                valid_moves.append((x-1, y))
        elif self.color == 'white':
            if x == 1:
                if self.path_is_clear((x+2, y)):
                    valid_moves.append((x+2, y))
                elif self.path_is_clear((x+1, y)):
                    valid_moves.append((x+1, y))
            if self.path_is_clear((x+1, y)):
                valid_moves.append((x+1, y))

        # Pawn captures
        
        if self.color == 'white':
            new_x, new_y = x+1, y-1
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = self.board.get_piece(new_x, new_y)
                if piece is not None and piece.color != self.color:
                    valid_moves.append((new_x, new_y))
            new_y = y+1
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = self.board.get_piece(new_x, new_y)
                if piece is not None and piece.color != self.color:
                    valid_moves.append((new_x, new_y)) 
        elif self.color == 'black':
            new_x, new_y = x-1, y-1
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = self.board.get_piece(new_x, new_y)
                if piece is not None and piece.color != self.color:
                    valid_moves.append((new_x, new_y))
            new_y = y+1
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = self.board.get_piece(new_x, new_y)
                if piece is not None and piece.color != self.color:
                    valid_moves.append((new_x, new_y))

        # En passant
        if self.board.en_passant_target is not None:
            if self.color == 'white' and x == 3:
                if self.position[1] - 1 == self.board.en_passant_target[1] or self.position[1] + 1 == self.board.en_passant_target[1]:
                    valid_moves.append((self.position[0] + 1, self.board.en_passant_target[1]))
            elif self.color == 'black' and x == 6:
                if self.position[1] - 1 == self.board.en_passant_target[1] or self.position[1] + 1 == self.board.en_passant_target[1]:
                    valid_moves.append((self.position[0] - 1, self.board.en_passant_target[1]))      
        
        if valid_moves is None:  # If there are no valid moves
            return []  # Return an empty list
        else:
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
                    piece = self.board.get_piece(new_x, new_y)
                    # If the new position is occupied by an opponent's piece, capture it
                    if piece is not None:
                        if piece.color != self.color:
                            valid_moves.append((new_x, new_y))
                        break
                    else:
                        valid_moves.append((new_x, new_y))
        if valid_moves is None:  # If there are no valid moves
            return []  # Return an empty list
        else:
            return valid_moves 

class Bishop(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'Bishop'

    # Implement the rules for bishop movements
    def get_valid_moves(self):
        valid_moves = []
        # Define the directions in which the bishop can move
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            for step in range(1, 8):
                new_x = self.position[0] + step * dx
                new_y = self.position[1] + step * dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    piece = self.board.get_piece(new_x, new_y)
                    if piece is None:
                        valid_moves.append((new_x, new_y))
                    elif piece.color != self.color:
                        valid_moves.append((new_x, new_y))
                        break
                    else:
                        break
        if valid_moves is None:  # If there are no valid moves
            return []  # Return an empty list
        else:
            return valid_moves 

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
                piece = self.board.get_piece(x, y)
                if piece is None or piece.color != self.color:  # Check if the square is empty or contains an opponent's piece
                    valid_moves.append((x, y))
        if valid_moves is None:  # If there are no valid moves
            return []  # Return an empty list
        else:
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
                    piece = self.board.get_piece(new_x, new_y)
                    if piece is None:
                        valid_moves.append((new_x, new_y))
                    elif piece.color != self.color:
                        valid_moves.append((new_x, new_y))
                        break
                    else:
                        break
        if valid_moves is None:  # If there are no valid moves
            return []  # Return an empty list
        else:
            return valid_moves 

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
                        if self.path_is_clear(destination) and self.position not in opponent_moves and (0,3) not in opponent_moves and (0,2) not in opponent_moves:
                            return True
                elif destination == (0,6):
                    if self.board[0][7].name == 'Rook' and self.board[0][7].color == 'white' and not self.board[0][7].hasMoved:
                        if self.path_is_clear(destination) and self.position not in opponent_moves and (0,5) not in opponent_moves and (0,6) not in opponent_moves:
                            return True
            return False
        else:
            if self.position == (7, 4):
                if destination == (7,2):
                    if self.board[7][0].name == 'Rook'and self.board[7][0].color == 'black' and not self.board[7][0].hasMoved:
                        if self.path_is_clear(destination) and self.position not in opponent_moves and (7,3) not in opponent_moves and (7,2) not in opponent_moves:
                            return True
                elif destination == (7,6):
                    if self.board[7][7].name == 'Rook' and self.board[7][7].color == 'black' and not self.board[7][7].hasMoved:
                        if self.path_is_clear(destination) and self.position not in opponent_moves and (7,5) not in opponent_moves and (7,6) not in opponent_moves:
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
        # Calculate the valid moves...
        valid_moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in directions:
            new_x, new_y = self.position[0] + dx, self.position[1] + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = self.board.get_piece(new_x, new_y)
                if piece is None or (piece.color != self.color and not isinstance(piece, King)):
                    # Check the square one step further
                    further_x, further_y = new_x + dx, new_y + dy
                    if 0 <= further_x < 8 and 0 <= further_y < 8:
                        further_piece = self.board.get_piece(further_x, further_y)
                        if further_piece is None or (further_piece.color != self.color and not isinstance(further_piece, King)):
                            valid_moves.append((new_x, new_y))
        return valid_moves

    
    
    def get_all_opponent_moves(self):
        opponent_moves = []
        for row in range(8):  # Assuming an 8x8 board
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece is not None and piece.color != self.color:
                    opponent_moves.extend(piece.get_valid_moves())
        return opponent_moves

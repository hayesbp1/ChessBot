import pygame as py
import Piece
import ChessEngine

class Board:
    def __init__(self, player_color):
        self.highlighted_squares = []
        self.player_color = player_color
        self.board = self.setup_board(player_color)
        self.draw_board(py.display.set_mode((800, 800)))
        self.en_passant_target = None
        self.turn = 0
        
    # def highlight_square(self, win, move, color=(255, 165, 0)):
    #     py.draw.rect(win, color, (move[1] * 100, move[0]* 100, 100, 100))
    #     py.display.update()

    def setup_board(self, player_color):
        board = [[None] * 8 for _ in range(8)]
        if player_color == 'black':
            # Create and place the white pieces
            board[0][0] = Piece.Rook('white', (0, 0), self)
            board[0][1] = Piece.Knight('white', (0, 1), self)
            board[0][2] = Piece.Bishop('white', (0, 2), self)
            board[0][3] = Piece.Queen('white', (0, 3), self)
            board[0][4] = Piece.King('white', (0, 4), self)
            board[0][5] = Piece.Bishop('white', (0, 5), self)
            board[0][6] = Piece.Knight('white', (0, 6), self)
            board[0][7] = Piece.Rook('white', (0, 7), self)
            for i in range(8):
                board[1][i] = Piece.Pawn('white', (1, i), self)
            # Create and place the black pieces
            board[7][0] = Piece.Rook('black', (7, 0), self)
            board[7][1] = Piece.Knight('black', (7, 1), self)
            board[7][2] = Piece.Bishop('black', (7, 2), self)
            board[7][3] = Piece.Queen('black', (7, 3), self)
            board[7][4] = Piece.King('black', (7, 4), self)
            board[7][5] = Piece.Bishop('black', (7, 5), self)
            board[7][6] = Piece.Knight('black', (7, 6), self)
            board[7][7] = Piece.Rook('black', (7, 7), self)
            for i in range(8):
                board[6][i] = Piece.Pawn('black', (6, i), self)
            return board
        else:
            # Create and place the white pieces
            board[7][0] = Piece.Rook('white', (7, 0), self)
            board[7][1] = Piece.Knight('white', (7, 1), self)
            board[7][2] = Piece.Bishop('white', (7, 2), self)
            board[7][3] = Piece.Queen('white', (7, 3), self)
            board[7][4] = Piece.King('white', (7, 4), self)
            board[7][5] = Piece.Bishop('white', (7, 5), self)
            board[7][6] = Piece.Knight('white', (7, 6), self)
            board[7][7] = Piece.Rook('white', (7, 7), self)
            for i in range(8):
                board[6][i] = Piece.Pawn('white', (6, i), self)
            # Create and place the black pieces
            board[0][0] = Piece.Rook('black', (0, 0), self)
            board[0][1] = Piece.Knight('black', (0, 1), self)
            board[0][2] = Piece.Bishop('black', (0, 2), self)
            board[0][3] = Piece.Queen('black', (0, 3), self)
            board[0][4] = Piece.King('black', (0, 4), self)
            board[0][5] = Piece.Bishop('black', (0, 5), self)
            board[0][6] = Piece.Knight('black', (0, 6), self)
            board[0][7] = Piece.Rook('black', (0, 7), self)
            for i in range(8):
                board[1][i] = Piece.Pawn('black', (1, i), self)
            return board
    
    def get_piece(self, row, col):
        piece = self.board[row][col]
        if piece is None:
            return None
        return piece

    def set_piece(self, piece, row, col):
        self.board[row][col] = piece

    
    def get_all_opponent_moves(self, color):
        opponent_moves = []
        for row in self.board:
            for piece in row:
                if piece is not None and piece.color != self.color and not isinstance(piece, Piece.King):
                    opponent_moves.extend(piece.get_valid_moves())
        return opponent_moves
    
    def get_current_player_color(self):
        return 'white' if self.turn % 2 == 0 else 'black'

    def get_king(self, color):
        for row in self.board:
            for piece in row:
                if piece is not None and piece.color == color and isinstance(piece, Piece.King):
                    return piece
                
    def get_square_color(self, row, col):
        # Check if the square is in the list of highlighted squares
        if (col, row) in self.highlighted_squares:
            return (255, 165, 0)  # Return the highlight color
        elif (row + col) % 2 == 0:
            return (255, 255, 255)  # Return the color for light squares
        else:
            return (115, 147, 179)  # Return the color for dark squares
                
    def draw_board(self, win):
        for row in range(8):
            for col in range(8):
                square_color = self.get_square_color(row, col)
                py.draw.rect(win, square_color, (row*100, col*100, 100, 100))
        for row in self.board:
            for piece in row:
                if piece is not None:
                    piece.draw(win)
        py.display.update()
    
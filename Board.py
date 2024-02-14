import pygame as py
from Piece import Rook, Knight, Bishop, Queen, King, Pawn
import ChessEngine

class Board:
    def __init__(self, player_color):
        self.player_color = player_color
        self.board = self.setup_board(player_color)
        self.drawBoard(py.display.set_mode((800, 800)))
        
    
    def setup_board(self, player_color):
        board = [[None] * 8 for _ in range(8)]
        if player_color == 'black':
            # Create and place the white pieces
            board[0][0] = Rook('white', (0, 0), self)
            board[0][1] = Knight('white', (0, 1), self)
            board[0][2] = Bishop('white', (0, 2), self)
            board[0][3] = Queen('white', (0, 3), self)
            board[0][4] = King('white', (0, 4), self)
            board[0][5] = Bishop('white', (0, 5), self)
            board[0][6] = Knight('white', (0, 6), self)
            board[0][7] = Rook('white', (0, 7), self)
            for i in range(8):
                board[1][i] = Pawn('white', (1, i), self)
            # Create and place the black pieces
            board[7][0] = Rook('black', (7, 0), self)
            board[7][1] = Knight('black', (7, 1), self)
            board[7][2] = Bishop('black', (7, 2), self)
            board[7][3] = Queen('black', (7, 3), self)
            board[7][4] = King('black', (7, 4), self)
            board[7][5] = Bishop('black', (7, 5), self)
            board[7][6] = Knight('black', (7, 6), self)
            board[7][7] = Rook('black', (7, 7), self)
            for i in range(8):
                board[6][i] = Pawn('black', (6, i), self)
            return board
        else:
            # Create and place the white pieces
            board[7][0] = Rook('white', (7, 0), self)
            board[7][1] = Knight('white', (7, 1), self)
            board[7][2] = Bishop('white', (7, 2), self)
            board[7][3] = Queen('white', (7, 3), self)
            board[7][4] = King('white', (7, 4), self)
            board[7][5] = Bishop('white', (7, 5), self)
            board[7][6] = Knight('white', (7, 6), self)
            board[7][7] = Rook('white', (7, 7), self)
            for i in range(8):
                board[6][i] = Pawn('white', (6, i), self)
            # Create and place the black pieces
            board[0][0] = Rook('black', (0, 0), self)
            board[0][1] = Knight('black', (0, 1), self)
            board[0][2] = Bishop('black', (0, 2), self)
            board[0][3] = Queen('black', (0, 3), self)
            board[0][4] = King('black', (0, 4), self)
            board[0][5] = Bishop('black', (0, 5), self)
            board[0][6] = Knight('black', (0, 6), self)
            board[0][7] = Rook('black', (0, 7), self)
            for i in range(8):
                board[1][i] = Pawn('black', (1, i), self)
            return board
    
    def getAllOpponentMoves(self, color):
        opponent_moves = []
        for row in self.board:
            for piece in row:
                if piece is not None and piece.color != color:
                    opponent_moves.extend(piece.get_valid_moves())
        return opponent_moves

    def getKing(self, color):
        for row in self.board:
            for piece in row:
                if piece is not None and piece.color == color and isinstance(piece, King):
                    return piece
                
    def drawBoard(self, win):
        win.fill((255, 255, 255))
        colors = [(255, 255, 255), (115, 147, 179)]
        for i in range(8):
            for j in range(8):
                py.draw.rect(win, colors[(i + j) % 2], (i * 100, j * 100, 100, 100))
        for row in self.board:
            for piece in row:
                if piece is not None:
                    piece.draw(win)
        py.display.update()
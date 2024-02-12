class Board:
    def __init__(self):
        self.board = self.setup_board()
    
    def setup_board(self):
        board = [[None] * 8 for _ in range(8)]
        # Create and place the white pieces
        board[0][0] = Rook('white', (0, 0), board)
        board[0][1] = Knight('white', (0, 1), board)
        board[0][2] = Bishop('white', (0, 2), board)
        board[0][3] = Queen('white', (0, 3), board)
        board[0][4] = King('white', (0, 4), board)
        board[0][5] = Bishop('white', (0, 5), board)
        board[0][6] = Knight('white', (0, 6), board)
        board[0][7] = Rook('white', (0, 7), board)
        for i in range(8):
            board[1][i] = Pawn('white', (1, i), board)
        # Create and place the black pieces
        board[7][0] = Rook('black', (7, 0), board)
        board[7][1] = Knight('black', (7, 1), board)
        board[7][2] = Bishop('black', (7, 2), board)
        board[7][3] = Queen('black', (7, 3), board)
        board[7][4] = King('black', (7, 4), board)
        board[7][5] = Bishop('black', (7, 5), board)
        board[7][6] = Knight('black', (7, 6), board)
        board[7][7] = Rook('black', (7, 7), board)
        for i in range(8):
            board[6][i] = Pawn('black', (6, i), board)
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
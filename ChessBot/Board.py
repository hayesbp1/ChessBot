# Initialize an empty 8x8 chess board
chess_board = [[None for _ in range(8)] for _ in range(8)]

# Set up the white pieces
chess_board[7][0] = 'WR'  # White Rooks
chess_board[7][7] = 'WR'
chess_board[7][1] = 'WN'  # White Knights
chess_board[7][6] = 'WN'
chess_board[7][2] = 'WB'  # White Bishops
chess_board[7][5] = 'WB'
chess_board[7][3] = 'WQ'  # White Queen
chess_board[7][4] = 'WK'  # White King

# Set up the white pawns
for i in range(8):
    chess_board[6][i] = 'WP'

# Set up the black pieces
chess_board[0][0] = 'BR'  # Black Rooks
chess_board[0][7] = 'BR'
chess_board[0][1] = 'BN'  # Black Knights
chess_board[0][6] = 'BN'
chess_board[0][2] = 'BB'  # Black Bishops
chess_board[0][5] = 'BB'
chess_board[0][3] = 'BQ'  # Black Queen
chess_board[0][4] = 'BK'  # Black King

# Set up the black pawns
for i in range(8):
    chess_board[1][i] = 'BP'

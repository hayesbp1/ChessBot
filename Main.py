from Board import Board
from Piece import Rook, Knight, Bishop, Queen, King, Pawn
import pygame

def main():
    board = Board('black')
    gameOver = False

    # Initialize Pygame
    pygame.init()

    # Set up the display
    win = pygame.display.set_mode((800, 800))  # Adjust to the size of your board
    square_size = 800 // 8
 
    # Game loop
    running = True
    selected_piece = None  # Variable to keep track of the currently selected piece
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse click
                y, x = pygame.mouse.get_pos()

                # Convert the screen coordinates to board coordinates
                row, col = x // square_size, y // square_size
                piece = board.get_piece(row, col)
                clicked_piece = piece if piece is not None and piece.color == board.get_current_player_color() else None
                # Check if there is a piece at the clicked square
                if clicked_piece is not None:
                    selected_piece = clicked_piece  # Set the selected piece
                    board.highlighted_squares = clicked_piece.get_valid_moves(board)
                    print(board.highlighted_squares)
                elif (row, col) in board.highlighted_squares and selected_piece is not None:
                    selected_piece.move((row, col), board)
                    board.highlighted_squares = []
                    print(board.highlighted_squares)
        # Draw the board
        board.draw_board(win)

    # Quit Pygame
    pygame.quit()
        

if __name__ == "__main__": 
    main()

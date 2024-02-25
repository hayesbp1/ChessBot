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
    in_check = False  # Variable to keep track of whether the current player is in check
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse click
                y, x = pygame.mouse.get_pos()
                # Convert the screen coordinates to board coordinates
                row, col = x // square_size, y // square_size

                # Get the piece at the clicked square
                piece = board.get_piece(row, col)
                clicked_piece = piece if piece is not None and piece.color == board.get_current_player_color() else None
                
                # Check if there is a piece at the clicked square
                if clicked_piece is not None:
                    selected_piece = clicked_piece  # Set the selected piece
                    board.highlighted_squares = clicked_piece.get_valid_moves()
                    print(board.highlighted_squares)

                elif (row, col) in board.highlighted_squares and selected_piece is not None:
                    selected_piece.move((row, col), board)
                    board.highlighted_squares = []

                    # Find out if king is in check after the move
                    in_check = board.is_in_check(board.get_current_player_color())
                    if in_check:
                        print("You are in check!")
        # Draw the board
        board.draw_board(win)

    # Quit Pygame
    pygame.quit()
        

if __name__ == "__main__": 
    main()

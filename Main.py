from Board import Board
from Piece import Rook, Knight, Bishop, Queen, King, Pawn
import pygame

def main():
    board = Board('white')
    gameOver = False

    # Initialize Pygame
    pygame.init()

    # Set up the display
    win = pygame.display.set_mode((800, 800))  # Adjust to the size of your board

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the board
        board.drawBoard(win)

    # Quit Pygame
    pygame.quit()
        

if __name__ == "__main__":
    main()

from lib2to3.pygram import python_grammar_no_print_and_exec_statement

import pygame
import sys
from src.utils.constants import *
from src.core.grid import make_grid
def main ():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_WIDTH))

    rows, cols = 15, 15
    floor_padding = 20
    floor_width = (WINDOW_WIDTH // 3)
    tile_size = (GRID_HEIGHT // rows)

    grid = make_grid(3,rows,cols,tile_size,floor_width)

    running = True
    while running:
        screen.fill(APP_BACKGROUND)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        for floor in grid:
            for row in floor:
                for node in row:
                    node.draw(screen)

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()




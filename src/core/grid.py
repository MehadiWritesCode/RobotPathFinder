import pygame
from pygments.styles.rainbow_dash import WHITE, GREEN, RED, BLUE
from src.utils.constants import *

class Node:
    def __init__ (self,row,col,floor,tile_size,floor_width):

        self.row = row
        self.col = col
        self.floor = floor
        self.tile_size = tile_size
        self.floor_width = floor_width

        self.x = col * tile_size + (floor*floor_width)
        self.y = row * tile_size

        self.color = WHITE
        self.is_elevators = False
        self.is_stairs = False
        self.neighbours = []


    def make_wall(self): self.color = BLACK
    def make_start(self): self.color = GREEN
    def make_end(self): self.color = RED

    def make_elevator(self):
        self.is_elevators = True
        self.color = TILE_ELEVATOR

    def make_stairs(self):
        self.is_stairs = True
        self.color = TILE_STAIRS

    def draw(self,win):
        gap = 2
        pygame.draw.rect(win, self.color,
                         (self.x, self.y + scale(45),
                          self.tile_size - gap, self.tile_size - gap),
                          border_radius=4)

def make_grid(floors, rows, cols, tile_size, floor_width):
    grid = []

    for f in range(floors):
        floor_grid = []

        for i in range(rows):
            row = []

            for j in range(cols):
                col = []
                node = Node(i,j,f,tile_size,floor_width)

                if i == rows // 2 and j == cols // 2:
                    node.make_elevator()

                elif (j==0 or j == cols - 1) and (i == 1 or i == rows - 2):
                    node.make_stairs()

                row.append(node)
            floor_grid.append(row)
        grid.append(floor_grid)
    return grid




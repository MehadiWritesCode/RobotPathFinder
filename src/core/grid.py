import pygame
from src.utils.constants import *


class Node:
    def __init__(self, row, col, floor, tile_size, floor_width):
        self.row = row
        self.col = col
        self.floor = floor
        self.tile_size = tile_size
        self.floor_width = floor_width

        self.x = col * tile_size + (floor * floor_width)
        self.y = row * tile_size

        self.color = TILE_EMPTY
        self.is_elevators = False
        self.is_stairs = False
        self.neighbours = []

    def make_wall(self): self.color = TILE_WALL
    def make_start(self): self.color = TILE_START
    def make_end(self): self.color = TILE_END

    def make_elevator(self):
        self.is_elevators = True
        self.color = TILE_ELEVATOR

    def make_stairs(self):
        self.is_stairs = True
        self.color = TILE_STAIRS

    def reset(self):
        if self.is_elevators:
            self.color = TILE_ELEVATOR
        elif self.is_stairs:
            self.color = TILE_STAIRS
        else:
            self.color = TILE_EMPTY

    def draw_with_offset(self, win, x_off, y_off, elevator_img, stairs_img):
        gap = 1

        self.x_off = x_off + (self.col * self.tile_size)
        self.y_off = y_off + (self.row * self.tile_size)

        pygame.draw.rect(
            win,
            self.color,
            (self.x_off, self.y_off, self.tile_size - gap, self.tile_size - gap),
            border_radius=5
        )

        if self.is_elevators:
            win.blit(elevator_img, (self.x_off, self.y_off))

        elif self.is_stairs:
            win.blit(stairs_img, (self.x_off, self.y_off))

    def is_hovered(self, mouse_pos):
        mx, my = mouse_pos
        return self.real_x <= mx < self.real_x + self.tile_size and \
               self.real_y <= my < self.real_y + self.tile_size

    def get_pos(self):
        return self.row, self.col

    def make_closed(self):
        if self.color not in [TILE_START, TILE_END, TILE_ELEVATOR, TILE_STAIRS]:
            self.color = (60, 65, 80)

    def make_open(self):
        if self.color not in [TILE_START, TILE_END, TILE_ELEVATOR, TILE_STAIRS]:
            self.color = SCANNING_OPEN

    def make_path(self):
        if self.color not in [TILE_START, TILE_END, TILE_ELEVATOR, TILE_STAIRS]:
            self.color = PATH_COLOR

    def update_neighbors(self, grid, num_floors, rows, cols):
        self.neighbors = []
        # SAME FLOOR NEIGHBOURS
        if self.row < rows - 1 and grid[self.floor][self.row + 1][self.col].color != TILE_WALL:
            self.neighbors.append(grid[self.floor][self.row + 1][self.col])
        if self.row > 0 and grid[self.floor][self.row - 1][self.col].color != TILE_WALL:
            self.neighbors.append(grid[self.floor][self.row - 1][self.col])
        if self.col < cols - 1 and grid[self.floor][self.row][self.col + 1].color != TILE_WALL:
            self.neighbors.append(grid[self.floor][self.row][self.col + 1])
        if self.col > 0 and grid[self.floor][self.row][self.col - 1].color != TILE_WALL:
            self.neighbors.append(grid[self.floor][self.row][self.col - 1])

        # FLOOR CHANGING
        if self.is_elevators or self.is_stairs:
            if self.floor < num_floors - 1: # GO UP
                self.neighbors.append(grid[self.floor + 1][self.row][self.col])
            if self.floor > 0: # DO DOWN
                self.neighbors.append(grid[self.floor - 1][self.row][self.col])


def make_grid(floors, rows, cols, tile_size, floor_width):
    grid = []

    for f in range(floors):
        floor_grid = []

        for i in range(rows):
            row = []

            for j in range(cols):
                node = Node(i, j, f, tile_size, floor_width)

                if i == rows // 2 and j == cols // 2:
                    node.make_elevator()

                elif (j == 0 or j == cols - 1) and (i == 1 or i == rows - 2):
                    node.make_stairs()

                row.append(node)

            floor_grid.append(row)

        grid.append(floor_grid)

    return grid



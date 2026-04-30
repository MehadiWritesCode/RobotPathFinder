# import pygame
# import heapq
# import time
# from src.utils.constants import MOVE_COST, ELEVATOR_COST, STAIRS_COST
# def heuristic(p1,p2):
#     x1, y1 = p1
#     x2, y2 = p2
#     return abs(x1 - x2) + abs(y1 - y2)
#
# def reconstruct_path(came_from, current, draw):
#     while current in came_from:
#         current = came_from[current]
#         current.make_path()
#         draw()
#
# def algorithm(draw,grid,start,end):
#     start_time = time.time()
#     count = 0
#     visited_count = 0
#     open_set = []
#     heapq.heappush(open_set,(0,count,start))
#     came_from = {}
#
#     g_score = {node: float("inf") for floor in grid for row in floor for node in row}
#     g_score[start] = 0
#
#     f_score = {node: float("inf") for floor in grid for row in floor for node in row}
#     f_score[start] = heuristic(start.get_pos(), end.get_pos())
#
#     open_set_hash = {start}
#
#     while open_set:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#
#         current = heapq.heappop(open_set)[2]
#         open_set_hash.remove(current)
#
#         if current == end:
#             reconstruct_path(came_from, end, draw)
#             end.make_end()
#             return True
#
#         for neighbor in current.neighbors:
#             cost = MOVE_COST
#
#             # IF LIFT OR STAIRS THEN UPDATE COST
#             if neighbor.is_elevators:
#                 cost = ELEVATOR_COST
#             elif neighbor.is_stairs:
#                 cost = STAIRS_COST
#
#             # GOAL SCORE
#             temp_g_score = g_score[current] + cost
#
#             if temp_g_score < g_score[neighbor]:
#                 came_from[neighbor] = current
#                 g_score[neighbor] = temp_g_score
#                 f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
#                 if neighbor not in open_set_hash:
#                     count += 1
#                     heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
#                     open_set_hash.add(neighbor)
#                     neighbor.make_open()
#
#         draw()
#
#         if current != start:
#             current.make_closed()
#     return False

import pygame
import heapq
import time
from src.utils.constants import MOVE_COST, ELEVATOR_COST, STAIRS_COST

#Manhattan Distance
def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

#BACKTRACK AND FINAL PATH PRINT
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):

    start_time = time.time()  # Start performance timer
    count = 0
    visited_count = 0  # Tracks total nodes explored
    open_set = []  # Priority queue for nodes to evaluate

    # Push start node with
    heapq.heappush(open_set, (0, count, start))
    came_from = {}  # Stores the most efficient parent for each node

    #Cost from start to current destionation
    g_score = {node: float("inf") for floor in grid for row in floor for node in row}
    g_score[start] = 0

    #Start to end total cost
    f_score = {node: float("inf") for floor in grid for row in floor for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while open_set:
        #Window event handle
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Get node with the lowest estimated total cost
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)
        visited_count += 1

        # Destination reached
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()

            # Calculate total shortest path
            path_cost = g_score[end]
            time_taken = (time.time() - start_time) * 1000
            return True, visited_count, path_cost, time_taken

        for neighbor in current.neighbors:
            # Assign dynamic traversal costs
            cost = MOVE_COST
            if neighbor.is_elevators:
                cost = ELEVATOR_COST
            elif neighbor.is_stairs:
                cost = STAIRS_COST

            # Tentative cost to reach neighbor via current node
            temp_g_score = g_score[current] + cost

            #If new path is better
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()  # Refresh UI during search

        #mark as closed
        if current != start:
            current.make_closed()

    # Search failed: no path exists between points
    return False, visited_count, 0, 0

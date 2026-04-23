import pygame
import heapq
from src.utils.constants import MOVE_COST, ELEVATOR_COST, STAIRS_COST
def heuristic(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw,grid,start,end):
    count = 0
    open_set = []
    heapq.heappush(open_set,(0,count,start))
    came_from = {}

    g_score = {node: float("inf") for floor in grid for row in floor for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for floor in grid for row in floor for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            cost = MOVE_COST

            # ২. যদি প্রতিবেশী ঘরটি লিফট বা সিঁড়ি হয়, তবে কস্ট বাড়িয়ে দিন
            if neighbor.is_elevators:
                cost = ELEVATOR_COST
            elif neighbor.is_stairs:
                cost = STAIRS_COST

            # ৩. এখন কস্ট যোগ করে নতুন g_score হিসাব করুন
            temp_g_score = g_score[current] + cost

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()
    return False





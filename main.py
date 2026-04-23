import pygame
from src.utils.constants import *
from src.core.grid import make_grid
from src.ui.components import Button
from src.core.algorithm import algorithm

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pathfinding Dashboard")

    # STATS
    stats = {
        "visited": 0,
        "cost": 0,
        "time": 0,
        "found": None
    }

    # COLORS
    SIDEBAR_WIDTH = scale(240)
    COLORS = {
        "bg": (14, 14, 18),
        "sidebar": (22, 22, 28),
        "card": (35, 35, 42),
        "shadow": (10, 10, 12),
        "accent": (0, 170, 255),
        "text": (235, 235, 235),
    }

    rows, cols = 10, 10
    num_floors = 6

    # ------------------------- GRID LAYOUT ------------------------
    cards_per_row = 3
    card_gap = 25

    left_padding = SIDEBAR_WIDTH + 25
    top_padding = 20

    available_width = WINDOW_WIDTH - SIDEBAR_WIDTH - 50

    floor_width = (available_width - card_gap * (cards_per_row - 1)) // cards_per_row

    # 🔥 FIX: AUTO HEIGHT (IMPORTANT)
    rows_needed = (num_floors + cards_per_row - 1) // cards_per_row
    available_height = WINDOW_HEIGHT - 40

    floor_height = (available_height - card_gap * (rows_needed - 1)) // rows_needed

    tile_size = min(floor_width // cols, floor_height // rows)

    grid = make_grid(num_floors, rows, cols, tile_size, floor_width)


    # ---------------------------- BUTTONS -------------------------
    btn_x = (SIDEBAR_WIDTH - scale(140)) // 2
    start_y = scale(120)
    gap = scale(55)

    buttons = [
        Button("WALL", btn_x, start_y, scale(140), scale(40), (70, 70, 75), (100, 100, 100), "WALL"),
        Button("START", btn_x, start_y + gap, scale(140), scale(40), (50, 140, 60), (70, 180, 90), "START"),
        Button("END", btn_x, start_y + gap * 2, scale(140), scale(40), (200, 60, 60), (230, 90, 90), "END"),
        Button("CLEAR", btn_x, start_y + gap * 3, scale(140), scale(40), (60, 60, 60), (90, 90, 90), "CLEAR"),
        Button("RUN", btn_x, WINDOW_HEIGHT - scale(90), scale(140), scale(50), (0, 140, 255), (0, 170, 255), "RUN")
    ]

    elevator_img = pygame.transform.scale(
        pygame.image.load("assets/elevator.png"),
        (tile_size - 4, tile_size - 4)
    )

    stairs_img = pygame.transform.scale(
        pygame.image.load("assets/stairs.png"),
        (tile_size - 4, tile_size - 4)
    )

    current_tool = ""
    running = True

    font = pygame.font.SysFont("Arial", 18, bold=True)

    def draw_sync():

        for f_idx, floor in enumerate(grid):

            row_idx = f_idx // cards_per_row
            col_idx = f_idx % cards_per_row
            x_off = left_padding + col_idx * (floor_width + card_gap) + (floor_width - cols * tile_size) // 2
            y_off = top_padding + row_idx * (floor_height + card_gap) + (floor_height - rows * tile_size) // 2

            for r in floor:
                for node in r:
                    node.draw_with_offset(screen, x_off, y_off, elevator_img, stairs_img)

        pygame.display.flip() #SCREEN UPDATE

    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(COLORS["bg"])


        # --------------------------- SIDEBAR-------------------------------

        pygame.draw.rect(screen, COLORS["sidebar"], (0, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT))
        pygame.draw.line(screen, (40, 40, 50), (SIDEBAR_WIDTH, 0), (SIDEBAR_WIDTH, WINDOW_HEIGHT), 2)

        screen.blit(font.render("CONTROL PANEL", True, COLORS["text"]), (40, 40))

        # ------------------------- RENDER STATISTICS -------------------------
        y_pos = scale(450)

        # Section Header
        stats_header = font.render("ALGORITHM STATS", True, (150, 150, 150))
        screen.blit(stats_header, (40, y_pos - 30))

        # Display each metric from the stats dictionary
        for key, value in stats.items():
            if key == "found": continue

            # Format label: "Visited: 100", "Time: 45.5 ms"
            label_text = f"{key.capitalize()}: {value}"
            if key == "time": label_text += " ms"

            stat_surf = font.render(label_text, True, COLORS["accent"])
            screen.blit(stat_surf, (40, y_pos))
            y_pos += 35  # Space between lines
        # ---------------------------------------------------------------------

       # ------------------------  FLOOR CARDS---------------------------------------

        for i in range(num_floors):

            row = i // cards_per_row
            col = i % cards_per_row

            x = left_padding + col * (floor_width + card_gap)
            y = top_padding + row * (floor_height + card_gap)

            # shadow
            pygame.draw.rect(
                screen,
                COLORS["shadow"],
                (x + 5, y + 5, floor_width, floor_height),
                border_radius=14
            )

            # card
            pygame.draw.rect(
                screen,
                COLORS["card"],
                (x, y, floor_width, floor_height),
                border_radius=14
            )

            screen.blit(
                font.render(f"FLOOR {i + 1}", True, COLORS["accent"]),
                (x + 12, y + 12)
            )


        # ----------------------------- EVENTS ---------------------------

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in buttons:
                    if btn.is_clicked(mouse_pos):
                        if btn.tool_name == "CLEAR":
                            grid = make_grid(num_floors, rows, cols, tile_size, floor_width)
                        elif btn.tool_name == "RUN":
                            start_node = None
                            end_node = None

                            # FINDING NEIGHBOUR AND START END NODE
                            for f in grid:
                                for r in f:
                                    for n in r:
                                        n.update_neighbors(grid, num_floors, rows, cols)
                                        if n.color == TILE_START: start_node = n
                                        if n.color == TILE_END: end_node = n

                            if start_node and end_node:
                                #NEW NODE CHECK THEN CALL
                                found, v_count, p_cost, t_taken = algorithm(draw_sync, grid, start_node, end_node)
                                stats["visited"] = v_count
                                stats["cost"] = p_cost
                                stats["time"] = round(t_taken, 2)

                                if not found:
                                   #IF ROAD NOT FOUND
                                    msg_font = pygame.font.SysFont("Arial", 30, bold=True)
                                    error_txt = msg_font.render("NO PATH FOUND!", True, (255, 50, 50))

                                    # SHOW MESSAGE
                                    text_rect = error_txt.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                                    screen.blit(error_txt, text_rect)
                                    pygame.display.flip()

                                    pygame.time.delay(1000)
                        else:
                            current_tool = btn.tool_name

        #--------------------------------- GRID DRAW---------------------------------

        for f_idx, floor in enumerate(grid):

            row = f_idx // cards_per_row
            col = f_idx % cards_per_row

            x_offset = left_padding + col * (floor_width + card_gap) + (floor_width - cols * tile_size) // 2

            y_offset = top_padding + row * (floor_height + card_gap) + (floor_height - rows * tile_size) // 2

            for r in floor:
                for node in r:
                    node.draw_with_offset(screen, x_offset, y_offset, elevator_img, stairs_img)

                    if pygame.mouse.get_pressed()[0]:
                        if node.x_off <= mouse_pos[0] < node.x_off + tile_size and \
                           node.y_off <= mouse_pos[1] < node.y_off + tile_size:

                            if current_tool == "WALL":
                                if not node.is_elevators and not node.is_stairs:
                                    node.make_wall()

                            elif current_tool == "START":
                                for f in grid:
                                    for rr in f:
                                        for n in rr:
                                            if n.color == TILE_START:
                                                n.reset()
                                node.make_start()

                            elif current_tool == "END":
                                for f in grid:
                                    for rr in f:
                                        for n in rr:
                                            if n.color == TILE_END:
                                                n.reset()
                                node.make_end()

                    elif pygame.mouse.get_pressed()[2]:
                        if node.x_off <= mouse_pos[0] < node.x_off + tile_size and \
                           node.y_off <= mouse_pos[1] < node.y_off + tile_size:
                            node.reset()

        for btn in buttons:
            btn.draw(screen, current_tool)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
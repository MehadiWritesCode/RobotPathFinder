import pygame
from src.utils.constants import *

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, tool_name):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.tool_name = tool_name

    def draw (self, screen, current_tool):
        is_active = (current_tool == self.tool_name)

        draw_color = self.hover_color if is_active or self.rect.collidepoint(pygame.mouse.get_pos()) else self.color

        pygame.draw.rect(screen, draw_color, self.rect, border_radius=10)

        if is_active:
            pygame.draw.rect(screen, TILE_EMPTY, self.rect, 2, border_radius=10)  #WHITE BORDER

        font = pygame.font.SysFont('Segoe UI', 14, bold=True)
        text_surf = font.render(self.text, True, TILE_EMPTY)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
# ui.py
import pygame
from config import BUTTON_COLOR, BUTTON_HOVER, TEXT_COLOR, font_medium

class Button:
    def __init__(self, x, y, w, h, text, action=None, font=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action
        self.font = font or font_medium
        self.hovered = False

    def draw(self, surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2, border_radius=6)
        text_surf = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.action:
                self.action()
                return True
        return False

def draw_bar(surface, x, y, w, h, value, color, label):
    pygame.draw.rect(surface, (60, 60, 60), (x, y, w, h), border_radius=4)
    w_val = int(w * max(0, min(1, value / 100)))
    pygame.draw.rect(surface, color, (x, y, w_val, h), border_radius=4)
    pygame.draw.rect(surface, TEXT_COLOR, (x, y, w, h), 2, border_radius=4)
    text = font_medium.render(f"{label}: {int(value)}%", True, TEXT_COLOR)
    surface.blit(text, (x + 5, y + 2))
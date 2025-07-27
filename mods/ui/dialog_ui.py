# mods/ui/dialog_ui.py
import pygame
from config import font_small, font_medium, SCREEN_HEIGHT, SCREEN_WIDTH, TEXT_COLOR
from ui import Button

class Portrait:
    def __init__(self, name, image_color, text_color):
        self.name = name
        self.color = image_color
        self.text_color = text_color

# Примеры портретов
PORTRAITS = {
    "doctor": Portrait("Доктор", (100, 150, 200), (200, 230, 255)),
    "survivor": Portrait("Выживший", (80, 100, 60), (220, 220, 200)),
    "soldier": Portrait("Солдат", (50, 80, 100), (250, 200, 200)),
    "scientist": Portrait("Учёный", (120, 120, 180), (240, 240, 255)),
    "child": Portrait("Ребёнок", (200, 150, 100), (255, 230, 200))
}

def draw_dialog_box(surface, text, portrait_key="survivor"):
    """Рисует диалог с портретом слева"""
    box_rect = pygame.Rect(200, SCREEN_HEIGHT - 250, 1000, 200)
    pygame.draw.rect(surface, (20, 30, 50), box_rect)
    pygame.draw.rect(surface, (100, 130, 180), box_rect, 3)

    portrait = PORTRAITS.get(portrait_key, PORTRAITS["survivor"])
    pygame.draw.rect(surface, portrait.color, (220, SCREEN_HEIGHT - 230, 100, 100))
    pygame.draw.rect(surface, (200, 200, 255), (220, SCREEN_HEIGHT - 230, 100, 100), 2)
    name = font_medium.render(portrait.name, True, portrait.text_color)
    surface.blit(name, (220, SCREEN_HEIGHT - 240))

    lines = []
    words = text.split(' ')
    line = ""
    for word in words:
        test = line + word + " "
        if font_small.size(test)[0] <= 700:
            line = test
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    for i, line in enumerate(lines):
        text_surf = font_small.render(line.strip(), True, TEXT_COLOR)
        surface.blit(text_surf, (340, SCREEN_HEIGHT - 220 + i * 22))
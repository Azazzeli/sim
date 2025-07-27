# config.py
import pygame

# === Окно ===
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
PANEL_HEIGHT = 200
WORLD_SIZE = 700
FPS = 60

# === Цвета ===
BACKGROUND = (15, 25, 35)
PANEL_COLOR = (35, 50, 70)
TEXT_COLOR = (230, 230, 230)
ACCENT = (220, 100, 80)
SAFE = (80, 180, 120)
NEUTRAL = (100, 150, 200)
WARNING = (220, 160, 60)
RED = (220, 80, 60)
GREEN = (80, 180, 120)
BLUE = (60, 130, 220)
YELLOW = (220, 160, 60)
BROWN = (160, 120, 80)

BUTTON_COLOR = (70, 100, 140)
BUTTON_HOVER = (90, 130, 180)

# === Шрифты ===
pygame.font.init()
font_small = pygame.font.SysFont('Arial', 16)
font_medium = pygame.font.SysFont('Arial', 20)
font_large = pygame.font.SysFont('Arial', 24, bold=True)
font_title = pygame.font.SysFont('Arial', 36, bold=True)

# === Биомы ===
BIOME_COLORS = {
    "city": (100, 100, 100),
    "forest": (20, 90, 40),
    "desert": (210, 190, 110),
    "water": (50, 120, 200),
    "military": (30, 60, 30),
    "hospital": (200, 220, 255),
    "warehouse": (150, 130, 90),
}

# === Предметы ===
ITEMS = {
    "food": {"name": "Консервы", "heal": 20},
    "water": {"name": "Вода", "heal": 25},
    "bandage": {"name": "Бинт", "heal": 30},
    "pistol": {"name": "Пистолет", "ammo": 6},
    "medkit": {"name": "Аптечка", "heal": 70}
}
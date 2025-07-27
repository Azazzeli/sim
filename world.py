# world.py
import pygame
import random
from config import BIOME_COLORS

class WorldMap:
    def __init__(self, width=50, height=50):
        self.width = width
        self.height = height
        self.map_data = self.generate_world()
        self.player_pos = [width // 2, height // 2]

    def generate_world(self):
        world = [["forest" for _ in range(self.width)] for _ in range(self.height)]
        for _ in range(8):
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            self._grow_area(world, x, y, "city", 15)
        for _ in range(3):
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            world[y][x] = "hospital"
        for _ in range(2):
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            world[y][x] = "military"
        for _ in range(4):
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            world[y][x] = "warehouse"
        return world

    def _grow_area(self, world, x, y, biome, size):
        if size <= 0 or not (0 <= x < self.width and 0 <= y < self.height):
            return
        world[y][x] = biome
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            if random.random() > 0.4:
                self._grow_area(world, x+dx, y+dy, biome, size-1)

    def draw(self, surface, x, y, size):
        cell_size = size // self.width
        for row in range(self.height):
            for col in range(self.width):
                biome = self.map_data[row][col]
                color = BIOME_COLORS.get(biome, (100, 100, 100))
                pygame.draw.rect(surface, color, (x + col * cell_size, y + row * cell_size, cell_size, cell_size))
        px = x + self.player_pos[0] * cell_size + cell_size // 2
        py = y + self.player_pos[1] * cell_size + cell_size // 2
        pygame.draw.circle(surface, (255, 50, 50), (px, py), 6)
# game.py
import pygame
import random
from config import *
from player import Character
from world import WorldMap
from ui import Button, draw_bar
from mods import load_mods

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Зомби-Апокалипсис: Выживание")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "start"
        self.fullscreen = False

        # ✅ Добавляем размеры как атрибуты
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        self.player = None
        self.world = WorldMap()
        self.log = []
        self.show_inventory = False
        self.current_event = None
        self.event_choices = []
        self.mods = []

        # ✅ Таймеры для событий
        self.event_timer = 0
        self.global_event_timer = 0  # ← Эта строка была пропущена!

        self.create_buttons()
        self.mods = load_mods(self)

    def create_buttons(self):
        self.start_buttons = [
            Button(self.SCREEN_WIDTH // 2 - 100, self.SCREEN_HEIGHT // 2 + 20, 200, 50, "Начать", self.start_game),
            Button(self.SCREEN_WIDTH // 2 - 100, self.SCREEN_HEIGHT // 2 + 80, 200, 50, "Выход", self.quit)
        ]
        self.game_buttons = [
            Button(self.SCREEN_WIDTH - 210, self.SCREEN_HEIGHT - PANEL_HEIGHT + 20, 200, 40, "Съесть еду", self.eat),
            Button(self.SCREEN_WIDTH - 210, self.SCREEN_HEIGHT - PANEL_HEIGHT + 70, 200, 40, "Выпить воду", self.drink),
            Button(self.SCREEN_WIDTH - 210, self.SCREEN_HEIGHT - PANEL_HEIGHT + 120, 200, 40, "Лечиться", self.heal),
            Button(self.SCREEN_WIDTH - 210, self.SCREEN_HEIGHT - PANEL_HEIGHT + 170, 200, 40, "Поиск припасов", self.search),
            Button(self.SCREEN_WIDTH - 210, self.SCREEN_HEIGHT - PANEL_HEIGHT + 220, 200, 40, "Инвентарь", self.toggle_inventory),
            Button(self.SCREEN_WIDTH - 210, self.SCREEN_HEIGHT - PANEL_HEIGHT + 270, 200, 40, "Следующий день", self.next_day),
            Button(self.SCREEN_WIDTH - 210, self.SCREEN_HEIGHT - PANEL_HEIGHT + 320, 200, 40, "Редактировать UI", self.toggle_ui_mode)
        ]
        self.game_over_buttons = [
            Button(self.SCREEN_WIDTH // 2 - 100, self.SCREEN_HEIGHT // 2 + 20, 200, 50, "Новая игра", self.new_game),
            Button(self.SCREEN_WIDTH // 2 - 100, self.SCREEN_HEIGHT // 2 + 80, 200, 50, "Выход", self.quit)
        ]

        # ✅ UI элементы
        self.ui_elements = {
            "map": {"x": 20, "y": 20, "size": 700},
            "log": {"x": 750, "y": 20, "w": 630, "h": 180},
            "hud": {"x": 20, "y": self.SCREEN_HEIGHT - PANEL_HEIGHT, "w": self.SCREEN_WIDTH - 40, "h": PANEL_HEIGHT - 20},
            "buttons": {"x": self.SCREEN_WIDTH - 210, "y": self.SCREEN_HEIGHT - PANEL_HEIGHT + 20},
            "inventory": {"x": 750, "y": 220, "w": 450, "h": 300}
        }

        self.ui_mode = False
        self.dragging = None

    def toggle_ui_mode(self):
        self.ui_mode = not self.ui_mode
        self.log.append("🔧 Режим редактирования UI: " + ("ВКЛ" if self.ui_mode else "ВЫКЛ"))

    def start_game(self):
        self.player = Character()
        self.player.game = self
        self.state = "playing"
        self.log = ["Вы проснулись в разрушенном городе..."]

    def new_game(self):
        self.state = "start"
        self.log = []
        self.current_event = None
        self.event_choices = []

    def quit(self):
        self.running = False

    def toggle_inventory(self):
        if not self.current_event:
            self.show_inventory = not self.show_inventory

    def eat(self):
        if not self.current_event:
            msg = self.player.eat()
            self.log.append(msg)

    def drink(self):
        if not self.current_event:
            msg = self.player.drink()
            self.log.append(msg)

    def heal(self):
        if not self.current_event:
            msg = self.player.heal()
            self.log.append(msg)

    def search(self):
        if not self.current_event:
            msg = self.player.search_supplies()
            self.log.append(msg)

    def next_day(self):
        if not self.player.alive or self.current_event:
            return

        self.player.update()

        for mod in self.mods:
            if hasattr(mod, "on_next_day"):
                mod.on_next_day(self)

        self.world.player_pos[0] = (self.world.player_pos[0] + random.randint(-1, 1)) % self.world.width
        self.world.player_pos[1] = (self.world.player_pos[1] + random.randint(-1, 1)) % self.world.height

        if not self.player.alive:
            self.log.append(f"💀 ВЫ УМЕРЛИ! Вы продержались {self.player.days} дней.")
            self.state = "game_over"

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = pygame.display.get_surface().get_size()
                    else:
                        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
                    return

            if self.ui_mode and event.type == pygame.MOUSEBUTTONDOWN:
                for name, el in self.ui_elements.items():
                    if name == "map":
                        rect = pygame.Rect(el["x"], el["y"], el["size"], el["size"])
                    elif name == "buttons":
                        continue
                    else:
                        rect = pygame.Rect(el["x"], el["y"], el["w"], el["h"])
                    if rect.collidepoint(mouse_pos):
                        self.dragging = name
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = None

            elif event.type == pygame.MOUSEMOTION and self.dragging:
                dx, dy = event.rel
                el = self.ui_elements[self.dragging]
                el["x"] += dx
                el["y"] += dy

            if not self.ui_mode:
                if self.current_event:
                    for btn in self.event_choices:
                        btn.check_hover(mouse_pos)
                        if btn.handle_event(event):
                            return
                    return

                buttons = []
                if self.state == "start":
                    buttons = self.start_buttons
                elif self.state == "playing":
                    buttons = self.game_buttons
                elif self.state == "game_over":
                    buttons = self.game_over_buttons

                for btn in buttons:
                    btn.check_hover(mouse_pos)
                    btn.handle_event(event)

    def draw_start(self):
        title = font_title.render("ЗОМБИ-АПОКАЛИПСИС", True, ACCENT)
        self.screen.blit(title, (self.SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        lines = ["Вы проснулись после катастрофы.", "Города погибли. Люди — зомби."]
        for i, line in enumerate(lines):
            text = font_medium.render(line, True, TEXT_COLOR)
            self.screen.blit(text, (self.SCREEN_WIDTH // 2 - text.get_width() // 2, 180 + i * 40))
        for btn in self.start_buttons:
            btn.draw(self.screen)

    def draw_game(self):
        el = self.ui_elements["map"]
        self.world.draw(self.screen, el["x"], el["y"], el["size"])

        el = self.ui_elements["log"]
        pygame.draw.rect(self.screen, (30, 40, 60), (el["x"], el["y"], el["w"], el["h"]), border_radius=8)
        pygame.draw.rect(self.screen, TEXT_COLOR, (el["x"], el["y"], el["w"], el["h"]), 2, border_radius=8)
        log_title = font_medium.render("📜 Журнал событий", True, YELLOW)
        self.screen.blit(log_title, (el["x"] + 10, el["y"] + 5))
        for i, msg in enumerate(self.log[-8:]):
            text = font_small.render(f"• {msg}", True, TEXT_COLOR)
            self.screen.blit(text, (el["x"] + 15, el["y"] + 35 + i * 22))

        el = self.ui_elements["hud"]
        pygame.draw.rect(self.screen, PANEL_COLOR, (el["x"], el["y"], el["w"], el["h"]))
        pygame.draw.line(self.screen, TEXT_COLOR, (el["x"], el["y"]), (el["x"] + el["w"], el["y"]), 2)

        if self.player:
            info = [f"Имя: {self.player.name}", f"День: {self.player.days}", f"Инвентарь: {self.player.inventory.get_total()}/12"]
            for i, text in enumerate(info):
                surf = font_medium.render(text, True, TEXT_COLOR)
                self.screen.blit(surf, (el["x"] + 20, el["y"] + 15 + i * 25))

            draw_bar(self.screen, el["x"] + 20, el["y"] + 100, 200, 20, self.player.hunger, WARNING, "Голод")
            draw_bar(self.screen, el["x"] + 20, el["y"] + 130, 200, 20, self.player.thirst, BLUE, "Жажда")
            draw_bar(self.screen, el["x"] + 20, el["y"] + 160, 200, 20, self.player.health, SAFE, "Здоровье")

            if hasattr(self.player, 'fatigue'):
                fatigue_label = font_medium.render("Усталость", True, WARNING)
                self.screen.blit(fatigue_label, (el["x"] + 250, el["y"] + 100))
                pygame.draw.rect(self.screen, (50, 50, 50), (el["x"] + 250, el["y"] + 130, 200, 15))
                fill = int(200 * self.player.fatigue / 100)
                pygame.draw.rect(self.screen, WARNING, (el["x"] + 250, el["y"] + 130, fill, 15))
                pygame.draw.rect(self.screen, TEXT_COLOR, (el["x"] + 250, el["y"] + 130, 200, 15), 1)
                text = font_small.render(f"{int(self.player.fatigue)}%", True, TEXT_COLOR)
                self.screen.blit(text, (el["x"] + 255, el["y"] + 132))

        el = self.ui_elements["buttons"]
        for i, btn in enumerate(self.game_buttons):
            btn.rect.x = el["x"]
            btn.rect.y = el["y"] + i * 50
            btn.draw(self.screen)

        if self.show_inventory:
            el = self.ui_elements["inventory"]
            pygame.draw.rect(self.screen, (40, 60, 80), (el["x"], el["y"], el["w"], el["h"]), border_radius=10)
            pygame.draw.rect(self.screen, TEXT_COLOR, (el["x"], el["y"], el["w"], el["h"]), 2, border_radius=10)
            title = font_medium.render("🎒 Инвентарь", True, GREEN)
            self.screen.blit(title, (el["x"] + 10, el["y"] + 10))
            i = 0
            for item, count in self.player.inventory.items.items():
                if count > 0:
                    name = ITEMS[item]["name"]
                    text = font_small.render(f"• {name}: {count} шт.", True, TEXT_COLOR)
                    self.screen.blit(text, (el["x"] + 20, el["y"] + 50 + i * 25))
                    i += 1
            if i == 0:
                empty = font_small.render("Инвентарь пуст...", True, WARNING)
                self.screen.blit(empty, (el["x"] + 20, el["y"] + 50))

        if self.current_event:
            pygame.draw.rect(self.screen, (30, 40, 60), (400, 400, 600, 200))
            pygame.draw.rect(self.screen, TEXT_COLOR, (400, 400, 600, 200), 2)
            text = font_medium.render(self.current_event["text"], True, WARNING)
            self.screen.blit(text, (420, 420))
            for btn in self.event_choices:
                btn.draw(self.screen)

        credit = font_small.render("Выполнил: Azzazeli", True, (120, 120, 120))
        self.screen.blit(credit, (self.SCREEN_WIDTH - 200, self.SCREEN_HEIGHT - 30))

        if self.ui_mode:
            for name, el in self.ui_elements.items():
                if name == "map":
                    rect = pygame.Rect(el["x"], el["y"], el["size"], el["size"])
                elif name == "buttons":
                    continue
                else:
                    rect = pygame.Rect(el["x"], el["y"], el["w"], el["h"])
                pygame.draw.rect(self.screen, YELLOW, rect, 2)
                label = font_small.render(name, True, YELLOW)
                self.screen.blit(label, (el["x"] + 5, el["y"] + 5))

    def draw_inventory_window(self):
        x, y = 900, 200
        pygame.draw.rect(self.screen, (40, 60, 80), (x, y, 450, 300), border_radius=10)
        pygame.draw.rect(self.screen, TEXT_COLOR, (x, y, 450, 300), 2, border_radius=10)
        title = font_medium.render("🎒 Инвентарь", True, GREEN)
        self.screen.blit(title, (x + 10, y + 10))
        i = 0
        for item, count in self.player.inventory.items.items():
            if count > 0:
                name = ITEMS[item]["name"]
                text = font_small.render(f"• {name}: {count} шт.", True, TEXT_COLOR)
                self.screen.blit(text, (x + 20, y + 50 + i * 25))
                i += 1
        if i == 0:
            empty = font_small.render("Инвентарь пуст...", True, WARNING)
            self.screen.blit(empty, (x + 20, y + 50))

    def draw_game_over(self):
        title = font_title.render("💀 ВЫ УМЕРЛИ", True, RED)
        self.screen.blit(title, (self.SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        stats = [f"Вы продержались {self.player.days} дней"]
        for i, line in enumerate(stats):
            text = font_large.render(line, True, TEXT_COLOR)
            self.screen.blit(text, (self.SCREEN_WIDTH // 2 - text.get_width() // 2, 200 + i * 50))
        for btn in self.game_over_buttons:
            btn.draw(self.screen)

    def draw(self):
        self.screen.fill(BACKGROUND)
        if self.state == "start":
            self.draw_start()
        elif self.state == "playing":
            self.draw_game()
        elif self.state == "game_over":
            self.draw_game_over()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
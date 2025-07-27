# mods/mod_markers.py
import pygame
import random
from config import font_small, YELLOW, SCREEN_HEIGHT, SCREEN_WIDTH, WORLD_SIZE
from ui import Button

class Marker:
    def __init__(self, x, y, marker_type, name, description):
        self.x = x
        self.y = y
        self.type = marker_type
        self.name = name
        self.description = description
        self.reached = False

def init(game):
    game.markers = []
    game.target_marker = None
    game.days_to_target = 0

    for _ in range(3):
        x = random.randint(0, 49)
        y = random.randint(0, 49)
        marker_type = random.choice(["shelter", "radio", "quest", "danger"])
        game.markers.append(Marker(x, y, marker_type, f"Место {len(game.markers)+1}", "Неизвестно"))

    original_handle_events = game.handle_events

    def enhanced_handle_events():
        mouse_pos = pygame.mouse.get_pos()
        world_x, world_y = 20, 20
        cell_size = WORLD_SIZE // 50

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
                return

            if game.current_event:
                for btn in game.event_choices:
                    btn.check_hover(mouse_pos)
                    if btn.handle_event(event):
                        return
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if world_x <= mouse_pos[0] <= world_x + WORLD_SIZE and \
                   world_y <= mouse_pos[1] <= world_y + WORLD_SIZE:
                    grid_x = (mouse_pos[0] - world_x) // cell_size
                    grid_y = (mouse_pos[1] - world_y) // cell_size
                    for marker in game.markers:
                        if marker.x == grid_x and marker.y == grid_y and not marker.reached:
                            set_target_marker(game, marker)
                            return

            buttons = []
            if game.state == "start":
                buttons = game.start_buttons
            elif game.state == "playing":
                buttons = game.game_buttons
            elif game.state == "game_over":
                buttons = game.game_over_buttons

            for btn in buttons:
                btn.check_hover(mouse_pos)
                btn.handle_event(event)

    game.handle_events = enhanced_handle_events

    original_draw_game = game.draw_game

    def enhanced_draw_game():
        original_draw_game()
        draw_markers(game, game.screen)

    game.draw_game = enhanced_draw_game

def set_target_marker(game, marker):
    game.target_marker = marker
    dx = abs(game.world.player_pos[0] - marker.x)
    dy = abs(game.world.player_pos[1] - marker.y)
    game.days_to_target = max(dx, dy)
    game.log.append(f"🎯 Направляемся к '{marker.name}' — {game.days_to_target} дней пути")

def draw_markers(game, screen):
    world_x, world_y = 20, 20
    cell_size = WORLD_SIZE // 50

    for marker in game.markers:
        if marker.reached:
            pygame.draw.circle(screen, (0, 255, 0), (world_x + marker.x * cell_size + cell_size//2, 
                                                    world_y + marker.y * cell_size + cell_size//2), 6)
            continue
        px = world_x + marker.x * cell_size + cell_size // 2
        py = world_y + marker.y * cell_size + cell_size // 2

        if marker.type == "shelter":
            pygame.draw.polygon(screen, (150, 75, 0), [(px-6, py+6), (px, py-6), (px+6, py+6)])
            pygame.draw.rect(screen, (100, 100, 200), (px-5, py, 10, 6))
        elif marker.type == "radio":
            pygame.draw.line(screen, (200, 200, 200), (px, py-6), (px, py+6), 2)
            pygame.draw.circle(screen, (255, 200, 0), (px, py-8), 3)
        elif marker.type == "quest":
            text = font_small.render("?", True, (255, 255, 0))
            screen.blit(text, (px-3, py-6))
        elif marker.type == "danger":
            pygame.draw.polygon(screen, (255, 0, 0), [(px, py-6), (px+6, py+6), (px-6, py+6)])

        mouse_pos = pygame.mouse.get_pos()
        if abs(mouse_pos[0] - px) < 20 and abs(mouse_pos[1] - py) < 20:
            tooltip = font_small.render(marker.name, True, YELLOW)
            screen.blit(tooltip, (px + 10, py - 10))

def on_next_day(game):
    if not game.target_marker or game.days_to_target <= 0:
        return

    game.days_to_target -= 1

    px, py = game.world.player_pos
    tx, ty = game.target_marker.x, game.target_marker.y
    dx = tx - px
    dy = ty - py
    move_x = 1 if dx > 0 else -1 if dx < 0 else 0
    move_y = 1 if dy > 0 else -1 if dy < 0 else 0

    if random.random() < 0.5:
        game.world.player_pos[0] += move_x
        game.world.player_pos[1] += move_y
    else:
        game.world.player_pos[1] += move_y
        game.world.player_pos[0] += move_x

    game.world.player_pos[0] %= game.world.width
    game.world.player_pos[1] %= game.world.height

    if game.days_to_target > 0:
        game.log.append(f"🚶‍♂️ В пути к '{game.target_marker.name}' — осталось {game.days_to_target} дней")
    else:
        game.target_marker.reached = True
        game.log.append(f"🎉 Вы достигли: {game.target_marker.name}!")

        if game.target_marker.type == "shelter":
            game.player.in_shelter = True
            game.log.append("🏠 Теперь вы в укрытии.")
        elif game.target_marker.type == "quest":
            game.player.inventory.add_item("food", 2)
            game.player.inventory.add_item("water", 2)
            game.log.append("🎁 Квест завершён! Получено: 2 еды и 2 воды")
        elif game.target_marker.type == "radio":
            game.log.append("📻 Вы нашли радиостанцию!")

        game.target_marker = None
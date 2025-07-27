# mods/mod_passive_recovery.py
import pygame
import random
from config import font_small, WARNING, TEXT_COLOR, SCREEN_HEIGHT, SCREEN_WIDTH, PANEL_HEIGHT

def init(game):
    if game.player and not hasattr(game.player, 'fatigue'):
        game.player.fatigue = 0

    original_draw_game = game.draw_game

    def enhanced_draw_game():
        original_draw_game()
        draw_fatigue_bar(game, game.screen)

    game.draw_game = enhanced_draw_game

def on_next_day(game):
    if not game.player.alive:
        return

    in_shelter = getattr(game.player, 'in_shelter', False)

    game.player.fatigue += random.randint(10, 15) if not in_shelter else 5
    game.player.fatigue = max(0, min(100, game.player.fatigue))

    if game.player.fatigue >= 90:
        game.player.health -= random.randint(3, 6)
    elif game.player.fatigue >= 70:
        game.player.health -= random.randint(1, 2)

def draw_fatigue_bar(game, screen):
    if not hasattr(game.player, 'fatigue'):
        return

    x, y = 250, SCREEN_HEIGHT - PANEL_HEIGHT + 150
    width, height = 200, 15

    fatigue_label = font_small.render("Усталость", True, WARNING)
    screen.blit(fatigue_label, (x, y - 18))

    pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))
    fill_width = int(width * game.player.fatigue / 100)
    pygame.draw.rect(screen, WARNING, (x, y, fill_width, height))
    pygame.draw.rect(screen, TEXT_COLOR, (x, y, width, height), 1)

    text = font_small.render(f"{int(game.player.fatigue)}%", True, TEXT_COLOR)
    screen.blit(text, (x + 5, y + 1))
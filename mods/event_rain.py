# mods/event_rain.py
import random

def on_next_day(game):
    if random.random() < 0.2:  # 20% шанс дождя
        game.log.append("🌧️ Пошёл дождь! Вы собрали дождевую воду.")
        success, _ = game.player.inventory.add_item("water", 1)
        if not success:
            game.log.append("Инвентарь полон!")

def init(game):
    # Регистрируем обработчик
    if not hasattr(game, 'event_handlers'):
        game.event_handlers = []
    game.event_handlers.append(on_next_day)
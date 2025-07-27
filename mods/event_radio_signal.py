# mods/event_radio_signal.py
import random
from ui import Button

def on_next_day(game):
    if random.random() < 0.1:
        game.radio_signal = (random.randint(0, 50), random.randint(0, 50))
        game.log.append("📻 Вы слышите сигнал: 'Помогите...' На карте появилась метка.")
        game.current_event = None
        game.event_choices = [
            Button(500, 500, 400, 40, "Идти на сигнал", lambda: go_to_signal(game)),
            Button(500, 550, 400, 40, "Игнорировать", lambda: ignore_signal(game))
        ]
        game.log.append("📻 Вы слышите сигнал в рации...")

def go_to_signal(game):
    if random.random() < 0.7:
        game.log.append("Вы нашли заброшенный склад. Припасы спасут вас!")
        game.player.inventory.add_item("food", 3)
        game.player.inventory.add_item("water", 3)
        game.player.inventory.add_item("medkit", 1)
    else:
        game.log.append("Это была ловушка! Зомби ждали вас.")
        game.player.health -= random.randint(20, 40)
    game.current_event = None
    game.event_choices = []

def ignore_signal(game):
    game.log.append("Вы решили не рисковать. Рация умолкла навсегда.")
    game.current_event = None
    game.event_choices = []
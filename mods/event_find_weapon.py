# mods/event_find_weapon.py
import random
from ui import Button

def find_weapon_event(game):
    if game.player.has_weapon or random.random() > 0.15:
        return
    weapons = ["нож", "пистолет", "дробовик", "труба"]
    weapon = random.choice(weapons)
    game.current_event = {"text": f"Вы нашли {weapon} в разбитом полицейском фургоне. Взять?"}
    game.event_choices = [
        Button(500, 500, 400, 40, "Взять", lambda: take_weapon(game, weapon)),
        Button(500, 550, 400, 40, "Оставить", lambda: leave_weapon(game))
    ]
    game.log.append(f"❗ Найдено оружие: {weapon}")

def take_weapon(game, weapon):
    game.player.has_weapon = True
    game.player.weapon_name = weapon
    game.log.append(f"Вы взяли {weapon}. Теперь можете защищаться.")
    game.current_event = None
    game.event_choices = []

def leave_weapon(game):
    game.log.append("Вы оставили оружие. Может, так безопаснее...")
    game.current_event = None
    game.event_choices = []

def on_next_day(game):
    find_weapon_event(game)
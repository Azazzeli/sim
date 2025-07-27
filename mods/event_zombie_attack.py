# mods/event_zombie_attack.py
import random
from ui import Button

def zombie_attack_event(game):
    game.current_event = {"text": "Зомби напали! У вас есть оружие?"}
    choices = []
    if game.player.has_weapon:
        choices.append(Button(500, 500, 400, 40, f"Атаковать ({game.player.weapon_name})", lambda: fight(game)))
    choices.append(Button(500, 550, 400, 40, "Убежать", lambda: escape(game)))
    choices.append(Button(500, 600, 400, 40, "Спрятаться", lambda: hide(game)))
    game.event_choices = choices
    game.log.append("🧟‍♂️ Нападение зомби!")

def fight(game):
    if random.random() < 0.7:
        game.log.append(f"Вы отбились с помощью {game.player.weapon_name}!")
        if random.random() < 0.3:
            game.log.append("Оружие сломалось...")
            game.player.has_weapon = False
            game.player.weapon_name = "нет"
    else:
        game.log.append("Вы ранены в бою!")
        game.player.health -= random.randint(20, 35)
    game.current_event = None
    game.event_choices = []

def escape(game):
    if random.random() < 0.6:
        game.log.append("Вы убежали, но потеряли припасы!")
        item = random.choice(["food", "water"])
        if game.player.inventory.items[item] > 0:
            game.player.inventory.use_item(item)
    else:
        game.log.append("Не успели убежать! Получили ранение.")
        game.player.health -= random.randint(15, 25)
    game.current_event = None
    game.event_choices = []

def hide(game):
    if random.random() < 0.8:
        game.log.append("Вы успешно спрятались.")
    else:
        game.log.append("Зомби нашли вас! Пришлось драться.")
        game.player.health -= random.randint(10, 20)
    game.current_event = None
    game.event_choices = []

def on_next_day(game):
    if random.random() < 0.2:
        zombie_attack_event(game)
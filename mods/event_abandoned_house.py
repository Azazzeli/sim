# mods/event_abandoned_house.py
import random
from ui import Button

def on_next_day(game):
    if random.random() < 0.2 and not game.current_event and game.player.alive:
        game.current_event = {
            "text": "Вы нашли заброшенный дом. Можно переночевать, но что внутри?"
        }
        game.event_choices = [
            Button(500, 500, 400, 40, "Переночевать", lambda: spend_night(game)),
            Button(500, 550, 400, 40, "Пройти мимо", lambda: ignore_house(game))
        ]
        game.log.append("🏚️ Вы нашли заброшенный дом...")

def spend_night(game):
    player = game.player
    if random.random() < 0.6:
        game.log.append("Ночь прошла спокойно. Вы отдохнули.")
        player.health = min(100, player.health + 20)
        player.hunger += 5
        player.thirst += 5
    else:
        game.log.append("Ночью напали зомби! Вы еле выбрались.")
        player.health -= random.randint(25, 40)
        if random.random() < 0.5:
            found = random.choice(["food", "water", "bandage"])
            player.inventory.add_item(found, 1)
            game.log.append(f"В суматохе вы схватили: {found}.")
    game.current_event = None
    game.event_choices = []
def spend_night(game):
    game.log.append("Вы переночевали в доме. Теперь это ваше укрытие.")
    game.player.in_shelter = True
    game.player.health = min(100, game.player.health + 10)

def ignore_house(game):
    game.log.append("Вы прошли мимо. Кто знает, что было внутри...")
    game.current_event = None
    game.event_choices = []
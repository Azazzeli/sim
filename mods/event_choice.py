# mods/event_rescue_survivor.py
import random
from ui import Button
from config import ITEMS

def generate_survivor_event():
    """Генерирует случайного выжившего с уникальным поведением"""
    types = [
        {
            "type": "good",
            "text": "Вы видите раненого выжившего. Он просит помощи.",
            "options": [
                {"text": "Помочь", "effect": "help_good"},
                {"text": "Игнорировать", "effect": "ignore"}
            ],
            "chance": 0.4
        },
        {
            "type": "sick",
            "text": "Человек кашляет и выглядит больным. Просит воды.",
            "options": [
                {"text": "Помочь", "effect": "help_sick"},
                {"text": "Отойти", "effect": "ignore"}
            ],
            "chance": 0.25
        },
        {
            "type": "trader",
            "text": "Выживший предлагает обмен: припасы на оружие.",
            "options": [
                {"text": "Обменяться", "effect": "trade"},
                {"text": "Отказаться", "effect": "ignore"}
            ],
            "chance": 0.2
        },
        {
            "type": "trickster",
            "text": "Человек плачет, но в руке что-то блестит...",
            "options": [
                {"text": "Подойти", "effect": "trick"},
                {"text": "Насторожиться", "effect": "ignore"}
            ],
            "chance": 0.15
        }
    ]
    return random.choices(types, weights=[t["chance"] for t in types])[0]

def on_next_day(game):
    # 25% шанс встретить выжившего
    if random.random() < 0.25 and not game.current_event and game.player.alive:
        survivor = generate_survivor_event()
        game.current_event = survivor
        game.event_choices = [
            Button(
                500, 500 + i * 50, 400, 40,
                choice["text"],
                lambda chosen_choice=choice: resolve_choice(chosen_choice, game)
            )
            for i, choice in enumerate(survivor["options"])
        ]
        game.log.append(f"❗ {survivor['text']}")

def resolve_choice(choice, game):
    effect = choice["effect"]
    player = game.player

    if effect == "help_good":
        success, msg = player.inventory.add_item("food", random.randint(1, 2))
        player.health = min(100, player.health + 10)
        game.log.append("Вы спасли выжившего. Он отдал вам припасы и ушёл.")
        if not success:
            game.log.append("Некуда класть! Припасы потеряны.")

    elif effect == "help_sick":
        if random.random() < 0.6:
            player.health -= random.randint(15, 25)
            game.log.append("Вы заразились! Он был болен.")
        else:
            game.log.append("Он умер у вас на руках... Но перед смертью дал ключ от склада.")
            player.inventory.add_item("food", 1)
            player.inventory.add_item("water", 1)

    elif effect == "trade":
        if player.inventory.items.get("pistol", 0) > 0:
            game.log.append("Вы отдали пистолет. Получили сумку с припасами.")
            player.inventory.use_item("pistol")
            player.inventory.add_item("food", 3)
            player.inventory.add_item("water", 2)
        elif player.inventory.items.get("ammo", 0) >= 3:
            game.log.append("Вы отдали патроны. Получили воду и бинты.")
            for _ in range(3):
                player.inventory.use_item("ammo")
            player.inventory.add_item("water", 2)
            player.inventory.add_item("bandage", 2)
        else:
            game.log.append("Нечем торговать. Он ушёл.")

    elif effect == "trick":
        if random.random() < 0.7:
            game.log.append("Это была ловушка! Вас ограбили!")
            stolen = random.choice(["food", "water", "medkit"])
            if player.inventory.items.get(stolen, 0) > 0:
                player.inventory.use_item(stolen)
                game.log.append(f"Украдена {ITEMS[stolen]['name']}!")
        else:
            game.log.append("Вы вовремя заметили нож. Нападавший сбежал.")
            player.health -= random.randint(5, 10)
            game.log.append("Вы получили лёгкое ранение.")

    elif effect == "ignore":
        reactions = [
            "Он молча кивнул и скрылся в тумане.",
            "Кричал вслед, но вы не остановились.",
            "Бросил в вас пустую банку и ушёл.",
            "Прошептал 'спасибо' и исчез."
        ]
        game.log.append(f"Вы прошли мимо. {random.choice(reactions)}")

    # Завершаем событие
    game.current_event = None
    game.event_choices = []
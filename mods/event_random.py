# mods/event_random.py
import random

def on_next_day(game):
    game.event_timer += 1
    if game.event_timer >= 3:
        game.event_timer = 0
        if random.random() > 0.3:
            event_type = "positive" if random.random() > 0.4 else "negative"
            events = {
                "positive": [
                    "Нашли припасы в разбитой машине",
                    "Дождь! Собрали чистую воду",
                    "Нашли аптечку в заброшенном доме",
                    "Спасли кошку. Стало легче на душе",
                    "Нашли карту с отметками убежищ"
                ],
                "negative": [
                    "Напали крысы!",
                    "Заблудились в лесу",
                    "Сломали ногу",
                    "Потеряли часть припасов",
                    "Заболели"
                ]
            }
            msg = random.choice(events[event_type])
            game.log.append(f"Событие: {msg}")
            if event_type == "negative":
                game.player.health -= random.randint(10, 20)
            elif event_type == "positive":
                item = random.choice(["food", "water", "bandage"])
                success, _ = game.player.inventory.add_item(item, 1)
                if not success:
                    game.log.append("Инвентарь полон!")
# mods/quest_random_npc.py
import random
from ui import Button

class Quest:
    def __init__(self, title, desc, goal, reward_text, reward_items):
        self.title = title
        self.desc = desc
        self.goal = goal  # например, "find_daughter", "bring_meds"
        self.reward_text = reward_text
        self.reward_items = reward_items
        self.completed = False

def generate_quest():
    quests = [
        Quest(
            "Найдите мою дочь",
            "Моя дочь пропала у старого моста. Пожалуйста, найдите её.",
            "find_daughter",
            "Спасибо! Вот, возьмите мой пистолет — он вам пригодится.",
            {"pistol": 1}
        ),
        Quest(
            "Принесите лекарство",
            "Мой сын болен. Нужны антибиотики. Их видели в больнице.",
            "bring_meds",
            "Вы спасли его! Вот припасы, которые я смог собрать.",
            {"medkit": 2, "food": 3, "water": 3}
        ),
        Quest(
            "Уничтожьте гнездо",
            "В канализации под школой роятся зомби. Очистите это место.",
            "clear_nest",
            "Вы сделали мир безопаснее. Примите благодарность.",
            {"ammo": 6, "bandage": 2, "food": 2}
        )
    ]
    return random.choice(quests)

def on_next_day(game):
    if hasattr(game, 'active_quest') and game.active_quest and not game.active_quest.completed:
        return  # Уже есть квест

    if random.random() < 0.15 and not game.current_event and game.player.alive:
        quest = generate_quest()
        game.current_event = {
            "text": f"Выживший просит о помощи: '{quest.desc}'"
        }
        game.event_choices = [
            Button(500, 500, 400, 40, "Принять", lambda: accept_quest(game, quest)),
            Button(500, 550, 400, 40, "Отказаться", lambda: decline_quest(game))
        ]
        game.log.append(f"❗ Новый квест: {quest.title}")

def accept_quest(game, quest):
    game.active_quest = quest
    game.log.append(f"Квест принят: {quest.title}")
    game.current_event = None
    game.event_choices = []

def decline_quest(game):
    game.log.append("Вы отказались. Выживший грустно кивнул.")
    game.current_event = None
    game.event_choices = []

def check_quest_completion(game):
    if not hasattr(game, 'active_quest') or not game.active_quest:
        return

    quest = game.active_quest
    if quest.completed:
        return

    # Проверяем выполнение (упрощённо)
    if quest.goal == "find_daughter" and random.random() < 0.3:
        complete_quest(game, quest)
    elif quest.goal == "bring_meds" and game.player.inventory.items.get("medkit", 0) > 0:
        game.player.inventory.use_item("medkit")
        complete_quest(game, quest)
    elif quest.goal == "clear_nest" and random.random() < 0.2:
        complete_quest(game, quest)

def complete_quest(game, quest):
    quest.completed = True
    game.log.append(f"✅ Квест завершён: {quest.title}")
    game.log.append(quest.reward_text)
    for item, count in quest.reward_items.items():
        game.player.inventory.add_item(item, count)
    game.active_quest = None
    if hasattr(game, 'reputation'):
        game.reputation = min(100, game.reputation + 15)
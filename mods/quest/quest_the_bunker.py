# mods/quests/quest_the_bunker.py
import random
from ui import Button

class BunkerQuest:
    def __init__(self):
        self.name = "Убежище"
        self.state = "start"
        self.faction = random.choice(["military", "survivors", "scientists"])
        self.moral = 0  # -10 (тиран), +10 (герой)

    def init(self, game):
        msg = {
            "military": "Вы нашли убежище военных. Они предлагают присоединиться.",
            "survivors": "Группа выживших просит пустить их в ваше укрытие.",
            "scientists": "Учёные ищут защиту. У них есть важные данные."
        }[self.faction]
        game.log.append(f"🚨 {msg}")

        game.current_event = {"text": "Принять решение?"}
        game.event_choices = [
            Button(500, 500, 400, 40, "Помочь", lambda: self.help(game)),
            Button(500, 550, 400, 40, "Отказать", lambda: self.refuse(game)),
            Button(500, 600, 400, 40, "Захватить", lambda: self.attack(game))
        ]
        game.active_quest = self

    def help(self, game):
        if self.faction == "military":
            game.log.append("Вы присоединились. Теперь вы командир отряда.")
            game.player.inventory.add_item("pistol", 1)
            game.player.inventory.add_item("ammo", 6)
            if hasattr(game, 'reputation'):
                game.reputation += 15
        elif self.faction == "survivors":
            game.log.append("Вы приняли их. Теперь вы лидер общины.")
            game.player.inventory.add_item("food", 5)
            game.player.inventory.add_item("water", 5)
            game.reputation += 25
        elif self.faction == "scientists":
            game.log.append("Они дали вам доступ к базе данных.")
            game.player.inventory.add_item("medkit", 2)
            game.player.inventory.add_item("food", 3)
            game.reputation += 20

        self.finish(game, "help")

    def refuse(self, game):
        game.log.append("Вы отказали. Они ушли.")
        if self.faction == "military":
            game.log.append("Ночью вы слышали выстрелы... Они ушли.")
        elif self.faction == "survivors":
            game.log.append("Один из них сказал: 'Мы запомним твоё лицо.'")
            game.reputation -= 10
        self.finish(game, "refuse")

    def attack(self, game):
        if random.random() < 0.6:
            game.log.append("Вы захватили убежище! Припасы ваши.")
            game.player.inventory.add_item("food", 8)
            game.player.inventory.add_item("water", 6)
            game.player.inventory.add_item("medkit", 2)
            if hasattr(game, 'reputation'):
                game.reputation -= 20
            game.log.append("⚠️ Но вы стали тираном...")
        else:
            game.log.append("Они оказались сильнее. Вы ранены и бежали.")
            game.player.health -= 40
        self.finish(game, "attack")

    def finish(self, game, choice):
        game.active_quest = None
        game.log.append("✅ Квест завершён: Убежище")

quest = BunkerQuest()

def init(game):
    if random.random() < 0.1:
        quest.init(game)

def on_next_day(game):
    pass  # Квест мгновенный
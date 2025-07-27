# mods/quests/quest_the_radio.py
import random
from ui import Button

class RadioQuest:
    def __init__(self):
        self.name = "Голос из прошлого"
        self.state = "signal"
        self.day = 0
        self.choices = []

    def init(self, game):
        game.log.append("📻 Вы ловите сигнал: '...если кто слышит... я в бункере под школой... 3 дня...'")

        game.current_event = {"text": "Идти на сигнал?"}
        game.event_choices = [
            Button(500, 500, 400, 40, "Идти", lambda: self.go(game)),
            Button(500, 550, 400, 40, "Игнорировать", lambda: self.ignore(game))
        ]
        game.active_quest = self

    def go(self, game):
        game.log.append("Вы идёте к школе. Дверь в подвал приоткрыта...")
        self.state = "explore"
        game.current_event = {"text": "Что делать?"}
        game.event_choices = [
            Button(500, 500, 400, 40, "Войти осторожно", lambda: self.enter_careful(game)),
            Button(500, 550, 400, 40, "Ворваться", lambda: self.enter_rush(game)),
            Button(500, 600, 400, 40, "Постучать", lambda: self.knock(game))
        ]

    def ignore(self, game):
        game.log.append("Вы прошли мимо. Рация умолкла.")
        self.finish(game, "ignore")

    def enter_careful(self, game):
        game.log.append("Вы видите женщину. Она в ужасе. 'Ты... не зомби?'")
        self.meet(game, "careful")

    def enter_rush(self, game):
        game.player.health -= 15
        game.log.append("Засада! Вы получили ранение, но отбились.")
        self.meet(game, "rush")

    def knock(self, game):
        game.log.append("Она открывает. 'Спасибо, что пришёл...'")

    def meet(self, game, style):
        game.current_event = {"text": "Она просит: 'Помоги мне выбраться. Я знаю, где база CDC.'"}
        game.event_choices = [
            Button(500, 500, 400, 40, "Помочь", lambda: self.help(game, style)),
            Button(500, 550, 400, 40, "Забрать карту", lambda: self.take_map(game, style)),
            Button(500, 600, 400, 40, "Оставить", lambda: self.leave(game, style))
        ]

    def help(self, game, style):
        game.log.append("Вы спасли её. Она открыла базу CDC.")
        game.player.inventory.add_item("medkit", 3)
        game.player.inventory.add_item("ammo", 6)
        if hasattr(game, 'reputation'):
            game.reputation += 30
        game.log.append("🌍 Теперь вы можете находить убежища легче.")
        self.finish(game, "help")

    def take_map(self, game, style):
        game.log.append("Вы забрали карту. Она закричала...")
        game.player.inventory.add_item("medkit", 5)
        if hasattr(game, 'reputation'):
            game.reputation -= 25
        game.log.append("⚠️ Но теперь вы не доверяете никому...")
        self.finish(game, "betray")

    def leave(self, game, style):
        game.log.append("Вы ушли. Она кричала вслед...")
        if hasattr(game, 'reputation'):
            game.reputation -= 10
        self.finish(game, "coward")

    def finish(self, game, result):
        game.active_quest = None
        game.log.append("✅ Квест завершён: Голос из прошлого")

quest = RadioQuest()

def init(game):
    if random.random() < 0.12:
        quest.init(game)

def on_next_day(game):
    pass
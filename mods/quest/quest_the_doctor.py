# mods/quests/quest_the_doctor.py
import random
from ui import Button

class DoctorQuest:
    def __init__(self):
        self.name = "Пропавший доктор"
        self.state = "start"  # start, finding, found, finished
        self.dialogue_step = 0
        self.trust = 0  # -10 (враги) ... 10 (союзники)

    def init(self, game):
        game.log.append("🧓 Пожилая женщина подходит к вам: 'Мой муж, доктор, пропал у больницы. Пожалуйста, найдите его...'")

        game.current_event = {
            "text": "Доктор пропал у разрушенной больницы. Помочь?"
        }
        game.event_choices = [
            Button(500, 500, 400, 40, "Помочь", lambda: self.accept(game)),
            Button(500, 550, 400, 40, "Отказаться", lambda: self.decline(game))
        ]

    def accept(self, game):
        game.log.append("Вы приняли квест: найти доктора.")
        game.active_quest = self
        self.state = "finding"
        game.current_event = None
        game.event_choices = []

    def decline(self, game):
        game.log.append("Вы отказались. Женщина заплакала и ушла.")
        game.current_event = None
        game.event_choices = []

    def update(self, game):
        if self.state == "finding" and random.random() < 0.4:
            self.enter_hospital(game)

    def enter_hospital(self, game):
        game.log.append("Вы вошли в больницу. Темно. Слышны шаги...")
        game.current_event = {
            "text": "В кабинете вы видите человека в халате. Он дрожит. 'Ты... не зомби?'"
        }
        game.event_choices = [
            Button(500, 500, 400, 40, "Сказать правду", lambda: self.tell_truth(game)),
            Button(500, 550, 400, 40, "Назваться солдатом", lambda: self.lie(game))
        ]
        self.state = "found"

    def tell_truth(self, game):
        game.log.append("Доктор кивает: 'Я собирал образцы вируса. Если хочешь — помоги мне.'")
        self.trust += 2
        self.offer_research(game)

    def lie(self, game):
        game.log.append("Он неуверенно: 'Если ты солдат... у меня есть данные, которые нужны армии.'")
        self.trust -= 1
        self.offer_research(game)

    def offer_research(self, game):
        game.current_event = {
            "text": "Он предлагает: 'У меня есть вакцина. Но нужно проверить. Поможешь?'"
        }
        game.event_choices = [
            Button(500, 500, 400, 40, "Помочь в исследовании", lambda: self.help_research(game)),
            Button(500, 550, 400, 40, "Забрать вакцину", lambda: self.steal_vaccine(game)),
            Button(500, 600, 400, 40, "Уйти", lambda: self.leave(game))
        ]

    def help_research(self, game):
        game.log.append("Вы помогли. Доктор создал стабильную вакцину.")
        game.player.inventory.add_item("medkit", 3)
        game.player.health = 100
        if hasattr(game, 'reputation'):
            game.reputation += 20
        game.log.append("🌍 НОВОСТЬ: Вакцина распространяется. Смертность падает.")
        self.finish(game)

    def steal_vaccine(self, game):
        game.log.append("Вы забрали вакцину. Доктор кричит: 'Ты обрекаешь мир на гибель!'")
        game.player.inventory.add_item("medkit", 5)
        if hasattr(game, 'reputation'):
            game.reputation -= 30
        game.log.append("⚠️ Радио: 'Вакцина украдена. Апокалипсис продолжается.'")
        self.finish(game)

    def leave(self, game):
        game.log.append("Вы ушли. Доктор остался один...")
        if hasattr(game, 'reputation'):
            game.reputation -= 5
        self.finish(game)

    def finish(self, game):
        self.state = "finished"
        game.active_quest = None
        game.log.append("✅ Квест завершён: Пропавший доктор")

# --- Глобальная инициализация ---
quest = DoctorQuest()

def init(game):
    if random.random() < 0.15:
        quest.init(game)

def on_next_day(game):
    if hasattr(game, 'active_quest') and game.active_quest == quest:
        quest.update(game)
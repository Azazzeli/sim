# mods/system_reputation.py
import random
from ui import Button

# Уровни репутации
REPUTATION_LEVELS = ["Незнакомец", "Доверяют", "Свой", "Легенда"]

def init(game):
    game.reputation = 0  # -100 (враги) ... 100 (герой)

def on_next_day(game):
    # Шанс встретить выжившего, реагирующего на репутацию
    if random.random() < 0.2 and game.reputation > 20 and not game.current_event:
        reactions = {
            20: "Выживший узнал вас: 'Это же герой из сектора 7!'",
            50: "Вас встречают с уважением. Вам дают припасы.",
            80: "Вас приглашают в убежище. Вам доверяют."
        }
        for threshold, text in sorted(reactions.items(), reverse=True):
            if game.reputation >= threshold:
                game.log.append(text)
                if game.reputation >= 50:
                    game.player.inventory.add_item("food", 2)
                    game.player.inventory.add_item("water", 2)
                break

def help_survivor(game):
    game.reputation = min(100, game.reputation + 10)
    game.log.append("Вы помогли выжившему. Ваша репутация растёт.")

def ignore_survivor(game):
    if game.reputation > 0:
        game.reputation = max(-100, game.reputation - 5)
    game.log.append("Вы прошли мимо. Кто-то наблюдал за вами...")

# Расширяем другие модули
def extend_rescue_event(game):
    """Эту функцию можно вызвать в других модулях"""
    pass
# mods/mod_radio_signals.py
import random


def on_next_day(game):
    if random.random() < 0.1:
        game.radio_signal = (random.randint(0, 50), random.randint(0, 50))
        game.log.append("📻 Вы слышите сигнал: 'Помогите...' На карте появилась метка.")
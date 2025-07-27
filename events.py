# events.py
import random

def trigger_choice_event():
    events = [
        {
            "text": "Вы видите раненого выжившего. Он просит помощи.",
            "choices": [
                {"text": "Помочь (потратить бинт)", "effect": "help_injured"},
                {"text": "Пройти мимо", "effect": "ignore"}
            ]
        },
        {
            "text": "Нашли полуистлевшие консервы. Выглядят подозрительно.",
            "choices": [
                {"text": "Съесть (риск отравления)", "effect": "eat_rotten_food"},
                {"text": "Выбросить", "effect": "discard"}
            ]
        },
        {
            "text": "Слышите крик вдалеке. Кто-то в беде.",
            "choices": [
                {"text": "Пойти на помощь", "effect": "investigate_cry"},
                {"text": "Спрятаться", "effect": "hide"}
            ]
        }
    ]
    return random.choice(events)
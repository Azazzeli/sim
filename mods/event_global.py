# mods/event_global.py
import random

def on_next_day(game):
    game.global_event_timer += 1
    if game.global_event_timer >= 10:
        game.global_event_timer = 0
        if random.random() > 0.5:
            events = [
                "☢️ Радиационный шторм!",
                "🌪️ Ураган прошёл по региону",
                "🔥 Лесные пожары в соседних районах",
                "🧟‍♂️ Волна зомби движется с севера",
                "📡 Радиосигналы снова работают"
            ]
            msg = random.choice(events)
            game.log.append(f"🌍 {msg}")
            game.player.health -= random.randint(10, 15)
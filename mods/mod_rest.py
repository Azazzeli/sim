# mods/mod_rest.py
def on_next_day(game):
    game.player.sleep_days = getattr(game.player, 'sleep_days', 0)
    game.player.sleep_days += 1

    if game.player.sleep_days >= 3:
        game.player.health -= 5
        if not hasattr(game, 'warned_no_rest'):
            game.log.append("Вы слишком устали. Найдите укрытие.")
            game.warned_no_rest = True
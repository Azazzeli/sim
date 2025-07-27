# mods/mod_shelter.py
def on_next_day(game):
    if game.player.in_shelter:
        game.player.health = min(100, game.player.health + 5)
        game.log.append("Вы отдохнули в укрытии.")
    def spend_night(game):
        game.log.append("Вы переночевали в доме. Теперь это ваше укрытие.")
        game.player.in_shelter = True  # ✅ Это должно быть здесь
        game.player.health = min(100, game.player.health + 15)    
# mods/mod_thirst_hunger.py
def on_next_day(game):
    player = game.player
    if player.thirst < 30 and player.thirst_timer >= 3:
        player.health -= 5
    if player.hunger < 30 and player.hunger_timer >= 4:
        player.health -= 2
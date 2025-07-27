# mods/perk_starter_pack.py
def init(game):
    if game.player:
        game.player.inventory.add_item("food", 2)
        game.player.inventory.add_item("water", 2)
        game.log.append("🎁 Начальный набор: +2 еды, +2 воды")
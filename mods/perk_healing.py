# mods/perk_healing.py
def init(game):
    """Регистрирует бонус: +10 к здоровью при старте"""
    if hasattr(game, 'player') and game.player:
        game.player.health = min(100, game.player.health + 10)
        game.log.append("🎁 Модуль: Вы получили +10 к здоровью!")
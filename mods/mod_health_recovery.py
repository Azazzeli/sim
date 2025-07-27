# mods/mod_health_recovery.py
def on_next_day(game):
    """Восстановление здоровья при хорошем питании и воде"""
    player = game.player
    if not player.alive:
        return

    if player.hunger > 75 and player.thirst > 75:
        recovery = 3
        player.health = min(100, player.health + recovery)
        if recovery > 0:
            game.log.append(f"❤️ Вы хорошо поели и напились — здоровье восстанавливается (+{recovery})")

    elif player.hunger > 50 and player.thirst > 50:
        game.log.append("Вы в норме. Здоровье стабильно.")
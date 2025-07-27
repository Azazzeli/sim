# mods/mod_weather.py
import random


BIOME_EFFECTS = {
    "arid": {"thirst": -2.0, "hunger": -0.5},
    "taiga": {"thirst": -0.5, "hunger": -2.0, "cold": True},
    "tropical": {"thirst": -1.5, "disease": 0.1}
}

def on_next_day(game):
    biome = game.world.map_data[game.world.player_pos[1]][game.world.player_pos[0]]
    effects = BIOME_EFFECTS.get(biome, {})
    
    if "cold" in effects and not game.player.has_shelter:
        game.player.health -= 2
        
    if random.random() < effects.get("disease", 0):
        game.player.health -= 10
        game.log.append("Вы заболели в тропиках!")
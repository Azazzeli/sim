# player.py
import random
from config import ITEMS

class Inventory:
    def __init__(self):
        self.items = {
            "food": 2,
            "water": 2,
            "bandage": 1,
            "pistol": 1,
            "medkit": 0
        }
        self.max_slots = 10

    def add_item(self, item_name, count=1):
        current = sum(self.items.values())
        if current + count > self.max_slots:
            return False, "Инвентарь полон!"
        if item_name not in self.items:
            self.items[item_name] = 0
        self.items[item_name] += count
        return True, f"Получено: {ITEMS[item_name]['name']} x{count}"

    def use_item(self, item_name):
        if self.items[item_name] <= 0:
            return False, "Нет такого предмета"
        self.items[item_name] -= 1
        return True, "Использовано"

    def get_total(self):
        return sum(self.items.values())

class Character:
    def __init__(self):
        self.name = random.choice(["Выживший", "Рей", "Макс", "Лина", "Джек", "Сара"])
        self.hunger = 100
        self.thirst = 100
        self.health = 100
        self.days = 0
        self.alive = True
        self.inventory = Inventory()

        # Новые атрибуты
        self.fatigue = 0
        self.in_shelter = False
        self.has_weapon = False
        self.weapon_name = "нет"

        # Таймеры
        self.hunger_timer = 0
        self.thirst_timer = 0
        self.dehydration_stage = 0
        self.starvation_stage = 0

    def log_event(self, msg):
        if hasattr(self, 'game') and self.game:
            self.game.log.append(msg)

    def update(self):
        if not self.alive:
            return

        self.days += 1
        self.hunger -= random.uniform(1.5, 2.5)
        self.thirst -= random.uniform(2.0, 3.0)

        # Таймеры
        if self.hunger < 30:
            self.hunger_timer += 1
        else:
            self.hunger_timer = 0
            self.starvation_stage = 0

        if self.thirst < 30:
            self.thirst_timer += 1
        else:
            self.thirst_timer = 0
            self.dehydration_stage = 0

        # Обезвоживание
        if self.thirst_timer >= 3:
            if self.dehydration_stage == 0:
                self.log_event("❗ Сильная жажда! Здоровье снижается.")
                self.dehydration_stage = 1
            self.health -= 5
        if self.thirst_timer >= 5:
            self.health -= 10

        # Голодание
        if self.hunger_timer >= 4:
            if self.starvation_stage == 0:
                self.log_event("❗ Истощение! Слабость.")
                self.starvation_stage = 1
            self.health -= 2
        if self.hunger_timer >= 7:
            self.health -= 5

        self.hunger = max(0, self.hunger)
        self.thirst = max(0, self.thirst)
        self.health = max(0, min(100, self.health))

        if self.health <= 0:
            self.alive = False

    def eat(self):
        if self.inventory.use_item("food")[0]:
            self.hunger = min(100, self.hunger + 30)
            self.hunger_timer = 0
            self.starvation_stage = 0
            return "Съели консервы. Голод уменьшен."
        return "Нет еды!"

    def drink(self):
        if self.inventory.use_item("water")[0]:
            self.thirst = min(100, self.thirst + 35)
            self.thirst_timer = 0
            self.dehydration_stage = 0
            return "Выпили воду. Жажда уменьшена."
        return "Нет воды!"

    def heal(self):
        if self.inventory.use_item("medkit")[0]:
            self.health = min(100, self.health + 70)
            return "Использовали аптечку. Полное восстановление!"
        elif self.inventory.use_item("bandage")[0]:
            self.health = min(100, self.health + 30)
            return "Перевязали рану. Здоровье частично восстановлено."
        return "Нет средств для лечения!"

    def search_supplies(self):
        found_items = ["food", "water", "bandage"]
        item = random.choice(found_items)
        count = 1
        success, msg = self.inventory.add_item(item, count)
        risk = random.random()
        if risk < 0.3:
            self.health -= random.randint(10, 20)
            return "Искал припасы — получил ранение! Но кое-что нашёл."
        return f"Поиск завершён: {msg}"
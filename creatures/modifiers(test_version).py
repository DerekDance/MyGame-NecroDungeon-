#####################
# Классы исключительно для тестирования!


class Creature:
    def __init__(self, name, health, attack):
        self.name = name  # имя для отладки
        self.health = health
        self.attack = attack
        self.modifiers = []  # Здесь будут модификаторы этого существа

    # Метод для проверки наличия модификаторов(для тестирования)!
    def show_modifiers(self):
        if self.modifiers:
            print(f"{self.name} имеет модификаторы:")
            for mod in self.modifiers:
                target_name = mod.target.name if mod.target else "???"
                print(f"  - {mod.name} на {target_name} ({mod.remaining_duration} ходов)")
    ##########################################################################

    def add_modifier(self, modifier):
        self.modifiers.append(modifier)# Добавляем модификатор в конец списка

    def update_modifiers(self, step=1):
        for modifier in self.modifiers[:]:  # Идём по КОПИИ списка (чтобы безопасно удалять)
            modifier.apply_effect()
            modifier.update(step)
            if not modifier.active:  # Если модификатор деактивирован
                self.modifiers.remove(modifier)  # Удалить из списка

#####################

class Modifier:
    def __init__(self, name, duration, target):
        self.name = name  # Название модификатора ("Poison", "WeakeningBlade")
        self.duration = duration  # Общая длительность действия
        self.remaining_duration = duration  # Оставшееся время (изначально равно duration)
        self.target = target  # Ссылка на существо, на которое действует модификатор
        self.active = True  # Флаг активности (True = действует)

    # Функция для отсчета времени действия модификатора
    def update(self, step):
        if self.duration > 0 and self.active:
            self.remaining_duration -= step
            if self.remaining_duration <= 0:
                self.deactivate()
                return True
        return False

    # Функция активации
    def activate(self):
        self.active = True
        self.remaining_duration = self.duration

    # Функция деактивации
    def deactivate(self):
        self.active = False
        self.remaining_duration = self.duration
#####################
class Poison(Modifier):
    def __init__(self, duration=3, damage=2,target=None):
        super().__init__("Poison", duration,target)
        self.damage = damage

    def apply_effect(self):
        if self.active and self.target:
            self.target.health -= self.damage
            print(f"☠️ Яд наносит {self.damage} урона!")


class WeakeningBlade(Modifier):
    def __init__(self, duration=2,damage = 1,target=None):
        super().__init__("WeakeningBlade", duration,target)

    def apply_effect(self):
        if self.active and self.target:
            self.target.attack -= 1
            print(f"⚔️ Слабая атака!")
#####################


# Тестирование

# Обьект класса Modifier()
Hero = Creature("Герой", 40, 5)
Goblin = Creature("Гоблин", 30, 2)

# Модификаторы создаются с указанием цели
poison_on_hero = Poison(target=Hero)
weakening_on_goblin = WeakeningBlade(target=Goblin)
Hero.add_modifier(poison_on_hero)
Goblin.add_modifier(weakening_on_goblin)

while Goblin.health > 0:
    print(f"DEBUG: Модификторы {Goblin.name} {Goblin.show_modifiers()}")
    print(f"DEBUG: Модификторы {Hero.name} {Hero.show_modifiers()}")
    if Hero.health <= 0:
        print("Герой погиб")
        break
    cmd = input("Введите 1,2 для атаки:\n>")

    if cmd == "1":
        print("*" * 10)
        Hero.update_modifiers()
        Goblin.update_modifiers()

        Goblin.health -= Hero.attack
        Hero.health -= Goblin.attack
        print(f"🗡️ {Hero.name} атакует с силой {Hero.attack}!")
        print(f"🛡️ {Goblin.name} контратакует с силой {Goblin.attack}!")
        print(f"Goblin.health:{Goblin.health}\nHero.health:{Hero.health}")
        print("*" * 10)

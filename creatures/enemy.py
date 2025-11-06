"""
Родительский класс для противников
"""
class Enemy:
    def __init__(self, name: str, health: int, attack: int, distance: int):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.distance = distance


    def take_damage(self, damage: int):
        self.health = max(0, self.health - damage)
        return self.health


    def is_alive(self) -> bool:
        return self.health > 0

"""
Классы противников
"""

class Dummy(Enemy):
    def __init__(self):
        super().__init__("Тренировочный манекен",20,1,3)


class Acolyte(Enemy):
    def __init__(self):
        super().__init__("Аколит",9,2,5)
        self.charge_turns = 0

    def update(self):
        """Вызывается каждый ход — обновляет состояние Аколита"""
        if self.charge_turns < 3:
            self.charge_turns += 1
        # Когда достигает 3 — остаётся 3, пока не выстрелит

    def can_shoot(self):
        """Можно ли стрелять?"""
        return self.charge_turns == 3

    def reset_charge(self):
        """Сбросить заряд после выстрела"""
        self.charge_turns = 0


class NecroStudent(Enemy):
    def __init__(self):
        super().__init__("Ученик-некроманта",9,2,3)


class MainSubstance(Enemy):
    def __init__(self):
        super().__init__("Субстанция",30,3,6)


class SubMini1(Enemy):
    def __init__(self):
        super().__init__("\u001b[30;1mМерзкая субстанция\u001b[0m",9,3,2)


class SubMini2(Enemy):
    def __init__(self):
        super().__init__(
            "\u001b[35mСклизкая субстанция\u001b[0m",11,2,1)


class Necromancer(Enemy):
    def __init__(self):
        super().__init__("\u001b[35mНекромант\u001b[0m",30,3,3)
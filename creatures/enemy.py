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
        """Получить урон"""
        self.health = max(0, self.health - damage)
        return self.health

    def is_alive(self) -> bool:
        """Жив ли противник?"""
        return self.health > 0


"""
Классы противников
"""

class Dummy(Enemy):
    def __init__(self):
        super().__init__(
            name="Тренировочный манекен",
            health=20,
            attack=1,
            distance=3
        )


class Acolyte(Enemy):
    def __init__(self):
        super().__init__(
            name="Аколит-некромант",
            health=9,
            attack=2,
            distance=5
        )


class NecroStudent(Enemy):
    def __init__(self):
        super().__init__(
            name="Ученик-некромант",
            health=9,
            attack=2,
            distance=3
        )


class MainSubstance(Enemy):
    def __init__(self):
        super().__init__(
            name="Мерзкая субстанция",
            health=30,
            attack=3,
            distance=6
        )

class SubMini1(Enemy):
    def __init__(self):
        super().__init__(
            name="\u001b[30;1mМерзкая субстанция\u001b[0m",
            health=9,
            attack=3,
            distance=2
        )

class SubMini2(Enemy):
    def __init__(self):
        super().__init__(
            name="\u001b[35mСклизкая субстанция\u001b[0m",
            health=11,
            attack=2,
            distance=1
        )



class Necromancer(Enemy):
    def __init__(self):
        super().__init__(
            name="\u001b[35mНекромант\u001b[0m",
            health=30,
            attack=3,
            distance=3
        )
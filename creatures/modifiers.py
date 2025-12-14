
"""
Универсальный класс для модификаторов существ
"""
class Modifier:
    def __init__(self, name, duration, target):
        self.name = name  # Название модификатора
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

#Регенерация здоровья
class RegenHP(Modifier):
    def __init__(self, duration=3, heal_power=1, target=None):
        super().__init__("RegenHP", duration, target)
        self.heal_power = heal_power  # Сколько HP восстанавливает за тик
        self.total_healed = 0  # Счётчик общего восстановленного здоровья







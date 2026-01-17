
from system import HelpSystem
from creatures import Hero
"""
Родительский класс для противников
"""

# Для использования форматирования строк
hp = HelpSystem()
#Создаем героя
hero = Hero()

class Enemy:
    def __init__(self, name, health, max_health, attack, distance):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.distance = distance
        self.charge_turns = 0
        self.modifiers = []  # Список модификаторов Противников

    #Проверка модификатора противника
    def has_active_modifier(self, modifier_name):
        """Проверяет, есть ли активный модификатор с указанным именем"""
        for existing in self.modifiers:
            if existing.name == modifier_name and existing.active:
                return True, existing
        return False, None

    # Добавление модификатора противника
    def add_modifier(self, modifier):
        # Используем вспомогательный метод
        has_active, existing_mod = self.has_active_modifier(modifier.name)

        if has_active:
            # Можно показать информацию о существующем
            print(f"{hp.YELLOW}Эффект '{modifier.name}' уже активен!{hp.RESET}")
            return False

        # Добавляем
        modifier.target = self
        self.modifiers.append(modifier)
        modifier.activate()
        return True

    # Обновление модификатора противника
    def update_all(self):
        for modifier in self.modifiers[:]:
            if not modifier.active:
                self.modifiers.remove(modifier)
                continue

            if hasattr(modifier, 'apply_effect'):
                is_finished = modifier.apply_effect()

                if is_finished:
                    self.modifiers.remove(modifier)



    def is_alive(self) -> bool:
        return self.health > 0

    """
    Для подготовки заряженных заклинаний:
    Комната 1 - Заряжание арбалета Аколита,
    Комната 2 - Заклинание Ученика-некроманта "Могильный хват"
    """
    def update(self,sum_steps,step):
        """Вызывается каждый ход — обновляет состояние Аколита"""
        if self.charge_turns < sum_steps:
            self.charge_turns += step

    def can_active(self,ready_step):
        """Можно ли стрелять?"""
        return self.charge_turns == ready_step

    def reset_charge(self):
        """Сбросить заряд после выстрела"""
        self.charge_turns = 0

    # Классы противников

# Манекен
class Dummy(Enemy):
    def __init__(self):
        super().__init__("Тренировочный манекен",20,20,1,3)


# Аколит
class Acolyte(Enemy):
    def __init__(self):
        super().__init__("Аколит",9,9,3,5)
        self.charge_turns = 0



# Ученик-некроманта
class NecroStudent(Enemy):
    def __init__(self):
        super().__init__("Ученик-некроманта",9,9,2,3)
        self.charge_turns = 0


# Субстанция
class MainSubstance(Enemy):
    def __init__(self):
        super().__init__("Субстанция",30,30,3,6)

    def anti_mitoz(self,flag):
        if isinstance (flag, bool):
            self.health = 28
            self.max_health = 28



class SubMini(Enemy):
    def __init__(self, name, health, max_health, attack, distance):
        super().__init__(name, health, max_health, attack, distance)

    def anti_mitoz(self, flag):
        if isinstance(flag, bool):
            self.health = 8
            self.max_health = 8



class SubMini2(Enemy):
    def __init__(self):
        super().__init__(
            "\u001b[35mСклизкая субстанция\u001b[0m",11,11,2,1)

    def anti_mitoz(self, flag):
        if isinstance(flag, bool):
            self.health = 9
            self.max_health = 9

# Некромант
class Necromancer(Enemy):
    def __init__(self):
        super().__init__("\u001b[35;1mНекромант\u001b[0m",30,30,3,3)
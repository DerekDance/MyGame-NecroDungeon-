
from system import HelpSystem
from creatures import Hero
import sys
import threading
import random
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
        self._input_active = False

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


    # Методы для наказания игрока за истечение таймера
    def timeout_message(self, hero, help_sys):
        """Вызывается по истечении таймера."""
        if not getattr(self, '_input_active', False):
            return

        self._input_active = False

        timeout_phrases = getattr(self, 'TIMEOUT_PHRASES', ['','',''])
        enemy_name = getattr(self,"name","Неизвестный")
        enemy_attack = getattr(self,"attack",0)

        hero.hero_health -= enemy_attack
        chosen_phrase = random.choice(timeout_phrases)
        print(f"\n{hp.START_TIRE}{hp.PURPLE}{enemy_name} - '{chosen_phrase}'{hp.RESET}")
        print(f"\n{enemy_name} атакует первым!")
        print(f"{hp.info_room(hero.hero_health, hero.hero_max_health, [self])}{hp.END_TIRE}")
        print(f"\n{hp.START_TIRE}У вас есть какое-то количество времени для следующего действия...{hp.END_TIRE}")

    def ask_for_action_hero(self, hero, help_sys, amount_of_time=30):
        """Запрашивает действие героя с таймером amount_of_time=30 по умолчанию)."""
        if self._input_active:
            raise RuntimeError("Запрос действия уже активен!")
        self._input_active = True
        user_input_ref = {'value': None}
        timer_ref = {'obj': None}

        def input_thread():
            try:
                print("\nНапишите какое действие вы хотите совершить (по-русски): ", end='', flush=True)
                user_input_ref['value'] = sys.stdin.readline().strip().lower()
            except Exception:
                user_input_ref['value'] = None

        thread = threading.Thread(target=input_thread)
        thread.daemon = True
        thread.start()

        # Создаём таймер, который вызовет метод экземпляра
        timer_ref['obj'] = threading.Timer(amount_of_time, self.timeout_message, args=(hero, hp))
        timer_ref['obj'].start()

        thread.join(amount_of_time)

        if thread.is_alive():
            # Время вышло
            timer_ref['obj'].cancel()
            self._input_active = False
            return None
        else:
            # Пользователь успел ответить
            timer_ref['obj'].cancel()
            self._input_active = False
            return user_input_ref['value']

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
        self.summon_distance = range(3, 7)
        self.summon_attack = range(2, 4)

    def skull_shoot(self, flag):
        if isinstance(flag, bool):
            self.summon_distance = range(3, 8)
            self.summon_attack = range(2, 3)

    TIMEOUT_PHRASES = [
        "Мёртвые не раздумывают - они повинуются!",
        "Твоя нерешительность - лучший союзник моей армии теней!",
        "Каждая упущенная секунда - ещё один глоток твоей жизненной силы!",
        "В моём царстве время течёт иначе... прямо как кровь из твоих ран!",
        "Ты замер, словно труп на виселице...",
        "Время кончилось... как и твои шансы!",
        "Ты что, надеялся, что смерть будет ждать?",
        "Упущенное время не вернуть...",
    ]

    TAUNTS_AFTER_PUSH = [
        "Как далеко ты отлетел? Достаточно, чтобы понять своё ничтожество?",
        "Ха! Ты даже не устоял перед лёгким взмахом моей руки!",
        "Падаешь так изящно... Может, сразу ляжешь в могилу?",
        "Разве это не унизительно? Тебя отшвырнуло, как щепку!"
    ]



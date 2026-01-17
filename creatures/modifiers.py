from system import HelpSystem
import random

# Для использования форматирования строк
hp = HelpSystem()

"""
Универсальный класс для модификаторов существ
"""
# Допустимые операции
VALID_OPERATIONS ={"+", "-", "*", "/"}

class Modifier:
    def __init__(self, name, duration, step, target, start_info_msg=None,show_message = False,display_name = None):
        self.start_info_msg = start_info_msg # Дополнительное сообщение
        self.duration = duration  # Общая длительность действия
        self.remaining_duration = duration  # Оставшееся время (изначально равно duration)
        self.target = target  # Ссылка на существо, на которое действует модификатор
        self.step = step  # Шаг, который используется в методе update()
        self.active = False  # Флаг активности (False = не действует)
        self.step_counter = 0  # Счетчик текущего шага
        self.show_message = show_message
        self.display_name = display_name or name
        self.name = name if name is not None else display_name# Техническое имя (для проверок)

    # Получить имена цели
    def get_health_attr_names(self):
        # Проверяем разные варианты имён
        if hasattr(self.target, "health") and hasattr(self.target, "max_health"):
            return "health", "max_health"
        elif hasattr(self.target, "hero_health") and hasattr(self.target, "hero_max_health"):
            return "hero_health", "hero_max_health"
        else:
            return None, None

    def update(self):
        """
        Обновляет состояние модификатора.
        Возвращает кортеж (завершен_ли, применять_ли_эффект)
        """
        if not self.active or self.duration <= 0:
            return True, False

        self.step_counter += 1

        # Проверяем, достигли ли нужного шага
        if self.step_counter >= self.step:
            self.step_counter = 0
            self.remaining_duration -= 1

            # Проверяем, не завершился ли модификатор
            if self.remaining_duration <= 0:
                self.deactivate()
                return True, True  # Завершен, но эффект применить нужно (в последний раз)

            return False, True  # Не завершен, эффект применить нужно

        return False, False  # Не завершен, эффект не применять

    # Функция активации
    def activate(self):
        self.active = True
        self.remaining_duration = self.duration

    # Функция деактивации
    def deactivate(self):
        self.active = False
        self.remaining_duration = self.duration


# Модификатор регенерации здоровья
class RegenHP(Modifier):
    """Модификатор, периодически восстанавливающий здоровье цели.

      Поддерживает как врагов (атрибуты `health`/`max_health`), так и героя (`hero_health`/`hero_max_health`).
      Эффект применяется каждые `step` шагов, пока не истечёт `duration` или здоровье не станет максимальным.
      """
    def __init__(self, target, duration, step, heal_power, show_message=False,display_name = None):
        if not hasattr(target, "health") and not hasattr(target, "hero_health"):
            raise ValueError(f"Цель {target} не имеет атрибутов здоровья!")
        super().__init__("RegenHP", duration, step, target)
        self.heal_power = heal_power
        self.show_message = show_message
        self.display_name = display_name

    # Применение регенерации
    def apply_effect(self):
        """Применяет эффект регенерации, если нужно"""
        # Обновляем состояние и получаем информацию
        is_finished, should_apply = self.update()

        # Если не нужно применять эффект на этом шаге, просто возвращаем
        if not should_apply:
            return is_finished

        health_attr, max_health_attr = self.get_health_attr_names()

        # Получить значения с проверкой
        current_hp = getattr(self.target, health_attr, None)
        max_hp = getattr(self.target, max_health_attr, None)

        if not isinstance(current_hp, (int, float)) or not isinstance(max_hp, (int, float)):
            print("Значения current_hp и max_hp должны быть числами!")
            self.deactivate()
            return True

        if current_hp is None or max_hp is None:
            print(f"Не могу найти атрибуты здоровья у {self.target}")
            self.deactivate()
            return True

        # Проверка
        if current_hp >= max_hp:
            self.deactivate()
            return True

        # Вычисление
        new_hp = min(current_hp + self.heal_power, max_hp)

        # Сколько вылечили
        healed_amount = new_hp - current_hp

        # Сохранение
        setattr(self.target, health_attr, new_hp)

        # Показ сообщения если не None
        if self.show_message:
            if healed_amount > 0:
                target_name = getattr(self.target, "name", "Неизвестный")
                print(
                    f"(💊)  {hp.PURPLE_BOLD}{target_name} восстановил {healed_amount} HP\nЗдоровье: {current_hp} -> {new_hp}{hp.RESET}")

        # Возвращаем информацию о завершении
        return is_finished


# Модификатор множителя урона
class DamageModifier(Modifier):
    """Модификатор, временно изменяющий урон цели с помощью арифметической операции.

     Поддерживает операции: сложение (+), вычитание (-), умножение (*), деление (/).
     Применяется к ближней ('melee') или дальней ('ranged') атаке.
     При деактивации восстанавливает исходное значение урона.
     """
    def __init__(self, target, duration, value,operation_type,attack_type,start_info_msg,show_message,display_name):
        # Проверяем операцию
        operation_type = operation_type.lower()
        if operation_type not in self.VALID_OPERATIONS:
            raise ValueError(f"Неизвестная операция: {operation_type}. "
                             f"Допустимо: {', '.join(self.VALID_OPERATIONS)}")
            # Проверяем значение
        self._validate_value(operation_type, value)

        super().__init__("DamageModifier", duration, 1, target, start_info_msg)
        self.value = value
        self.original_attack = None
        self.operation_type = operation_type #Параметр выбора математической операции для модификатора
        self.attack_type = attack_type #Тип атаки
        self.show_message = show_message
        self.display_name = display_name

    # Функция проверки значений
    def _validate_value(self, operation_type, value):
        if operation_type in ["+", "-"] and value <= 0:
            raise ValueError(f"Для {operation_type} значение должно быть > 0")
        elif operation_type == "*" and value <= 1.0:
            raise ValueError("Для умножения множитель должен быть > 1.0")
        elif operation_type == "/" and value <= 0:
            raise ValueError("Для деления значение должно быть > 0")


    # Функция активации мультиурона
    def activate(self):
        #Защита от повторного применения
        if self.active:
            print("Уже активен!")
            return

        attack_attr = self.get_attack_attr_names()

        if not attack_attr:
            print(f"Не могу найти атрибуты атаки у {self.target}")
            return

        # Получить значения с проверкой
        current_attack = getattr(self.target, attack_attr, None)

        if not isinstance(current_attack, (int, float)):
            print("Значения current_attack должно быть числом!")
            return

        if current_attack is None:
            print(f"Не могу найти атрибуты атаки у {self.target}")
            return
        # Устанавливаем атаку до модификатора
        self.original_attack = current_attack

        self.operation_type = self.operation_type.lower()
        if self.operation_type == "+":
            new_attack = self.original_attack + self.value
        elif self.operation_type == "*":
            new_attack = self.original_attack * self.value
        elif self.operation_type == "-":
            new_attack = max(self.original_attack - self.value,0)
        elif self.operation_type == "/":
            if self.value == 0:
                print("Ошибка: деление на ноль!")
                return
            new_attack = self.original_attack / self.value
        # Сохраняем новую атаку обьекту
        setattr(self.target, attack_attr, new_attack)
        # Получаем имя для форматирования
        target_name = getattr(self.target, "name", "Неизвестный")
        print(f"{self.start_info_msg}\n"
              f"-  Урон '{target_name}' = {current_attack:.1f} → {new_attack:.1f}\n"
              f"-  Урон '{current_attack:.1f} {self.operation_type} {self.value}' на {self.duration} шага(ов){hp.RESET}")
        #Вызывается родительский activate. self.active устанавливает True
        super().activate()


    # Функция деактивации мультиурона
    def deactivate(self):
        if not self.active:
            return  # Уже деактивирован
        # Получаем имя для форматирования
        target_name = getattr(self.target, "name", "Неизвестный")
        if self.original_attack is not None:
            attack_attr = self.get_attack_attr_names()
            if attack_attr:
                setattr(self.target, attack_attr, self.original_attack)
        # Вызывается родительский deactivate. self.active устанавливает False
        super().deactivate()


    # Получить имена атаки цели
    def get_attack_attr_names(self):
        if self.attack_type == "melee":
            if hasattr(self.target, "attack"):
                return "attack"
            elif hasattr(self.target, "hero_attack"):
                return "hero_attack"
        elif self.attack_type == "ranged":
            if hasattr(self.target, "hero_range_attack"):
                return "hero_range_attack"
            else:
                return None
        else:
            return

    #Применение модификатора множитель урона
    def apply_effect(self):
        is_finished, _ = self.update()

        if is_finished:
            # Сообщение ТОЛЬКО когда модификатор завершился
            target_name = getattr(self.target, "name", "Неизвестный")
            print(f"{self.start_info_msg} {target_name} закончился{hp.RESET}")

        return is_finished


# Модификатор полета снаряда
class ProjectileModifier(Modifier):
    def __init__(self, target, duration, value,operation_type,start_info_msg,finish_info_msg):
        # Проверяем операцию
        operation_type = operation_type.lower()
        if operation_type not in self.VALID_OPERATIONS:
            raise ValueError(f"Неизвестная операция: {operation_type}. "
                             f"Допустимо: {', '.join(self.VALID_OPERATIONS)}")
            # Проверяем значение
        self._validate_value(operation_type, value)

        super().__init__("ProjectileModifier", duration, 1, target)
        self.value = value
        self.operation_type = operation_type #Параметр выбора математической операции для модификатора
        self.start_info_msg = start_info_msg
        self.finish_info_msg = finish_info_msg


    # Функция проверки значений
    def _validate_value(self, operation_type, value):
        if operation_type in ["+", "-"] and value <= 0:
            raise ValueError(f"Для {operation_type} значение должно быть > 0")
        elif operation_type == "*":
            raise ValueError("Умножение не доступно для этого метода!")
        elif operation_type == "/":
            raise ValueError("Деление не доступно для этого метода!")


# Функция активации полета снаряда ПОКА НЕ РАБОТАЕТ
    def activate(self):
        #Защита от повторного применения
        if self.active:
            print("Уже активен!")
            return

        health_attr, max_health_attr = self.get_health_attr_names()

        # Получить значения с проверкой
        current_hp = getattr(self.target, health_attr, None)
        max_hp = getattr(self.target, max_health_attr, None)

        if not isinstance(current_hp, (int, float)) or not isinstance(max_hp, (int, float)):
            print("Значения current_hp и max_hp должны быть числами!")
            self.deactivate()
            return True

        if current_hp is None or max_hp is None:
            print(f"Не могу найти атрибуты здоровья у {self.target}")
            self.deactivate()
            return True

        # Вычисление
        new_hp = min(current_hp,max_hp)

        self.operation_type = self.operation_type.lower()
        # Прибавляет здоровья
        if self.operation_type == "+":
            new_hp = min(current_hp + self.value,max_hp)
        # Отнимает здоровье
        elif self.operation_type == "-":
            new_hp = current_hp - self.value

        # Сохранение
        setattr(self.target, health_attr, new_hp)
        target_name = getattr(self.target, "name", "Неизвестный")
        print(f"{self.start_info_msg}{target_name}{self.finish_info_msg}\n{hp.RESET}")
        #Вызывается родительский activate. self.active устанавливает True
        super().activate()






        














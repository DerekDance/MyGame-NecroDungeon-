from system import HelpSystem

# Для использования форматирования строк
hp = HelpSystem()

"""
Универсальный класс для модификаторов существ
"""


class Modifier:
    def __init__(self, name, duration, step, target):
        self.name = name  # Название модификатора
        self.duration = duration  # Общая длительность действия
        self.remaining_duration = duration  # Оставшееся время (изначально равно duration)
        self.target = target  # Ссылка на существо, на которое действует модификатор
        self.step = step  # Шаг, который используется в методе update()
        self.active = True  # Флаг активности (True = действует)
        self.step_counter = 0  # Счетчик текущего шага

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
    def __init__(self, target, duration, step, heal_power, show_message=False):
        if not hasattr(target, "health") and not hasattr(target, "hero_health"):
            raise ValueError(f"Цель {target} не имеет атрибутов здоровья!")
        super().__init__("RegenHP", duration, step, target)
        self.heal_power = heal_power
        self.show_message = show_message

    # Получить имена цели
    def get_health_attr_names(self):
        # Проверяем разные варианты имён
        if hasattr(self.target, "health") and hasattr(self.target, "max_health"):
            return "health", "max_health"
        elif hasattr(self.target, "hero_health") and hasattr(self.target, "hero_max_health"):
            return "hero_health", "hero_max_health"
        else:
            return None, None

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
class MultiDamage(Modifier):
    def __init__(self, target, duration, multi_value):
        if multi_value <= 1.0:
            raise ValueError("Множитель должен быть больше 1.0!")
        super().__init__("MultiDamage", duration, 1, target)
        self.multi_value = multi_value
        self.original_attack = None

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
        # Устанавливаем атаку после модификатора
        new_attack = self.original_attack * self.multi_value
        # Сохраняем новую атаку обьекту
        setattr(self.target, attack_attr, new_attack)
        # Получаем имя для форматирования
        target_name = getattr(self.target, "name", "Неизвестный")
        print(f"(🗡️){hp.CYAN_BOLD} Урон {target_name} увеличен с {current_attack:.1f} → {new_attack:.1f}\n"
              f"(🗡️){hp.CYAN_BOLD} Урон {target_name} увеличен в {self.multi_value}× на {self.duration} тиков{hp.RESET}{hp.RESET}")
        #Вызывается родительский activate. self.active устанавливает True
        super().activate()


    # Функция деактивации мультиурона
    def deactivate(self):
        # Получаем имя для форматирования
        target_name = getattr(self.target, "name", "Неизвестный")
        if self.original_attack is not None:
            attack_attr = self.get_attack_attr_names()
            if attack_attr:
                setattr(self.target, attack_attr, self.original_attack)

        print(f"(🗡️){hp.CYAN_BOLD} Эффект усиления {target_name} закончился{hp.RESET}")
        # Вызывается родительский deactivate. self.active устанавливает False
        super().deactivate()


    # Получить имена атаки цели
    def get_attack_attr_names(self):
        if hasattr(self.target, "attack"):
            return "attack"
        elif hasattr(self.target, "hero_attack"):
            return "hero_attack"
        else:
            return None

    #Применение модификатора множитель урона
    def apply_effect(self):
        # Игнорируем should_apply
        is_finished, _ = self.update()

        # Если время вышло - деактивируем
        if is_finished:
            self.deactivate()

        return is_finished
        














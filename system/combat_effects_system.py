
from system import HelpSystem

# Для использования форматирования строк
hp = HelpSystem()

"""
Универсальный класс для модификаторов существ
"""

class Modifier:
    def __init__(self, name, duration, step, target,
                 one_time=False,  # ← По умолчанию False
                 cooldown_turns=0,
                 cooldown_start_msg=None,
                 cooldown_end_msg=None,
                 start_info_msg=None,
                 show_message=False,
                 display_name=None):

        self.valid_operations =  {"+", "-", "*", "/"} # Допустимые операции
        self.start_info_msg = start_info_msg # Дополнительное сообщение
        self.duration = duration  # Общая длительность действия
        self.remaining_duration = duration  # Оставшееся время (изначально равно duration)
        self.target = target  # Ссылка на существо, на которое действует модификатор
        self.step = step  # Шаг, который используется в методе update()
        self.active = False  # Флаг активности (False = не действует)
        self.step_counter = 0  # Счетчик текущего шага
        self.show_message = show_message
        self.display_name = display_name or name
        self.name = name if name is not None else display_name # Техническое имя (для проверок)

        # Подготовка модификатора,если есть
        self.cooldown_active = False # Активна ли подготовка
        self.one_time = one_time # Эффект применяется один раз и сразу завершается (мгновенное действие)
        self.cooldown_turns = cooldown_turns # Сколько ходов длится подготовка
        self.remaining_cooldown_turns = cooldown_turns  # Оставшееся время (изначально равно cooldown_turns)
        self.cooldown_start_msg = cooldown_start_msg
        self.cooldown_end_msg = cooldown_end_msg

        if self.cooldown_turns and self.cooldown_turns > 0:
            self.cooldown_active = True
            self.remaining_cooldown_turns = self.cooldown_turns
        else:
            self.active = True
            self.remaining_duration = self.duration


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
        print(
            f"[UPDATE] {self.display_name}: active={self.active}, cd={self.remaining_cooldown_turns},"
            f" rem_dur={self.remaining_duration}, step_counter={self.step_counter}")
        # Фаза 1: Подготовка (cooldown)
        if self.cooldown_turns and self.remaining_cooldown_turns > 0:
            if self.cooldown_start_msg and self.remaining_cooldown_turns == self.cooldown_turns:
                print(self.cooldown_start_msg)
            self.remaining_cooldown_turns -= 1

            # Если это был последний ход подготовки
            if self.remaining_cooldown_turns == 0:
                # Активируем эффект
                if self.cooldown_end_msg:
                    print(self.cooldown_end_msg)
                self.active = True
                self.remaining_duration = self.duration
            else:
                self.active = False

            return False, False

        # Если уже активен
        if self.active and self.duration > 0:
            self.step_counter += 1
            if self.step_counter >= self.step:
                self.step_counter = 0
                self.remaining_duration -= 1

                # Эффект применяется один раз и сразу завершается (мгновенное действие)
                if self.one_time or self.remaining_duration <= 0:
                    self.deactivate()
                    return True, True

                return False, True

        return False, False

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
        super().__init__(
            name="RegenHP",
            duration=duration,
            step=step,
            target=target,
            one_time = False,
            cooldown_turns=0,  # ← Мгновенная активация
            show_message=show_message,
            display_name=display_name
        )
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
        self.attack_type = attack_type
        self.operation_type = operation_type
        self.value = value
        self.valid_operations = Modifier.valid_operations
        operation_type = operation_type.lower()
        if operation_type not in self.valid_operations:
            raise ValueError(f"Неизвестная операция: {operation_type}. "
                             f"Допустимо: {', '.join(self.valid_operations)}")
            # Проверяем значение
        self._validate_value(operation_type, value)
        super().__init__(
            name="DamageModifier",
            duration=duration,
            step=1,
            target=target,
            one_time=False,
            cooldown_turns=0,  # ← Мгновенная активация
            start_info_msg=start_info_msg,
            show_message=show_message,
            display_name=display_name,
        )


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


class Projectile(Modifier):
    """Модификатор, представляющий летящий снаряд или отложенный эффект с задержкой по времени.

            Используется для моделирования объектов, которые:
            - "летят" к цели в течение заданного числа ходов (`distance`),
            - по достижении цели применяют эффект: наносят урон или восстанавливают здоровье,
            - могут быть уничтожены досрочно (например, при увороте игрока).

            Эффект активируется только по истечении длительности (когда снаряд "достигает" цели).
            Поддерживает только операции сложения ('+') и вычитания ('-') над здоровьем цели.
            """
    def __init__(self, target, distance, power, message_when_receiving_damage,
                 message_when_dodging, operation_type, display_name,
                 one_time=True, dodgeable=True,auto_recast=False, **kwargs):

        super().__init__(
            name="Projectile",
            duration=distance,
            step=1,
            target=target,
            display_name=display_name,
            one_time=one_time,
            **kwargs  # ← Без перезаписи параметров!
        )

        self.auto_recast = auto_recast #Перезапуск снаряда для работы в цикле while файла main.py
        self.operation_type = operation_type  # Параметр выбора математической операции для модификатора
        self.power = power
        self.dodgeable = dodgeable #Можно ли увернуться от снаряда
        self.message_when_receiving_damage = message_when_receiving_damage #Сообщение при достижении цели
        self.message_when_dodging = message_when_dodging #Сообщение при удачном увороте от снаряда
        self.display_name = display_name

        # Проверяем операцию
        operation_type = operation_type.lower()
        if operation_type not in self.valid_operations:
            raise ValueError(f"Неизвестная операция: {operation_type}. "
                             f"Допустимо: {', '.join(self.valid_operations)}")
            # Проверяем значение
        self._validate_value(operation_type, power)

    # Функция проверки значений
    def _validate_value(self, operation_type, power):
        if operation_type in ["+", "-"] and power <= 0:
            raise ValueError(f"Для {operation_type} значение должно быть > 0")
        elif operation_type == "*":
            raise ValueError("Нельзя использовать умножение с этим модификатором!")
        elif operation_type == "/":
            raise ValueError("Нельзя использовать деление с этим модификатором!")

    def activate(self):
        super().activate()

    def apply_effect(self):
        is_finished, should_apply = self.update()

        if not self.target.is_alive():
            self.deactivate()
            return True

        if is_finished:
            # Применяем эффект
            health_attr, max_health_attr = self.get_health_attr_names()
            if health_attr and max_health_attr:
                target_name = getattr(self.target, "name", "Неизвестный")
                current = getattr(self.target, health_attr)
                max_hp = getattr(self.target, max_health_attr)

                if self.operation_type == "-":
                    new_value = max(current - self.power, 0)
                elif self.operation_type == "+":
                    new_value = min(current + self.power, max_hp)

                setattr(self.target, health_attr, new_value)
                print(self.message_when_receiving_damage)
                print(f"{hp.YELLOW_STAR_START}Здоровье {target_name}: {new_value}|{max_hp}{hp.YELLOW_STAR_END}")

            # Проверка auto_recast
            if not isinstance(self.auto_recast, int) or self.auto_recast < 0:
                print("Значение auto_recast должно быть неотрицательным целым числом!")

            elif self.auto_recast > 0:
                # Создаём новый снаряд с уменьшенным счётчиком
                new_projectile = Projectile(
                    target=self.target,
                    distance=self.duration,
                    power=self.power,
                    operation_type=self.operation_type,
                    message_when_receiving_damage=self.message_when_receiving_damage,
                    message_when_dodging=self.message_when_dodging,
                    display_name=self.display_name,
                    one_time=self.one_time,
                    dodgeable=self.dodgeable,
                    auto_recast=self.auto_recast - 1,  # ← уменьшаем здесь, не изменяя self
                    cooldown_turns=getattr(self, 'cooldown_turns', 0),
                    cooldown_start_msg=getattr(self, 'cooldown_start_msg', None),
                    cooldown_end_msg=getattr(self, 'cooldown_end_msg', None)
                )
                self.target.add_modifier(new_projectile)

            # Всегда деактивируем текущий снаряд
            self.deactivate()
            return True

        return False


class ReverseStep(Modifier):
    def __init__(self, target, duration, display_name="Реверс-поступь",
                 cooldown_turns=0,
                 cooldown_start_msg=None,
                 cooldown_end_msg=None,
                 auto_recast=0):  # ← добавляем auto_recast
        super().__init__(
            name="ReverseStep",
            duration=duration,
            step=1,
            target=target,
            one_time=False,  # всегда периодический
            cooldown_turns=cooldown_turns,
            cooldown_start_msg=cooldown_start_msg,
            cooldown_end_msg=cooldown_end_msg,
            display_name=display_name
        )
        # Валидация auto_recast
        if not isinstance(auto_recast, int) or auto_recast < 0:
            raise ValueError("auto_recast должен быть неотрицательным целым числом")
        self.auto_recast = auto_recast

        # Проверка наличия у цели параметра reverse_step_active
        if not hasattr(self.target, 'reverse_step_active'):
            raise AttributeError(f"Цель {self.target} не поддерживает reverse_step_active")


    def apply_effect(self):
        is_finished, _ = self.update()

        # Эффект активен только если он вышел из cooldown и ещё не завершился
        if self.active and not is_finished:
            self.target.reverse_step_active = True
        else:
            self.target.reverse_step_active = False

        # Если эффект завершился
        if is_finished:
            self.target.reverse_step_active = False
            print(f"{hp.START_TIRE}(🦶) Магия заклинания {hp.PURPLE}'Реверс - поступь'{hp.RESET} рассеялась...{hp.END_TIRE}")

            # Проверяем auto_recast
            if self.auto_recast > 0:
                # Создаём новый экземпляр с уменьшенным счётчиком
                new_effect = ReverseStep(
                    target=self.target,
                    duration=self.duration,
                    display_name=self.display_name,
                    cooldown_turns=self.cooldown_turns,  # можно также перезапускать cooldown
                    cooldown_start_msg=self.cooldown_start_msg,
                    cooldown_end_msg=self.cooldown_end_msg,
                    auto_recast=self.auto_recast - 1
                )
                self.target.add_modifier(new_effect)

            return True

        return False


        














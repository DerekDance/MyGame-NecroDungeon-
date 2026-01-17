from system import HelpSystem

# Для использования форматирования строк
hp = HelpSystem()

class BattleSystem:

    # Выбор цели для атаки
    def select_target(self, targets):
        """
        Позволяет выбрать цель из списка.
        :param targets: список объектов-целей
        :return: выбранный объект или None
        """
        # Фильтруем только живых (если есть атрибут health)
        alive_targets = [
            t for t in targets
            if not hasattr(t, 'health') or getattr(t, 'health', 0) > 0
        ]

        if not alive_targets:
            print("Нет доступных целей.")
            return None

        if len(alive_targets) == 1:
            # Возвращаем единственного врага
            return alive_targets[0]

        # Показываем меню
        print("Выберите цель:")
        for i, target in enumerate(alive_targets, 1):
            name = getattr(target, 'name', f'Цель {i}')
            health = getattr(target, 'health', '???')
            print(f"({i}) {name}")

        try:
            choice = int(input("Номер цели (0 для отмены): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(alive_targets):
                # Возвращаем цель с текущим индексом
                return alive_targets[choice - 1]
            else:
                print("Неверный номер.")
                return None
        except ValueError:
            print("Введите число.")
            return None


    def enemies_attack_target(self,target_attacked,*attack_group):
        """
        Наносит урон герою от нескольких противников на заданной дистанции.
        :param target_attacked: объект  с атрибутами health,hero_health,is_alive()
        :param attack_group: кортежи вида (противник, дистанция_атаки)
        :return: строка с результатами атак
        """
        results = []

        for i, group in enumerate(attack_group):

            # Проверка структуры группы
            if not isinstance(group, (list, tuple)) or len(group) < 2:
                results.append(f"Ошибка: группа {i} имеет неверный формат")
                continue

            enemy, enemy_attack_range = group[0], group[1]

            # Проверка объекта противника
            if enemy is None:
                results.append(f"{i} - противник не задан")
                continue

            # Получение имени противника для сообщений
            if not hasattr(enemy, 'distance'):
                results.append(f"Ошибка: {getattr(enemy, 'name', 'Объект')} не имеет атрибута distance")
                continue

            if not hasattr(enemy, 'attack'):
                results.append(f"Ошибка: {getattr(enemy, 'name', 'Объект')} не имеет атрибута attack")
                continue

            if hasattr(target_attacked, 'health'):
                health_attr = 'health'

            elif hasattr(target_attacked, 'hero_health'):
                health_attr = 'hero_health'

            else:
                results.append(f"Ошибка: {getattr(target_attacked, 'name', 'Объект')} не имеет атрибута hero_health или health")
                continue

            # Получаем имена противника и атакуемого противником
            enemy_name = str(getattr(enemy, 'name', f'Противник_{i}'))
            target_attacked_name = str(getattr(target_attacked, 'name', f'Неизвестный'))

            # Проверка корректности значения атаки, должно быть целое число
            try:
                enemy_attack = int(getattr(enemy, 'attack', 0))
            except (ValueError, TypeError):
                enemy_attack = 0
                results.append(f"Предупреждение: у {enemy_name} некорректный attack")

            # Проверка корректности дальности атаки
            try:
                enemy_attack_range = int(enemy_attack_range)

                if enemy_attack_range <= 0:
                    results.append(f"Ошибка: дальность атаки {enemy_name} не может иметь отрицательные значения или равняться нулю!")
                    continue

            except (ValueError, TypeError) as e:
                results.append(f"Ошибка: неверное числовое значение ({enemy_name}): {e}")
                continue

            # Нанесение урона герою
            if enemy.distance == enemy_attack_range:
                # Получаем актуальное здоровье цели (важно для нескольких атак)
                current_health = getattr(target_attacked, health_attr, 0)
                new_health = current_health - enemy_attack
                setattr(target_attacked, health_attr, new_health)

                if target_attacked.is_alive():
                    results.append(f"{enemy_name} наносит {hp.RED}{enemy_attack}{hp.RESET} единиц урона {target_attacked_name} с дистанции "
                               f"{hp.RED}{enemy_attack_range}{hp.RESET}\nЗдоровье {hp.CYAN}{target_attacked_name}{hp.RESET} = {new_health}")
                else:
                    results.append(f"{enemy_name} атакует, но {target_attacked_name} уже мёртв.")
            else:
                continue

        results = "\n".join(results)
        return f"{hp.START_TIRE}{results}{hp.END_TIRE}"


    def move_enemies(self, *movement_groups):
        """
        Движение противников.

        Args:
            *movement_groups: группы в формате [enemy, steps, cmd, border]
                - enemy: объект противника с атрибутом distance
                - steps: целое число шагов
                - cmd: '+' для удаления, '-' для приближения
                - border: предельное расстояние:
                    * для '+' - максимальная дистанция (нельзя превысить)
                    * для '-' - минимальная дистанция (нельзя подойти ближе)
        """
        results = []

        for i, group in enumerate(movement_groups):
            # Проверка структуры группы
            if not isinstance(group, (list, tuple)) or len(group) < 4:
                results.append(f"Ошибка: группа {i} имеет неверный формат")
                continue

            enemy, steps, cmd, border = group[0], group[1], group[2], group[3]

            # Проверка объекта противника
            if enemy is None:
                results.append(f"Пропуск: группа {i} - противник не задан")
                continue

            if not hasattr(enemy, 'distance'):
                results.append(f"Ошибка: {getattr(enemy, 'name', 'Объект')} не имеет атрибута distance")
                continue

            # Получение имени противника для сообщений
            enemy_name = getattr(enemy, 'name', f'Противник_{i}')

            # Проверка корректности шагов и границы
            try:
                border = int(border)
                steps = int(steps)

                if steps < 0:
                    results.append(f"Ошибка: шаги не могут быть отрицательными ({enemy_name})")
                    continue
                elif steps == 0:
                    results.append(f"{enemy_name} не двигается")
                    continue

                if border < 1:
                    results.append(f"Ошибка: граница не может быть меньше 1 ({enemy_name})")
                    continue

            except (ValueError, TypeError) as e:
                results.append(f"Ошибка: неверное числовое значение ({enemy_name}): {e}")
                continue

            # Обработка движения
            current = enemy.distance

            if cmd == '+':
                # Для отдаления: new = min(текущее + шаги, граница)
                potential_new = current + steps
                new = min(border, potential_new)

                if new == border and border <= potential_new:
                    enemy.distance = border
                    results.append(f"{enemy_name} достиг предельной дистанции. Дистанция: {border}")
                else:
                    enemy.distance = new
                    if new == current:
                        results.append(f"{enemy_name} не может отдалиться дальше {border}. Дистанция: {current}")
                    else:
                        results.append(f"{enemy_name} отдалился на {new - current} шагов. Дистанция: {new}")

            elif cmd == '-':
                # Для приближения: new = max(текущее - шаги, граница, 1)
                # Где граница - минимальное расстояние, ближе которого нельзя подойти
                potential_new = current - steps
                new = max(border, potential_new, 1)  # Не меньше границы и не меньше 1

                if new == border and border >= potential_new:
                    enemy.distance = border
                    results.append(f"{enemy_name} достиг минимально допустимой дистанции. Дистанция: {border}")
                else:
                    enemy.distance = new
                    if new == current:
                        results.append(f"{enemy_name} не может приблизиться ближе {border}. Дистанция: {current}")
                    else:
                        results.append(f"{enemy_name} приблизился на {current - new} шагов. Дистанция: {new}")

            else:
                results.append(f"Ошибка: неизвестная команда '{cmd}' для {enemy_name}")

        results = "\n".join(results)
        return f"{hp.START_TIRE}{results}{hp.END_TIRE}"


    # Приблизить всех
    def move_all_enemies_closer(self, enemies, min_distance=1):
        """
            Движение всех противников вперед.
                enemies: список противников
                min_distance: целое число допустимой дистанции
        """
        for enemy in enemies:
            if getattr(enemy, 'health', 0) > 0 and getattr(enemy, 'distance', min_distance) > min_distance:
                enemy .distance -= 1

    # Отдалить всех
    def move_all_enemies_away(self, enemies, max_distance=4):
        """
            Движение всех противников вперед.
                enemies: список противников
                max_distance: целое число максимальной дистанции
                максимальная дистанция отдаления = 4 по умолчанию"""
        for enemy in enemies:
            if getattr(enemy, 'health', 0) > 0 and getattr(enemy, 'distance', max_distance) < max_distance:
                enemy.distance += 1


    # Найти всех живых противников, находящихся на заданной дистанции (по умолчанию — 1),
    # и подготовить их в формате, готовом к передаче в другие методы.
    def get_enemies_in_distance_attack(self,enemies, distance_attack=1):
        """Возвращает список кортежей (враг, дистанция_атаки=1 по умолчанию) для тех, кто рядом и жив."""
        return [
            (enemy, distance_attack) for enemy in enemies
            if getattr(enemy, 'health', 0) > 0 and getattr(enemy, 'distance', 999) == distance_attack
        ]
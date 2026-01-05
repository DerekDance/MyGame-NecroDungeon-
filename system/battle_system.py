from system import HelpSystem

# Для использования форматирования строк
hp = HelpSystem()

class BattleSystem:

    def move_enemies(self, *movement_groups):
        """
        Движение противников.
                - обьект: объект противника с атрибутом distance
                - шаги: целое число шагов
                - команда: '+' для удаления, '-' для приближения
        """
        results = []

        for i, group in enumerate(movement_groups):
            # Проверка структуры группы
            if not isinstance(group, (list, tuple)) or len(group) < 3:
                results.append(f"Ошибка: группа {i} имеет неверный формат")
                continue

            enemy, steps, cmd = group[0], group[1], group[2]

            # Проверка объекта противника
            if enemy is None:
                results.append(f"Пропуск: группа {i} - противник не задан")
                continue

            if not hasattr(enemy, 'distance'):
                results.append(f"Ошибка: {getattr(enemy, 'name', 'Объект')} не имеет атрибута distance")
                continue

            # Получение имени противника для сообщений
            enemy_name = getattr(enemy, 'name', f'Противник_{i}')

            # Проверка корректности шагов
            try:
                steps = int(steps)
                if steps < 0:
                    results.append(f"Ошибка: шаги не могут быть отрицательными ({enemy.name})")
                    continue
                elif steps == 0:
                    results.append(f"{enemy_name} не двигвется")
                    continue
            except (ValueError, TypeError):
                results.append(f"Ошибка: неверное значение шагов ({enemy_name})")
                continue

            # Обработка движения
            current = enemy.distance

            if cmd == '+':
                new = current + steps
                enemy.distance = new
                results.append(f"{enemy.name} отдалился на {steps} шагов. Дистанция: {new}")

            elif cmd == '-':
                new = max(1, current - steps)  # Минимальная дистанция = 1
                enemy.distance = new
                if new < current:
                    results.append(f"{enemy.name} приблизился на {steps} шагов. Дистанция: {new}")
                else:
                    results.append(f"{enemy.name} уже на минимальной дистанции: {new}")

            else:
                results.append(f"Ошибка: неизвестная команда '{cmd}' для {enemy.name}")

        results = "\n".join(results)
        return f"{hp.START_TIRE}{results}{hp.END_TIRE}"
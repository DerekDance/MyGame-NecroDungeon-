from system import HelpSystem


# Для использования форматирования строк
hp = HelpSystem()

"""
Класс Героя
"""
class Hero:
    def __init__(self):
        self.hero_health = 20
        self.hero_max_health = 20
        self.hero_attack = 3
        self.hero_range_attack = 6
        self.hero_gold = 1
        self.hero_potion_strength = 2
        self.hero_potion_heal = 0
        self.hero_potion_of_regen_hp = 3
        self.count_crit_attack  = 0
        self.hero_scroll_of_sparks = 10000
        self.hero_bullet = 3
        self.bullet_of_sparks = 0
        self.damage_bullet_of_sparks = 12
        self.regen_health_left = 0
        self.regen_ticks = 0

    # Процесс регенерации
    def process_regen(self):
        if self.regen_health_left > 0 and self.hero_health < self.hero_max_health:
            self.regen_ticks -= 1
            if self.regen_ticks <= 0:
                if self.hero_health < self.hero_max_health:
                    self.hero_health += 1
                    self.regen_health_left -= 1
                    self.regen_ticks = 4
                    print(f"(💊) {hp.PURPLE_BOLD}Вы восстановили 1 Здоровье\nЕще будет восстановлено: {self.regen_health_left}{hp.RESET}")
                else:
                    print(f"(💊) {hp.PURPLE_BOLD}Регенерация завершена (достигнут максимум здоровья){hp.RESET}")

    def shooting_with_spark_bullets(self, enemies):
        # Проверяем, что у героя есть патроны
        if self.bullet_of_sparks <= 0:
            print(f"{hp.START_TIRE}(📜) {hp.YELLOW_BOLD}У вас нет патронов искр{hp.RESET}{hp.END_TIRE}")
            return

        # Проверяем, является ли enemies списком или отдельным врагом
        if isinstance(enemies, list):
            # Если enemies - это список
            if not enemies:
                print(f"{hp.START_TIRE}(📜) {hp.YELLOW_BOLD}Нет врагов для атаки{hp.RESET}{hp.END_TIRE}")
                return
            # Можно пройтись по всем врагам или выбрать первого
            for enemy in enemies:
                if enemy.distance <= 3:  # Только в пределах досягаемости
                    if enemy.distance == 1:
                        enemy.health -= self.damage_bullet_of_sparks
                        enemy.distance += 1  # Откидываем врага при ближнем выстреле
                    elif enemy.distance == 2:
                        enemy.health -= self.damage_bullet_of_sparks // 2
                    elif enemy.distance == 3:
                        enemy.health -= self.damage_bullet_of_sparks // 4
                    print(
                        f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD}Вы выстрелили в {enemy.name or 'врага'}.{hp.RESET}"
                        f"{hp.info_room(self.hero_health, self.hero_max_health, enemies)}{hp.END_TIRE}")
                else:
                    print(
                        f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD}Выстрелом из ружья вы не наносите урон {enemy.name or 'врагу'}, слишком большое расстояние.{hp.RESET}"
                        f"{hp.info_room(self.hero_health, self.hero_max_health, enemies)}{hp.END_TIRE}")
        else:
            # Если enemies - это один враг
            enemy = enemies
            if enemy.distance <= 3:  # Только в пределах досягаемости
                if enemy.distance == 1:
                    enemy.health -= self.damage_bullet_of_sparks
                    enemy.distance += 1  # Откидываем врага при ближнем выстреле
                elif enemy.distance == 2:
                    enemy.health -= self.damage_bullet_of_sparks // 2
                elif enemy.distance == 3:
                    enemy.health -= self.damage_bullet_of_sparks // 4
                print(
                    f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD}Вы выстрелили в {enemy.name or 'врага'}.{hp.RESET}"
                    f"{hp.info_room(self.hero_health, self.hero_max_health, [enemy])}{hp.END_TIRE}")
            else:
                print(
                    f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD}Выстрелом из ружья вы не наносите урон {enemy.name or 'врагу'}, слишком большое расстояние.{hp.RESET}"
                    f"{hp.info_room(self.hero_health, self.hero_max_health, [enemy])}{hp.END_TIRE}")

        # Уменьшаем количество патронов после всех выстрелов
        self.bullet_of_sparks -= 1
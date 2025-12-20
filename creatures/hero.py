from system import HelpSystem

# Для использования форматирования строк
hp = HelpSystem()

"""
Класс Героя
"""
class Hero:
    def __init__(self,name = "Герой"):
        self.name = name
        self.hero_health = 10
        self.hero_max_health = 20
        self.hero_attack = 3
        self.hero_range_attack = 6
        self.hero_gold = 1
        self.hero_potion_strength = 2
        self.hero_potion_heal = 0
        self.hero_potion_of_regen_hp = 3
        self.count_crit_attack  = 0
        self.hero_scroll_of_sparks = 1
        self.hero_bullet = 3
        self.bullet_of_sparks = 0
        self.damage_bullet_of_sparks = 12
        self.modifiers = [ ] #Список модификаторов Героя

    #Добавление модификатора
    def add_modifier(self,modifier):
        modifier.target = self
        self.modifiers.append(modifier)
        modifier.activate()

    def update_all(self):
        """Обновить все модификаторы"""
        for modifier in self.modifiers[:]:
            if not modifier.active:
                self.modifiers.remove(modifier)
                continue

            if hasattr(modifier, 'apply_effect'):
                modifier.apply_effect()
            elif hasattr(modifier, 'update'):
                modifier.update()

    #Стрельба искрами
    def shooting_with_spark_bullets(self, enemies):
        if self.bullet_of_sparks <= 0:
            print(f"{hp.START_TIRE}(📜) {hp.YELLOW_BOLD}У вас нет патронов искр{hp.RESET}{hp.END_TIRE}")
            return

        # Нормализуем входные данные в список
        if not isinstance(enemies, list):
            enemies = [enemies]

        # Фильтруем только живых врагов
        alive_enemies = []
        for enemy in enemies:
            if enemy.is_alive():
                alive_enemies.append(enemy)

        if not alive_enemies:
            print(f"{hp.START_TIRE}(📜) {hp.YELLOW_BOLD}Нет живых врагов для атаки{hp.RESET}{hp.END_TIRE}")
            return

        targets_hit = 0
        for enemy in alive_enemies:
            if enemy.distance <= 3:  # Только в пределах досягаемости
                if enemy.distance == 1:
                    enemy.health -= self.damage_bullet_of_sparks
                    enemy.distance += 1  # Откидываем врага при ближнем выстреле
                elif enemy.distance == 2:
                    enemy.health -= self.damage_bullet_of_sparks // 2
                elif enemy.distance == 3:
                    enemy.health -= self.damage_bullet_of_sparks // 4

                targets_hit += 1
                print(
                    f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD}Вы выстрелили в {enemy.name or 'врага'}.{hp.RESET}"
                    f"{hp.info_room(self.hero_health, self.hero_max_health, enemies)}{hp.END_TIRE}")
            else:
                print(
                    f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD}Выстрелом из ружья вы не наносите урон {enemy.name or 'врагу'}, слишком большое расстояние.{hp.RESET}"
                    f"{hp.info_room(self.hero_health, self.hero_max_health, enemies)}{hp.END_TIRE}")

        # Уменьшаем количество патронов
        self.bullet_of_sparks -= 1
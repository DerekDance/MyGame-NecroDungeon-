from system import HelpSystem

# Для использования форматирования строк
hp = HelpSystem()
"""
Класс Героя
"""
class Hero:
    def __init__(self,name = "Герой"):
        self.name = name
        self.hero_health = 20
        self.hero_max_health = 20
        self.hero_attack = 3
        self.hero_range_attack = 6
        self.hero_gold = 1
        self.hero_potion_strength = 999
        self.hero_potion_heal = 0
        self.hero_potion_of_regen_hp = 999
        self.count_crit_attack  = 0 # НЕ НУЖНЫЙ ПАРАМЕТР
        self.hero_scroll_of_sparks = 999
        self.hero_bullet = 3
        self.bullet_of_sparks = 0
        self.damage_bullet_of_sparks = 12
        self.modifiers = [] #Список модификаторов Героя
        self.hero_type_attack = "melee" #Атака мечом(тип атаки) по умолчанию

    # Жив ли герой
    def is_alive(self) -> bool:
        return self.hero_health > 0

    #Проверка модификатора героя
    def has_active_modifier(self, modifier_name):
        for mod in self.modifiers:
            if mod.duration > 0 and getattr(mod, 'display_name', None) == modifier_name:
                return True, mod
        return False, None

    # Добавление модификатора героя
    def add_modifier(self, modifier):
        # Используем вспомогательный метод
        has_active, existing_mod = self.has_active_modifier(modifier.name)

        if has_active:
            # Можно показать информацию о существующем
            if modifier.show_message:
                print(f"{hp.YELLOW}Эффект Героя:'{modifier.display_name}' уже активен!{hp.RESET}")
                return False
            else:
                return False
        # Добавляем
        modifier.target = self
        self.modifiers.append(modifier)
        modifier.activate()
        return True

    #Обновление модификатора героя
    def update_all(self):
        for modifier in self.modifiers[:]:
            if not modifier.active:
                self.modifiers.remove(modifier)
                continue

            if hasattr(modifier, 'apply_effect'):
                is_finished = modifier.apply_effect()

                if is_finished:
                    self.modifiers.remove(modifier)


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
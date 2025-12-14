from system import HelpSystem


# Для использования форматирования строк
hp = HelpSystem()

"""
Класс Героя
"""
class Hero:
    def __init__(self):
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
        #Параметры для регенерации здоровья
        self.regen_timer = 0
        self.total_regen_hp = 0
        self.regen_delay = 0
        self.regen_per_tick = 0
        self.regen_active = False


    #Для установки параметров регенерации
    def start_regen(self,total_regen_hp,regen_delay,regen_per_tick):
        self.total_regen_hp = total_regen_hp
        self.regen_delay = regen_delay
        self.regen_per_tick = regen_per_tick
        self.regen_active = True

        #Регенерация здоровья
    def process_regen(self):
        if not self.regen_active:
            return
        elif self.total_regen_hp <= 0:
            self.regen_active = False
        elif self.total_regen_hp > 0 and self.hero_health < self.hero_max_health:
            if self.regen_timer < self.regen_delay:
                self.regen_timer += 1
            else:
                heal_amount = min(self.regen_per_tick ,self.hero_max_health - self.hero_health,self.total_regen_hp)
                self.hero_health += heal_amount
                self.total_regen_hp -= heal_amount
                self.regen_timer = 0
                print(f"(💊) {hp.PURPLE_BOLD}Вы восстановили {heal_amount} Здоровье\n"
                      f"Еще будет восстановлено: {self.total_regen_hp}{hp.RESET}")
        else:
            print(f"(💊) {hp.PURPLE_BOLD}Регенерация завершена (достигнут максимум здоровья){hp.RESET}")
            self.total_regen_hp = 0
            self.regen_active = False

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
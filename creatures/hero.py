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
        self.hero_scroll_of_sparks = 1
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
                    print(f"(💊) \u001b[35;1mВы восстановили 1 Здоровье\nЕще будет восстановлено: {self.regen_health_left}\u001b[0m")
                else:
                    print(f"(💊) \u001b[35;1mРегенерация завершена (достигнут максимум здоровья)\u001b[0m")

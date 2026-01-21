from system import RegenHP,DamageModifier,Projectile
from system import HelpSystem


hp = HelpSystem()

#########---Готовые шаблоны модификатора RegenHP---#########

# Создание зелья регенерации здоровья героя из инвентаря
def create_hero_potion_of_regen_hp(target):
        return RegenHP(
                target=target,
                duration=3,
                step=3,
                heal_power=1,
                show_message=True,
                display_name='Зелье регенерации здоровья'
            )

# Регенерация здоровья за кодовое слово
def create_low_regen_hp(target):
        return RegenHP(
            target=target,
            duration=10,
            step=5,
            heal_power=1,
            show_message=True,
            display_name='Остатки зелья регенерации здоровья'
        )

#########---Готовые шаблоны модификатора DamageModifier---#########

# Создание зелья силы героя из инвентаря
def create_hero_potion_of_strength(target):
        return DamageModifier(
                    target=target,
                    duration=5,
                    value=1.5,
                    operation_type = "*",
                    attack_type = "melee",
                    start_info_msg = f"{hp.CYAN_BOLD}(🗡️) Использовано Зелье силы",
                    show_message=True,
                    display_name = 'Зелье силы',
                )

# Дебафф "Загрязнение ствола" субстанции
def create_sub_debuff_ranged(target):
        return DamageModifier(
                    target=target,
                    duration=6,
                    value=5,
                    operation_type="-",
                    attack_type="ranged",
                    start_info_msg=f"{hp.START_TIRE}{hp.GREEN_BOLD}(🦠) Дебафф 'Загрязненный ствол' на",
                    show_message=False,
                    display_name='Загрязненный ствол'
                )

# Дебафф "Облепленный клинок" субстанции
def create_sub_debuff_melee(target):
        return DamageModifier(
                    target=target,
                    duration=6,
                    value=3,
                    operation_type="-",
                    attack_type="melee",
                    start_info_msg=f"{hp.START_TIRE}{hp.GREEN_BOLD}(🦠) Дебафф 'Облепленный клинок' на",
                    show_message=False,
                    display_name='Облепленный клинок'
                )


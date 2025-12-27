# -*- coding: utf-8 -*-
from creatures import *
from system import *
import sys
import threading
import random
import time



#Создаем противников
dummy = Dummy()
acolyte = Acolyte()
necro_student = NecroStudent()
sub = MainSubstance()
sub_mini1 = SubMini1()
sub_mini2 = SubMini2()
necromancer = Necromancer()

# Создание обьекта класса HelpSystem
hp = HelpSystem()

# Создание обьекта класса InventorySystem
inventory_system = InventorySystem()

# Создание обьекта класса InventorySystem
achievements_system = AchievementsSystem()
# Вызов ГЛАВНОГО МЕНЮ
achievements_system.main_menu()

name = achievements_system.current_player_name
#Создаем героя
hero = Hero(name = name)  # Передаем имя в конструктор

part_1 =""
part_2 =""
list_of_command =["в","н","а","р","п","у","о","с"]
hero_choice = ""

#Пропуск комнат для их тестирования по отдельности. Значение True, чтобы пропустить комнату, False - не пропускать.
pass_null_room = True
pass_first_room = True
pass_second_room = True
pass_three_room = True
pass_four_room_phase_one = False
pass_four_room_phase_two = False
pass_five_room_phase_one = False
pass_five_room_phase_two = False
pass_five_room_phase_three = False

#Переменные для достижений:
fast_as_hermes = 0   #для достижения 'спринтерского' прохождения игры
skull_shoot = 0# для достижения 'отстрел'
flag_skull_shoot = False # для достижения 'отстрел'
eat_for_mimic_backpack = False # для достижения 'голод'
flag_anti_mitoz = False #для достижения 'анти-митоз'

#Переменные используемые в: Подготовка - Заклинание "Реверс поступь"(5.3) и др.
cast_spell = 0 #для корректной работы прописываем число 0
time_action_hero_spell = 0 #время действия какого-либо навыка

####################
#Для получения награды за какое-либо достижение и все, что связано с достижениями.
action_hero = ""
used_commands = set()#для того, чтобы нельзя было ввести команду еще раз.
jokes_bonuses = ["(🏃‍♂️)Реактивное отступление:\n\n'Скорость принятия решений': +200%\n'Спринтерские качества': +150%\n'Чувство самосохранения': +300%","(🎯) Распознал угрозу Level 9000+\n\n'Инстинкт выживания': +250%\n'Зрение как у ястреба': +80%\n'Умение оценивать риски': +400%","(🧠) Не вступил в бой с арбалетчиком:\n\n'Мудрость': +500%\n'Тактическое мышление': +350%\n'Понимание что геройство ≠ суицид: +999%","(🗺️) Запомнил путь к выходу:\n\n'Пространственная память': +120%\n'Навык ориентации': +90%\n'Способность к быстрой эвакуации': +180%"]
def price():
    global action_hero, used_commands, flag_skull_shoot, eat_for_mimic_backpack, flag_anti_mitoz
    if action_hero in used_commands:
        print(f"{hp.START_TIRE}Команда {hp.CYAN}{action_hero}'{hp.RESET} уже использована!{hp.END_TIRE}")
        return
    if action_hero == "уверенность":
        print(f"{hp.START_TIRE}(🎁) Вы вернулись в подземелье с прокаченными характеристиками, ниже представлены эти характеристики.")
        print(f"{hp.START_TIRE}{random.choice(jokes_bonuses)}")
        used_commands.add("уверенность")
        low_regen = RegenHP(
            target=hero,
            duration=10,
            step=5,
            heal_power=1,
            show_message=True
        )
        hero.add_modifier(low_regen)
    elif action_hero == "абсурд":
        hero.count_crit_attack += 1
        print(f"{hp.START_TIRE}(🎁) Вы осознали(наверное),что не стоит сражаться с магическим зеркалом.\n{hp.YELLOW_STAR_START}(🎁) Первый ваш удар в новой игре будет с {hp.CYAN_BOLD} двойным уроном{hp.RESET}, желательно не бить по зеркалу.{hp.YELLOW_STAR_END}")
        used_commands.add("абсурд")
    elif action_hero == "отстрел":
        hero.hero_bullet += 1
        flag_skull_shoot = not flag_skull_shoot
        print(
            f"{hp.START_TIRE}(🎁) Вы получаете за отстрел черепов:\n{hp.YELLOW_STAR_START} -1 от максимальной атаки всех летающих черепов\n +1 к максимальной дистанции черепов до вас\n + 1 Пуля{hp.YELLOW_STAR_END}{hp.END_TIRE}")
        used_commands.add("отстрел")
    elif action_hero == "голод":
        eat_for_mimic_backpack = True
        print(
            f"{hp.START_TIRE}(🎁) Вы сделали заготовки из еды, чтобы в случае чего накормить {hp.PURPLE}'рюкзака-мимика'{hp.RESET}, если он попытается вас добить. Для себя перекус вы тоже сделали.{hp.END_TIRE}")
        used_commands.add("голод")
    elif action_hero == "антиделение":
        hero.hero_scroll_of_sparks += 1
        flag_anti_mitoz = not flag_anti_mitoz
        print(
            f"{hp.START_TIRE}(🎁) Чтобы легче было разбираться с противниками.Вы получаете.\n{hp.YELLOW_STAR_START} + 1 Свиток искр\n Здоровье Субстанции понижено на 2 единицы\n Здоровье Мерзкой субстанции понижено на 1 единицу\n Здоровье Склизкой субстанции понижено на 1 единицу{hp.YELLOW_STAR_END}{hp.END_TIRE}")
        used_commands.add("антиделение")
    elif action_hero == "гермес":
        print(f"{hp.START_TIRE}(⏳) Пока недоступна активация этой команды. Запомните ее и следите за обновлениями игры!{hp.END_TIRE}")
    elif action_hero == "time loop":
        print(f"{hp.START_TIRE}(⏳) Пока недоступна активация этой команды. Запомните ее и следите за обновлениями игры!{hp.END_TIRE}")
          	    
    	     	    
##################################

#Для работы "зелья силы" и hero.count_crit_attack НУЖНО БУДЕТ УДАЛИТЬ ПОСЛЕ ИЗМЕНЕНИЯ РАБОТЫ ЗЕЛИЙ СИЛЫ ВО ВСЕМ КОДЕ.
#ПРЕЖДЕ ЧЕМ УДАЛЯТЬ НЕОБХОДИМО ПЕРЕРАБОТАТЬ ДЕБАФФЫ СУБСТАНЦИИ В 4-ОЙ КОМНАТЕ(ПЕРВАЯ ФАЗА),
# И ПЕРЕРАБОТАТЬ ПОЛНОСТЬЮ 4-УЮ КОМНАТУ(ВТОРАЯ ФАЗА)
def crit():
	if hero.count_crit_attack < 0:
		hero.count_crit_attack = 0

##################################


#(4)Команда"у" для мерзкой субстанции(вторая фаза)
def dodge_sub_mini1():
	global action_hero,part_1
	if sub_mini1.distance == 1:
			hero.hero_health -= sub_mini1.attack
			part_1 = ("Вы пытаетесь увернуться от удара мерзкой субстанции, но все равно получаете урон.")
	elif sub_mini1.distance != 1:
			sub_mini1.distance -= 1
			part_1 =("Вы просто уворачиваетесь на месте, но мерзкая субстанция далеко от вас.Она подползает ближе к вам.")
#(4)Команда"у" для склизкой субстанции(вторая фаза)
def dodge_sub_mini2():
	global action_hero,part_2
	if sub_mini1.distance == 1:
			hero.hero_health -= sub_mini2.attack
			part_2 = ("Вы пытаетесь увернуться от удара склизкой субстанции, но все равно получаете урон.")
	elif sub_mini2.distance != 1:
			sub_mini2.distance -= 1
			part_2 =("Вы просто уворачиваетесь на месте, но склизкая субстанция далеко от вас.Она подползает ближе к вам.")
#(1)Стрельба с использованием "свитка искр" по Аколиту

#(4)Стрельба с использованием "свитка искр" по мерзкой субстанции
def sparks_four_room_sub_mini1():
	global part_1,part_2
	if sub_mini1.distance == 1:
		sub_mini1.health -= hero.damage_bullet_of_sparks
		hero.bullet_of_sparks -= 0.5
		part_1 = f"(📜)  {hp.YELLOW_BOLD}Вы нанесли значительный урон мерзкой субстанции."
	elif sub_mini1.distance == 2:
		sub_mini1.health -= (hero.damage_bullet_of_sparks // 2)
		hero.bullet_of_sparks -= 0.5
		part_1 = f"(📜)  {hp.YELLOW_BOLD}Вы нанесли урон мерзкой субстанции."
	elif sub_mini1.distance > 2:
		sub_mini1.health -= (hero.damage_bullet_of_sparks // 4)
		hero.bullet_of_sparks -= 0.5
		part_1 = f"(📜)  {hp.YELLOW_BOLD}Вы нанесли незначительный урон мерзкой субстанции."
#(4)Стрельба с использованием "свитка искр" по склизкой субстанции
def sparks_four_room_sub_mini2():
	global part_2
	if sub_mini2.distance == 1:
		sub_mini2.health -= hero.damage_bullet_of_sparks
		hero.bullet_of_sparks -= 0.5
		part_2 = "Вы нанесли значительный урон склизкой субстанции.Сноп искр озарил светом помещение."
	elif sub_mini2.distance == 2:
		sub_mini2.health -= (hero.damage_bullet_of_sparks // 2)
		hero.bullet_of_sparks -= 0.5
		part_2 = "Вы нанесли урон склизкой субстанции.Сноп искр озарил светом помещение."
	elif sub_mini2.distance > 2:
		sub_mini2.health -= (hero.damage_bullet_of_sparks // 4)
		hero.bullet_of_sparks -= 0.5
		part_2 = "Вы нанесли незначительный урон склизкой субстанции.Сноп искр озарил светом помещение."

"""(0) Привал у подземелья: Обучение"""

# Список ожидаемых команд в порядке прохождения обучения
expected_commands = ["в", "н", "п", "а", "у", "с", "о", "р"]

# Индекс текущего шага
step = 0

print(f"""{hp.START_TIRE}(⛺) Устроив привал не далеко от подземелья, ты возвёл примитивный манекен для отработки техник, которым тебя обучил наставник.\n(🔮) {hp.CYAN} Ричард{hp.RESET}, твой верный спутник,
 произнёс - {hp.CYAN}'Мудрое решение. Нам предстоит схватка с грозным противником. Мой опыт, добытый в боях, к твоим услугам — я буду направлять тебя, как смогу'.{hp.RESET}{hp.END_TIRE}""")
print(f"{hp.START_TIRE}(!) Для начала попробуйте сделать шаг вперед написав команду {hp.CYAN}'в'{hp.RESET}, а потом шаг назад, написав команду {hp.CYAN}'н'{hp.RESET}.\nНеобходимо писать только первую букву какой-либо команды.\n(!) Если не хотите проходить обучение введите {hp.RED}'выход'{hp.RESET}.{hp.END_TIRE}")

while hero.hero_health > 0:
    dummy.update_all()
    hero.update_all()
    price()
    if pass_null_room:
        break

    action_hero = input("Напишите какое действие вы хотите совершить(по русски):").lower().strip()
    print("\n\n\n\n\n\n")

    if action_hero == "выход":
        fast_as_hermes += 1
        achievements_system.add_completed_location("(0) Привал у подземелья", 1)
        print(f"{hp.START_TIRE}(⚡) {hp.YELLOW_BOLD} Вы стремительно вышли из обучения.{hp.RESET}{hp.END_TIRE}")
        break

    if action_hero == "обучен":
        hero.hero_gold += 1
        hero.hero_max_health += 1
        cast_spell = 2  # для совместимости с основной игрой (Аколит будет целиться)
        print(f"{hp.START_TIRE}(🎁) Вы получаете:\n{hp.YELLOW_STAR_START} + 1 к Максимальному здоровью.\n + 1 Золотую монету{hp.YELLOW_STAR_END}{hp.END_TIRE}")
        break

    # Если обучение уже завершено — выходим
    if step >= len(expected_commands):
        break

    if action_hero == expected_commands[step]:
        # Выполняем действие для текущего шага
        if step == 0:  # "в"
            dummy.distance -= 1
            print(f"{hp.START_TIRE}(!) Хорошо. Дистанция между манекеном уменьшилась.Теперь шаг назад(команда {hp.CYAN}'н'{hp.RESET}).{hp.info_room(hero.hero_health,hero.hero_max_health,[dummy])}{hp.END_TIRE}")

        elif step == 1:  # "н"
            dummy.distance += 1
            print(f"{hp.START_TIRE}(!) Хорошо. Дистанция между манекеном увеличилась.Таким образом можно сокращать дистанцию с противником для удара мечом или же увеличивать дистанцию для выстрелов из ружья. Еще можно уворачиваться от некоторых навыков противника.{hp.info_room(hero.hero_health,hero.hero_max_health,[dummy])}{hp.END_TIRE}")
            print(f"{hp.START_TIRE}(!) Теперь давайте вызовем команду помощь-справка {hp.CYAN}'п'{hp.RESET}, чтобы понять какие характеристики и предметы у нашего персонажа. Напишите в консоли слово справка.{hp.END_TIRE}")

        elif step == 2:  # "п"
            print(f"{hp.START_TIRE}(!) При вызове 'помощь-справки' ваш соратник {hp.CYAN}Ричард{hp.RESET} будет давать вам советы, содержание которых будет зависеть от комнаты в которой вы находитесь.\n(🔮) {hp.CYAN} Ричард - 'Пока советую тебе, просто пройти это обучение до конца'.{hp.RESET}")
            hp.show_full_help(hero)
            dummy.distance = 1
            print(f"{hp.START_TIRE}(!) Ну чтож пора навалять манекену. Напишите в консоли букву {hp.CYAN}'а'{hp.RESET}, чтобы атаковать манекена мечом.{hp.END_TIRE}")

        elif step == 3:  # "а"
            dummy.health -= hero.hero_attack
            print(f"{hp.START_TIRE}(!) Ударом меча вы расрутили манекен, похоже он попытается вас ударить.Введите команду {hp.CYAN}'у'{hp.RESET} в консоли, чтобы увернуться от удара.{hp.info_room(hero.hero_health,hero.hero_max_health,[dummy])}{hp.END_TIRE}")

        elif step == 4:  # "у"
            dummy.distance = 4
            print(f"{hp.START_TIRE}(!) Уворот от атаки манекена — это способ создать момент для контратаки. Используйте его, когда противник замахивается, чтобы он промахнулся и открылся для вашего удара.{hp.END_TIRE}")
            print(f"{hp.START_TIRE}(!) Вы отошли от манекена подальше и вытаскиваете ружье.Введите команду {hp.CYAN}'с'{hp.RESET} в консоли, чтобы стрелять из ружья в манекена.{hp.END_TIRE}")

        elif step == 5:  # "с"
            dummy.health -= hero.hero_range_attack
            print(f"{hp.START_TIRE}(!) Выстрелом вы попадаете в манекена.\n(🔮) {hp.CYAN} Ричард - 'Отличный выстрел'.{hp.RESET}{hp.END_TIRE}")
            print(f"{hp.START_TIRE}(!) Количество пуль ограничено, чтобы посмотреть сколько пуль осталось у героя необходимо ввести команду 'п'(помощь-справка).Следите за количеством пуль, иначе противник может воспользоваться, вашей попыткой выстрелить без пуль.{hp.END_TIRE}")
            print(f"{hp.START_TIRE}(!) Стрелять можно только с дистанции больше двух шагов.{hp.END_TIRE}")
            print(f"{hp.START_TIRE}(!) Кажется вы не взяли из рюкзака больше пуль.Введите команду осмотр-поиск {hp.CYAN}'о'{hp.RESET}, чтобы найти в рюкзаке пули.{hp.END_TIRE}")

        elif step == 6:  # "о"
            print(f"{hp.START_TIRE}(!) Команда 'поиск' нужна для обыскивания комнат, анализа ситуации в бою.{hp.END_TIRE}")
            print(f"{hp.START_TIRE}(!) Необходимо проверить все снаряжение в рюкзаке. Введите последнюю команду {hp.CYAN}'р'{hp.RESET}.{hp.END_TIRE}")

        elif step == 7:  # "р"
            print(f"{hp.START_TIRE}(!) С помощью команды 'р'(рюкзак) можно использовать предметы облегчающие прохождение игры.\n(❤️‍🩹){hp.GREEN_BOLD}Зелье лечения востанавливает 5 очков здоровья, больше максимального здоровья восстановить не сможет.{hp.RESET}\n(🗡️)  {hp.CYAN_BOLD}Зелье силы увеличивает одну атаку в два раза.Эффект от всех выпитых зельев силы суммируется.\nКритическая атака пропадет только когда вы нанесете урон по чему-то(промахи в счет).{hp.RESET}\n(📜)  {hp.YELLOW_BOLD}Свиток искр нужен для того, стобы ружье стреляло дробью.Чем меньше дистанция до противника тем больше урон.{hp.RESET}\n(💊) {hp.PURPLE_BOLD} Зелье регенерации здоровья позволит вам восстановить здоровье через какое-то количество ходов.Регенерация не пропадает при переходе в последующие локации.{hp.RESET}\n(!) Есть еще важный момент. Как только вы побеждаете противника(у противника здоровье ноль или меньше нуля),то вам можно написать что угодно или нажать enter, чтобы перейти в следующую локацию.{hp.END_TIRE}")

        # Переход к следующему шагу
        step += 1

        # Проверка: обучение завершено?
        if step == len(expected_commands):
            print(f"{hp.START_TIRE}(🔮) {hp.CYAN} Ричард - 'Ты готов! Ты сможешь одолеть Некроманта!'.{hp.RESET}Ричард вернулся в небольшой магический шар в вашей руке, так как он заточен Некромантом в этом артефакте.{hp.END_TIRE}")
            hero.hero_gold += 1
            hero.hero_max_health += 1
            achievements_system.add_completed_location("(0) Привал у подземелья", 1)
            achievements_system.add_achievement(achievements_system.character_data, "TRAINED", 1)
            cast_spell = 2  # для совместимости (чтобы Аколит сразу целился)
            print(f"{hp.START_TIRE}(🎖) Получено достижение {hp.CYAN}'Я прочитал инструкцию!'{hp.RESET}\n\n(🎁) Поздравляю вы прошли обучение и знаете основы игры.\n(🎁) За прохождение обучения вы получаете небольшой подарок:\n{hp.YELLOW_STAR_START} + 1 к Максимальному здоровью.\n + 1 Золотую монету{hp.YELLOW_STAR_END}\n(!) Чтобы в начале следующей игры получить сразу подарок(без обучения), напишите команду {hp.CYAN_BOLD}'обучен'{hp.RESET}.{hp.END_TIRE}")

    else:
        # Неправильная команда на текущем шаге
        print(f"{hp.START_TIRE}(!) Вы делаете что-то не так{hp.END_TIRE}")

#########################

"""(1) Темный коридор: Бой с Аколитом"""

# Начальная справка
print(
            f"{hp.YELLOW}В игре есть девять активных действий.Вводить нужно только первую букву(есть исключения) команды:\n"
            f"""- в (вперед)            - н (назад)                  - у (увернуться)\n- а (атака мечом)       - с (стрельба из ружья)      - о (осмотр-поиск)\n- п (помощь-справка)    - р (рюкзак)                 - искры(выстрел дробью){hp.RESET}{hp.YELLOW_STAR_END}""")



not_attack = [0, 1, -1]  # дистанции, на которых Аколит не может атаковать

print(
    f"{hp.START_TIRE}В узком коридоре вы замечаете фигуру в оборванном плаще, которая направляет арбалет на вас.\n"
    f"Коридор имеет множественные пустые углубления, в которых можно будет укрыться от выстрелов.{hp.END_TIRE}"
)

while hero.hero_health > 0:
    try:
        acolyte.update_all()
        hero.update_all()
        price()

        if pass_first_room:
            break

        # Обновляем состояние Аколита каждый ход
        acolyte.update(3,1)

        # Показываем фазу зарядки
        if acolyte.charge_turns == 1:
            print(f"{hp.START_TIRE}(🏹) Аколит судорожно пытается достать болт из сумки, чтобы зарядить арбалет.{hp.END_TIRE}")
        elif acolyte.charge_turns == 2:
            print(f"{hp.START_TIRE}(🏹) Аколит зарядил арбалет.{hp.END_TIRE}")
        elif acolyte.charge_turns == 3:
            print(f"{hp.START_TIRE}(🏹) Аколит целится в вас из арбалета.{hp.END_TIRE}")

        # Получаем действие игрока
        action_hero = input("Напишите какое действие вы хотите совершить (по-русски): ").lower()
        print("\n\n\n")

        # Проверка: Аколит побеждён?
        if not acolyte.is_alive():
            hp.reset_all_help()
            hero.hero_gold += 1
            hero.hero_scroll_of_sparks += 1
            achievements_system.add_killed_monster("Аколит",2)
            achievements_system.add_completed_location("(1) Темный коридор", 2)
            print(
                f"{hp.GREEN}(*) С последним ударом Аколит упал замертво. Вы подняли золотую монету...\n"
                f"(*) Вы одолели Аколита!{hp.YELLOW}\n{hp.YELLOW_STAR_START} + 1 Золотая монета.\n + 1 'Свиток Искр.'{hp.YELLOW_STAR_END}"
            )
            print(
                f"{hp.START_TIRE}Войдя в открытую дверь дальше по коридору, вы закрываете дверь.\n"
                f"При беглом осмотре угрозы вы никакой не заметили для себя.{hp.END_TIRE}"
            )
            break

        # Нестандартные выходы
        elif acolyte.distance < -1:
            fast_as_hermes += 1
            achievements_system.add_completed_location("(1) Темный коридор", 2)
            print(f"{hp.START_TIRE}(⚡) {hp.YELLOW_BOLD}Захлопнув за собой металлическую дверь, вы просто сбежали от Аколита...{hp.RESET}{hp.END_TIRE}")
            break

        elif acolyte.distance > 8:
            achievements_system.add_achievement(achievements_system.character_data, "BYPASSING", 2)
            print(
                f"{hp.GREEN}(*) Получив какое-то количество болтов в спину, вы вышли из подземелья, "
                f"поняв, что быть искателем приключений вам не хочется.{hp.END_TIRE}\033[0m"
            )
            print(
                f"{hp.START_TIRE}(🎁) Вы прошли игру нестандартным способом. Введите в следующей игре "
                f"{hp.CYAN_BOLD}'уверенность'{hp.RESET}, чтобы получить небольшой бонус.\n"
                f"(🎁) Удачи в следующей игре!{hp.END_TIRE}"
            )
            sys.exit()

        # АТАКА АКОЛИТА (если он готов стрелять и герой не уклонился)
        if acolyte.can_active(3) and action_hero != "у" and acolyte.distance not in not_attack:
            hero.hero_health -= acolyte.attack
            acolyte.reset_charge()  # сброс заряда после выстрела
            print(f"{hp.START_TIRE}(🏹) Аколит попадает в вас из арбалета и наносит вам урон.{hp.info_room(hero.hero_health,hero.hero_max_health,[acolyte])}{hp.END_TIRE}")

        # Обработка действий игрока

        # Выстрел дробью "искры"
        elif action_hero == "искры" and hero.bullet_of_sparks > 0:
            hero.shooting_with_spark_bullets(acolyte)

        elif action_hero == "с":
            if hero.hero_bullet <= 0:
                print(f"{hp.START_TIRE} Похоже, у вас закончились патроны.{hp.info_room(hero.hero_health,hero.hero_max_health,[acolyte])}{hp.END_TIRE}")
            elif hero.hero_bullet > 0 and acolyte.distance > 2:
                hero.hero_bullet -= 1
                acolyte.health -= hero.hero_range_attack
                print(f"{hp.START_TIRE} Вы попадаете из ружья в Аколита.{hp.info_room(hero.hero_health,hero.hero_max_health,[acolyte])}{hp.END_TIRE}")
            else:
                print(f"{hp.START_TIRE} Такая дистанция не позволяет сделать выстрел.{hp.info_room(hero.hero_health,hero.hero_max_health,[acolyte])}{hp.END_TIRE}")

        elif action_hero == "в":
            acolyte.distance -= 1
            print(f"{hp.START_TIRE} Вы двигаетесь вперёд.{hp.info_room(hero.hero_health,hero.hero_max_health,[acolyte])}{hp.END_TIRE}")

        elif action_hero == "н":
            acolyte.distance += 1
            print(f"{hp.START_TIRE} Вы двигаетесь назад.{hp.info_room(hero.hero_health,hero.hero_max_health,[acolyte])}{hp.END_TIRE}")

        elif action_hero == "а":
            if acolyte.distance in not_attack:
                acolyte.distance += 1
                acolyte.health -= hero.hero_attack
                print(f"{hp.START_TIRE} Вы поражаете своим мечом Аколита. Он делает шаг назад.{hp.info_room(hero.hero_health,hero.hero_max_health,[acolyte])}{hp.END_TIRE}")
            else:
                print(f"{hp.START_TIRE} Вы рассекаете воздух мечом.{hp.info_room(hero.hero_health,hero.hero_max_health,[acolyte])}{hp.END_TIRE}")

        elif action_hero == "о":
            print(f"{hp.START_TIRE}(🔍) Ничего примечательного кроме Аколита с арбалетом вы не заметили.{hp.info_room(hero.hero_health,hero.hero_max_health,[acolyte])}{hp.END_TIRE}")

        elif action_hero == "п":
            hp.show_full_help(hero)

        elif action_hero == "р":
            inventory_system.open_backpack(hero)

        # Недопустимая дистанция для выстрела Аколита (без атаки)
        elif acolyte.distance in not_attack:
            print(f"{hp.START_TIRE}(🏹) Аколит не может выстрелить с такого расстояния.{hp.info_room(hero.hero_health,hero.hero_max_health,[acolyte])}{hp.END_TIRE}")

        # Уворачивание от выстрела (если Аколит целится, но герой уклонился)
        elif action_hero == "у":
            if acolyte.can_active(3):
                acolyte.reset_charge()
                print(f"{hp.START_TIRE}(🏹) Благодаря углублениям в стенах вам удаётся увернуться от выстрела из арбалета.{hp.info_room(hero.hero_health,hero.hero_max_health,[acolyte])}{hp.END_TIRE}")
            else:
                print(f"{hp.START_TIRE} Вы просто уворачиваетесь на месте.{hp.info_room(hero.hero_health,hero.hero_max_health,[acolyte])}{hp.END_TIRE}")

        else:
            print(f"{hp.START_TIRE}Неизвестная команда.{hp.END_TIRE}")

    except Exception as e:
        print(f"Возникла какая-то ошибка: {hp.RED_BOLD}{e}{hp.RESET}")
else:
    print(f"{hp.START_TIRE}(☠️) Похоже вы погибли от переизбытка арбалетных болтов в организме.{hp.END_TIRE}")
    sys.exit()

"""(2) Комната с наспех брошенными вещами"""

#Счетчик для повторений команды "о".
count_search = 0

#Счетчик для повторений команды "рывок" и начала боя
count_dash = 0
start_fight = 0
ready_bluff = False #обманный маневр Ученика-некроманта
bluff_lines = [
    "(🧟‍♂) Ученик резко взмахивает руками... но ничего не происходит.",
    "(🧟‍♂) Он хрипло произносит заклинание... но ничего не происходит.",
    "(🧟‍♂) Мертвец делает резкий жест и усмехается.",
    "(🧟‍♂) Под ногами будто дрогнула тень... но это лишь иллюзия.",
    "(🧟‍♂) Воздух на миг становится тяжёлым... похоже на уловку.",
    "(🧟‍♂) Он кричит неизвестные слова, но ничего не происходит — видимо, проверяет вашу реакцию.",
    "(🧟‍♂) Ему не хватает сил — ритуал прерывается. Возможно он имитирует атаку.",
    "(🧟‍♂) Вы чувствуете ложный холод под ногами... но это всего лишь игра на нервы."
]

while hero.hero_health > 0:
    action_hero = input("Напишите какое действие вы хотите совершить(по русски): ").lower()
    print("\n\n\n\n\n\n")
    necro_student.update_all()
    hero.update_all()
    if pass_second_room == True:
        break

    # Обновляем состояние Ученика-некроманта каждый ход, но после НАЧАЛА боя
    if start_fight == 1:
        necro_student.update(4, 1)

    ###########
    # Для работы советов до начала боя
    if start_fight == 0:
        hp.help_states["help_second_room_before_fight"] = True
        hp.help_states["help_second_room_in_fight"] = False  # Выключаем боевые подсказки

    # Для работы советов во время боя
    elif start_fight == 1:
        hp.reset_all_help()  # Сначала выключаем все
        hp.help_states["help_second_room_in_fight"] = True  # Затем включаем только боевые
    ###########

    ###########
    # (2) Навык "Могильный хват" Ученика-некроманта
    if ready_bluff == True:
        if action_hero in ("в", "н","у"):
            necro_student.charge_turns = 3  # увеличиваем скорость заряда, если блеф сработал
            print(f"{hp.START_TIRE}(🧟‍♂) {hp.PURPLE}Вы попытались как-то увернуться от возможного заклинания, но это был блеф.\n"
                  f" Скорость заряда заклинания 'Могильный хват' увеличена.\n"
                  f"Ученик-некроманта усмехается над вами.{hp.RESET} {hp.END_TIRE}")
        ready_bluff = False


    elif necro_student.charge_turns == 1 and start_fight == 1:
        if random.random() < 0.5:  # 50% шанс
            print(f"{hp.START_TIRE}{random.choice(bluff_lines)}{hp.END_TIRE}")
            ready_bluff = True
        else:
            print(f"{hp.START_TIRE}(🧟‍♂) {hp.PURPLE}Руки Ученика-некроманта начинают тускло светятся фиолетовым светом.{hp.RESET}{hp.END_TIRE}")

    elif necro_student.charge_turns == 2:
        print(f"{hp.START_TIRE}(🧟‍♂) {hp.PURPLE}Ученик-некроманта использует какое-то неизвестное заклинание.{hp.RESET}{hp.END_TIRE}")
    elif necro_student.charge_turns == 3:
        print(f"{hp.START_TIRE}(🧟‍♂) {hp.PURPLE}Под вашими ногами начинает шевелиться земля...{hp.RESET}{hp.END_TIRE}")

    if not necro_student.is_alive() and count_dash != 3:
        count_dash = 0  # сброс count_dash для следующих комнат
        count_search = 0  # сброс count_search для следующих комнат
        hero.hero_potion_heal += 1
        achievements_system.add_killed_monster("Ученик-некромант",2)
        achievements_system.add_completed_location("(2) Комната с наспех брошенными вещами", 2)
        print(f"{hp.START_TIRE}{hp.GREEN}(*)С последним ударом вашего клинка тело Ученика-некроманта обмякло на полу подземелья, обыскав труп вы нашли зелье лечения.\n(*)Вы одолели Ученика-некроманта !\033[0m\n{hp.YELLOW}*********\nЗелье лечения +1\n**********\033[0m{hp.END_TIRE}")
        break
    ###########

#(2)Нестандартный способ прохождения
    if action_hero== "в" and count_dash == 3 and start_fight == 0:
        count_dash = 0#сброс count_dash для следующих комнат
        count_search = 0#сброс count_search для следующих комнат
        hero.hero_potion_heal += 1
        fast_as_hermes += 1
        achievements_system.add_completed_location("(2) Комната с наспех брошенными вещами", 2)
        print(f"{hp.START_TIRE}(⚡) {hp.YELLOW_BOLD} Плечом вы выбиваете дверь, как раз припечатав к стенке, затаившегося Ученика-некроманта.Он отключился. Вы обыскали его и пошли дальше...{hp.RESET}\n{hp.YELLOW}*********\nЗелье лечения +1\n**********{hp.RESET}{hp.END_TIRE}")
        break
    #(2)Работа заклинания "Могильный хват"
    elif action_hero == "н" and necro_student.can_active(4) and start_fight == 1:
        necro_student.reset_charge()
        ready_bluff = False
        print(f"{hp.START_TIRE}(🧟‍♂) {hp.PURPLE}Сделав шаг назад вам удалось увернуться от рук мертвецов, вырвавшихся из под земли.Руки исчезают в земле.Ученик-некроманта подходит ближе.{hp.RESET}{hp.info_room(hero.hero_health,hero.hero_max_health,[necro_student])}{hp.END_TIRE}")
    elif action_hero == "в" and necro_student.can_active(4) and start_fight == 1:
        necro_student.reset_charge()
        ready_bluff = False
        print(f"{hp.START_TIRE}(🧟‍♂) {hp.PURPLE}Сделав шаг вперед вам удалось увернуться от рук мертвецов, вырвавшихся из под земли.Руки исчезают в земле.Ученик-некроманта делает шаг назад.{hp.RESET}{hp.info_room(hero.hero_health,hero.hero_max_health,[necro_student])}{hp.END_TIRE}")
    elif necro_student.can_active(4) and start_fight == 1:
        necro_student.reset_charge()
        ready_bluff = False
        hero.hero_health -= necro_student.attack
        print(f"{hp.START_TIRE}(🧟‍♂) {hp.PURPLE}Руки мертвецов вырываются из под земли и наносят вам урон.Руки исчезают в земле.{hp.RESET}{hp.info_room(hero.hero_health,hero.hero_max_health,[necro_student])}{hp.END_TIRE}")

    #(2)Команда "о"
    if action_hero == "о" and count_search == 0 and start_fight != 1:
        count_search += 1
        print(f"{hp.START_TIRE}(🔍) Осматриваясь в комнате, вы замечаете наспех брошенные вещи, капли крови на полу и различные полупыстые сумки. В комнате довольно таки темно и лишь свеча на столе, тусклым светом освещает пространство вокруг. Возможно стоит повнимательнее здесь все осмотреть.{hp.END_TIRE}")
    elif action_hero == "о" and count_search == 1 and start_fight != 1:
        count_search += 1
        hero.hero_potion_strength += 1
        hero.hero_gold += 1
        print(f"{hp.START_TIRE}(🔍) Подойдя ближе к столу вы замечаете лежащую монету, какое-то зелье и блокнот с открытыми страницами. Если хотите прочитать записи введите команду - поиск.{hp.END_TIRE}{hp.YELLOW_STAR_START}Золото +1\nЗелье силы +1{hp.YELLOW_STAR_END}")
    elif action_hero == "о" and count_search == 2 and start_fight != 1:
        count_search += 1
        print(f"{hp.START_TIRE}(🔍) Просматривая текст вы нашли любопытные строки\n...в результате ритуалов удалось создать некую субстанцию из останков жертв,которая подчиняется создателю. При нанесении увечий субстанции, было обнаружено, что она делится на части и спустя короткое время пред нами предстало две субстанции.При нанесении единого сокрушительного удара субстанция распадалась и темная магия исчезала в ней...\nВам слышится какой-то шорох позади... {hp.END_TIRE}")
    elif action_hero != "у" and count_search == 3 and start_fight == 0:
        necro_student.distance = 2
        start_fight = 1
        hero.hero_health -= necro_student.attack
        print(f"{hp.START_TIRE}Продолжая искать что-то примечательное вы не замечаете, Ученика-некроманта,который сразу же метнул в вас нож \nУченик-некроманта подходит ближе к вам и собирается сделать выпад с кинжалом.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[necro_student])}")
    elif action_hero == "о" and count_search == 3 and necro_student.distance == 2 and start_fight == 1:
        hero.hero_health -= necro_student.attack
        print(f"{hp.START_TIRE}Пока вы что-то разглядываете, Ученик-некроманта делает подшаг с выпадом, наносит вам урон и делает шаг обратно.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[necro_student])}")

    #(2)Команда "у"
    elif action_hero == "у" and count_search != 3 and start_fight == 0:
        print(f"{hp.START_TIRE}Вы просто уворачиваетесь на месте. Ничего не происходит.{hp.END_TIRE}")
    elif action_hero == "у" and necro_student.distance != 2 and start_fight == 0:
        start_fight = 1
        necro_student.distance = 2
        print(f"{hp.START_TIRE}Используя какое-то внутренее чутье или же просто удачу вам удалось увернуться от летящего ножа.\nУченик-некроманта подходит ближе к вам и собирается сделать удар с подшагом.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[necro_student])}")

    #(2) Команда "а"
    elif action_hero == "а" and count_search != 3 and start_fight == 0:
            print(f"{hp.START_TIRE}Вы просто рассекаете воздух мечом. Ничего не происходит.{hp.END_TIRE}")

    elif action_hero == "а" and count_search == 3 and necro_student.distance == 2 and start_fight == 1:
            hero.hero_health -= necro_student.attack
            print(f"{hp.START_TIRE}Вы взмахнули мечом, но не попали, так как Ученик-некроманта стоит вне досягаемости вашей атаки. В свою очередь он сделал подшаг и наносит удар кинжалом.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[necro_student])}")

    elif action_hero == "а" and count_search == 3 and necro_student.distance == 1 and start_fight == 1:
            necro_student.health -= hero.hero_attack
            necro_student.distance += 1
            print(f"{hp.START_TIRE}Взмахом меча вы поражаете Ученика-некроманта. Получив увечья он отшатнулся и сделал шаг назад.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[necro_student])}")

    #(2) Команда "искры" с использованием свитка искр
    elif action_hero == "искры":
        if start_fight == 0 and hero.bullet_of_sparks >= 1:
            necro_student.health -= hero.damage_bullet_of_sparks // 4
            hero.bullet_of_sparks -= 1
            start_fight = 1
            count_search = 3
            print(f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD}Выхватив ружье вы стреляете прямо в стол.Из дула вылетает сноп искр. Вдребезги разлетается какая-то склянка, летают в воздухе страницы блокнота. Притаившийся Ученик-некроманта, получает частично урон от разлетевшейся дроби.Он шагнул к вам с кинжалом наготове. {hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[necro_student])}")
        else:
            hero.shooting_with_spark_bullets(necro_student)


    #(2) Команда "с" (обычная)
    elif action_hero == "с" and start_fight == 0:
        hero.hero_bullet -= 1
        start_fight = 1
        necro_student.distance -= 1
        count_search = 3
        print(f"{hp.START_TIRE}Выхватив ружье вы стреляете прямо в стол. Вдребезги разлетается какая-то склянка, летают в воздухе страницы блокнота.От неожиданности, притаившийся Ученик-некроманта, замешкался и промахивается, бросая в вас нож.Он шагнул к вам с кинжалом наготове. {hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[necro_student])}")
    elif action_hero == "с" and start_fight == 1 and necro_student.distance == 1:
        hero.hero_health -= necro_student.attack
        necro_student.distance += 1
        print(f"{hp.START_TIRE}Не получится выстрелить с такого близкого расстояния. В свою очередь Ученик-некроманта бьет вас кинжалом и делает шаг назад.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[necro_student])}")
    elif action_hero == "с" and start_fight == 1 and necro_student.distance == 2:
        hero.hero_health -= necro_student.attack
        print(f"{hp.START_TIRE}Не получится выстрелить с такого близкого расстояния. В свою очередь Ученик-некроманта делает подшаг и бьет вас кинжалом.После он отходит от вас на шаг.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[necro_student])}")

    #(2) Команда "п"
    elif action_hero == "п":
        hp.show_full_help(hero)

    #(2) Команды "в" и "н" до боя
    elif action_hero == "в" and count_search != 3 and start_fight == 0:
        count_dash += 1
        print(f"{hp.START_TIRE}Вы делаете резкий рывок, в надежде войти в схватку с возможным противником, но ничего не происходит.{hp.END_TIRE}")
    elif action_hero == "н" and count_search != 3 and start_fight == 0:
        print(f"{hp.START_TIRE}Вы делаете шаг назад, но ничего не происходит.{hp.END_TIRE}")
    elif action_hero == "у" and count_search == 3 and necro_student.distance == 2 and start_fight == 1:
        necro_student.distance -= 1
        print(f"{hp.START_TIRE}Сделав выпад с подшагом некромант пытается нанести вам урон, но вы ловко уворачиваетесь от его кинжала.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[necro_student])}")
    elif action_hero == "н" and count_search == 3 and necro_student.distance in (1, 2):
        print(f"{hp.START_TIRE}Вы делаете шаг назад, а Ученик-некроманта ловко реагирует и делает рывок в вашу сторону. Можно так с ним долго кружить по комнате.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[necro_student])}")
    elif action_hero == "в" and count_search == 3 and necro_student.distance in (1, 2):
        print(f"{hp.START_TIRE}Вы делаете рывок в сторону Ученика-некроманта, а он в свою очередь ловко реагирует и делает рывок в обратную сторону. Можно так с ним долго кружить по комнате.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[necro_student])}")

    #(2) Рюкзак
    elif action_hero == "р":
        inventory_system.open_backpack(hero)

    else:
        print(f"{hp.START_TIRE}Неизвестная команда.{hp.END_TIRE}")

else:
    print(f"{hp.START_TIRE}☠️Похоже вы погибли от многократных ударов кинжалом{hp.END_TIRE}")
    sys.exit()


"""(3) Помещение с зеркалом: Зеркало-торговец"""

# Ассортимент магазина
mirror_heartfruit = 1
mirror_stone_of_sharpness = 1
mirror_potion_strength = 1
mirror_potion_of_regen_hp = 1
mirror_food = 1
hero_choice = ""

# Счетчики действий
count_dodge = 0
count_dash = 0
count_search = 0

print(f"{hp.START_TIRE}(🪞) Двигаясь дальше вы замечаете стоящее волшебное зеркало.\n"
      f" Вы раньше о нем слышали, зеркало позволяет менять золото на какие-либо предметы.\n"
      f" Для покупки необходимо ввести - {hp.CYAN}купить а потом номер предмета{hp.RESET}.{hp.END_TIRE}")

while hero.hero_health > 0:
    action_hero = input("Напишите какое действие вы хотите совершить(по русски): ")
    print("\n\n\n\n\n\n")

    # (3) Подсказки соратника
    hp.reset_all_help()  # сброс всех значений на False
    hp.help_states["help_three_room"] = True  # Включаем подсказки третьей комнаты

    hero.update_all()

    if pass_three_room:
        break

    # (3) Торговля с зеркалом
    elif action_hero == "купить":
        print(f"""{hp.START_TIRE}Предметы для покупки:

(0) Введите 0, чтобы выйти из меню торговли.

(1) (💖) {hp.RED} Сердцефрукт{hp.RESET} - 1 {hp.YELLOW}Золотая монета{hp.RESET}
Количество: {mirror_heartfruit}
- прибавляет 3 очка к максимальному здоровью и восстанавливает немного здоровья

(2) (🪨) {hp.CYAN} Волшебный камень остроты{hp.RESET} - 2 {hp.YELLOW}Золотые монеты{hp.RESET}
Количество: {mirror_stone_of_sharpness}
- увеличивает урон персонажа на 1

(3) (🗡️) {hp.CYAN_BOLD} Зелье силы{hp.RESET} - 2 {hp.YELLOW}Золотые монеты{hp.RESET}
Количество: {mirror_potion_strength}
- увеличивает одну атаку в два раза.

(4) (💊) {hp.PURPLE_BOLD} Зелье регенерации здоровья{hp.RESET} - 1 {hp.YELLOW}Золотая монета{hp.RESET}
Количество: {mirror_potion_of_regen_hp}
- восстанавливает здоровье через определенное количество ходов.

(5) (🍖) {hp.YELLOW_BOLD} Полевой набор еды{hp.RESET} - 1 {hp.YELLOW}Золотая монета{hp.RESET}
Количество: {mirror_food}
- восстанавливает 3 единицы здоровья.{hp.END_TIRE}""")

        while hero_choice != "0":
            try:
                hero_choice = str(input(f"{hp.START_TIRE}Напишите номер предмета, который вы хотите купить: {hp.END_TIRE} "))
                if hero_choice == "0":
                    print(f"{hp.START_TIRE}(!) Вы перестали торговать с зеркалом.{hp.END_TIRE}")
                elif hero_choice == "1" and hero.hero_gold >= 1:
                    if mirror_heartfruit > 0:
                        mirror_heartfruit -= 1
                        hero.hero_max_health += 3
                        hero.hero_health += 1
                        hero.hero_gold -= 1
                        print(f"{hp.YELLOW_STAR_START}(💖) Вы купили Сердцефрукт:\nВаше здоровье: {hero.hero_health}|{hero.hero_max_health}\nВаше золото: {hero.hero_gold}{hp.YELLOW_STAR_END}")
                    else:
                        print(f"{hp.START_TIRE}(💖) Сердцефрукты закончились.{hp.END_TIRE}")
                elif hero_choice == "2" and hero.hero_gold >= 2:
                    if mirror_stone_of_sharpness > 0:
                        mirror_stone_of_sharpness -= 1
                        hero.hero_attack += 1
                        hero.hero_gold -= 2
                        print(f"{hp.YELLOW_STAR_START}(🪨) Вы купили Волшебный камень остроты:\nВаша атака: {hero.hero_attack}\nВаше золото: {hero.hero_gold}{hp.YELLOW_STAR_END}")
                    else:
                        print(f"{hp.START_TIRE}(🪨) Волшебные камни остроты закончились.{hp.END_TIRE}")
                elif hero_choice == "3" and hero.hero_gold >= 2:
                    if mirror_potion_strength > 0:
                        mirror_potion_strength -= 1
                        hero.hero_potion_strength += 1
                        hero.hero_gold -= 2
                        print(f"{hp.YELLOW_STAR_START}(🗡️) Вы купили Зелье силы:\nЗелье силы: {hero.hero_potion_strength}\nВаше золото: {hero.hero_gold}{hp.YELLOW_STAR_END}")
                    else:
                        print(f"{hp.START_TIRE}(🗡️) Зелья силы закончились.{hp.END_TIRE}")
                elif hero_choice == "4" and hero.hero_gold >= 1:
                    if mirror_potion_of_regen_hp > 0:
                        mirror_potion_of_regen_hp -= 1
                        hero.hero_potion_of_regen_hp += 1
                        hero.hero_gold -= 1
                        print(f"{hp.YELLOW_STAR_START}(💊) Вы купили Зелье регенерации здоровья:\nЗелье регенерации здоровья: {hero.hero_potion_of_regen_hp}\nВаше золото: {hero.hero_gold}{hp.YELLOW_STAR_END}")
                    else:
                        print(f"{hp.START_TIRE}(💊) Зелья регенерации здоровья закончились.{hp.END_TIRE}")
                elif hero_choice == "5" and hero.hero_gold >= 1:
                    if mirror_food > 0:
                        mirror_food -= 1
                        hero.hero_health = min(hero.hero_health + 3, hero.hero_max_health)
                        hero.hero_gold -= 1
                        print(f"{hp.YELLOW_STAR_START}(🍖) Вы купили Полевой набор еды:\n+ 3 к Здоровью\nВаше здоровье: {hero.hero_health}|{hero.hero_max_health}\nВаше золото: {hero.hero_gold}{hp.YELLOW_STAR_END}")
                    else:
                        print(f"{hp.START_TIRE}(🍖) Полевые наборы еды закончились.{hp.END_TIRE}")
                else:
                    print(f"{hp.START_TIRE}Не хватает денег или неправильная команда.{hp.END_TIRE}")
            except:
                print("Возникла какая-то ошибка")
        else:
            hero_choice = ""

    # (3) Награда за многократное нажатие "у"
    elif action_hero == "у" and count_dodge == 0:
        count_dodge += 1
        print(f"{hp.START_TIRE}(🪞) Вы просто уворачиваетесь смотря в зеркало, ваше отражение уворачивается вместе с вами{hp.END_TIRE}")
    elif action_hero == "у" and count_dodge == 1:
        count_dodge += 1
        print(f"{hp.START_TIRE}(🪞) Вы делаете сначала уворот влево, а потом и вправо. Ваше отражение повторяет за вами. Вы точно хотите продолжить этим заниматься ?{hp.END_TIRE}")
    elif action_hero == "у" and count_dodge == 2:
        count_dodge += 1
        hero.hero_range_attack += 2
        print(f"{hp.START_TIRE}(🪩) Вы продолжаете делать увороты при этом {hp.CYAN_BOLD} добавив хлопки к каждому движению рук и двигая ритмично ногами под какую-то слышимую только вам музыку{hp.RESET}.Ваше отражение повторяет за вами, до определенного момента, пока не решило в вас запустить книгой прям из зеркала. Вам не сильно больно, да и книга это была необычная, а {hp.CYAN_BOLD}'Руководство модернизации порохового оружия'{hp.RESET}.Вам удалось разобраться в ней и теперь ваше ружье наносит больше урона.{hp.END_TIRE}\n{hp.YELLOW}**********\n(📙) 'Руководство модернизации порохового оружия'\n+ 2 к Атаке в дальнем бою\nВаша атака в дальнем бою: {hero.hero_range_attack}\n**********{hp.RESET}")
    elif action_hero == "у" and count_dodge == 3:
        print(f"{hp.START_TIRE}(🪞) Вы пытаетесь повторить тоже самое, но ничего не происходит.{hp.END_TIRE}")

    # (3) Многократное нажатие действия "в" и выход из комнаты
    elif action_hero == "н":
        if count_dash == 0:
            count_dash -= 1
            print(f"{hp.START_TIRE}(🪞) Вы решили отойти от зеркала на шаг.{hp.END_TIRE}")
        elif count_dash == -1:
            print(f"{hp.START_TIRE}(🪞) Может стоит подойти к зеркалу поближе?{hp.END_TIRE}")
        else:
            print(f"{hp.START_TIRE}(🪞) Спиной вы уперлись в стену.{hp.END_TIRE}")
    elif action_hero == "в":
        if count_dash == -1:
            count_dash += 1
            print(f"{hp.START_TIRE}(🪞) Вы делаете шаг вперед.{hp.END_TIRE}")
        elif count_dash == 0:
            count_dash += 1
            print(f"{hp.START_TIRE}(🪞) Вы просто решили сделать рывок к зеркалу, вы стоите почти в упор к нему.{hp.END_TIRE}")
        elif count_dash == 1:
            count_search = 0  # сброс count_search
            count_dash = 0
            count_dodge = 0
            achievements_system.add_completed_location("(3) Помещение с зеркалом", 1)
            print(f"{hp.START_TIRE}{hp.GREEN}(*) Сделав рывок вы прошли сквозь зеркало и как-то оказались в другой комнате.{hp.RESET}{hp.END_TIRE}")
            break

    # (3) Команда "о" и повтор этой команды
    elif action_hero == "о" and count_search == 0:
        count_search += 1
        print(f"{hp.START_TIRE}(🪞) В комнате вы не нашли выхода. Это тупик.{hp.END_TIRE}")
    elif action_hero == "о" and count_search == 1:
        hero.hero_health = min(hero.hero_health + 2, hero.hero_max_health)
        count_search += 1
        print(f"{hp.START_TIRE}(💊) Вы нашли небольшой набор медицины на столике рядом с зеркалом. Обработав свои раны и перевязав их вы востановили себе здоровье.{hp.END_TIRE}\n{hp.YELLOW}**********\n+ 2 к Здоровью\nВаше здоровье: {hero.hero_health}|{hero.hero_max_health}\n**********{hp.RESET}")
    elif action_hero == "о" and count_search == 2:
        print(f"{hp.START_TIRE}(🪞) Вы ничего примечательного не находите.{hp.END_TIRE}")

    # (3) Команда "а" и ее последствия
    elif action_hero == "а" and count_dash == 0:
            print(f"{hp.START_TIRE}Вы размахиваетесь мечом.Ничего не происходит.{hp.END_TIRE}\n{hp.YELLOW}**********\nВаше здоровье: {hero.hero_health}|{hero.hero_max_health}\n**********{hp.RESET}")
    elif action_hero == "а" and count_dash == 1:
            hero.hero_health -= hero.hero_attack
            print(f"{hp.START_TIRE}Вы размахиваетесь мечом и бьете по зеркалу, половина меча исчезает в зеркале, ваше отражение делает тоже самое и вы чувствуете как ваш же меч вас ранит.{hp.END_TIRE}\n{hp.YELLOW}**********\nВаше здоровье: {hero.hero_health}|{hero.hero_max_health}\n**********{hp.RESET}")

    # (3) Команда "искры" с использованием свитка искр
    elif action_hero == "искры" and hero.bullet_of_sparks >= 1:
        hero.hero_health -= hero.damage_bullet_of_sparks
        hero.bullet_of_sparks -= 1
        print(f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD}Вы наставляете ружье и стреляете. Ваше отражение делает тоже самое.Вы получили урон от выстрела ружья раскаленной дробью.Это довольно-таки больно.{hp.END_TIRE}{hp.YELLOW_STAR_START}Ваше здоровье: {hero.hero_health}|{hero.hero_max_health}{hp.YELLOW_STAR_START}")

    # (3) Команда "с" и ее последствия
    elif action_hero == "с" and hero.hero_bullet > 0:
        hero.hero_health -= hero.hero_range_attack
        hero.hero_bullet -= 1
        print(f"{hp.START_TIRE}Вы наставляете ружье и стреляете. Ваше отражение делает тоже самое.Вы получили урон от выстрела ружья.{hp.END_TIRE}\n{hp.YELLOW}**********\nВаше здоровье: {hero.hero_health}|{hero.hero_max_health}\n**********{hp.RESET}")

    # (3) Команда "п"
    elif action_hero == "п":
        hp.show_full_help(hero)

    # (3) Здесь прописан рюкзак для 3-ой комнаты
    elif action_hero == "р":
        inventory_system.open_backpack(hero)

else:
    achievements_system.add_achievement(achievements_system.character_data, "SUICIDE", 1)
    print(f"{hp.START_TIRE}(☠️) Вы мертвы. Вы забили себя своим же мечом досмерти или застрелили себя.{hp.END_TIRE}")
    print(f"{hp.START_TIRE}(🎖) Получено достижение {hp.CYAN}'Самоубийство из вредности'{hp.RESET}\n\n Введите в следующей игре {hp.CYAN}'абсурд'{hp.RESET},чтобы получить утешительный приз.{hp.END_TIRE}")
    sys.exit()


"""(4) Древний зал: Субстанция"""

the_substance_strikes_msg = ""  # Сообщение показывающие наносит ли удар субстанция при sub_init = True
lock_backpack = False  # заблокированный рюкзак героя
sub_init = False  # инициатива Субстанции переходит к ней после вашего удара
split_msg = 0  # сообщение о скором разделении
split_health = range(1, 10)  # диапазон разделения субстанции
defeat_of_sub = 0  # счетчик поражения субстанции
print(f"{hp.START_TIRE}Пройдя через зеркало вы оказались в зале какой-то древней цивилизации, впереди виднеется проход, арка которого украшена вырезанными неизвестными символами.\n"
      f" Проход преграждает некая субстанция, собранная из множества тел.\n"
      f" Услышав звук со стороны зеркала она медленно движется в вашу сторону.{hp.END_TIRE}")
if flag_anti_mitoz == True:
    sub.health = 28
else:
    sub.health = 300

# (4) Бой с единственной субстанцией
while sub.health not in split_health:
    sub_debuff = None  # Дебафф Субстанции
    # Обновление состояний (модификаторы, здоровье и т.д.)
    sub.update_all()
    hero.update_all()

    if pass_four_room_phase_one:
        break

    # Подсказки соратника
    hp.reset_all_help()
    hp.help_states["help_fourth_room_phase_one"] = True

    # Ввод действия
    action_hero = input("Напишите какое действие вы хотите совершить(по русски): ").lower().strip()
    print("\n\n\n\n\n\n")

    # Специальные условия выхода
    if count_dash == 3:
        count_search = 0
        fast_as_hermes += 1
        achievements_system.add_completed_location("(4) Древний зал", 2)
        print(f"{hp.START_TIRE}(⚡) {hp.YELLOW_BOLD}Вам удалось пройти через арку в следующее помещение.{hp.RESET}{hp.END_TIRE}")
        break

    if sub.health <= 0:
        defeat_of_sub += 1
        count_search = 0
        hero.hero_bullet += 2
        achievements_system.add_killed_monster("Субстанция", 2)
        achievements_system.add_completed_location("(4) Древний зал", 2)
        achievements_system.add_achievement(achievements_system.character_data, "ANTI_MITOZ", 3)
        print(f"{hp.START_TIRE}{hp.GREEN}(*) Субстанция на ваших глазах распадается и исчезает вместе с темной магией.\n{hp.RESET}\n"
              f"(🎖) Получено достижение {hp.CYAN}'Анти-митоз'{hp.RESET}. Введите в следующей игре {hp.CYAN}'антиделение'{hp.RESET}, чтобы получить награду.\n"
              f"{hp.YELLOW_STAR_START} + 2 Пули{hp.YELLOW_STAR_END}{hp.END_TIRE}")
        break

    if hero.hero_health <= 0:
        print(f"{hp.START_TIRE}☠️ Вы погибли. Вас поглотила субстанция.{hp.END_TIRE}")
        sys.exit()

    # Предупреждение о разделении
    if sub.health < 16 and split_msg == 0:
        split_msg += 1
        print(f"{hp.START_TIRE}Создается впечатление, что субстанция хочет разделиться...{hp.END_TIRE}")

    # Основная обработка действий
    handled = False  # флаг: было ли действие обработано

    # --- Атака мечом ("а") ---
    if action_hero == "а":
        handled = True
        if sub.distance != 1:
            print(
                f"{hp.START_TIRE}Слишком далеко, чтобы атаковать мечом!{hp.info_room(hero.hero_health, hero.hero_max_health, [sub])}{hp.END_TIRE}")
        else:
            #  Проверка: активен ли ЛЮБОЙ дебафф оружия?
            any_weapon_debuff = (hero.has_active_modifier("Облепленный клинок")[0] or
                                 hero.has_active_modifier("Загрязненный ствол")[0])

            if not any_weapon_debuff:
                sub_debuff = DamageModifier(
                    target=hero,
                    duration=6,
                    value=3,
                    operation_type="-",
                    attack_type="melee",
                    start_info_msg=f"{hp.GREEN_BOLD}(🦠) Ваш меч покрылся слоем слизи. Ваша атака мечом снизилась.",
                    end_info_msg=f"{hp.GREEN_BOLD}(🦠) Эффект ослабления 'Облепленный клинок' для",
                    display_name="Облепленный клинок"
                )
                print(f"{hp.START_TIRE}(🦠) {hp.GREEN_BOLD}Ваш меч покрылся слоем слизи. Ваша атака мечом снизилась.{hp.RESET}{hp.END_TIRE}")
            #  РАСЧЁТ УРОНА — ВНЕ ЗАВИСИМОСТИ от создания дебаффа
            current_attack = hero.hero_attack
            for mod in hero.modifiers:
                if mod.active and mod.attack_type == "melee" and mod.operation_type == "-":
                    current_attack -= mod.value
            current_attack = max(current_attack, 0)

            lock_backpack = True

            if not sub_init:
                # Первый удар: Субстанция не бьёт в ответ
                sub.health -= current_attack
                sub_init = True
                print(
                    f"{hp.START_TIRE}Вы наносите урон Субстанции мечом. Субстанция задрожала от недовольства.{hp.info_room(hero.hero_health, hero.hero_max_health, [sub])}{hp.END_TIRE}")
            else:
                # Последующие удары: Субстанция бьёт в ответ
                sub.health -= current_attack
                hero.hero_health -= sub.attack
                print(
                    f"{hp.START_TIRE}Вы наносите урон Субстанции мечом, но она бьет вас в ответ. Она продолжает яростно дрожать.{hp.info_room(hero.hero_health, hero.hero_max_health, [sub])}{hp.END_TIRE}")

    # --- Выстрел из ружья ("с") ---
    elif action_hero == "с":
        handled = True
        if hero.hero_bullet <= 0:
            print(
                f"{hp.START_TIRE}Похоже, у вас закончились пули.{hp.info_room(hero.hero_health, hero.hero_max_health, [sub])}{hp.END_TIRE}")
        else:
            if sub.distance <= 1:
                # Слишком близко — выстрел невозможен
                hero.hero_health -= sub.attack
                print(
                    f"{hp.START_TIRE}Субстанция бьет вас, как только вы пытаетесь выстрелить с такого расстояния.{hp.info_room(hero.hero_health, hero.hero_max_health, [sub])}{hp.END_TIRE}")
            else:
                #  Проверка: активен ли ЛЮБОЙ дебафф оружия?
                any_weapon_debuff = (hero.has_active_modifier("Облепленный клинок")[0] or
                                     hero.has_active_modifier("Загрязненный ствол")[0])

                if sub.distance > 2 and not any_weapon_debuff:
                    sub_debuff = DamageModifier(
                        target=hero,
                        duration=6,
                        value=5,
                        operation_type="-",
                        attack_type="ranged",
                        start_info_msg=f"{hp.GREEN_BOLD}(🦠) После выстрела Субстанция сделала стремительный плевок. Ваше ружье в слизи. Ваша дальняя атака снизилась.",
                        end_info_msg=f"{hp.GREEN_BOLD}(🦠) Эффект ослабления 'Загрязненный ствол' для",
                        display_name="Загрязненный ствол"
                    )
                    print(
                        f"{hp.START_TIRE}{hp.GREEN_BOLD}(🦠) После выстрела Субстанция сделала стремительный плевок. Ваше ружье в слизи.{hp.RESET}{hp.END_TIRE}")

                #  РАСЧЁТ УРОНА — ВСЕГДА, с учётом ВСЕХ активных дебаффов
                current_range_attack = hero.hero_range_attack
                for mod in hero.modifiers:
                    if mod.active and mod.attack_type == "ranged" and mod.operation_type == "-":
                        current_range_attack -= mod.value
                current_range_attack = max(current_range_attack, 0)

                lock_backpack = True

                #  НАНЕСЕНИЕ УРОНА И РАСХОД ПУЛЬ
                sub.health -= current_range_attack
                hero.hero_bullet -= 1

                # Логика инициативы Субстанции
                if not sub_init:
                    # Первый выстрел: Субстанция приближается, но не бьёт
                    sub.distance = max(sub.distance - 1, 1)
                    sub_init = True
                    print(
                        f"{hp.START_TIRE}Сделав выстрел из ружья, вы попадаете по субстанции. Она движется вам навстречу.{hp.info_room(hero.hero_health, hero.hero_max_health, [sub])}{hp.END_TIRE}")
                else:
                    # Последующие выстрелы: Субстанция реагирует агрессивно
                    if sub.distance > 2:
                        sub.distance = max(sub.distance - 2, 1)
                        print(
                            f"{hp.START_TIRE}{hp.GREEN_BOLD}Сделав выстрел из ружья, вы попадаете по субстанции. Субстанция делает стремительный рывок в вашу сторону, абсурдный для её массы.{hp.info_room(hero.hero_health, hero.hero_max_health, [sub])}{hp.END_TIRE}")
                    else:
                        # Уже рядом — бьёт и отталкивает
                        hero.hero_health -= sub.attack
                        sub.distance = min(sub.distance + 1, 5)
                        print(
                            f"{hp.START_TIRE}{hp.GREEN_BOLD}(🦠) Субстанция делает стремительный рывок в вашу сторону и врезается в вас, отталкивая и нанося урон.{hp.info_room(hero.hero_health, hero.hero_max_health, [sub])}{hp.END_TIRE}")

    # --- Прочие команды ---
    elif action_hero == "в":  # вперёд
        handled = True
        if sub.distance > 1:
            sub.distance -= 1
            print(f"{hp.START_TIRE}Вы делаете шаг вперёд.{hp.info_room(hero.hero_health, hero.hero_max_health, [sub])}{hp.END_TIRE}")
        else:
            hero.hero_health -= sub.attack
            sub.distance += 1
            print(f"{hp.START_TIRE}Пытаясь обойти субстанцию, она бьет вас, отталкивая от себя.{hp.info_room(hero.hero_health, hero.hero_max_health, [sub])}{hp.END_TIRE}")

    elif action_hero == "н":  # назад
        handled = True
        if sub.distance > 1:
            sub.distance += 1
            print(f"{hp.START_TIRE}Вы двигаетесь назад.{hp.info_room(hero.hero_health, hero.hero_max_health, [sub])}{hp.END_TIRE}")
            # Логика нестандартного прохождения
            if sub.distance > 3:
                if count_dash == 0:
                    count_dash = 1
                    print(f"{hp.START_TIRE}Вы отходите назад, но опираетесь на стену, вы движетесь вдоль стены.{hp.END_TIRE}")
                elif count_dash == 1:
                    count_dash = 2
                    print(f"{hp.START_TIRE}Вы двигаетесь аккуратно вдоль стены, субстанция очень медленно движется к вам, отодвигаясь от прохода, который ведёт дальше в подземелье.{hp.END_TIRE}")
                elif count_dash == 2:
                    count_dash = 3
                    print(f"{hp.START_TIRE}Вы продолжаете двигаться вдоль стены. Выход уже совсем рядом.{hp.END_TIRE}")
            else:
                count_dash = 0  # сброс, если расстояние <= 3
        else:
            # sub.distance == 1
            sub.distance += 1
            sub_init = False  # сброс инициативы при отходе
            print(f"{hp.START_TIRE}Вы увернулись от удара субстанции, сделав шаг назад. Субстанция перестала дрожать.{hp.info_room(hero.hero_health, hero.hero_max_health, [sub])}{hp.END_TIRE}")

    elif action_hero == "у":  # увернуться
        handled = True
        if sub.distance == 1:
            hero.hero_health -= sub.attack
            sub.distance += 1
            print(f"{hp.START_TIRE}Вы пытаетесь увернуться от удара субстанции, но она всегда бьет непредсказуемо. Вы получаете урон и вас немного откидывает.{hp.info_room(hero.hero_health, hero.hero_max_health, [sub])}{hp.END_TIRE}")
        else:
            print(f"{hp.START_TIRE}Вы просто уворачиваетесь на месте.{hp.info_room(hero.hero_health, hero.hero_max_health, [sub])}{hp.END_TIRE}")

    elif action_hero == "о":  # осмотреться
        handled = True
        if count_search == 0:
            count_search += 1
            print(f"{hp.START_TIRE}Ничего примечательного вы не видите. Только очень медленно двигающуюся субстанцию.{hp.END_TIRE}")
        elif count_search == 1:
            count_search += 1
            hero.hero_bullet += 2
            print(f"{hp.START_TIRE}Вы обнаружили в углу комнаты ружье, рядом с которым лежали патроны.\n{hp.YELLOW_STAR_START}{hp.YELLOW} +2 Пули\nКоличество пуль: {hero.hero_bullet}{hp.RESET}{hp.YELLOW_STAR_END}{hp.END_TIRE}")
        else:
            print(f"{hp.START_TIRE}Больше вы ничего не обнаружили.{hp.END_TIRE}")

    elif action_hero == "р":  # рюкзак
        handled = True
        if lock_backpack:
            if sub.distance > 1:
                lock_backpack = False
                sub.distance -= 1
                print(f"{hp.START_TIRE}(🦠) {hp.GREEN_BOLD}Ненадолго отвернувшись, вы попытались вскрыть сумку, но слизь намертво склеила её. Пришлось забыть о снаряжении и вернуться к бою. Субстанция подползает ближе.{hp.RESET}{hp.info_room(hero.hero_health, hero.hero_max_health, [sub])}{hp.END_TIRE}")
            else:
                hero.hero_health -= sub.attack
                sub.distance += 2
                print(f"{hp.START_TIRE}(🦠) {hp.GREEN_BOLD}Пока вы пытались открыть сумку, субстанция наносит вам урон и отбрасывает вас от себя.{hp.RESET}{hp.info_room(hero.hero_health, hero.hero_max_health, [sub])}{hp.END_TIRE}")
        else:
            inventory_system.open_backpack(hero)

    elif action_hero == "п":  # помощь
        handled = True
        hp.show_full_help(hero)

    else:
        print(f"{hp.START_TIRE}Неизвестная команда.{hp.END_TIRE}")
        handled = True

    # Применение дебаффа (если создан)
    if sub_debuff is not None:
        hero.add_modifier(sub_debuff)
        sub_debuff = None  # сброс

else:
    count_search = 0
    print(f"{hp.START_TIRE}(🦠) {hp.GREEN_BOLD}Субстанция раздвоилась после вашей атаки.\n"
          f"Теперь перед вами две субстанции поменьше.{hp.RESET}{hp.END_TIRE}")
# (4) Вторая фаза сражения

sub_mini_init = 0  # очки подготовки ударов субстанций
if flag_anti_mitoz:
    sub_mini1.health = 8
    sub_mini2.health = 10
else:
    sub_mini1.health = 9
    sub_mini2.health = 11

while sub_mini1.health > 0 or sub_mini2.health > 0:
    sub_mini1.update_all()
    sub_mini2.update_all()
    hero.update_all()
    if pass_four_room_phase_two:
        break

    # (4) Подсказки соратника
    hp.reset_all_help()
    hp.help_states["help_fourth_room_phase_two"] = True

    # (4) Обработка критического удара
    crit()

    if count_dash == 3:  # нестандартный выход
        break
    if sub.health <= 0:
        break
    if hero.hero_health <= 0:
        print(f"{hp.START_TIRE}☠️Вас поглотили.Вы погибли.{hp.END_TIRE}")
        break

    action_hero = input("Напишите какое действие вы хотите совершить(по русски): ").lower()
    print("\n\n\n\n\n\n")

    # (4) Команда "а" (атака мечом)
    if action_hero == "а":
        target = input(f"{hp.START_TIRE}Выберите кого вы будете атаковать мечом(введите цифру):\n(1){sub_mini1.name}\n(2){sub_mini2.name}{hp.END_TIRE}").lower()
        if target == "1" and sub_mini1.health <= 0:
            print(f"{hp.START_TIRE}Похоже вы одолели мерзкую тварь.\nЗдоровье {sub_mini1.name}: {sub_mini1.health}{hp.END_TIRE}")
        elif target == "2" and sub_mini2.health <= 0:
            print(f"{hp.START_TIRE}Похоже вы одолели склизкую тварь.\nЗдоровье {sub_mini2.name}: {sub_mini2.health}{hp.END_TIRE}")
        elif target == "1" and sub_mini1.distance != 1 and sub_mini2.distance == 1:
            if hero.count_crit_attack > 0:
                hero.hero_health -= sub_mini2.attack
                sub_mini1.distance -= 1
                hero.count_crit_attack -= 1
                print(f"{hp.START_TIRE}(🗡️)  {hp.CYAN_BOLD}Вы попытались нанести удар заряженным мечом по мерзкой субстанции, но не достали до нее.Заряд на мече пропал.{hp.RESET}Склизкая субстанция бьет вас.Мерзкая субстанция подползает ближе к вам.{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}{hp.END_TIRE}")
            else:
                hero.hero_health -= sub_mini2.attack
                sub_mini1.distance -= 1
                print(f"{hp.START_TIRE}Вы попытались нанести удар мечом по мерзкой субстанции, но не достали до нее.Склизкая субстанция бьет вас.Мерзкая субстанция подползает ближе к вам.{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}{hp.END_TIRE}")
        elif target == "2" and sub_mini2.distance != 1 and sub_mini1.distance == 1:
            if hero.count_crit_attack > 0:
                hero.hero_health -= sub_mini1.attack
                sub_mini2.distance -= 1
                hero.count_crit_attack -= 1
                print(f"{hp.START_TIRE}(🗡️)  {hp.CYAN_BOLD}Вы попытались нанести удар заряженным мечом по склизкой субстанции, но не достали до нее.Заряд на мече пропал.{hp.RESET}.Мерзкая субстанция бьет вас.Склизкая субстанция подползает ближе к вам.{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}{hp.END_TIRE}")
            else:
                hero.hero_health -= sub_mini1.attack
                sub_mini2.distance -= 1
                print(f"{hp.START_TIRE}Вы попытались нанести удар мечом по склизкой субстанции, но не достали до нее.Мерзкая субстанция бьет вас.Склизкая субстанция подползает ближе к вам.{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}{hp.END_TIRE}")
        elif target in ("1", "2") and sub_mini1.distance > 1 and sub_mini2.distance > 1:
            if hero.count_crit_attack > 0:
                sub_mini1.distance -= 1
                sub_mini2.distance -= 1
                hero.count_crit_attack -= 1
                print(f"{hp.START_TIRE}(🗡️)  {hp.CYAN_BOLD}Вы рассекаете воздух заряженным мечом.Заряд на мече пропал.{hp.RESET}Обе субстанции подползают ближе к вам.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
            else:
                sub_mini1.distance -= 1
                sub_mini2.distance -= 1
                print(f"{hp.START_TIRE}Вы рассекаете воздух мечом.Обе субстанции подползают ближе к вам.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
        elif target == "1" and sub_mini1.distance == 1:
            damage_mult = 3 if sub_mini2.health <= 0 and sub_mini_init == 1 else 2
            sub_mini1.health -= hero.hero_attack * damage_mult
            if sub_mini2.health > 0 and sub_mini2.distance == 1:
                hero.hero_health -= sub_mini2.attack
            elif sub_mini2.health <= 0:
                hero.hero_health -= sub_mini1.attack
            sub_mini_init = 1
            if hero.count_crit_attack > 0:
                hero.count_crit_attack -= 1
            print(f"{hp.START_TIRE}(🗡️)  {hp.CYAN_BOLD}Вы наносите урон мерзкой субстанции ударом {'заряженного' if hero.count_crit_attack < 1 else 'мечом'}.{hp.RESET}{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
        elif target == "2" and sub_mini2.distance == 1:
            damage_mult = 3 if sub_mini1.health <= 0 and sub_mini_init == 1 else 2
            sub_mini2.health -= hero.hero_attack * damage_mult
            if sub_mini1.health > 0 and sub_mini1.distance == 1:
                hero.hero_health -= sub_mini1.attack
            elif sub_mini1.health <= 0:
                hero.hero_health -= sub_mini2.attack
            sub_mini_init = 1
            if hero.count_crit_attack > 0:
                hero.count_crit_attack -= 1
            print(f"{hp.START_TIRE}(🗡️)  {hp.CYAN_BOLD}Вы наносите урон склизкой субстанции ударом {'заряженного' if hero.count_crit_attack < 1 else 'мечом'}.{hp.RESET}{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")

    # (4) Команда "с" с использованием свитка искр
    elif action_hero == "искры" and hero.bullet_of_sparks >= 1:
        sparks_four_room_sub_mini1()
        sparks_four_room_sub_mini2()
        print(f"{hp.START_TIRE}{part_1 + part_2}{hp.END_TIRE}{hp.info_room(hero.hero_health, hero.hero_max_health, [sub_mini1, sub_mini2])}")
        continue

    # (4) Команда "с" (обычная стрельба)
    elif action_hero == "с":
        if hero.hero_bullet <= 0:
            print(f"{hp.START_TIRE}У вас кончились патроны.{hp.END_TIRE}")
        else:
            range_target = input(f"{hp.START_TIRE}Выберите в кого вы будете стрелять(введите цифру):\n(1){sub_mini1.name}\n(2){sub_mini2.name}{hp.END_TIRE}").lower()
            if range_target == "1" and sub_mini1.health <= 0:
                print(f"{hp.START_TIRE}Похоже вы одолели мерзкую тварь.\nЗдоровье {sub_mini1.name}: {sub_mini1.health}{hp.END_TIRE}")
            elif range_target == "2" and sub_mini2.health <= 0:
                print(f"{hp.START_TIRE}Похоже вы одолели склизкую тварь.\nЗдоровье {sub_mini2.name}: {sub_mini2.health}{hp.END_TIRE}")
            elif range_target == "1" and sub_mini1.distance < 3:
                print(f"{hp.START_TIRE}Слишком близкое расстояние для выстрела.{hp.END_TIRE}")
            elif range_target == "2" and sub_mini2.distance < 3:
                print(f"{hp.START_TIRE}Слишком близкое расстояние для выстрела.{hp.END_TIRE}")
            elif range_target == "1" and sub_mini1.distance > 2:
                sub_mini1.health -= hero.hero_range_attack
                hero.hero_bullet -= 1
                if sub_mini2.distance == 1 and sub_mini2.health > 0:
                    hero.hero_health -= sub_mini2.attack
                sub_mini1.distance -= 1
                sub_mini2.distance = max(1, sub_mini2.distance - 1) if sub_mini2.health > 0 else sub_mini2.distance
                print(f"{hp.START_TIRE}Своим выстрелом вы попадаете в мерзкую субстанцию и она подползает ближе к вам. Вторая субстанция {'наносит вам урон.' if sub_mini2.distance == 1 else 'тоже подползает ближе к вам.'}{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
            elif range_target == "2" and sub_mini2.distance > 2:
                sub_mini2.health -= hero.hero_range_attack
                hero.hero_bullet -= 1
                if sub_mini1.distance == 1 and sub_mini1.health > 0:
                    hero.hero_health -= sub_mini1.attack
                sub_mini2.distance -= 1
                sub_mini1.distance = max(1, sub_mini1.distance - 1) if sub_mini1.health > 0 else sub_mini1.distance
                print(f"{hp.START_TIRE}Своим выстрелом вы попадаете в склизкую субстанцию и она подползает к вам ближе. Вторая субстанция {'наносит вам урон.' if sub_mini1.distance == 1 else 'тоже подползает ближе к вам.'}{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")

    # (4) Команда "в" (вперёд)
    elif action_hero == "в":
        if sub_mini1.health <= 0 and sub_mini2.health <= 0:
            pass
        elif sub_mini1.health <= 0:
            if sub_mini2.distance == 1:
                hero.hero_health -= sub_mini2.attack
                print(f"{hp.START_TIRE}Вы просто обходите по кругу склизкую субстанцию, и то, что осталось от второй субстанции.Склизкой субстанции удается вас ударить.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
            else:
                sub_mini2.distance -= 1
                print(f"{hp.START_TIRE}Вы подходите ближе к склизкой субстанции, обходя то, что осталось от второй субстанции.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
        elif sub_mini2.health <= 0:
            if sub_mini1.distance == 1:
                hero.hero_health -= sub_mini1.attack
                print(f"{hp.START_TIRE}Вы просто обходите по кругу мерзкую субстанцию, и то, что осталось от второй субстанции.Мерзкой субстанции удается вас ударить.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
            else:
                sub_mini1.distance -= 1
                print(f"{hp.START_TIRE}Вы подходите ближе к мерзкой субстанции, обходя то, что осталось от второй субстанции.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
        else:
            if sub_mini1.distance == 1 and sub_mini2.distance == 1:
                hero.hero_health -= (sub_mini1.attack + sub_mini2.attack)
                print(f"{hp.START_TIRE}Обходя тварей по кругу, вы получаете урон от обеих субстанций.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
            elif sub_mini1.distance > 1 and sub_mini2.distance == 1:
                hero.hero_health -= sub_mini2.attack
                sub_mini1.distance -= 1
                print(f"{hp.START_TIRE}Пытаясь обойти по кругу склизкую субстанцию вы все-таки получаете урон от нее.Другая подползает ближе к вам.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
            elif sub_mini1.distance == 1 and sub_mini2.distance > 1:
                hero.hero_health -= sub_mini1.attack
                sub_mini2.distance -= 1
                print(f"{hp.START_TIRE}Пытаясь обойти по кругу мерзкую субстанцию вы все-таки получаете урон от нее.Другая подползает ближе к вам.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
            else:
                sub_mini1.distance -= 1
                sub_mini2.distance -= 1
                print(f"{hp.START_TIRE}Вы двигаетесь навстречу двум субстанциям.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")

    # (4) Команда "н" (назад)
    elif action_hero == "н":
        if sub_mini1.distance <= 0:
            sub_mini1.distance = 1
        if sub_mini2.distance <= 0:
            sub_mini2.distance = 1
        if sub_mini1.health <= 0 and sub_mini2.health <= 0:
            pass
        elif sub_mini1.health <= 0:
            if sub_mini2.distance == 1:
                sub_mini2.distance += 1
            elif sub_mini2.distance == 4:
                sub_mini2.distance -= 1
                print(f"{hp.START_TIRE}Похоже вы уперлись в стену,вы пытаетесь двигаться вдоль стены.Склизкая субстанция подползает ближе к вам.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
            else:
                sub_mini2.distance += 1
            sub_mini_init = 0
            print(f"{hp.START_TIRE}Вы делаете шаг назад.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
        elif sub_mini2.health <= 0:
            if sub_mini1.distance == 1:
                sub_mini1.distance += 1
            elif sub_mini1.distance == 4:
                sub_mini1.distance -= 1
                print(f"{hp.START_TIRE}Похоже вы уперлись в стену, вы пытаетесь двигаться вдоль стены.Мерзкая субстанция подползает ближе к вам.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
            else:
                sub_mini1.distance += 1
            sub_mini_init = 0
            print(f"{hp.START_TIRE}Вы делаете шаг назад.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
        else:
            if sub_mini1.distance == 1 and sub_mini2.distance == 1:
                sub_mini1.distance += 1
                sub_mini2.distance += 1
                print(f"{hp.START_TIRE}Вы уворачиваетесь от удара обоих субстанций сделав шаг назад.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
            elif sub_mini1.distance == 4 and sub_mini2.distance == 4:
                sub_mini1.distance -= 1
                sub_mini2.distance -= 1
                print(f"{hp.START_TIRE}Вы достигли максимальной дистанции. Обе субстанции подползают ближе.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
            elif sub_mini1.distance == 1:
                sub_mini1.distance += 1
                sub_mini2.distance = max(1, sub_mini2.distance - 1)
                print(f"{hp.START_TIRE}Вы делаете шаг назад и уворачиваетесь от удара мерзкой субстанции.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
            elif sub_mini2.distance == 1:
                sub_mini2.distance += 1
                sub_mini1.distance = max(1, sub_mini1.distance - 1)
                print(f"{hp.START_TIRE}Вы делаете шаг назад и уворачиваетесь от удара склизкой субстанции.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
            else:
                sub_mini1.distance += 1
                sub_mini2.distance += 1
                print(f"{hp.START_TIRE}Вы делаете шаг назад.{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[sub_mini1,sub_mini2])}")
            sub_mini_init = 0

    # (4) Рюкзак
    elif action_hero == "р":
        inventory_system.open_backpack(hero)

    # (4) Осмотр
    elif action_hero == "о":
        print(f"{hp.START_TIRE}Ничего примечательного вы не нашли.{hp.END_TIRE}")

    # (4) Помощь
    elif action_hero == "п":
        hp.show_full_help(hero)

    # (4) Увернуться
    elif action_hero == "у":
        dodge_sub_mini1()
        dodge_sub_mini2()
        print(f"{hp.START_TIRE}{part_1 + part_2}{hp.END_TIRE}{hp.info_room(hero.hero_health, hero.hero_max_health, [sub_mini1, sub_mini2])}")

    # Неизвестная команда
    elif action_hero not in list_of_command:
        print(f"{hp.START_TIRE}Неизвестная команда.{hp.END_TIRE}")

else:
    print(f"{hp.START_TIRE}{hp.GREEN}(*) Вы одолели две субстанции.{hp.RESET}\n{hp.YELLOW_STAR_START} + 2 Пули{hp.YELLOW_STAR_END}{hp.END_TIRE}")
    hero.hero_bullet += 2
    achievements_system.add_killed_monster("2-Субстанции", 2)
    achievements_system.add_completed_location("(4) Древний зал", 2)


"""(5)  Древняя гробница: Некромант"""

# Первая фаза боя с Некромантом

# (5) Счетчики способностей Некроманта:

# Первая фаза
flag_winner = False
# Вызов снаряда и его характеристики
summon_projectile = 0  # для корректной работы прописываем число 0
##############
# Для работы награды 'отстрел'
if flag_skull_shoot:
    summon_distance = range(3, 8)
    summon_attack = range(2, 3)
else:
    summon_distance = range(3, 7)
    summon_attack = range(2, 4)
###############
skull_attack = 0
skull_distance = 0
skull_fly = 0
# Подготовка отталкивающего удара
cast_punch = 0  # для корректной работы прописываем число 0
ready_punch = 0
change_of_skulls = False  # Переменная для смены снарядов во второй фазе боя.
change_of_attacks = False  # Переменная для смены вида специальной атаки Некроманта во второй фазе
cast_special_attack = 0  # Подготовка спец удара Некроманта
special_attack_distance = 1  # Дистанция специальной атаки Некроманта до героя по умолчанию равна 1
ready_special_attack = 0
cast_spell_mimic_backpack = 0  # Подготовка призыва заклинания 'Голодный рюкзак' во второй фазе
mimic_backpack_spell_time = 0  # Время действия заклинания 'Голодный рюкзак' во второй фазе
magic_field_var = 0  # переменная сообщающая о безопасности поля Некроманта

print(f"{hp.START_TIRE}Вы двигаетесь по небольшому коридору, стены и потолок,\n"
      f"которого украшены вырезанными неизвестными символами.\n"
      f"Чем дальше вы проходите тем ярче они светятся фиолетовым светом.\n"
      f"Дойдя до конца вы оказываетесь в пыльном помещении в центре которого левитирует в воздухе\n"
      f"тот ради которого вы проделали весь этот путь.Судя по всему {hp.PURPLE}Некромант{hp.RESET} снимает силовое поле,\n"
      f"которое огораживает {hp.PURPLE}таинственную статую в черных доспехах{hp.RESET}.\n"
      f"Он оборачивается на вас и приземляется на землю.\n"
      f"Пора выполнить контракт, расправившись с {hp.PURPLE}Некромантом{hp.RESET}.{hp.END_TIRE}")

necromancer_taunts_after_push = [
    "Как далеко ты отлетел? Достаточно, чтобы понять своё ничтожество?",
    "Ха! Ты даже не устоял перед лёгким взмахом моей руки!",
    "Падаешь так изящно... Может, сразу ляжешь в могилу?",
    "Разве это не унизительно? Тебя отшвырнуло, как щепку!"
]

# (5) Функция с таймером 50 секунд.
def ask_for_action_hero():
    global timer, input_active
    input_active = True

    # Создаем поток для ввода
    def input_thread():
        global user_input
        try:
            print("\nНапишите какое действие вы хотите совершить (по-русски): ", end='', flush=True)
            user_input = sys.stdin.readline().strip().lower()
        except:
            user_input = None

    # Запускаем поток ввода
    input_thread_obj = threading.Thread(target=input_thread)
    input_thread_obj.daemon = True
    input_thread_obj.start()

    # Таймер на 50 секунд
    timer = threading.Timer(50.0, timeout_message)
    timer.start()

    # Ждем завершения ввода или таймера
    input_thread_obj.join(50.0)
    if input_thread_obj.is_alive():
        # Время вышло, прерываем ввод
        timer.cancel()
        input_active = False
        return None
    else:
        # Пользователь успел ввести
        timer.cancel()
        input_active = False
        return user_input


# Функция timeout_message().
def timeout_message():
    global input_active
    if not input_active:
        return
    necromancer_phrases = [
        "Мёртвые не раздумывают - они повинуются!",
        "Твоя нерешительность - лучший союзник моей армии теней!",
        "Каждая упущенная секунда - ещё один глоток твоей жизненной силы!",
        "В моём царстве время течёт иначе... прямо как кровь из твоих ран!",
        "Ты замер, словно труп на виселице...",
        "Время кончилось... как и твои шансы!",
        "Ты что, надеялся, что смерть будет ждать?",
        "Упущенное время не вернуть...",
    ]
    hero.hero_health -= necromancer.attack
    chosen_phrase = random.choice(necromancer_phrases)
    print(f"\n{hp.START_TIRE}{hp.PURPLE}Некромант - '{chosen_phrase}'{hp.RESET}\nНекромант атакует первым!\n{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
    # Автоматически запрашиваем новое действие
    print(f"\n{hp.START_TIRE}У вас есть 50 секунд для следующего действия...{hp.END_TIRE}")


# (5.1) Основной игровой цикл 1-ой фазы боя
input_active = False

while hero.hero_health > 0:
    necromancer.update_all()
    hero.update_all()
    price()
    # (5) Подсказки соратника
    hp.reset_all_help()  # сброс всех значений на False
    hp.help_states["help_five_room_phase_one"] = True  # Включаем подсказки пятой комнаты(первая фаза)

    try:
        if pass_five_room_phase_one:
            break
        action_hero = ask_for_action_hero()
        if action_hero is None:
            continue
        if skull_shoot == 2:
            skull_shoot += 1
            hero.hero_bullet += 1
            flag_skull_shoot = True
            achievements_system.add_achievement(achievements_system.character_data, "SKULLS_HUNTER", 2)
            print(f"{hp.START_TIRE}(🎖) Получено достижение {hp.CYAN}'Охотник за черепами'{hp.RESET}\n"
                  f"(🎁) Вы получаете преимущество за отстрел черепов.\n"
                  f"{hp.YELLOW_STAR_START} -1 от максимальной атаки всех летающих черепов\n"
                  f" +1 к максимальной дистанции черепов до вас\n + 1 Пуля{hp.YELLOW_STAR_END}\n"
                  f"(🎁) Чтобы получить награду в следующей игре введите {hp.CYAN}'отстрел'{hp.RESET}.{hp.END_TIRE}")

        # (5.1) hero.count_crit_attack
        crit()
        if necromancer.health <= 0:
            achievements_system.add_killed_monster("Некромант 1-ая фаза", 2)
            achievements_system.add_completed_location("(5)  Древняя гробница и Некромант", 2)
            necromancer.health = 30
            ####### Сброс переменных ####
            skull_fly = 0
            summon_projectile = 0
            skull_distance = 0
            summon_projectile = 0
            cast_spell = 0
            time_action_hero_spell = 0
            #########
            necromancer.distance += 3
            hero.hero_potion_heal += 1
            hero.hero_bullet += 2
            print(f"{hp.START_TIRE}{hp.PURPLE}(*) После нанесенного урона Некромант телепортировался подальше от вас.\nНекромант - 'Ты думал это все? Я уже умер тысячу раз... и тысячу раз восставал!'{hp.RESET}\n{hp.YELLOW_STAR_START} + 2 Пули\n + 1 Зелье лечения{hp.YELLOW_STAR_END}{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            break

        # (5.1) Код отвечающий за работу снаряда Некроманта в 1-ой фазе:
        if summon_projectile != 5:
            summon_projectile += 1
        elif summon_projectile == 5 and skull_fly == 0:  # Если summon_projectile равен 5, то будет призван череп.
            skull_distance = random.choice(summon_distance)
            skull_attack = random.choice(summon_attack)
            skull_fly = 1
            print(f"{hp.START_TIRE}(💀) Позади вас в одной из многочисленных открытых гробниц вылетает призванный {hp.PURPLE}Некромантом{hp.RESET}, пылающий огнем, череп.Череп летит в вашу сторону.{hp.YELLOW}\n***************\nДистанция до героя: {skull_distance}\nАтака черепа: {skull_attack}\n***************{hp.END_TIRE}")
        elif skull_distance != 1 and skull_fly == 1:
            skull_distance -= 1  # Полет снаряда до героя
        # -------------------------------------
        # (5.1) Команда "у" от снаряда
        elif action_hero == "у" and skull_distance == 1 and skull_fly == 1:
            skull_fly = 0
            summon_projectile = 0
            print(f"{hp.START_TIRE}(💀) Череп пролетев мимо вас разбивается об землю.Вам удалось увернуться.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
        # -------------------------------------------------
        elif skull_distance == 1 and skull_fly == 1:
            hero.hero_health -= skull_attack
            skull_fly = 0
            summon_projectile = 0
            skull_distance = 0
            print(f"{hp.START_TIRE}(💀) Максимально приблизившись к вам, череп открыв пасть устремился в вашу спину и разбившись о нее наносит вам урон темной магией {hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")

        # (5.1) Код описывающий действие заклинания "Реверс-поступь" в 1-ой фазе
        if cast_spell != 10:
            cast_spell += 1  # Прибавляем cast_spell для начала работы заклинания
        elif cast_spell == 10 and time_action_hero_spell == 0:
            time_action_hero_spell = -1  # Значение -1 нужно для того, чтобы нижнее условие сработало.
            print(f"{hp.START_TIRE}(🦶) Направив руку на вас,{hp.PURPLE}, Некромант{hp.RESET} вызвал заклинание {hp.PURPLE}'Реверс-поступь'{hp.RESET}{hp.END_TIRE}")
        elif cast_spell == 10 and time_action_hero_spell == -1:
            time_action_hero_spell = 5  # Начало действия заклинания "Реверс-поступь"
        elif time_action_hero_spell != 1:
            time_action_hero_spell -= 1  # Действие заклинания, пока time_action_hero_spell не равно нулю.

        # (5.1) Код описывающий "Отталкивающий удар" Некроманта
        if cast_punch < 7:
            cast_punch += 1  # Перезарядка "Отталкивающего удара"
        elif cast_punch < 8:
            cast_punch += 1
            necromancer.distance += 3
            print(f"{hp.START_TIRE}(👊)  {hp.PURPLE}Некромант \u001b[0 переместился подальше от вас с помощью темной магии, заряжает свободной рукой {hp.PURPLE}'Отталкивающий удар'{hp.RESET}.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
        elif cast_punch < 14:
            cast_punch += 1
            print(f"{hp.START_TIRE}(👊)  {hp.PURPLE}Некромант{hp.RESET} продолжает заряжать свободной рукой {hp.PURPLE}'Отталкивающий удар'{hp.RESET}.{hp.END_TIRE}")
        elif cast_punch == 14 and ready_punch == 0:
            ready_punch = 1
            print(f"{hp.START_TIRE}(👊)  {hp.PURPLE}'Отталкивающий удар' Некроманта готов.{hp.RESET}{hp.END_TIRE}")
        elif ready_punch == 1:
            ready_punch = 2  # Чтобы сообщение о готовности удара больше не появлялось

        # (5.1) Команда "а" и 'Отталкивающий удар некроманта'
        if action_hero == "а" and necromancer.distance == 1 and cast_punch < 9:
            necromancer.health -= hero.hero_attack
            necromancer.distance += 1
            print(f"{hp.START_TIRE}Ударом меча вы наносите урон {hp.PURPLE}Некроманту{hp.RESET}. Он делает шаг назад и готовится сделать удар с выпадом.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")  # удар с выпадом
        elif action_hero == "а" and necromancer.distance == 2:
            hero.hero_health -= necromancer.attack
            print(f"{hp.START_TIRE}Сделав удар мечом вы рассекаете воздух.Некромант делает удар с выпадом и отходит назад.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")  # удар с выпадом
        elif action_hero == "а" and necromancer.distance == 1 and cast_punch != 14 and ready_punch == 0:
            necromancer.health -= hero.hero_attack
            necromancer.distance += 1
            cast_punch = 0  # сброс подготовки удара Некроманта
            ready_punch = 0  # сброс подготовки удара Некроманта
            print(f"{hp.START_TIRE}Мечом вы поражаете {hp.PURPLE}Некроманта{hp.RESET} и он перестал заряжать {hp.PURPLE}'Отталкивающий удар'{hp.RESET}. Он делает шаг назад.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
        elif action_hero == "а" and necromancer.distance == 1 and ready_punch == 2:
            necromancer.distance += 3
            hero.hero_health -= 2
            if skull_distance < 3:
                skull_distance = 1
                ready_punch = 0
                cast_punch = 0
            elif skull_distance > 3:
                skull_distance -= 3
                ready_punch = 0
                cast_punch = 0
            print(f"{hp.START_TIRE}(👊) Своим мечом вы пытаетесь нанести урон, но {hp.PURPLE} Некромант{hp.RESET} быстрым движением руки бьет вас {hp.PURPLE}'Отталкивающим ударом'{hp.RESET}.\nВы пролетев приличное расстояние получаете урон при падении.\n{hp.PURPLE}Некромант - '{random.choice(necromancer_taunts_after_push)}'{hp.RESET}{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")

        #######################
        # (5.1) Секретный способ пройти игру #
        elif action_hero == "а" and necromancer.distance < 1 and ready_punch == 2:
            necromancer.distance += 3
            flag_winner = True
            fast_as_hermes += 1
            achievements_system.add_completed_location("(5)  Древняя гробница и Некромант", 2)
            achievements_system.add_completed_location("(6)  Древняя гробница и  израненный Некромант", 2)
            achievements_system.add_completed_location("(7)  Орда мертвых и  полумертвый Некромант", 2)
            print(f"{hp.START_TIRE}(⚡) Своим мечом вы пытаетесь нанести урон, но {hp.PURPLE}Некромант{hp.RESET} быстрым движением руки бьет вас {hp.PURPLE}'Отталкивающим ударом'{hp.RESET}.\nВы пролетев приличное расстояние оказываетесь у подножия той самой статуи.Вы касаетесь пальцами постамента.В глазах засияло, а потом все погрузилось в мрак...{hp.END_TIRE}")
        elif flag_winner:
            print(f"{hp.START_TIRE}(🎉) Поздравляем! Вы прошли босса игры {hp.CYAN_BOLD} не стандартным способом.{hp.RESET}\nВведите в начале новой игры два слова с пробелом посередине: {hp.CYAN_BOLD}\"time loop\"{hp.RESET}, чтобы пройти игру на более высокой сложности.{hp.END_TIRE}")
            if fast_as_hermes == 5:
                achievements_system.add_achievement(achievements_system.character_data, "PACIFIST", 4)
                print(f"{hp.START_TIRE}(🎖) Получено достижение {hp.CYAN}'Пацифист'{hp.RESET} за прохождение игры нестандартным способом без убийств.\n\nВведите {hp.CYAN}'гермес' {hp.RESET}для получения награды в новой игре.{hp.END_TIRE}")
            sys.exit()
        elif necromancer.distance < 1:
            necromancer.distance += 3
            hero.hero_health -= 2
            if skull_distance < 3:
                skull_distance = 1
            elif skull_distance > 3:
                skull_distance -= 3
            print(f"{hp.START_TIRE}\n{hp.PURPLE}Некромант - 'Встречай свою смерть лицом к лицу жалкий человечишка!{hp.RESET}\nС помощью темной магии {hp.PURPLE}Некромант{hp.RESET} отталкивает вас так, чтобы вы были перед ним, а не за спиной.Вы отлетели на значительное расстояние и получили небольшой урон при падении. {hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")

        elif action_hero == "в" and necromancer.distance == 1 and time_action_hero_spell == 0 and cast_spell != 10:
            necromancer.distance -= 1
            print(f"{hp.START_TIRE}{hp.PURPLE}Некромант - 'Надумал обойти меня негодяй?!'{hp.RESET}{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")

        #######################
        elif time_action_hero_spell == 1 and cast_spell == 10:
            print(f"{hp.START_TIRE}(🦶) Магия заклинания {hp.PURPLE}'Реверс - поступь'{hp.RESET} рассеялась...{hp.END_TIRE}")
            cast_spell = 0
            time_action_hero_spell = 0
        #######################

        # (5.1) Команда "в"
        elif action_hero == "в" and necromancer.distance == 1:
            if time_action_hero_spell != 0 and cast_spell == 10:
                necromancer.distance += 1
                print(f"{hp.START_TIRE}{hp.PURPLE}Некромант -*зловещая усмешка* Хочешь идти 'вперёд'? Как насчёт ШАГА НАЗАД?!{hp.RESET}{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}")
        elif action_hero == "в" and necromancer.distance == 2:
            print(f"{hp.START_TIRE}Вы двигаетесь навстречу, а он в свою очередь, усмехаясь делает шаг назад, с кинжалом наготове.Так долго с ним можно кружить по комнате.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
        elif action_hero == "в" and necromancer.distance != 1:
            if time_action_hero_spell != 0 and cast_spell == 10:
                necromancer.distance += 1
                print(f"{hp.START_TIRE}{hp.PURPLE}Некромант -*зловещая усмешка* Хочешь идти 'вперёд'? Как насчёт ШАГА НАЗАД?!{hp.RESET}{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}")
            else:
                necromancer.distance -= 1
                print(f"{hp.START_TIRE}Вы двигаетесь вперед{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")

        # (5.1) Команда "у"
        elif action_hero == "у" and necromancer.distance == 1:
            necromancer.distance += 1
            print(f"{hp.START_TIRE}Вы уворачиваетесь на месте. {hp.PURPLE}Некромант{hp.RESET} просто сделал шаг назад.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
        elif action_hero == "у" and necromancer.distance == 2:
            necromancer.distance -= 1
            print(f"{hp.START_TIRE}{hp.PURPLE}Некромант{hp.RESET} сделав выпад с кинжалом, промахивается по вам. Дистанция между вами уменьшилась.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")

        # (5.1) Команда "н"
        elif action_hero == "н" and necromancer.distance != 1:
            if time_action_hero_spell != 0 and cast_spell == 10:
                necromancer.distance -= 1
                print(f"{hp.START_TIRE}{hp.PURPLE}Некромант -*зловещая усмешка* Ты сказал 'назад'? Отлично... ИДЁМ ВПЕРЁД!{hp.RESET}{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}")
            else:
                necromancer.distance += 1
                print(f"{hp.START_TIRE}Вы двигаетесь назад{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
        elif action_hero == "н" and necromancer.distance == 1:
            if time_action_hero_spell != 0 and cast_spell == 10:
                print(f"{hp.START_TIRE}{hp.PURPLE}Некромант -*зловещая усмешка* Просто постой на месте!{hp.RESET}{hp.END_TIRE}{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}")
            else:
                necromancer.distance += 1
                print(f"{hp.START_TIRE}Вы двигаетесь назад{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")

        # (5.1) Команда "р"
        elif action_hero == "р":
            inventory_system.open_backpack(hero)

        # (5.1) Команда "п".
        elif action_hero == "п":
            hp.show_full_help(hero)

        # (5.1) Команда "искры" с использованием свитка искр.
        elif action_hero == "искры" and hero.bullet_of_sparks >= 1:
            if cast_punch >= 8 and ready_punch != 1:
                hero.shooting_with_spark_bullets(necromancer)
                print(f" {hp.YELLOW_BOLD}Некромант перестает заряжать 'Отталкивающий удар'{hp.RESET}.{hp.END_TIRE}")
                cast_punch = 0
                ready_punch = 0
            else:
                hero.shooting_with_spark_bullets(necromancer)

        # (5.1) Команда "о"
        elif action_hero == "о" and skull_distance > 1:
            print(f"{hp.START_TIRE}Быстро оглядевшись, вы замечаете летящий Череп.\nЕго дистанция примерно: {random.randint(skull_distance-1,skull_distance+1)} или {random.randint(skull_distance-1,skull_distance+1)}{hp.END_TIRE}")
        elif action_hero == "о":
            print(f"{hp.START_TIRE}Быстро оглядевшись, угрозу для себя вы не обнаружили кроме {hp.PURPLE}Некроманта{hp.RESET} напротив.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")

        # (5.1) Команда "с"
        elif action_hero == "с" and hero.hero_bullet <= 0:
            hero.hero_bullet = 0
            print(f"{hp.START_TIRE}Похоже у вас кончились патроны.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
        elif action_hero == "с" and necromancer.distance != 1:
            range_target = input(f"{hp.START_TIRE}Выберите в кого вы будете стрелять(введите цифру):\n(1){hp.PURPLE}Некромант{hp.RESET}\n(2)летающий Череп{hp.END_TIRE}").lower()
            if range_target not in ("1", "2"):
                print(f"{hp.START_TIRE}Не решившись выбрать цель для выстрела, вы опускаете ружье.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            elif range_target == "1" and necromancer.distance >= 3 and cast_punch != 14 and ready_punch != 1:
                necromancer.health -= hero.hero_range_attack
                cast_punch = 0
                ready_punch = 0
                hero.hero_bullet -= 1
                necromancer.distance -= 1
                print(f"{hp.START_TIRE}Вы попадаете по {hp.PURPLE}Некроманту{hp.RESET} и он перестает заряжать {hp.PURPLE}'Отталкивающий удар'{hp.RESET}. Он делает шаг вперед.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            elif range_target == "1" and necromancer.distance >= 3:
                hero.hero_bullet -= 1
                necromancer.health -= hero.hero_range_attack
                necromancer.distance -= 1
                print(f"{hp.START_TIRE}Вы попадаете по {hp.PURPLE}Некроманту{hp.RESET}.Он делает шаг вперед.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            elif range_target == "1" and necromancer.distance < 3:
                print(f"{hp.START_TIRE}Нельзя выстрелить по {hp.PURPLE}Некроманту{hp.RESET} с такого близкого расстояния.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            elif range_target == "2" and skull_distance == 0:
                print(f"{hp.START_TIRE}В воздухе нет летающего Черепа.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            elif range_target == "2" and skull_distance >= 3:
                skull_fly = 0
                summon_projectile = 0
                skull_distance = 0
                hero.hero_bullet -= 1
                skull_shoot += 1  # очки для сбития черепов выстрелами
                print(f"{hp.START_TIRE}(💀) Своим выстрелом вы разбили вдребезги, летящий к вам, Череп.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            elif range_target == "2" and skull_distance < 3:
                print(f"{hp.START_TIRE}Не получится выстрелить с такого расстояния.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")

    except Exception as e:
        print(f"{hp.START_TIRE}Произошла ошибка: {hp.RED_BOLD}{e}{hp.RESET}{hp.END_TIRE}")
        if 'timer' in globals():
            timer.cancel()
            input_active = False

# Вторая фаза боя с Некромантом

# (5.2) Основной игровой цикл 2-ой фазы боя
input_active = False

while hero.hero_health > 0:
    necromancer.update_all()
    hero.update_all()
    # (5) Подсказки соратника
    hp.reset_all_help()  # сброс всех значений на False
    hp.help_states["help_five_room_phase_two"] = True  # Включаем подсказки пятой комнаты(первая фаза)

    price()
    try:
        if pass_five_room_phase_two:
            break
        action_hero = ask_for_action_hero()
        timeout_message()
        if action_hero is None:
            continue
        if necromancer.health <= 0:
            achievements_system.add_killed_monster("Некромант 2-ая фаза", 2)
            achievements_system.add_completed_location("(5)  (6)  Древняя гробница и  израненный Некромант", 2)
            # Сброс переменных#
            skull_fly = 0
            summon_projectile = 0
            skull_distance = 0
            summon_projectile = 0
            cast_spell = 0
            time_action_hero_spell = 0
            #######
            necromancer.health = 30
            necromancer.distance += 1
            hero.hero_bullet += 2
            hero.hero_potion_of_regen_hp += 1
            print(f"{hp.START_TIRE}{hp.PURPLE}(*) Изувеченный Некромант еле отходит от вас.\n"
                  f"Куски плоти свисают с его лица оголяя череп. Глаза его горят синим пламенем.\n"
                  f"Некромант - 'Ты достойный противник, но ты все равно пополнишь мою армию.Готовься к смерти жалкий человечишка!'{hp.RESET}\n"
                  f"{hp.YELLOW_STAR_START} + 2 Пули\n"
                  f" + 1 Зелье регенерации здоровья{hp.YELLOW_STAR_END}{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            break

        # (5.2) Код отвечающий за работу снаряда Некроманта в 2-ой фазе:

        elif summon_projectile != 5:
            summon_projectile += 1
        elif summon_projectile == 5 and skull_fly == 0:
            skull_distance = random.choice(summon_distance)
            skull_attack = random.choice(summon_attack)
            skull_fly = 1
            if change_of_skulls == False:  # Синий череп со стандартной скоростью полета.
                print(f"{hp.START_TIRE}(\u001b[44m💀){hp.RESET})Позади вас в одной из многочисленных открытых гробниц вылетает призванный {hp.PURPLE}Некромантом{hp.RESET}, \u001b[34;1mпылающий синим огнем 'Череп-призрак'{hp.RESET}.Череп летит в вашу сторону.{hp.YELLOW}\n***************\nДистанция до героя: {skull_distance}\nАтака черепа: {skull_attack}\n***************{hp.END_TIRE}")
            elif change_of_skulls == True:  # Красный череп с удвоенной скоростью полета
                print(f"{hp.START_TIRE}(\u001b[41m💀){hp.RESET}) Позади вас в одной из многочисленных открытых гробниц быстро вылетает призванный {hp.PURPLE}Некромантом{hp.RESET},{hp.RED_BOLD} пылающий ярко-красным огнем, 'Череп-призрак'{hp.RESET}.{hp.RED_BOLD} Череп{hp.RESET} стремительно летит в вашу сторону. {hp.YELLOW}\n***************\nДистанция до героя: {skull_distance}\nАтака черепа: {skull_attack}\n***************{hp.END_TIRE}")

        elif skull_distance > 1 and skull_fly == 1:
            if change_of_skulls == False:
                skull_distance -= 1  # Полет синего 'Черепа-призрака' до героя
            elif change_of_skulls == True:
                skull_distance -= 2  # Полет красного быстрого 'Черепа-призрака' до героя
        elif action_hero == "у" and skull_fly != 1:
            print(f"{hp.START_TIRE}Вы просто уворачиваетесь на месте.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
        # -----------Черепа-снаряды---------#
        elif action_hero == "у" and skull_fly == 1:
            if (skull_distance == 1 and not change_of_skulls) or (skull_distance < 3 and change_of_skulls):
                skull_fly = 0
                summon_projectile = 0
                skull_distance = 0
                skull_color = "(\u001b[44m💀 {hp.RESET}) \u001b[34;1mСиний{hp.RESET}" if not change_of_skulls else "(\u001b[41m💀 {hp.RESET}) {hp.RED_BOLD} Красный{hp.RESET}"
                change_of_skulls = not change_of_skulls
                print(f"{hp.START_TIRE}{skull_color} Череп-призрак пролетев мимо вас рассеивается в воздухе. Вам удалось увернуться.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
        # ---------------------------------------#
        elif skull_distance <= 1 and skull_distance >= 0 and skull_fly == 1:
            hero.hero_health -= skull_attack
            skull_fly = 0
            summon_projectile = 0
            skull_distance = 0
            change_of_skulls = not change_of_skulls  # Смена снарядов
            print(f"{hp.START_TIRE}(💀) Максимально приблизившись к вам, 'Череп-призрак' открыв пасть устремился в вашу спину. Он наносит вам урон. {hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")

        # (5.2) Работа заклинания "Щит от выстрелов".
        if cast_spell < 3:
            cast_spell += 1
        elif cast_spell == 3 and time_action_hero_spell == 1:
            time_action_hero_spell = 0
            cast_spell = 0
            print(f"{hp.START_TIRE}(🛡️) Действие заклинания {hp.PURPLE}'Купол Лича'{hp.RESET} закончилось...{hp.END_TIRE}")
        elif cast_spell == 3 and time_action_hero_spell == 0:
            time_action_hero_spell = 4
            print(f"{hp.START_TIRE}(🛡️)  {hp.PURPLE}Некромант{hp.RESET} вызвал заклинание {hp.PURPLE}'Купол Лича'{hp.RESET}.Вокруг него создается магическое поле{hp.END_TIRE}")
        elif cast_spell == 3 and time_action_hero_spell != 1:
            time_action_hero_spell -= 1  # Действие заклинания пока time_action_hero_spell не равно единицы.

        # (5.2) Работа заклинания "Голодный рюкзак"
        if mimic_backpack_spell_time == 1 and cast_spell_mimic_backpack == 1:
            cast_spell_mimic_backpack = 0
            mimic_backpack_spell_time = 0
            print(f"{hp.START_TIRE}(🎒) Действие заклинания {hp.PURPLE}'Голодный рюкзак'{hp.RESET}закончилось...{hp.END_TIRE}")
        elif cast_spell_mimic_backpack < 10 and mimic_backpack_spell_time == 0:
            cast_spell_mimic_backpack += 1  # Прибавляем по единице пока не достигнем 10.
        elif cast_spell_mimic_backpack == 10 and mimic_backpack_spell_time == 0:
            mimic_backpack_spell_time = 6
            cast_spell_mimic_backpack = 1
            print(f"{hp.START_TIRE}(🎒) Вытянув руки вперед {hp.PURPLE} Некромант{hp.RESET} вызывает неизвестное заклинание. За вашей спиной что-то заурчало.{hp.END_TIRE}")
        elif mimic_backpack_spell_time != 0 and action_hero != "р":
            mimic_backpack_spell_time -= 1  # Время действия заклинания "Голодный рюкзак" уменьшаем на 1 за каждый ход.
        elif action_hero == "р" and mimic_backpack_spell_time != 0 and cast_spell_mimic_backpack == 1:
            if hero.hero_health < 4 and eat_for_mimic_backpack == False:
                hero.hero_health -= necromancer.attack
                cast_spell_mimic_backpack = 0
                mimic_backpack_spell_time = 0
                achievements_system.add_achievement(achievements_system.character_data, "DONT_OPEN", 1)
                print(f"{hp.START_TIRE}(🎖) Получено достижение {hp.CYAN}'Не открывай рюкзак'{hp.RESET}\n\n(🎒) Попытавшись открыть рюкзак вы получаете летальный урон от {hp.PURPLE} укуса острых зубов рюкзака-мимика. Некромант{hp.RESET} насмехается над вами.Вас одолел {hp.PURPLE}'Рюкзак-мимик'{hp.RESET}.\n(🎁) Введите слово {hp.CYAN}'голод'{hp.RESET} для получения подарка за такое достижение в новой игре.({hp.END_TIRE}")
            elif hero.hero_health < 4 and eat_for_mimic_backpack == True:
                hero.hero_health += 2
                eat_for_mimic_backpack = False
                cast_spell_mimic_backpack = 0
                mimic_backpack_spell_time = 0
                print(f"{hp.START_TIRE}(🍖) Вам удалось подкормить {hp.PURPLE}'рюкзак-мимика{hp.RESET}, да и сами вы немного перекусили.Рюкзак стал прежним.Еды у вас больше нет.\n{hp.YELLOW_STAR_START} + 2 к здоровью{hp.YELLOW_STAR_END}{hp.END_TIRE}")
            else:
                hero.hero_health -= necromancer.attack
                cast_spell_mimic_backpack = 0
                mimic_backpack_spell_time = 0
                print(f"{hp.START_TIRE}(🎒) Попытавшись открыть рюкзак вы получаете урон от {hp.PURPLE} укуса острых зубов рюкзака-мимика. Некромант{hp.RESET} насмехается над вами. Рюкзак стал прежним.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")

        # (5.2) Работа специальной атаки некроманта.
        if cast_special_attack != 5:
            cast_special_attack += 1  # Подготовка специального удара Некроманта.
        elif cast_special_attack == 5 and ready_special_attack == 1 and special_attack_distance != 0:
            special_attack_distance -= 1  # Уменьшаем пока не станет равной 0
        elif cast_special_attack == 5 and ready_special_attack == 0:
            ready_special_attack = 1  # для работы следующего условия
            necromancer.distance += 2
            if change_of_attacks == False:
                special_attack_distance = (necromancer.distance - 1)
                print(f"{hp.START_TIRE}(🧟) Некромант отскочив от вас, призывает перед собой нечто, движущееся под землей. Вы видете траекторию движения по слегка приподнимающейся плитке в зале.{hp.YELLOW}\n***************\nДистанция чего-то движущегося под землей до вас: {special_attack_distance}\n***************\n{hp.END_TIRE}")
            elif change_of_attacks == True:
                special_attack_distance = (necromancer.distance + 1)
                print(f"{hp.START_TIRE}(🧟) Некромант отскочив от вас, призывает за вашей спиной нечто, движущееся под землей. Вы видете траекторию движения по слегка приподнимающейся плитке в зале.{hp.YELLOW}\n***************\nДистанция чего-то движущегося под землей до вас: {special_attack_distance}\n***************\n{hp.END_TIRE}")

        # (5.2) Команда "а".
        if action_hero == "а" and necromancer.distance == 1:  # Если дистанция 1
            necromancer.health -= hero.hero_attack
            necromancer.distance += 1
            print(f"{hp.START_TIRE}Ударом меча вы наносите урон {hp.PURPLE}Некроманту{hp.RESET}. Он делает шаг назад.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
        elif action_hero == "а" and necromancer.distance > 1:  # Если дистанция больше 1
            necromancer.health -= hero.hero_attack
            necromancer.distance += 1
            print(f"{hp.START_TIRE}Мечом вы промахиваетесь по {hp.PURPLE}Некроманту{hp.RESET}. Он делает шаг назад.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")

        # (5.2) Команда "н" и специальная атака
        elif cast_special_attack == 5 and ready_special_attack == 1 and special_attack_distance == 0 and change_of_attacks == False:
            if action_hero == "н":
                necromancer.distance += 1
                cast_special_attack = 0
                ready_special_attack = 0
                change_of_attacks = not change_of_attacks
                print(f"{hp.START_TIRE}(🧟) Сделав шаг назад вы уворачиваетесь от рук мертвецов, вырвавшихся из под земли.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            else:
                hero.hero_health -= necromancer.attack
                cast_special_attack = 0
                ready_special_attack = 0
                change_of_attacks = not change_of_attacks
                print(f"{hp.START_TIRE}(🧟) Из под земли под вами вырываются руки мертвецов. Своими острыми когтями они наносят вам урон и уходят снова под землю.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
        elif action_hero == "н":
            if necromancer.distance < 8:
                necromancer.distance += 1
                print(f"{hp.START_TIRE}Вы делаете шаг назад.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            else:
                print(f"{hp.START_TIRE}Вы на максимальной дистанции.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")

        # (5.2) Команда "в" и специальная атака
        elif cast_special_attack == 5 and ready_special_attack == 1 and special_attack_distance == 0 and change_of_attacks == True:
            if action_hero == "в" and necromancer.distance == 1:
                cast_special_attack = 0
                ready_special_attack = 0
                change_of_attacks = not change_of_attacks
                print(f"{hp.START_TIRE}(🧟) Сделав шаг вперед вы уворачиваетесь от рук мертвецов, вырвавшихся из под земли.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            elif action_hero == "в" and necromancer.distance > 0:
                necromancer.distance -= 1
                cast_special_attack = 0
                ready_special_attack = 0
                change_of_attacks = not change_of_attacks
                print(f"{hp.START_TIRE}(🧟) Сделав шаг вперед вы уворачиваетесь от рук мертвецов, вырвавшихся из под земли.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            else:
                hero.hero_health -= necromancer.attack
                cast_special_attack = 0
                ready_special_attack = 0
                change_of_attacks = not change_of_attacks
                print(f"{hp.START_TIRE}(🧟) Из под земли под вами вырываются руки мертвецов. Своими острыми когтями они наносят вам урон и уходят снова под землю.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
        elif action_hero == "в":
            if necromancer.distance > 1:
                necromancer.distance -= 1
                print(f"{hp.START_TIRE}Вы делаете шаг вперед.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            else:
                print(f"{hp.START_TIRE}Вы обходите Некроманта по кругу.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")

        # (5.2) Команда "о"
        elif action_hero == "о":
            if skull_distance > 1:
                print(f"{hp.START_TIRE}Быстро оглядевшись, вы замечаете летящий Череп.\nЕго дистанция примерно: {random.randint(skull_distance-1,skull_distance+1)} или {random.randint(skull_distance-1,skull_distance+1)}{hp.END_TIRE}")
            elif ready_special_attack == 1 and change_of_attacks == False:
                print(f"{hp.START_TIRE}Вы видите как нечто движется под землей на дистанции : {special_attack_distance} {hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}")
            elif ready_special_attack == 1 and change_of_attacks == True:
                print(f"{hp.START_TIRE}Быстро обернувшись вы видите как нечто движется под землей на дистанции : {special_attack_distance}")
            elif magic_field_var == 0 and time_action_hero_spell > 1:
                magic_field_var = 1
                print(f"{hp.START_TIRE}Вы провели мечом по краю магического поля Некроманта.Ничего не произошло. После вы схватили камень и бросили его. Камень, который вы бросили в магическое поле не прошел дальше.{hp.END_TIRE}")  # Сообщение подсказка
            else:
                print(f"{hp.START_TIRE}У вас не получилось отвлечься от боя и понаблюдать за обстановкой вокруг.{hp.END_TIRE}")

        # (5.2) Команда "искры" с использованием свитка искр.
        elif action_hero == "искры":
            if time_action_hero_spell != 0 and hero.bullet_of_sparks >= 1:
                hero.bullet_of_sparks -= 1
                print(f"{hp.START_TIRE}(🛡️) Магическое поле не дает пройти вашей пуле дальше. Вы не попадаете по {hp.PURPLE}Некроманту{hp.RESET}.{hp.END_TIRE}")
            else:
                hero.shooting_with_spark_bullets(necromancer)

        # (5.2) Команда "с"
        elif action_hero == "с" and hero.hero_bullet <= 0:
            hero.hero_bullet = 0
            print(f"{hp.START_TIRE}Похоже у вас кончились патроны.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
        elif action_hero == "с" and necromancer.distance != 1:
            range_target = input(f"{hp.START_TIRE}Выберите в кого вы будете стрелять(введите цифру):\n(1){hp.PURPLE}Некромант{hp.RESET}\n(2)летающий Череп{hp.END_TIRE}").lower()
            if range_target not in ("1", "2"):
                print(f"{hp.START_TIRE}Не решившись выбрать цель для выстрела, вы опускаете ружье.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            elif range_target == "1" and necromancer.distance >= 3 and time_action_hero_spell != 0:
                hero.hero_bullet -= 1
                necromancer.distance += 1
                print(f"{hp.START_TIRE}(🛡️) Магическое поле не дает пройти вашей пуле дальше. Вы не попадаете по {hp.PURPLE}Некроманту{hp.RESET}.Он делает шаг назад.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            elif range_target == "1" and necromancer.distance >= 3:
                hero.hero_bullet -= 1
                necromancer.health -= hero.hero_range_attack
                necromancer.distance -= 1
                print(f"{hp.START_TIRE}Вы попадаете по {hp.PURPLE}Некроманту{hp.RESET}.Он делает шаг вперед.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            elif range_target == "1" and necromancer.distance < 3:
                print(f"{hp.START_TIRE}Нельзя выстрелить по {hp.PURPLE}Некроманту{hp.RESET} с такого близкого расстояния.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            elif range_target == "2" and skull_distance == 0:
                print(f"{hp.START_TIRE}В воздухе нет летающего Черепа.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            elif range_target == "2" and skull_distance >= 3:
                hero.hero_bullet -= 1
                print(f"{hp.START_TIRE}(💀) Пуля прошла насквозь 'Черепа-призрака'и он продолжает лететь в вас.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
            elif range_target == "2" and skull_distance < 3:
                print(f"{hp.START_TIRE}Не получится выстрелить с такого расстояния.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")

        # (5.2) Команда "р"
        elif action_hero == "р":
            inventory_system.open_backpack(hero)

        # (5.2) Команда "п".
        elif action_hero == "п":
            hp.show_full_help(hero)
    except Exception as e:
        print(f"{hp.START_TIRE}Произошла ошибка: {hp.RED_BOLD}{e}{hp.RESET}{hp.END_TIRE}")
        if 'timer' in globals():
            timer.cancel()
            input_active = False

# Третья фаза боя с Некромантом

#(5.3)Переменные третьей фазы
choise_weapon = ""#Выбранное оружие по умолчанию
undead_func = ""#Функция заклинания "Восставшие мертвецы"
choice_undead_func = ""#Выбор функции для заклинания "Восставшие мертвецы"
undead_timer = 0#Таймер для заклинания "Восставшие мертвецы"
special = False #Переменная спец-удара для каждого оружия
axe_swing = 0#Замах топором(подготовка удара)
input_active = False
#(5.3)Функции смены оружия третьей фазы
def shield_and_sword():
	global action_hero,special
#(5.3) Оружие "Щит и меч"
#(5.3)shield_and_sword() команда "а"
	if action_hero == "а" and necromancer.distance == 1 and special == False:
		if hero.count_crit_attack > 0:
			hero.hero_health -= necromancer.attack
			hero.count_crit_attack -= 1
			print(f"{hp.START_TIRE}(🗡️)  {hp.CYAN_BOLD}Заряженным мечом вы подаете по щиту Некроманта.Он бьет вас мечом.{hp.RESET}{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
		else:
			hero.hero_health -= necromancer.attack
			print(f"{hp.START_TIRE}(🛡️🗡️) Своим ударом вы попадаете по тяжелому щиту Некроманта не нанося ему урон, он бьет вас мечом.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "а" and necromancer.distance == 1 and special == True:
		necromancer.health -= hero.hero_attack
		necromancer.distance += 1
		special = not special
		print(f"{hp.START_TIRE}(🛡️🗡️) Ударив мечом в бок Некроманта вы наносите ему урон.Он делает шаг назад.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "а" and necromancer.distance > 1 and special == False:
		special = not special
		print(f"{hp.START_TIRE}(🛡️🗡️) Сделав замах ваш клинок рассек воздух.Некромант открывшись наносит удар мечом, не попадая по вам.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
#(5.3)shield_and_sword() команда "н"
	elif action_hero == "н":
		necromancer.distance += 1
		print(f"{hp.START_TIRE}(🛡️🗡️)  Вы делаете шаг назад.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
#(5.3)shield_and_sword() команда "в"
	elif action_hero == "в" and necromancer.distance == 1 and special == False:
		special = not special
		print(f"{hp.START_TIRE}(🛡️🗡️)  Сделав выпад Некромант промахивается. Вы обошли его со стороны щита и стоите сбоку от него.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "в" and necromancer.distance > 1:
		necromancer.distance -= 1
		print(f"{hp.START_TIRE}(🛡️🗡️) Вы делаете шаг вперед.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
#(5.3)shield_and_sword() команда "у"
	elif action_hero == "у" and necromancer.distance > 1:
		necromancer.distance -= 1
		print(f"{hp.START_TIRE}(🛡️🗡️) Вы просто увернулись на месте. Некромант подходит ближе.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "у" and necromancer.distance == 1 and special == False:
			hero.hero_health -= necromancer.attack
			print(f"{hp.START_TIRE}(🛡️🗡️) Вы увернулись от атаки меча но получили урон от толчка шипастого щита Некроманта.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
#(5.3)shield_and_sword() команда "с"
	elif action_hero == "с" and necromancer.distance < 3:
		if hero.bullet_of_sparks > 0 and necromancer.distance == 1 and special == False:
			hero.bullet_of_sparks -= 1
			hero.hero_health -= (hero.damage_bullet_of_sparks // 2) + necromancer.attack
			print(f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD} Выстрелом из ружья вы попадаете в щит Некроманта. Пули отрикошетели от щита и нанесли вам урон, вдобавок Некромант бьет вас мечом.Вам очень больно.{hp.RESET}.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
		elif hero.bullet_of_sparks > 0 and necromancer.distance == 1 and special == True:
			hero.bullet_of_sparks -= 1
			necromancer.health -= hero.damage_bullet_of_sparks
			necromancer.distance += 1
			print(f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD} Выстрелом из ружья вы попадаете в Некроманта когда он не прикрывал свое тело щитом.Его откидывает от вас.Вы наносите значительный урон.{hp.RESET}.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
		elif hero.bullet_of_sparks > 0 and necromancer.distance == 2 and special == False:
			hero.bullet_of_sparks -= 1
			hero.hero_health -= hero.damage_bullet_of_sparks // 4
			special = not special
			print(f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD} Выстрелом из ружья вы попадаете в щит Некроманта. Пули частично отрикошетели от щита и нанесли вам урон.Некромант открывшись наносит удар мечом, не попадая по вам{hp.RESET}.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
		elif hero.bullet_of_sparks > 0 and necromancer.distance == 2 and special == True:
			hero.bullet_of_sparks -= 1
			necromancer.health -= hero.damage_bullet_of_sparks // 2
			print(f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD} Выстрелом из ружья вы попадаете в Некроманта когда он не прикрывал свое тело щитом. Вы наносите урон.{hp.RESET}.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
		else:
			print(f"{hp.START_TIRE}(🛡️🗡️) Нельзя выстрелить с такой дистанции.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "с" and hero.hero_bullet <= 0:
		print(f"{hp.START_TIRE}(🛡️🗡️) Похоже у вас кончились патроны.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "с" and special == True and necromancer.distance > 2:
	    	if hero.bullet_of_sparks > 0:
	    		hero.bullet_of_sparks -= 1
	    		necromancer.health -= hero.damage_bullet_of_sparks // 4
	    		necromancer.distance -= 1
	    		special = not special
	    		print(f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD} Выстрелом из ружья вы попадаете в неприкрытое щитом тело и наносите незначительный урон.Некромант подходит ближе{hp.RESET}.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	    	else:
	    		hero.hero_bullet -= 1
	    		necromancer.health -= hero.hero_range_attack
	    		necromancer.distance -= 1
	    		special = not special
	    		print(f"{hp.START_TIRE}(🛡️🗡️) Брешь в защите Некроманта позволила вам нанести ему урон выстрелом.Прикрывшись щитом он подходит ближе.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "с" and special == False and necromancer.distance > 2:
	    	if hero.bullet_of_sparks > 0:
	    		hero.bullet_of_sparks -= 1
	    		print(f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD} Выстрелом из ружья вы попадаете в щит Некроманта.Он подходит ближе{hp.RESET}.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	    	else:
	    		hero.hero_bullet -= 1
	    		necromancer.distance -= 1
	    		print(f"{hp.START_TIRE}(🛡️🗡️) Некромант прикрылся щитом от вашего выстрела и подходит ближе.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
#(5.3)Оружие "Трезубец"
def trident():
	global action_hero,special
#(5.3)trident() команда "а"
	if action_hero == "а" and necromancer.distance == 3:
		hero.hero_health -= necromancer.attack
		print(f"{hp.START_TIRE}(🔱) Своим трезубцем Некромант поражает вас.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "а" and necromancer.distance == 2:
		necromancer.distance += 1
		print(f"{hp.START_TIRE}(🔱) Сделав удар мечом вы рассекаете воздух.Некромант делает шаг назад.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "а" and necromancer.distance == 1 and special == False:
		necromancer.health -= hero.hero_attack
		special = not special
		print(f"{hp.START_TIRE}(🔱) Сделав удар мечом вы поражаете Некроманта.Он перехватил трезубец по другому.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "а" and necromancer.distance == 1 and special == True:
		necromancer.distance += 2
		print(f"{hp.START_TIRE}(🔱) Ваш удар мечом Некромант парирует, отталкивая вас и при этом сделав шаг назад.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "а" and necromancer.distance > 3:
		necromancer.distance -= 1
		print(f"{hp.START_TIRE}(🔱) Вы рассекаете воздух мечом. Некромант подходит ближе.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
#(5.3)trident()Команда "в"
	elif action_hero == "в" and necromancer.distance == 1 and special == False:
		special = not special
		print(f"{hp.START_TIRE}(🔱) Вы обходите Некроманта по кругу.Он перехватил трезубец по другому. {hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "в" and necromancer.distance < 3 and necromancer.distance != 1:
		necromancer.distance -= 1
		print(f"{hp.START_TIRE}(🔱) Вы делаете шаг вперед. {hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "в" and necromancer.distance == 2:
		necromancer.distance -= 1
		print(f"{hp.START_TIRE}(🔱) Вы делаете шаг вперед. {hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "в" and necromancer.distance == 1 and special == True:
		necromancer.distance += 2
		print(f"{hp.START_TIRE}(🔱) Некромант отталкивает вас и делает шаг назад. {hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "в" and necromancer.distance == 3 and special == False:
		necromancer.distance -= 1
		print(f"{hp.START_TIRE}(🔱) Сделав шаг вперед вы сокращаете дистанцию с Некромантом. {hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "в" and necromancer.distance == 3 and special == True:
		special = not special
		necromancer.distance -= 1
		hero.hero_health -= necromancer.attack
		print(f"{hp.START_TIRE}(🔱) Сделав шаг вперед вы натыкаетесь на удар трезубца Некроманта. {hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "в" and necromancer.distance == 4:
		necromancer.distance -= 1
		print(f"{hp.START_TIRE}(🔱) Вы делаете шаг вперед. {hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
#(5.3)trident() команда "н"
	elif action_hero == "н" and necromancer.distance > 3:
		print(f"{hp.START_TIRE}(🔱) Некромант с помощью темной магии не дает вам увеличить дистанцию.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "н" and necromancer.distance == 1 and special == True:
		necromancer.distance += 1
		special = not special
		print(f"{hp.START_TIRE}(🔱) Сделав шаг назад вы уворачиваетесь от отталкивающего выпада Некроманта.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "н" and necromancer.distance == 3 and special == True:
		necromancer.distance += 1
		special = not special
		print(f"{hp.START_TIRE}(🔱) Сделав шаг назад, Некромант сделал выпад, но промазал.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "н" and necromancer.distance == 3 and special == False:
		print(f"{hp.START_TIRE}(🔱) Сделав шаг назад, Некромант сделал шаг вам навстречу.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "н" and necromancer.distance == 2:
		necromancer.distance += 1
		print(f"{hp.START_TIRE}(🔱) Сделав шаг назад вы увеличили дистанцию между вами.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
#(5.3)trident() команда "у"
	elif action_hero == "у" and necromancer.distance == 3 and special == False:
		special = not special
		print(f"{hp.START_TIRE}(🔱) Вы увернулись от выпада трезубца Некроманта.Он сосредоточился на следующем ударе.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "у" and necromancer.distance == 3 and special == True:
		hero.hero_health -= necromancer.attack
		special = not special
		print(f"{hp.START_TIRE}(🔱) Некромант предугадал вашу траекторию уворота и попадает в вас трезубцем.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "у" and necromancer.distance < 3:
		necromancer.distance += 1
		special = True
		print(f"{hp.START_TIRE}(🔱) Вы уворачиваетесь на месте.Некромант делает шаг назад,увеличивая с вами дистанцию.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
#(5.3)trident() команда "с"
	elif action_hero == "с" and necromancer.distance < 3:
		if hero.bullet_of_sparks > 0 and necromancer.distance == 1 and special == False:
			hero.bullet_of_sparks -= 1
			necromancer.health -= hero.damage_bullet_of_sparks
			necromancer.distance += 2
			special = not special
			print(f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD} Выстрелом из ружья вы попадаете в Некроманта.Вы наносите значительный урон.Он делает шаг назад{hp.RESET}.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
		elif hero.bullet_of_sparks > 0 and necromancer.distance == 1 and special == True:
			necromancer.distance += 2
			print(f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD} Некромант оказался быстрее и отталкивает вас от себя трезубцем при этом сделав шаг назад.Выстрелить вам не удалось.{hp.RESET}.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
		elif hero.bullet_of_sparks > 0 and necromancer.distance == 2 and special == False:
			hero.bullet_of_sparks -= 1
			necromancer.health -= hero.damage_bullet_of_sparks // 2
			necromancer.distance += 1
			special = not special
			print(f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD} Выстрелом из ружья вы попадаете в Некроманта.Он делает шаг назад{hp.RESET}.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
		elif hero.bullet_of_sparks > 0 and necromancer.distance == 2 and special == True:
			hero.bullet_of_sparks -= 1
			necromancer.health -= hero.damage_bullet_of_sparks // 2
			necromancer.distance += 1
			special = not special
			print(f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD} Выстрелом из ружья вы попадаете в Некроманта.Он делает шаг назад{hp.RESET}{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
		else:
			print(f"{hp.START_TIRE}(🔱) Нельзя выстрелить с такой дистанции.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "с" and hero.hero_bullet <= 0:
		print(f"{hp.START_TIRE}(🔱) Похоже у вас кончились патроны.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "с" and necromancer.distance == 3:
	    	hero.hero_health -= necromancer.attack
	    	print(f"{hp.START_TIRE}(🔱) Попытавшись выстрелить, Некромант мгновенно наносит вам урон трезубцем.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "с" and necromancer.distance > 3:
	    	if hero.bullet_of_sparks > 0:
	    		hero.bullet_of_sparks -= 1
	    		necromancer.health -= hero.damage_bullet_of_sparks // 4
	    		necromancer.distance -= 1
	    		print(f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD} Выстрелом из ружья вы частично попадаете в Некроманта.Вы наносите незначительный урон.Он делает шаг вперед{hp.RESET}{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	    	else:
	    		hero.hero_bullet -= 1
	    		necromancer.health -= hero.hero_range_attack
	    		necromancer.distance -= 1
	    		print(f"{hp.START_TIRE}(🔱) Вы попадаете в Некроманта.Он подходит ближе.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
#(5.3)Оружие "Топор"
def axe():
	global action_hero,special,axe_swing
	if action_hero == "в" and necromancer.distance == 1 and special == False and axe_swing == 0:
		axe_swing = 1
		print(f"{hp.START_TIRE}(🪓) Вы обходите Некроманта по кругу.Топор он все еще держит над головой.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "в" and necromancer.distance == 1 and special == False and axe_swing == 1:
		axe_swing = 0
		special = not special
		print(f"{hp.START_TIRE}(🪓) Вы обходите Некроманта по кругу при этом увернувшись от удара топором.Топор окутывают фиолетовые частицы темной магии.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "в" and necromancer.distance == 1 and special == True and axe_swing == 0:
		axe_swing = 1
		print(f"{hp.START_TIRE}(🪓) Вы обходите Некроманта по кругу.Топор он держит от бедра.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "в" and necromancer.distance == 1 and special == True and axe_swing == 1:
		hero.hero_health -= necromancer.attack*2
		necromancer.distance += 1
		axe_swing = 0
		special = not special
		print(f"{hp.START_TIRE}(🪓) Вы обходите Некроманта по кругу при этом получив значительный урон от кругового удара.Вас откидывает. Топор становится прежним.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "у" and necromancer.distance == 1 and special == False and axe_swing == 0:
		axe_swing = 1
		print(f"{hp.START_TIRE}(🪓) Вы просто уворачиваетесь на месте.Некромант держит топор над головой.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "у" and necromancer.distance == 1 and special == False and axe_swing == 1:
		axe_swing = 0
		special = not special
		print(f"{hp.START_TIRE}(🪓) Вы увернулись от удара топора.Топор окутывают фиолетовые частицы темной магии.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "у" and necromancer.distance == 1 and special == True and axe_swing == 0:
		axe_swing = 1
		print(f"{hp.START_TIRE}(🪓) Вы просто уворачиваетесь на месте.Некромант держит топор от бедра.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "у" and necromancer.distance == 1 and special == True and axe_swing == 1:
		hero.hero_health -= necromancer.attack*2
		necromancer.distance += 1
		axe_swing = 0
		special = not special
		print(f"{hp.START_TIRE}(🪓) Попытавшись увернуться вы все равно получаете значительный урон от кругового удара.Вас откидывает. Топор становится прежним.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "а" and necromancer.distance == 1 and special == False and axe_swing == 0:
		necromancer.health -= hero.hero_attack
		axe_swing = 1
		print(f"{hp.START_TIRE}(🪓) Вы наносите урон Некроманту.Топор он все еще держит над головой.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "а" and necromancer.distance == 1 and special == True and axe_swing == 0:
		necromancer.health -= hero.hero_attack
		axe_swing = 1
		print(f"{hp.START_TIRE}(🪓) Вы наносите урон Некроманту.Заряженный топор он все еще держит от бедра.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif necromancer.distance == 1 and special == False and axe_swing == 0:
		axe_swing = 1
		print(f"{hp.START_TIRE}(🪓) Некромант делает замах двуручным топором.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif necromancer.distance == 1 and special == True and axe_swing == 0:
		axe_swing = 1
		print(f"{hp.START_TIRE}(🪓) Некромант делает замах двуручным топором окутанным фиолетовыми частицами.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "н" and necromancer.distance == 1 and special == False and axe_swing == 1:
		axe_swing = 0
		special = not special
		necromancer.distance += 1
		print(f"{hp.START_TIRE}(🪓) Сделав шаг назад вы увернулись от удара.Топор окутывают фиолетовые частицы темной магии.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "н" and necromancer.distance == 1 and special == True and axe_swing == 1:
		axe_swing = 0
		special = not special
		necromancer.distance += 1
		print(f"{hp.START_TIRE}(🪓) Сделав шаг назад вы увернулись от стремительного кругового удара.Топор Некроманта стал прежним.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif necromancer.distance == 1 and special == False and axe_swing == 1:
		axe_swing = 0
		hero.hero_health -= necromancer.attack*2
		necromancer.distance += 1
		print(f"{hp.START_TIRE}(🪓) Некромант попадает в вас двуручным топором.Вы получаете значительный урон.Вас откидывает от него.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif necromancer.distance == 1 and special == True and axe_swing == 1:
		axe_swing = 0
		hero.hero_health -= necromancer.attack*2
		necromancer.distance += 1
		special = not special
		print(f"{hp.START_TIRE}(🪓) Некромант стремительно делает круговой удар.Вы получаете значительные увечья и вас откидывает от него.Частицы вокруг топора исчезли.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
#(5.3)вперед(),назад()
	elif action_hero == "н" and necromancer.distance == 2:
			print(f"{hp.START_TIRE}(🪓) С помощью темной магии Некромант не позволяет вам увеличить дистанцию.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "в" and necromancer.distance > 1:
			necromancer.distance -= 1
			print(f"{hp.START_TIRE}(🪓) Вы делаете шаг вперед.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "н" and necromancer.distance < 1:
			necromancer.distance += 1
			print(f"{hp.START_TIRE}(🪓) Вы делаете шаг назад.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
#(5.3)axe() команда "с"
	elif action_hero == "с" and necromancer.distance < 3:
		if hero.bullet_of_sparks > 0 and necromancer.distance == 1:
			hero.bullet_of_sparks -= 1
			necromancer.health -= hero.damage_bullet_of_sparks
			special = not special
			print(f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD} Выстрелом из ружья вы попадаете в Некроманта.Вы наносите значительный урон.{hp.RESET}{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
		elif hero.bullet_of_sparks > 0 and necromancer.distance == 2:
			hero.bullet_of_sparks -= 1.
			necromancer.health -= hero.damage_bullet_of_sparks // 2
			special = not special
			print(f"{hp.START_TIRE}(📜)  {hp.YELLOW_BOLD} Выстрелом из ружья вы попадаете в Некроманта и наносите ему урон.{hp.RESET}{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
		else:
			print(f"{hp.START_TIRE}(🪓) Нельзя выстрелить с такой дистанции.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
	elif action_hero == "с" and hero.hero_bullet <= 0:
		print(f"{hp.START_TIRE}(🪓) Похоже у вас кончились патроны.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")

list_of_weapons = {trident:'(🔱)"Трезубец ночи"',shield_and_sword: '(🛡️🗡️)"Щит и меч"',axe: '(🪓)"Топор тьмы"'}#Список функций с разными оружиями Некроманта
weapon_func = list(list_of_weapons.keys())

#(5.3) Заклинание "Восставшие мертвецы":

#Стрельба Скелета-лучника(Навык 1-ого уровня)
def undead_shoot():
	global action_hero
	if action_hero == "у":
		print(f"{hp.START_TIRE}(🧟) Вы увернулись от стрелы Скелета-лучника{hp.END_TIRE}")
	else:
		hero.hero_health -= necromancer.attack
		print(f"{hp.START_TIRE}(🧟) Стрела Скелета-лучника попала в вас и наносит вам урон{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
#Руки мертвецов(Навык 1-ого уровня)
def undead_hands():
		global action_hero
		if action_hero == "в" or action_hero == "н":
			print(f"{hp.START_TIRE}(🧟) Вы увернулись от рук мертвецов вырвавшихся из под земли.{hp.END_TIRE}")
		else:
			hero.hero_health -= necromancer.attack
			print(f"{hp.START_TIRE}(🧟) Вырвавшиеся руки мертвецов атакуют вас разрывая когтями ваши ноги.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
#Тихо подошедший мертвец(лечение Некроманта, Навык 1-ого уровня)
def undead_life_drain():
		global action_hero
		if action_hero == "а":
			print(f"{hp.START_TIRE}(🧟) Ударом меча мертвеца откидывает от вас и Некроманта. Неуклюже попятившись он падает на землю.{hp.END_TIRE}")
		else:
			necromancer.health += 3
			print(f"{hp.START_TIRE}(🧟) Некромант пожирает темной магией остатки жизненной силы мертвеца. На пол падают кости, которые мгновенно превратились в прах.Некромант восстановил себе здоровье.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
#Выбитый из рук меч героя(Навык 1-ого уровня)
def undead_disarm():
	if action_hero == "о":
		print(f"{hp.START_TIRE}(🧟) Вы быстро нашли меч и ударом меча поражаете тихо подошедшего мертвеца. Он падает на пол и больше не двигается.{hp.END_TIRE}")
	else:
		hero.hero_health -= necromancer.attack
		print(f"{hp.START_TIRE}(🧟) Не успев быстро найти меч вы получаете урон от тихо подошедшего мертвеца. Найдя все-таки клинок вы поражаете мертвеца и он падает навзничь.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")

# Список фраз и функций заклинания "Восставшие мертвецы"
undead_list = {
    undead_shoot: "Из толпы мертвых Скелет-лучник целится в вас.",
    undead_hands: "Вы чувствуете как-будто, что-то шевелится под вашими ногами.",
    undead_life_drain: " В пылу битвы вы замечаете мертвеца, который идет четко к Некроманту не обращая на вас внимания.Он рядом с вами и в шаге от Некроманта",
    undead_disarm: "Некромант с помощью заклинания, недалеко откидывает ваш меч.Необходимо его найти."
}
undead_func = list(undead_list.keys())

while hero.hero_health > 0:
    necromancer.update_all()
    hero.update_all()
    price()
    # (5) Подсказки соратника
    hp.reset_all_help()  # сброс всех значений на False
    hp.help_states["help_five_room_phase_third"] = True  # Включаем подсказки пятой комнаты(первая фаза)

    try:
        if pass_five_room_phase_three:
            break
        action_hero = ask_for_action_hero()
        timeout_message()
        if action_hero is None:
            continue
        if necromancer.health <= 0:
            flag_winner = True
            print(f"{hp.START_TIRE}{hp.GREEN}(*) С последним ударом вашего клинка тело Некроманта обмякло на полу.\n"
                  f"С исчезновением тёмной магии, мертвецы вокруг рухнули на землю, обратившись в прах.\n"
                  f" Подойдя к статуи в темных доспехах вы касаетесь пальцами постамента. В глазах засияло, а потом все погрузилось в мрак...{hp.RESET}{hp.END_TIRE}")
            if flag_winner:
                achievements_system.add_killed_monster("Некромант 3-ая фаза", 2)
                achievements_system.add_completed_location("(7)  Орда мертвых и  полумертвый Некромант", 2)
                print(f"{hp.START_TIRE}(🎉) Поздравляем! Вы прошли игру.\nВведите в начале новой игры два слова с пробелом посередине: {hp.CYAN_BOLD}\"time loop\"{hp.RESET}, чтобы пройти игру на более высокой сложности.{hp.END_TIRE}")
                sys.exit()

        # (5.3) Смена оружия Некроманта
        if cast_spell == 0:
            choise_weapon = random.choice(weapon_func)  # Мгновенная смена оружия
            weapon_name = list_of_weapons[choise_weapon]
            print(f"{hp.START_TIRE}(🔄) Некромант мгновенно меняет оружие на {weapon_name}{hp.END_TIRE}")
            # Устанавливаем параметры для нового цикла атаки
            cast_spell = 1
            time_action_hero_spell = 8  # Сколько ходов будет действовать это оружие
            special = False
            axe_swing = 0
        elif cast_spell == 1:
            if time_action_hero_spell > 0:
                choise_weapon()  # Используем текущее выбранное оружие
                time_action_hero_spell -= 1
            else:
                cast_spell = 0  # Завершаем цикл атаки этим оружием
                time_action_hero_spell = 0
                special = False
                axe_swing = 0
                print(f"{hp.START_TIRE}(🔄) Некромант прекращает использовать текущее оружие.{hp.END_TIRE}")

        # Общий таймер для заклинания "Восставшие мертвецы"
        if undead_timer < 50:
            undead_timer += 1

        # Сообщения для заклинания "Восставшие мертвецы"
        if undead_timer == 10:
            print(f"{hp.START_TIRE}(🧟) Воздух взорвался сухим перестуком костей и ледяным воем.За спиной Некроманта, в кромешной тьме зажглись десятки синих точек — словно созвездие из ненавидящих, немигающих глаз, впившихся в вас из вечности...{hp.PURPLE}Мертвецы встают из могил.{hp.RESET}{hp.END_TIRE}")
        elif undead_timer == 20:
            print(f"{hp.START_TIRE}(🧟) {hp.PURPLE} Количество мертвецов увеличивается. Они медленно двигаются к вам со всех сторон.{hp.RESET}{hp.END_TIRE}")
        elif undead_timer == 30:
            print(f"{hp.START_TIRE}(🧟) Вы видите как множество мертвецов создают вокруг вас кольцо.Нужно поскорее расправиться с Некромантом.{hp.END_TIRE}")
        elif undead_timer == 40:
            hero.hero_health -= necromancer.attack
            print(f"{hp.START_TIRE}(🧟) Времени остается мало, количество мертвецов увеличивается. Кому-то из них удается вас ударить. Вы отталкиваете от себя мертвецов, попутно размахивая мечом. Некромант насмехается над вами.{hp.info_room(hero.hero_health,hero.hero_max_health,[necromancer])}{hp.END_TIRE}")
        elif undead_timer == 50:
            hero.hero_health = 0
            print(f"{hp.START_TIRE}(☠️) Вас поглотила волна мертвой плоти. Сотни рук разрывали доспехи, десятки ртов впивались в плоть.")

        # Диапазон вызова сообщений и вызова самих функций заклинания "Восставшие мертвецы"
        elif undead_timer in [15, 25, 35, 45]:
            choice_undead_func = random.choice(undead_func)
            name_undead_func = undead_list[choice_undead_func]
            print(f"{hp.START_TIRE}(🧟) {name_undead_func}{hp.END_TIRE}")
        elif undead_timer in [16, 26, 36, 46]:
            choice_undead_func()

        # (5.3) Команда-заглушка "о"
        elif action_hero == "о":
            print(f"{hp.START_TIRE}Лучше не отвлекаться от сражения.{hp.END_TIRE}")

        # (5.3) Команда "р"
        elif action_hero == "р":
            inventory_system.open_backpack(hero)

        # (5.3) Команда "п".
        elif action_hero == "п":
            hp.show_full_help(hero)

    except Exception as e:
        print(f"{hp.START_TIRE}Произошла ошибка: {hp.RED_BOLD}{e}{hp.RESET}{hp.END_TIRE}")
        if 'timer' in globals():
            timer.cancel()
            input_active = False

else:
    print(f"{hp.START_TIRE}(☠️) Вы погибли, но смерть не стала концом. Синее пламя некромантии выжгло вашу душу и наполнило тело новой, тёмной силой. Вы открыли глаза — теперь они горят холодным синим огнём вечной службы. Герой пал, воин тьмы восстал {hp.END_TIRE}")
	
					
	
	
	
	
	
	
	
	
			
	
	
	
	
		 
		 
		 
		 
		



		
		

	
			
		
		
		
		
	
		
			
		
	
	
		


	




		
		

			
	

	
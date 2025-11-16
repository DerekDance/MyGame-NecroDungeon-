import json
import random

class HelpSystem:
    YELLOW = "\u001b[33m"
    YELLOW_BOLD = "\u001b[33;1m"
    GREEN = "\u001b[32m"
    GREEN_BOLD = "\u001b[32;1m"
    PURPLE = "\u001b[35m"
    PURPLE_BOLD = "\u001b[35;1m"
    BLUE = "\u001b[36m"
    RED = "\u001b[31m"
    RED_BOLD = "\u001b[31;1m"
    CYAN = "\u001b[36m"
    CYAN_BOLD = "\u001b[36;1m"
    RESET = "\u001b[0m"

    #(1.1) Подсказки Ричарда __init__() и форматы строк
    def __init__(self):
        with open("data/help_messages.json","r",encoding = 'utf-8') as file:
            self.help_messages = json.load(file)
            self.YELLOW_STAR_START = f"{self.YELLOW}\n***************{self.RESET}\n"
            self.YELLOW_STAR_END = f"{self.YELLOW}\n***************{self.RESET}"
            self.START_TIRE = f"\n{self.CYAN}--------------------------------------{self.RESET}\n"
            self.END_TIRE = f"\n{self.CYAN}--------------------------------------{self.RESET}\n"

    # Советы из всех комнат в виде словаря.help_first_room должен быть всегда True в начале игры.
        self.help_states = {
            "help_first_room": True,
            "help_second_room_before_fight": False,
            "help_second_room_in_fight": False,
            "help_three_room": False,
            "help_fourth_room_phase_one": False,
            "help_fourth_room_phase_two": False,
            "help_five_room_phase_one": False,
            "help_five_room_phase_two": False,
            "help_five_room_phase_third": False}

    #(1.2) Функция, работающая при вызове команды "п"
    def show_help(self):
        for key, value in self.help_states.items():
            if value == True:
                print(f"{self.CYAN_BOLD}{random.choice(self.help_messages[key])}{self.RESET}")


    #(1.3) Функция для сброса булевых значений на False
    def reset_all_help(self):
        for key in self.help_states:
            self.help_states[key] = False


    #(2) Информирование о характеристиках героя и противников
    def info_room(self, hero_health, hero_max_health, enemies):
        enemy_lines = []
        for enemy in enemies:

            if isinstance(enemy, dict):
                name = enemy['name']
                health = enemy['health']
                distance = enemy['distance']
            else:

                name = getattr(enemy, 'name', 'Неизвестный')
                health = getattr(enemy, 'health', '???')
                distance = getattr(enemy, 'distance', '???')

            enemy_lines.append(
                f"Здоровье \u001b[35m{name}\u001b[0m: {health}\n"
                f"Дистанция до вас: {distance}"
            )

        enemies_block = "\n".join(enemy_lines)

        return (
            f"{self.YELLOW_STAR_START}"
            f"Ваше здоровье: {hero_health}|{hero_max_health}\n"
            f"{enemies_block}"
            f"{self.YELLOW_STAR_END}"
        )


    # (3) Информирование о характеристиках героя
    def show_full_help(self,hero):
        self.show_help()
        print(
            f"{self.YELLOW_STAR_START}"
            f"Информация о герое на данный момент:\n"
            f"Здоровье: {self.CYAN}{hero.hero_health}|{hero.hero_max_health}{self.RESET}\n"
            f"Атака мечом: {self.CYAN}{hero.hero_attack}{self.RESET}\n"
            f"Атака из ружья: {self.CYAN}{hero.hero_range_attack}{self.RESET}\n"
            f"Количество пуль: {self.CYAN}{hero.hero_bullet}{self.RESET}\n"
            f"Золото: {self.CYAN}{hero.hero_gold}{self.RESET}\n"
            f"Зелье силы: {self.CYAN}{hero.hero_potion_strength}{self.RESET}\n"
            f"Зелье здоровья: {self.CYAN}{hero.hero_potion_heal}{self.RESET}\n"
            f"Свитки искр: {self.CYAN}{hero.hero_scroll_of_sparks}{self.RESET}")
        print(
            f"{self.YELLOW}В игре есть восемь активных действий.Вводить нужно только первую букву команды:\n"
            f"- в (вперед)\n"
            f"- н (назад)\n"
            f"- у (увернуться)\n"
            f"- а (атака мечом)\n"
            f"- с (стрельба из ружья)\n"
            f"- о (осмотр-поиск)\n"
            f"- п (помощь-справка)\n"
            f"- р (рюкзак){self.RESET}"
            f"{self.YELLOW_STAR_END}")



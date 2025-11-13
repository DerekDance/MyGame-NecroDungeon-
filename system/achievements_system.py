from system import HelpSystem
import json
import random
import sys

# Для использования форматирования строк
hp = HelpSystem()

class AchievementsSystem:
    ACHIEVEMENTS = {
        "ANTI_MITOZ": {
            "name": f"(🎖️) 'Анти-митоз'",
            "message": f"(🎖) Получено достижение {hp.CYAN}'Анти-митоз'{hp.RESET}"
        },
        "TRAINED": {
            "name": f"(🎖️) 'Я прочитал инструкцию!'",
            "message": f"(🎖) Получено достижение {hp.CYAN}'Я прочитал инструкцию!'{hp.RESET}"
        },
        "SUICIDE": {
            "name": f"(🎖️) 'Самоубийство из вредности'",
            "message": f"(🎖) Получено достижение {hp.CYAN}'Самоубийство из вредности'{hp.RESET}"
        },
        "BYPASSING": {
            "name": f"(🎖️) 'В обход правил'",
            "message": f"(🎖) Получено достижение {hp.CYAN}'В обход правил'{hp.RESET}"
        },
        "PACIFIST": {
            "name": f"(🎖️) 'Пацифист'",
            "message": f"(🎖) Получено достижение {hp.CYAN}'Пацифист'{hp.RESET}"
        },
        "DONT_OPEN": {
            "name": f"(🎖️) 'Не открывай рюкзак'",
            "message": f"(🎖) Получено достижение {hp.CYAN}'Не открывай рюкзак'{hp.RESET}"
        },
        "SKULLS_HUNTER": {
            "name": f"(🎖️) 'Охотник за черепами'",
            "message": f"(🎖) Получено достижение {hp.CYAN}'Охотник за черепами'{hp.RESET}"
        }
    }

    def __init__(self):
        self.players_data = self.load_data()
        self.players = self.players_data.get("players", [])

    # (1) Функция загрузки данных
    def load_data(self):
        try:
            with open("data/players.json", "r", encoding='utf-8') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"{hp.CYAN}Файл не найден,создаем новый!{hp.RESET}")
        except Exception as e:
            print(f"Произошла ошибка: {hp.RED}{e}{hp.RESET}")
        return {"players": []}

    # (2) Функция сохранения данных
    def save_data(self):
        try:
            with open("data/players.json", "w", encoding='utf-8') as file:
                json.dump(self.players_data, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Произошла ошибка: {hp.RED}{e}{hp.RESET}")

    # (3) Функция добавления достижения
    def add_achievement(self, player, achievement_key):
        achievements = player.get("achievements", [])
        achievement_data = self.ACHIEVEMENTS.get(achievement_key)

        if achievement_data and achievement_key not in achievements:
            achievements.append(achievement_key)
            player["achievements"] = achievements
            print(achievement_data["message"])

    # (4) Функция показа рейтинга игроков
    def show_rating(self):
        if not self.players:
            print("Список игроков пуст!")
        else:
            print("-----------Рейтинг Игроков----------")
            for i, player in enumerate(self.players):
                name = player.get("name", "")
                kill_monsters = player.get("kill_monsters", 0)
                completed_locations = player.get("completed_locations", 0)
                games_played = player.get("games_played", 0)
                achievements = player.get("achievements", [])
                print(
                    f"Имя: {name}\nКоличество сыгранных игр : {games_played}\nПройденные локации:{completed_locations}\nУбито противников: {kill_monsters}")
                if achievements:
                    print("-------Достижения-------")
                    for achievement_key in achievements:
                        achievement_data = self.ACHIEVEMENTS.get(achievement_key)
                        if achievement_data:
                            print(f" {hp.CYAN}{achievement_data['name']}{hp.RESET}\n-------------------------")
                        else:
                            print(f" {achievement_key}")
                else:
                    print(f"🎖️ Достижения: \u001b[90mпока нет{hp.RESET}")
                print("─" * 50)

    # (5) Метод главного меню
    def main_menu(self):
        character_data = None
        menu_choice = ""
        while True:
            menu_choice = input("Введите цифру:\n(1) Начать игру\n(2) Рейтинг игроков\n(3) Выход\n>")
            if menu_choice == "3":
                print("Пока!")
                sys.exit()
            elif menu_choice == "2":
                self.show_rating()
            elif menu_choice == "1":
                name_hero = input("Введите имя героя:\n>").strip()

                if not name_hero:
                    print("Имя героя не может быть пустым!")
                    continue
                elif len(name_hero) < 3:
                    print("Слишком короткое имя! Имя должно быть больше двух символов")
                    continue
                elif len(name_hero) > 20:
                    print("Слишком длинное имя! Имя должно быть не больше двадцати символов")
                    continue

                player_in_the_rating_table = None
                for player in self.players:
                    if player["name"].lower() == name_hero.lower():
                        player_in_the_rating_table = player
                        break

                if player_in_the_rating_table:
                    print("Такой игрок уже существует")
                    password = input("Введите код доступа:\n>")
                    if password == player_in_the_rating_table.get("password", ""):
                        print("Код доступа верный! Загружаем существующие данные")
                        character_data = player_in_the_rating_table
                    else:
                        print("(Х) Код доступа неправильный!")
                        continue
                else:
                    password = input("Придумайте код доступа\n>")
                    character_data = {
                        "name": name_hero,
                        "kill_monsters": 0,
                        "completed_locations": 0,
                        "games_played": 0,
                        "best_score": 0,
                        "password": password,
                        "achievements": []
                    }
                    # Добавляем нового игрока в список
                    self.players.append(character_data)



                # Обновление статистики игрока
                character_data["games_played"] = character_data.get("games_played", 0) + 1
                # Сохранение данных
                self.players_data["players"] = self.players
                self.save_data()
                print("💾 Данные сохранены!")
                break  # выйти из цикла меню


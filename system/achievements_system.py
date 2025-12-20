from system import HelpSystem
import json
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
        #  Убедимся, что в players только словари
        self.players = [p for p in self.players_data.get("players", []) if isinstance(p, dict)]
        self.character_data = None

        # Для получения имени игрока
    @property
    def current_player_name(self):
        """Возвращает имя текущего игрока"""
        if self.character_data:
            return self.character_data.get("name")
        return None

    @property
    def current_player(self):
        """Возвращает все данные текущего игрока"""
        return self.character_data


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
    def add_achievement(self, player, achievement_key, all_score):
        achievements = player.get("achievements", [])
        achievement_data = self.ACHIEVEMENTS.get(achievement_key)

        if achievement_data and achievement_key not in achievements:
            achievements.append(achievement_key)
            player["achievements"] = achievements
            print(achievement_data["message"])
            self.character_data["all_score"] = self.character_data.get("all_score", 0) + all_score
            self.save_data()

    # (4) Функция показа рейтинга игроков
    def show_rating(self):
        if not self.players:
            print(f"{hp.RED}Список игроков пуст!{hp.RESET}")
        else:
            print(f"{hp.START_TIRE}        ⭐ Рейтинг Игроков  ⭐      {hp.END_TIRE}")
            # Сортировка игроков по убыванию
            self.players.sort(key=lambda p: p.get("all_score", 0), reverse=True)
            self.players = self.players[:16]
            for i, player in enumerate(self.players):
                # ✅ Проверяем, что player — словарь
                if not isinstance(player, dict):
                    print(f"[DEBUG] Некорректный игрок: {hp.RED}{player}{hp.RESET}")
                    continue

                completed_locations_list = player.get("completed_locations_list", [])
                last_location = completed_locations_list[-1] if completed_locations_list else "Нет"

                name = player.get("name", "")
                kill_monsters = player.get("kill_monsters", 0)
                completed_locations = player.get("completed_locations", 0)
                games_played = player.get("games_played", 0)
                achievements = player.get("achievements", [])
                all_score = player.get("all_score", 0)

                print(
                    f"Имя: {hp.CYAN}{name}{hp.RESET}\n"
                    f"Количество сыгранных игр : {hp.CYAN}{games_played}{hp.RESET}\n"
                    f"Пройденные локации : {hp.CYAN}{completed_locations}{hp.RESET}\n"
                    f"Локация до которой доходил(а) : {hp.CYAN}{last_location}{hp.RESET}\n"
                    f"Убито противников : {hp.CYAN}{kill_monsters}{hp.RESET}\n"
                    f"Общее количество очков : {hp.CYAN}{all_score}{hp.RESET}")

                if achievements:
                    print(f"{hp.CYAN}-------Достижения-------{hp.RESET}")
                    for achievement_key in achievements:
                        achievement_data = self.ACHIEVEMENTS.get(achievement_key)
                        if achievement_data:
                            print(f" {hp.CYAN}{achievement_data['name']}{hp.RESET}\n-------------------------")
                        else:
                            print(f" {achievement_key}")
                else:
                    print(f"🎖️ Достижения: пока нет")
                print("─" * 50)

    # (5) Добавляем пройденную локацию
    def add_completed_location(self, location_name, all_score):
        if not self.character_data:
            print(f"{hp.RED}❌ Нет активного игрока.{hp.RESET}")
            return

        completed_list = self.character_data.get("completed_locations_list", [])
        if location_name not in completed_list:
            completed_list.append(location_name)
            self.character_data["completed_locations_list"] = completed_list
            self.character_data["all_score"] = self.character_data.get("all_score", 0) + all_score
            self.character_data["completed_locations"] += 1
            print(f"🏆 Локация '{location_name}' засчитана как пройденная!")
        else:
            print(f"🔄 Локация '{location_name}' уже была пройдена ранее.")

        # Сохраняем изменения
        self.players_data["players"] = self.players
        self.save_data()

    # (5) Добавляем поверженных противников
    def add_killed_monster(self, monster_name, all_score,):
        if not self.character_data:
            print(f"{hp.RED}❌ Нет активного игрока.{hp.RESET}")
            return

        # Просто увеличиваем счётчик
        self.character_data["kill_monsters"] = self.character_data.get("kill_monsters", 0) + 1
        self.character_data["all_score"] = self.character_data.get("all_score", 0) + all_score

        if monster_name:
            print(f"(💀) Повержен: {monster_name}")
        else:
            print("(💀) Повержен один противник.")

        # Сохраняем данные
        self.players_data["players"] = self.players
        self.save_data()

    # (7) Метод главного меню
    def main_menu(self):
        character_data = None
        menu_choice = ""
        while True:
            menu_choice = input(f"Доступные команды:\n{hp.CYAN}(1) Начать игру\n(2) Рейтинг игроков\n(3) Выход{hp.RESET}\nВведите цифру: ")
            if menu_choice == "3":
                print("Пока!")
                sys.exit()
            elif menu_choice == "2":
                self.show_rating()
            elif menu_choice == "1":
                name_hero = input(f"{hp.CYAN}Введите имя героя: {hp.RESET}").strip()

                if not name_hero:
                    print(f"Имя героя не может быть {hp.RED}пустым!{hp.RESET}")
                    continue
                elif len(name_hero) < 3:
                    print(f"Слишком {hp.RED}короткое имя!{hp.RESET} Имя должно быть больше двух символов")
                    continue
                elif len(name_hero) > 20:
                    print(f"Слишком {hp.RED}длинное имя!{hp.RESET} Имя должно быть не больше двадцати символов")
                    continue

                player_in_the_rating_table = None
                for i,player in enumerate(self.players):
                    if player["name"].lower() == name_hero.lower():
                        player_in_the_rating_table = player
                        break

                if player_in_the_rating_table:
                    print(f"Такой игрок уже существует\nИгрок находится на {hp.RED}{i + 1}{hp.RESET} месте в рейтинговой таблице")
                    password = input(f"{hp.CYAN}Введите код доступа: {hp.RESET}")
                    if password == player_in_the_rating_table.get("password", ""):
                        print(f"{hp.CYAN}Код доступа верный! Загружаем существующие данные{hp.RESET}")
                        self.character_data = player_in_the_rating_table
                    else:
                        print(f"{hp.RED}(Х) Код доступа неправильный!{hp.RESET}")
                        continue
                else:
                    password = input(f"Придумайте {hp.CYAN}код доступа{hp.RESET}: ")
                    self.character_data = {
                        "name": name_hero,
                        "kill_monsters": 0,
                        "completed_locations": 0,
                        "completed_locations_list": [],
                        "games_played": 0,
                        "all_score": 0,
                        "password": password,
                        "achievements": []
                    }
                    # Добавляем нового игрока в список
                    self.players.append(self.character_data)



                # Обновление статистики игрока
                self.character_data["games_played"] = self.character_data.get("games_played", 0) + 1
                # Сохранение данных
                self.players_data["players"] = self.players
                self.save_data()
                print("Данные сохранены!")
                break  # выйти из цикла меню


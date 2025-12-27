from system import HelpSystem

#Для использования форматирования строк
hp = HelpSystem()

class InventorySystem:
    def init(self):
        self.backpack_items = {
            "зелье силы": "hero_potion_strength",
            "зелье лечения": "hero_potion_heal",
            "свиток искр" : "hero_scroll_of_sparks",
            "зелье регенерации здоровья" : "hero_potion_of_regen_hp"
        }

    # (1) Функция отображения рюкзака
    def show_backpack(self, hero):

        items = {
            f"{hp.CYAN}--- Зелье силы{hp.RESET}": hero.hero_potion_strength,
            f"{hp.CYAN}--- Зелье лечения{hp.RESET}": hero.hero_potion_heal,
            f"{hp.CYAN}--- Свиток искр{hp.RESET}" : hero.hero_scroll_of_sparks,
            f"{hp.CYAN}--- Зелье регенерации здоровья{hp.RESET}" : hero.hero_potion_of_regen_hp
        }
        menu_items = [f"{hp.YELLOW_STAR_START}{hp.YELLOW}(🎒) Содержимое рюкзака{hp.RESET}"]

        for name, count in items.items():
            if count > 0:
                menu_items.append(f"{name}: {count}")
        if len(menu_items) == 1:
            menu_items.append("---Рюкзак пустой---")
        return "\n".join(menu_items)

    # (2) Функция использования зелий
    def use_item(self, hero, hero_choice):
        result = ""

        if hero_choice == "1":
            from creatures import DamageModifier
            if hero.hero_potion_strength > 0:
                multiplier = DamageModifier(
                    target=hero,
                    duration=3,
                    value=1.5,
                    operation_type = "*",
                    attack_type = "melee",
                    start_info_msg = f"{hp.CYAN_BOLD}(🗡️) Использовано Зелье силы",
                    end_info_msg = f"(🗡️){hp.CYAN_BOLD} Эффект усиления от Зелья силы",
                    display_name = "Зелье силы"
                )

                if hero.add_modifier(multiplier):  # Проверяем успех добавления
                    hero.hero_potion_strength -= 1
                else:
                    # add_modifier уже вывел сообщение об ошибке
                    pass
            else:
                result = f"{hp.RED}Нет зелья силы!{hp.RESET}"

        elif hero_choice == "2":
            if hero.hero_potion_heal > 0:
                hero.hero_health = min(hero.hero_health + 5, hero.hero_max_health)
                hero.hero_potion_heal -= 1
                result = f"(❤️‍🩹)  {hp.GREEN_BOLD}Вы выпили зелье лечения.{hp.RESET}"
            else:
                result = f"{hp.RED}Нет зелья лечения!{hp.RESET}"

        elif hero_choice == "3":
            if hero.hero_scroll_of_sparks > 0:
                hero.bullet_of_sparks += 1
                hero.hero_scroll_of_sparks -= 1
                result = (f"(📜)  {hp.YELLOW_BOLD}Прочитав свиток на вашем ружье появились раскаленные красные символы.\n"
                          f"Введите на русском {hp.CYAN}'искры'{hp.RESET},{hp.YELLOW_BOLD} чтобы выстрелить дробью.{hp.RESET}")
            else:
                result = f"{hp.RED}Нет свитков искр!{hp.RESET}"

        elif hero_choice == "4":
            from creatures import RegenHP
            if hero.hero_potion_of_regen_hp > 0:
                potion_regen_hp = RegenHP(
                    target=hero,
                    duration=3,
                    step=3,
                    heal_power=1,
                    show_message=True
                )
                if hero.add_modifier(potion_regen_hp):
                    hero.hero_potion_of_regen_hp -= 1
                    result = f"(💊)  {hp.PURPLE_BOLD} Активирована регенерация здоровья.{hp.RESET}"
                else:
                    pass
            else:
                result = f"{hp.RED}Нет зелья регенерации!{hp.RESET}"

        elif hero_choice == "0":
            result = "Вы закрыли рюкзак"

        else:
            result = "Нет такого предмета"

        return result


    # (3) Функция меню рюкзака
    def get_backpack_menu(self):
            return f"{hp.START_TIRE}{hp.GREEN_BOLD}Справка по использованию предметов из рюкзака:\n(0) Закрыть рюкзак\n""(1) Зелье силы - Увеличивает следующую атаку в 2 раза\n""(2) Зелье лечения - Восстанавливает 5 здоровья)\n""(3) Свиток искр - Позволяет стрелять дробью\n"f"(4) Зелье регенерации - Восстанавливает здоровье со временем{hp.RESET}{hp.END_TIRE}".strip()


    # (4) Функция для вызова в main инвентаря одной строкой - open_backpack(hero)
    def open_backpack(self, hero):
        print(f"{hp.START_TIRE}")
        # Начало формата
        hero_choice = ""
        while hero_choice != "0":
            try:
                # Показываем содержимое рюкзака
                print(self.show_backpack(hero))

                hero_choice = input(f"Выберите предмет или введите {hp.CYAN}'м'{hp.RESET} для подсказки: ").lower()
                print(f"{hp.YELLOW_STAR_END}")


                if hero_choice == "0":
                    print("Рюкзак закрыт.")
                    break
                elif hero_choice == "м":
                    # Показываем меню выбора
                    print(self.get_backpack_menu())
                else:
                    # Используем выбранный предмет
                    result = self.use_item(hero, hero_choice)
                    print(result)


            except Exception as e:
                print(f"Ошибка при использовании предмета: {hp.RED}{e}{hp.RESET}")
                return False

        print(f"{hp.END_TIRE}")
        return True

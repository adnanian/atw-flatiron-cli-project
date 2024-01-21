# lib/cli.py

from menu_tools.helpers import (
    begin_divider,
    end_divider,
    execute_clear_terminal,
    main_menu
)


def main():
    while True:
        menu()
        choice = input("> ")
        execute_clear_terminal()
        main_menu.execute_command(int(choice))


def menu():
    print()
    end_divider()
    begin_divider()
    print("Please select an option:")
    main_menu.display_commands()


if __name__ == "__main__":
    main()

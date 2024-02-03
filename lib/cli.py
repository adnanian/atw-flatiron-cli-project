# lib/cli.py

from menu_tools.helpers import (
    begin_divider,
    end_divider,
    execute_clear_terminal,
    get_current_menu
)


def main():
    while True:
        menu()
        choice = input("> ")
        execute_clear_terminal()
        try:
            choice = int(choice)
            get_current_menu().execute_command(choice)
        except Exception as exc:
            print("Must type a number from the menu list to select an option.")


def menu():
    print()
    end_divider()
    begin_divider()
    print(get_current_menu().key_name)
    print("Please select an option:")
    get_current_menu().display_commands()


if __name__ == "__main__":
    main()

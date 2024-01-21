# lib/menu_tools/helpers.py
from menu_tools.menu import Menu
import os

clear_terminal_on = False


def divider():
    """Prints 100 asterisks to the terminal."""
    print("*" * 100)


def begin_divider():
    """Prints a line of asterisks using the divider() function; then breaks another line."""
    divider()
    print()


def end_divider():
    """Breaks a line; then prints another line of asterisks using the divider() function"""
    print()
    divider()


def helper_1():
    print("Performing useful function#1.")


def exit_program():
    print("Goodbye!")
    exit()


def toggle_clear_terminal():
    global clear_terminal_on
    clear_terminal_on = not clear_terminal_on
    try:
        main_menu.get_command_by_callback(
        toggle_clear_terminal
        ).prompt = f"Clear Terminal After Each Command: {'ON' if clear_terminal_on else 'OFF'}"
    except Exception as e:
        print("Error toggling clear terminal mode: ", e)
        
    
def execute_clear_terminal():
    if clear_terminal_on:
        os.system('clear')
    print()


""" Declare main menu commands"""
main_menu = Menu()
main_menu.add_command("Exit the program", exit_program)
main_menu.add_command("Some useful function", helper_1)
main_menu.add_command(
    f"Clear Terminal After Each Command: {'ON' if clear_terminal_on else 'OFF'}",
    toggle_clear_terminal,
)

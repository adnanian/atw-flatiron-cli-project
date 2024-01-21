# lib/menu_tools/helpers.py
from menu_tools.menu import Menu


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
    
""" Declare main menu commands"""    
main_menu = Menu()
main_menu.add_command("Exit the program", exit_program)
main_menu.add_command("Some useful function", helper_1)
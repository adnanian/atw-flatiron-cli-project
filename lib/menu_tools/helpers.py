# lib/menu_tools/helpers.py
from menu_tools.menu import Menu
from models.classification import Classification
from models.language import Language
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
    
def return_to_main_menu():
    global current_menu
    current_menu = Menu.all["main"]
    
def get_current_menu():
    return current_menu

# Main Menu

def exit_program():
    print("Goodbye!")
    exit()

def display_everything():
    """Prints all the tables in the language_categories database."""
    
    # Print the classifications table
    classifications = Classification.get_all()
    Classification.table_heading()
    for row in classifications:
        print(row.table_row())
        
    print("\n")
    
    # Print the languages table
    languages = Language.get_all()
    Language.table_heading()
    for row in languages:
        print(row.table_row())
    
def load_classifications_menu():
    global current_menu
    current_menu = Menu.all["classifications"]
    print(current_menu.key_name)

def load_languages_menu():
    global current_menu
    current_menu = Menu.all["languages"]
    print(current_menu.key_name)

def toggle_clear_terminal():
    global clear_terminal_on
    clear_terminal_on = not clear_terminal_on
    try:
        current_menu.get_command_by_callback(
        toggle_clear_terminal
        ).prompt = f"Clear Terminal After Each Command: {'ON' if clear_terminal_on else 'OFF'}"
    except Exception as e:
        print("Error toggling clear terminal mode: ", e)
        
    
def execute_clear_terminal():
    if clear_terminal_on:
        os.system('clear')
    print()

""" Declare main menu commands"""
main_menu = Menu("main")
main_menu.add_command("Exit the program", exit_program)
main_menu.add_command("Display entire database", display_everything)
main_menu.add_command("Work with classifications", load_classifications_menu)
main_menu.add_command("Work with languages", load_languages_menu)
main_menu.add_command(
    f"Clear Terminal After Each Command: {'ON' if clear_terminal_on else 'OFF'}",
    toggle_clear_terminal,
)

# Classifications Menu
classifications_menu = Menu("classifications")
classifications_menu.add_command("Exit the program", exit_program)
classifications_menu.add_command("Return to main menu", return_to_main_menu)
classifications_menu.add_command("Work with languages", load_languages_menu)

# Languages Menu
languages_menu = Menu("languages")
languages_menu.add_command("Exit the program", exit_program)
languages_menu.add_command("Return to main menu", return_to_main_menu)
languages_menu.add_command("Work with classifications", load_languages_menu)

# Set current menu to "main"
current_menu = Menu.all["main"]


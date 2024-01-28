# lib/menu_tools/helpers.py
from menu_tools.menu import Menu
from models.classification import Classification
from models.language import Language
from models.model_helpers import (is_non_empty_string)
import os

clear_terminal_on = False
CELL_CHAR_LIMIT = 30

# Universal prompts
EXIT_PROMPT = "Exit the program"
TOGGLE_CLEAR_TERMINAL_PROMPT = f"Clear Terminal After Each Command: {'ON' if clear_terminal_on else 'OFF'}"
MAIN_MENU_PROMPT = "Return to main menu"
CLASSIFICATIONS_PROMPT = "Work with classifications"
LANGUAGES_PROMPT = "Work with languages"

# For all menus

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

def format_string_cell_left(var, char_limit):
    if not is_non_empty_string:
        var = str(var)
    if ((length := len(var)) > char_limit):
        var = var[0:(char_limit - 3)] + "..."
    space_size = char_limit - length
    spaces = ' ' * space_size
    return var + spaces

def format_string_cell_center(var, char_limit):
    if not is_non_empty_string:
        var = str(var)
    if ((length := len(var)) <= char_limit):
        pass
        total_spaces = char_limit - length
        var_index = int(total_spaces / 2)
        left_spaces = ' ' * var_index
        right_spaces = ' ' * (total_spaces - var_index)
        
        #print(f"Length of name: {length}")
        #print(f"Total spaces: {total_spaces}")
        #print(f"Var Index: {var_index}")
        #print(f"Left Spaces: {left_spaces}")
        #print(f"Right Spaces: {right_spaces}")   
        
        return left_spaces + var + right_spaces
    else:
        raise ValueError(f"String must be {char_limit} characters or less.")
    
def format_string_cell_right(var, char_limit):
    if not is_non_empty_string:
        var = str(var)
    if ((length := len(var)) > char_limit):
        var = var[0:(char_limit - 3)] + "..."
    space_size = char_limit - length
    spaces = ' ' * space_size
    return spaces + var

def table_row(values, column_lengths):
    if (len(values) == len(column_lengths)):
        if type(values) is tuple:
            row = ""
            for index in range(length := len(values)):
                formatted_column = format_string_cell_right(values[index], column_lengths[index])
                divider = "|" if (index < length - 1) else ""
                column = f" {formatted_column} {divider}"
                row += column
            return row
        else:
            raise TypeError("Values in the table must be passed as a tuple.")
    else:
        raise ValueError("Values and column lengths must be the same size")
    
def table_header(title, values, column_lengths):
    row = table_row(values, column_lengths)
    return f"{title}\n\n{row}\n{('-' * len(row))}"
    

# Main Menu

def exit_program():
    print("Goodbye!")
    exit()

def display_everything():
    """Prints all the tables in the language_categories database."""
    
    # Print the classifications table
    print_classifications_as_table()
    
    # Print the languages table
    print_languages_as_table()
    
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
main_menu.add_command(EXIT_PROMPT, exit_program)
main_menu.add_command(TOGGLE_CLEAR_TERMINAL_PROMPT, toggle_clear_terminal)
main_menu.add_command("Display entire database", display_everything)
main_menu.add_command(CLASSIFICATIONS_PROMPT, load_classifications_menu)
main_menu.add_command(LANGUAGES_PROMPT, load_languages_menu)


# Classifications Menu

def get_classification_column_lengths():
    pass

def print_classifications_as_table():
    """ TODO """
    classifications = Classification.get_all()
    header_names = ("name", "geographic_location")
    column_lengths = [max(len(header), int(Classification.get_longest_attribute_length(header)[0])) for header in header_names]
    print(table_header("Language Classifications", header_names, column_lengths))
    for classification in classifications:
        name = classification.name
        location = classification.geographic_location
        cells = (name, location)
        print(table_row(cells, column_lengths))
    print()
    
def create_classification():
    """ TODO """
    pass
    name = input("Enter the classification name: ")
    geographic_location = input("Enter the classification's geographic location: ")
    try:
        pass
        classification = Classification.create(name, geographic_location)
        print("Classification successfully created")
    except Exception as exc:
        pass


""" Declare classifications commands"""
classifications_menu = Menu("classifications")
classifications_menu.add_command(EXIT_PROMPT, exit_program)
classifications_menu.add_command(MAIN_MENU_PROMPT, return_to_main_menu)
classifications_menu.add_command(LANGUAGES_PROMPT, load_languages_menu)
classifications_menu.add_command("Display classifications table", print_classifications_as_table)


# Languages Menu

def print_languages_as_table():
    languages = Language.get_all()
    header_names = ("name", "number_of_speakers", "country_of_origin", "status", "classification")
    column_lengths = [max(len(header), int(Language.get_longest_attribute_length(header)[0])) for header in header_names]
    print(table_header("Languages", header_names, column_lengths))
    for language in languages:
        name = language.name
        speakers = '{:,}'.format(language.number_of_speakers)
        country = language.country_of_origin
        status = language.status
        classification_name = Classification.find_by_id(language.classification_id).name
        cells = (name, speakers, country, status, classification_name)
        print(table_row(cells, column_lengths))
    print()

languages_menu = Menu("languages")
languages_menu.add_command(EXIT_PROMPT, exit_program)
languages_menu.add_command(MAIN_MENU_PROMPT, return_to_main_menu)
languages_menu.add_command(CLASSIFICATIONS_PROMPT, load_classifications_menu)
languages_menu.add_command("Display languages table", print_languages_as_table)

# Set current menu to "main"
current_menu = Menu.all["main"]


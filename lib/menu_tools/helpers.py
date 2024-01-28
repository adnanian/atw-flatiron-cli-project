# lib/menu_tools/helpers.py
from menu_tools.menu import Menu
from menu_tools.formatting import *
from models.classification import Classification
from models.language import Language
import os

# Constants
clear_terminal_on = False
CELL_CHAR_LIMIT = 30


# Universal prompts
EXIT_PROMPT = "Exit the program"
TOGGLE_CLEAR_TERMINAL_PROMPT = (
    f"Clear Terminal After Each Command: {'ON' if clear_terminal_on else 'OFF'}"
)
MAIN_MENU_PROMPT = "Return to main menu"
CLASSIFICATIONS_PROMPT = "Work with classifications"
LANGUAGES_PROMPT = "Work with languages"

# For all menus


def return_to_main_menu():
    global current_menu
    current_menu = Menu.all["main"]


def get_current_menu():
    return current_menu


# Main Menu


def exit_program():
    """TODO"""
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
        ).prompt = (
            f"Clear Terminal After Each Command: {'ON' if clear_terminal_on else 'OFF'}"
        )
    except Exception as e:
        print("Error toggling clear terminal mode: ", e)


def execute_clear_terminal():
    if clear_terminal_on:
        os.system("clear")
    print()


""" Declare main menu commands"""
main_menu = Menu("main")
main_menu.add_command(EXIT_PROMPT, exit_program)
main_menu.add_command(TOGGLE_CLEAR_TERMINAL_PROMPT, toggle_clear_terminal)
main_menu.add_command("Display entire database", display_everything)
main_menu.add_command(CLASSIFICATIONS_PROMPT, load_classifications_menu)
main_menu.add_command(LANGUAGES_PROMPT, load_languages_menu)


# Classifications Menu


def non_id_classification_column_names():
    """TODO"""
    column_names = [column[1] for column in Classification.get_column_names()]
    column_names = tuple(column_names[1 : len(column_names)])
    return column_names


def get_classification_column_lengths(header_names):
    """TODO"""
    return [
        max(len(header), int(Classification.get_longest_attribute_length(header)[0]))
        for header in header_names
    ]


def print_classification_table_row(classification, column_lengths):
    """TODO"""
    if isinstance(classification, Classification):
        name = classification.name
        location = classification.geographic_location
        cells = (name, location)
        print(table_row(cells, column_lengths))
    else:
        raise TypeError("First argument must be a classification.")


def display_classifications(title, classification_rows):
    """Displays a given set of rows from the classifications table in a cli table format."""
    header_names = non_id_classification_column_names()
    column_lengths = get_classification_column_lengths(header_names)
    print(table_header(title, header_names, column_lengths))
    for classification in classification_rows:
        print_classification_table_row(classification, column_lengths)
    print()


def print_classifications_as_table():
    """TODO"""
    display_classifications("Language Classifications", Classification.get_all())


def create_classification():
    """TODO"""
    name = input("Enter the classification name: ")
    geographic_location = input("Enter the classification's geographic location: ")
    try:
        classification = Classification.create(name, geographic_location)
        display_classifications("Classification successfully created", [classification])
    except Exception as exc:
        print("Classification creation failed: ", exc)


def update_classification():
    name = input("Enter the name of the classification you would like to update: ")
    if classification := Classification.find_by_name(name):
        try:
            new_name = input(
                "\nEnter the classification's new name.\n"
                + "If you wish to keep the current value, simply press ENTER: "
            )
            new_name = new_name if new_name else classification.name
            print(new_name)
            new_location = input(
                "\nEnter the classification's new geographic location.\n"
                + "If you wish to keep the current value, simply press ENTER: "
            )
            new_location = (
                new_location if new_location else classification.geographic_location
            )
            print(new_location)
            # Update
            classification.name = new_name
            classification.geographic_location = new_location
            classification.update()
            display_classifications(
                "\nClassification successfully updated",
                [Classification.find_by_name(new_name)],
            )
        except Exception as exc:
            print("Classification update failed:", exc)
    else:
        print(f"Classification with name, '{name}', not found.")


def delete_classification():
    name = input("Enter the name of the classification to delete: ")
    if clasification := Classification.find_by_name(name):
        clasification.delete()
        print(f"Classification with name, '{name}' deleted!")
    else:
        print(f"Classification with name, '{name}' not found!")


def list_languages_in_classification():
    name = input("Enter the classification name: ")
    if classification := Classification.find_by_name(name):
        display_languages(classification.languages())


""" Declare classifications commands"""
classifications_menu = Menu("classifications")
classifications_menu.add_command(EXIT_PROMPT, exit_program)
classifications_menu.add_command(MAIN_MENU_PROMPT, return_to_main_menu)
classifications_menu.add_command(LANGUAGES_PROMPT, load_languages_menu)
classifications_menu.add_command(
    "Display classifications table", print_classifications_as_table
)
classifications_menu.add_command("Create classification", create_classification)
classifications_menu.add_command("Update classification", update_classification)
classifications_menu.add_command("Delete classification", delete_classification)
classifications_menu.add_command(
    "List a classification's languages", list_languages_in_classification
)


# Languages Menu
def non_id_language_column_names():
    """TODO"""
    column_names = [column[1] for column in Language.get_column_names()]
    column_names[-1] = "classification"
    column_names = tuple(column_names[1 : len(column_names)])
    return column_names


def get_language_column_lengths(header_names):
    """TODO"""
    return [
        max(len(header), int(Language.get_longest_attribute_length(header)[0]))
        for header in header_names
    ]


def print_language_table_row(language, column_lengths):
    """TODO"""
    if isinstance(language, Language):
        name = language.name
        speakers = "{:,}".format(language.number_of_speakers)
        country = language.country_of_origin
        status = language.status
        classification_name = Classification.find_by_id(language.classification_id).name
        cells = (name, speakers, country, status, classification_name)
        print(table_row(cells, column_lengths))
    else:
        raise TypeError("First argument must be a language.")


def display_languages(title, language_rows):
    """Displays a given set of rows from the languages table in a cli table format."""
    header_names = non_id_language_column_names()
    column_lengths = get_language_column_lengths(header_names)
    print(table_header(title, header_names, column_lengths))
    for language in language_rows:
        print_language_table_row(language, column_lengths)
    print()


def create_language():
    """TODO"""
    name = input("Enter the language name: ")
    speakers = int(
        input(
            "\nEnter the number of speakers for that language.\n"
            + "Do not use commas: "
        )
    )
    country = input("\nEnter the country the language originates from: ")
    status = input(
        "\nEnter the language's current existence status:\n\n"
        + "LIVING - language is alive today and currently in use by millions of people\n"
        + "ENDANGERED - language which has a very few number of native speakers and at risk of going extinct\n"
        + "DEAD - language that has no native speakers, but is spoken as a second language in some areas\n"
        + "EXTINCT - language that is no longer extinct and no longer possible to revive\n\n"
        + "Status: "
    )
    classification_name = input("Enter the classification name: ").title()
    classification_id = Classification.find_by_name(classification_name).id
    try:
        language = Language.create(name, speakers, country, status, classification_id)
        display_languages("Language successfully created", [language])
    except Exception as exc:
        print("Language creation failed: ", exc)


def update_language():
    name = input("Enter the name of the language you would like to update: ")
    if language := Language.find_by_name(name):
        try:
            # New name
            new_name = input(
                "\nEnter the language's new name.\n"
                + "If you wish to keep the current value, simply press ENTER: "
            )
            new_name = new_name if new_name else language.name
            print(new_name)

            # New speaker count
            new_speaker_count = input(
                "\nEnter the language's new speaker count (No commas).\n"
                + "If you wish to keep the current value, simply press ENTER: "
            )
            new_speaker_count = (
                int(new_speaker_count) if new_speaker_count else language.number_of_speakers
            )
            print(new_speaker_count)

            # New country
            new_country = input(
                "\nEnter the language's new country of origin.\n"
                + "If you wish to keep the current value, simply press ENTER: "
            )
            new_country = new_country if new_country else language.country_of_origin
            print(new_country)

            # New status
            new_status = input(
                "\nEnter the language's new status.\n"
                + "If you wish to keep the current value, simply press ENTER: "
            )
            new_status = new_status if new_status else language.status
            print(new_status)

            # New classification id
            new_classification_name = input(
                "\nEnter the language's new classification name.\n"
                + "If you wish to keep the current value, simply press ENTER: "
            )
            print(new_classification_name)
            new_classification_id = (
                Classification.find_by_name(new_classification_name).id
                if new_classification_name
                else language.classification_id
            )
            #print(new_classification_id)

            # Update
            language.name = new_name
            language.number_of_speakers = new_speaker_count
            language.country_of_origin = new_country
            language.status = new_status
            language.classification_id = new_classification_id
            language.update()
            display_languages(
                "\nLanguage successfully updated", [Language.find_by_name(new_name)]
            )
        except Exception as exc:
            print("Language update failed:", exc)
    else:
        print(f"Language with name, '{name}', not found.")


def delete_language():
    name = input("Enter the name of the language to delete: ")
    if language := Language.find_by_name(name):
        language.delete()
        print(f"Language with name, '{name}' deleted!")
    else:
        print(f"Language with name, '{name}' not found!")


def print_languages_as_table():
    display_languages("Languages", Language.get_all())


languages_menu = Menu("languages")
languages_menu.add_command(EXIT_PROMPT, exit_program)
languages_menu.add_command(MAIN_MENU_PROMPT, return_to_main_menu)
languages_menu.add_command(CLASSIFICATIONS_PROMPT, load_classifications_menu)
languages_menu.add_command("Display languages table", print_languages_as_table)
languages_menu.add_command("Create language", create_language)
languages_menu.add_command("Update language", update_language)
languages_menu.add_command("Delete language", delete_language)

# Set current menu to "main"
current_menu = Menu.all["main"]

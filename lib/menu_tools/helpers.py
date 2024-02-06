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

# Prompt for commands that take the user to the main menu.
MAIN_MENU_PROMPT = "Return to main menu"

# Prompt for commands that take the user to the classifications menu.
CLASSIFICATION_MENU_PROMPT = "Go to classifications menu"

# Prompt for commands that require to enter a number associated with a printed classification name.
SELECT_CLASSIFICATION_PROMPT = (
    "Type a number from the list above to select a classification: "
)

# Prompt for commands that take the user to the languages menu.
LANGUAGE_MENU_PROMPT = "Go to languages menu"

# Prompt for commands that reqruie to enter a number associated with a printed language name.
SELECT_LANGUAGE_PROMPT = "Type a number from the list above to select a language: "


# For all menus


def return_to_main_menu():
    """ Set the current menu to the main menu. """
    global current_menu
    current_menu = Menu.all["main"]


def get_current_menu():
    """ Get the current menu to be displayed to the user. """
    return current_menu


def invalid_option_message():
    """ Prints a message stating that an invalid number has been entered by the user. """
    print("Invalid option number entered.")


def select_model_name_option(prompt, model_name):
    """
    Prints a menu of model names (either Classification or Language) to the user,
    allowing the user to select a number associated with the name attribute of 
    the model instance. Once a number is selected, the model object is returned.

    Args:
        prompt (str): the prompt to display to the user.
        model_name (Classification or Language): the name of the model (classification or language).

    Raises:
        ValueError: If the model_name argument isn't passed as either "classification or language"

    Returns:
        Classification, Language, or None: the model object if a valid number was selected, None otherwise.
    """
    if isinstance(model_name, str) and (
        model_name == Classification.MODEL_NAME or model_name == Language.MODEL_NAME
    ):
        names = {
            option_number + 1: model.name
            for option_number, model in zip(
                range(
                    Classification.row_count()[0]
                    if model_name == Classification.MODEL_NAME
                    else Language.row_count()[0]
                ),
                Classification.get_all()
                if model_name == Classification.MODEL_NAME
                else Language.get_all(),
            )
        }
        print_dictionary_as_menu(names)
        print()
        model_to_return = None
        try:
            name = names[int(input(prompt))]
            model_to_return = (
                Classification.find_by_name(name)
                if model_name == Classification.MODEL_NAME
                else Language.find_by_name(name)
            )
        except Exception as exc:
            invalid_option_message()
        finally:
            return model_to_return
    else:
        raise ValueError("Model name must be either a classification or language.")


# Main Menu


def exit_program():
    """ Terminates the program. """
    print("Goodbye!")
    exit()


def display_everything():
    """Prints all the tables in the language_categories database."""
    # Print the classifications table
    print_classifications_as_table()
    # Print the languages table
    print_languages_as_table()


def load_classifications_menu():
    """ Sets the current menu to the classifications menu and displays the current data to the user. """
    global current_menu
    current_menu = Menu.all["classifications"]
    #print(current_menu.key_name)
    print_classifications_as_table()


def load_languages_menu():
    """ Sets the current menu to the languages menu and displays the current data to the user. """
    global current_menu
    current_menu = Menu.all["languages"]
    #print(current_menu.key_name)
    print_languages_as_table()


def toggle_clear_terminal():
    """
    Enables or disables the setting to clear the terminal after the execution of a command by a user typing a number.
    If this setting is on at the time this method is called, then calling it will toggle it off.
    If this setting is off at the time this method is called, then calling it will toggle it on.
    """
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
    """ Clears the terminal (if the setting is on) and prints a new empty line. """
    if clear_terminal_on:
        os.system("clear")
    print()


""" Declare main menu commands"""
main_menu = Menu("main")
main_menu.add_command(EXIT_PROMPT, exit_program)
main_menu.add_command(TOGGLE_CLEAR_TERMINAL_PROMPT, toggle_clear_terminal)
main_menu.add_command("Display entire database", display_everything)
main_menu.add_command(CLASSIFICATION_MENU_PROMPT, load_classifications_menu)
main_menu.add_command(LANGUAGE_MENU_PROMPT, load_languages_menu)


# Classifications Menu

def non_id_classification_column_names():
    """ Returns all the column names from the classifications table (with the exception of id).

    Returns:
        tuple: the non-id column names as a tuple 
    """
    column_names = [column[1] for column in Classification.get_column_names()]
    column_names = tuple(column_names[1 : len(column_names)])
    return column_names

def get_classification_column_lengths(header_names):
    """Returns the longest lengths from the cells of each non-id classificaiton column.

    Args:
        header_names (tuple): the names of the columns/headers

    Returns:
        list: the calculated column lengths as a list.
    """
    return [
        max(len(header), int(Classification.get_longest_attribute_length(header)[0]))
        for header in header_names
    ]

def print_classification_table_row(classification, column_lengths, row_number):
    """ Displays to the user the information of one Classification instance as a table row.

    Args:
        classification (Classification): the Classification object.
        column_lengths (list): the column lengths that the row should be set to.
        row_number (int): the row number to print.

    Raises:
        TypeError: if the first argument is not an instance of Classification.
    """
    if isinstance(classification, Classification):
        name = classification.name
        location = classification.geographic_location
        cells = (name, location)
        print(table_row(cells, column_lengths, row_number))
    else:
        raise TypeError("First argument must be a classification.")

def display_classifications(title, classification_rows):
    """Displays a given set of rows from the classifications table in a cli table format."""
    header_names = non_id_classification_column_names()
    column_lengths = get_classification_column_lengths(header_names)
    print(table_header(title, header_names, column_lengths))
    for classification, row_number in zip(classification_rows, range(1, len(classification_rows) + 1)):
        print_classification_table_row(classification, column_lengths, row_number)
    print()

def print_classifications_as_table():
    """
    Displays the entire classifications table to the user.
    """
    display_classifications("Classifications", Classification.get_all())

def create_classification():
    """
    Prompts a user to enter values for a name and geographic_location to create a new instance of Classification.
    """
    try:
        name = input("Enter the classification name: ")
        geographic_location = input("Enter the classification's geographic location: ")
        classification = Classification.create(name, geographic_location)
        display_classifications("Classification successfully created", [classification])
    except Exception as exc:
        print("Classification creation failed: ", exc)

def update_classification():
    """ Prompts the user to update the attribute values of an instance of classification. """
    if classification := select_model_name_option(
        SELECT_CLASSIFICATION_PROMPT, Classification.MODEL_NAME
    ):
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

def delete_classification():
    """ Prompts the user to delete a classification instance. """
    if classification := select_model_name_option(
        SELECT_CLASSIFICATION_PROMPT, Classification.MODEL_NAME
    ):
        classification.delete()
        print(f"Classification with name, '{classification.name}' deleted!")

def list_languages_in_classification():
    """ Prompts the user to list all the languages of a classification. """
    if classification := select_model_name_option(
        SELECT_CLASSIFICATION_PROMPT, Classification.MODEL_NAME
    ):
        display_languages(
            f"{classification.name} Languages", classification.languages()
        )


""" Declare classifications commands"""
classifications_menu = Menu("classifications")
classifications_menu.add_command(EXIT_PROMPT, exit_program)
classifications_menu.add_command(MAIN_MENU_PROMPT, return_to_main_menu)
classifications_menu.add_command(LANGUAGE_MENU_PROMPT, load_languages_menu)
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
    """ Returns all the column names from the languages table (with the exception of id).

    Returns:
        tuple: the non-id column names as a tuple 
    """
    column_names = [column[1] for column in Language.get_column_names()]
    column_names[-1] = "classification"
    column_names = tuple(column_names[1 : len(column_names)])
    return column_names

def get_language_column_lengths(header_names):
    """Returns the longest lengths from the cells of each non-id language column.

    Args:
        header_names (tuple): the names of the columns/headers

    Returns:
        list: the calculated column lengths as a list.
    """
    return [
        max(len(header), int(Language.get_longest_attribute_length(header)[0]))
        for header in header_names
    ]

def print_language_table_row(language, column_lengths, row_number):
    """ Displays to the user the information of one Language instance as a table row.

    Args:
        language (Language): the Language object.
        column_lengths (list): the column lengths that the row should be set to.
        row_number (int): the row number to print.

    Raises:
        TypeError: if the first argument is not an instance of Classification.
    """
    if isinstance(language, Language):
        name = language.name
        speakers = "{:,}".format(language.number_of_speakers)
        country = language.country_of_origin
        status = language.status
        classification_name = Classification.find_by_id(language.classification_id).name
        cells = (name, speakers, country, status, classification_name)
        print(table_row(cells, column_lengths, row_number))
    else:
        raise TypeError("First argument must be a language.")

def display_languages(title, language_rows):
    """Displays a given set of rows from the languages table in a cli table format."""
    header_names = non_id_language_column_names()
    column_lengths = get_language_column_lengths(header_names)
    print(table_header(title, header_names, column_lengths))
    for language, row_number in zip(language_rows, range(1, len(language_rows) + 1)):
        print_language_table_row(language, column_lengths, row_number)
    print()
    
def print_languages_as_table():
    """  Displays the entire languages table to the user. """
    display_languages("Languages", Language.get_all())
    
def select_language_status():
    """ Displays a mini menu of the different language statuses that a user is prompted to add to the language object. """
    print()
    statuses = {
        option_number + 1: status
        for option_number, status in zip(
            range(len(Language.STATUSES)),
            Language.STATUSES
        )
    }
    print_dictionary_as_menu(statuses)
    status = None
    try:
        status = statuses[int(input("Type a number from the list above to select the language's status: "))]
    except Exception as exc:
        invalid_option_message()
    finally:
        print()
        return status

def create_language():
    """Prompts a user to enter values to create a new instance of Language."""
    try:
        name = input("Enter the language name: ")
        speakers = int(
            input(
                "\nEnter the number of speakers for that language.\n"
                + "Do not use commas: "
            )
        )
        country = input("\nEnter the country the language originates from: ")
        status = select_language_status()
        classification = select_model_name_option(SELECT_CLASSIFICATION_PROMPT, Classification.MODEL_NAME)
        classification_id = classification.id if classification else None
        language = Language.create(name, speakers, country, status, classification_id)
        display_languages("Language successfully created", [language])
    except Exception as exc:
        print("Language creation failed: ", exc)


def update_language():
    """ Prompts the user to update the attribute values of an instance of Language. """
    if language := select_model_name_option(SELECT_LANGUAGE_PROMPT, Language.MODEL_NAME):
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
                int(new_speaker_count)
                if new_speaker_count
                else language.number_of_speakers
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
            change_status = input(
                "\nType any key if you would like to update the status.\n"
                + "If you wish to keep the current value, simply press ENTER: "
            )
            new_status = select_language_status() if change_status else language.status
            print(new_status)

            # New classification id
            change_classification = input(
                "\nType any key if you would like to update the classification.\n"
                + "If you wish to keep the current value, simply press ENTER: "
            )
            new_classification_id = None
            if change_classification:
                new_classification = select_model_name_option(SELECT_CLASSIFICATION_PROMPT, Classification.MODEL_NAME)
                new_classification_id = new_classification.id if new_classification else None
            else:
                new_classification_id = language.classification_id
            # print(new_classification_id)

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

def delete_language():
    """ Prompts the user to delete a Language instance. """
    if language := select_model_name_option(SELECT_LANGUAGE_PROMPT, Language.MODEL_NAME):
        language.delete()





languages_menu = Menu("languages")
languages_menu.add_command(EXIT_PROMPT, exit_program)
languages_menu.add_command(MAIN_MENU_PROMPT, return_to_main_menu)
languages_menu.add_command(CLASSIFICATION_MENU_PROMPT, load_classifications_menu)
languages_menu.add_command("Display languages table", print_languages_as_table)
languages_menu.add_command("Create language", create_language)
languages_menu.add_command("Update language", update_language)
languages_menu.add_command("Delete language", delete_language)

# Set current menu to "main"
current_menu = Menu.all["main"]

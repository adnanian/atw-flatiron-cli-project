from models.model_helpers import is_non_empty_string

# When printing out table headers.
ROW_NUMBER_HEADER = "Row #"

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

# NOT USED
def format_string_cell_left(var, char_limit):
    """ Justifies a table cell to the left and returns that value to be displayed to the cell.

    Args:
        var (str): the string.
        char_limit (int): _description_

    Returns:
        str: var padded to the righty by a calculated number of spaces. 
             if the length of var is greater than the char_limit, then var is trimmmed.
    """
    if not is_non_empty_string:
        var = str(var)
    if (length := len(var)) > char_limit:
        var = var[0 : (char_limit - 3)] + "..."
    space_size = char_limit - length
    spaces = " " * space_size
    return var + spaces

# NOT USED
def format_string_cell_center(var, char_limit):
    """ Justifies a table cell to the center and returns that value to be displayed to the cell.

    Args:
        var (str): the string.
        char_limit (int): _description_

    Returns:
        str: var padded to the righty by a calculated number of spaces. 
             if the length of var is greater than the char_limit, then var is trimmmed.
    """
    if not is_non_empty_string:
        var = str(var)
    if (length := len(var)) <= char_limit:
        pass
        total_spaces = char_limit - length
        var_index = int(total_spaces / 2)
        left_spaces = " " * var_index
        right_spaces = " " * (total_spaces - var_index)

        # print(f"Length of name: {length}")
        # print(f"Total spaces: {total_spaces}")
        # print(f"Var Index: {var_index}")
        # print(f"Left Spaces: {left_spaces}")
        # print(f"Right Spaces: {right_spaces}")

        return left_spaces + var + right_spaces
    else:
        raise ValueError(f"String must be {char_limit} characters or less.")


def format_string_cell_right(var, char_limit):
    """ Justifies a table cell to the right and returns that value to be displayed to the cell.

    Args:
        var (str): the string.
        char_limit (int): _description_

    Returns:
        str: var padded to the righty by a calculated number of spaces. 
             if the length of var is greater than the char_limit, then var is trimmmed.
    """
    if not is_non_empty_string:
        var = str(var)
    if (length := len(var)) > char_limit:
        var = var[0 : (char_limit - 3)] + "..."
    space_size = char_limit - length
    spaces = " " * space_size
    return spaces + var


def table_row(values, column_lengths, row_number):
    """ Formats the values of a model instance as a table row and returns that format.

    Args:
        values (tuple): the model instance's attributes; the columns
        column_lengths (tuple): the lengths that each cell in the table should be set to.
        row_number (int or str): the row number for the table format.

    Raises:
        ValueError: If row_number is not a positive integer or the string: 'Row #'.
        TypeError: If the variable passed in values is not a tuple.
        ValueError: If the lengths of values and column_lengths are not equal.

    Returns:
        str: a table row of the model instance's attribute values to print to the terminal.
    """
    if len(values) == len(column_lengths):
        if type(values) is tuple:
            if ((type(row_number) is int and row_number > 0) or row_number == ROW_NUMBER_HEADER):
                ROW_NUMBER_LENGTH = 6
                row = format_string_cell_right(str(row_number), ROW_NUMBER_LENGTH) + " |"
                for index in range(length := len(values)):
                    formatted_column = format_string_cell_right(
                        values[index], column_lengths[index]
                    )
                    divider = "|" if (index < length - 1) else ""
                    column = f" {formatted_column} {divider}"
                    row += column
            else:
                raise ValueError("Row number must be either a positive integer or the string header 'Row #'")
            
            return row
        else:
            raise TypeError("Values in the table must be passed as a tuple.")
    else:
        raise ValueError("Values and column lengths must be the same size")


def table_header(title, values, column_lengths):
    """Formats the attribute names of a model instance as a table header and returns that format.

    Args:
        title (str): the name of the table
        values (tuple): the model instance's attribute names, the column names
        column_lengths (_type_): the lengths that the columns should be set to.

    Returns:
        str: a table header of the model instance's attribute names to print to the terminal.
    """
    row = table_row(values, column_lengths, ROW_NUMBER_HEADER)
    return f"{title}\n\n{row}\n{('-' * len(row))}"

def print_dictionary_as_menu(dictionary):
    """ TODO """
    [print(f"{key}. {value}") for key, value in dictionary.items()]
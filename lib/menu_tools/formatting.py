from models.model_helpers import is_non_empty_string

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

def format_string_cell_left(var, char_limit):
    """ TODO """
    if not is_non_empty_string:
        var = str(var)
    if (length := len(var)) > char_limit:
        var = var[0 : (char_limit - 3)] + "..."
    space_size = char_limit - length
    spaces = " " * space_size
    return var + spaces


def format_string_cell_center(var, char_limit):
    """ TODO """
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
    """ TODO """
    if not is_non_empty_string:
        var = str(var)
    if (length := len(var)) > char_limit:
        var = var[0 : (char_limit - 3)] + "..."
    space_size = char_limit - length
    spaces = " " * space_size
    return spaces + var


def table_row(values, column_lengths):
    """ TODO """
    if len(values) == len(column_lengths):
        if type(values) is tuple:
            row = ""
            for index in range(length := len(values)):
                formatted_column = format_string_cell_right(
                    values[index], column_lengths[index]
                )
                divider = "|" if (index < length - 1) else ""
                column = f" {formatted_column} {divider}"
                row += column
            return row
        else:
            raise TypeError("Values in the table must be passed as a tuple.")
    else:
        raise ValueError("Values and column lengths must be the same size")


def table_header(title, values, column_lengths):
    """ TODO """
    row = table_row(values, column_lengths)
    return f"{title}\n\n{row}\n{('-' * len(row))}"

def print_dictionary_as_menu(dictionary):
    [print(f"{key}. {value}") for key, value in dictionary.items()]
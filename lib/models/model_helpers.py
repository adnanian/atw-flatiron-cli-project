NAME_COL_LIMIT = 24

def is_non_empty_string(var):
    return isinstance(var, str) and len(var)


def validate_attribute_text(var, attribute_name):
    """Validator function - if a given variable and attribute name, both must be non empty strings."""

    var_is_string = is_non_empty_string(var)
    attr_is_string = is_non_empty_string(attribute_name)

    if not (var_is_string and attr_is_string):
        raise ValueError(f"'{attribute_name.title()}' must be a non-empty string.")
"""
def format_string_cell(var):
    if not is_non_empty_string:
        var = str(var)
    if ((length := len(var)) <= NAME_COL_LIMIT):
        pass
        total_spaces = NAME_COL_LIMIT - length
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
        raise ValueError("String must be 24 characters or less.")
"""
    
def format_string_cell(var):
    if not is_non_empty_string:
        var = str(var)
    if ((length := len(var)) > NAME_COL_LIMIT):
        var = var[0:(NAME_COL_LIMIT - 3)] + "..."
    space_size = NAME_COL_LIMIT - length
    spaces = ' ' * space_size
    return var + spaces
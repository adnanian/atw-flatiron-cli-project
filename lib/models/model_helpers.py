NAME_COL_LIMIT = 24

def is_non_empty_string(var):
    """Validates if a given variable is a non-empty string.

    Args:
        var (any): the variable.

    Returns:
        bool: True if var is a non-empty string; False otherwise.
    """
    return isinstance(var, str) and len(var)


def validate_attribute_text(var, attribute_name):
    """Validator function - if a given variable and attribute name, both must be non empty strings."""

    var_is_string = is_non_empty_string(var)
    attr_is_string = is_non_empty_string(attribute_name)

    if not (var_is_string and attr_is_string):
        raise ValueError(f"'{attribute_name.title()}' must be a non-empty string.")
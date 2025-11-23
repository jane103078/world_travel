# ***************************************************************
# Author: (Hsing-E Tsai)
# Lab: (week5 input_validation)
# Date: (10/22/2025)
# Description: Provides reusable functions to validate user input,
#              including integers, floats, strings, yes/no, and
#              selection from a list.
# ***************************************************************

def check_range(val, ge=None, gt=None, le=None, lt=None):
    """Check if val meets given range constraints."""
    if ge is not None and val < ge:
        print(f"Must be greater than or equal to {ge}.")
        return False
    if gt is not None and val <= gt:
        print(f"Must be greater than {gt}.")
        return False
    if le is not None and val > le:
        print(f"Must be less than or equal to {le}.")
        return False
    if lt is not None and val >= lt:
        print(f"Must be less than {lt}.")
        return False
    return True


def input_int(prompt="Please enter a whole number greater "
                     "than or equal to 0 and less than 100: ",
              error="Not a valid whole number. Try again.",
              ge=None, gt=None, le=None, lt=None):

    """
    Prompts the user for an integer and checks if it meets given conditions.

    Parameters:
        prompt: Input message.
        error: Error message.
        ge: great or equal to value.
        gt: greater than value.
        le: less or equal to value.
        lt: less than value.

    Returns:
        A valid integer.
    """

    while True:
        try:
            val = int(input(prompt))
            if check_range(val, ge, gt, le, lt):
                return val
        except ValueError:
            print(error)


def input_float(prompt="Please enter a decimal number between 1 and 30 inclusive:",
                error="Not a valid decimal number. Try again.",
                ge=None, gt=None, le=None, lt=None):

    """
    Prompts the user for a float and checks if it meets given conditions.

    Parameters:
        prompt: Input message.
        error: Error message.
        ge: great or equal to value.
        gt: greater than value.
        le: less or equal to value.
        lt: less than value.

    Returns:
        A valid float.
    """

    while True:
        try:
            val = float(input(prompt))
            if check_range(val, ge, gt, le, lt):
                return val
        except ValueError:
            print(error)


def input_string(prompt="Please enter text: ",
                 error="Invalid input. Try again.",
                 valid=lambda s: bool(s.strip())):
    """
    Prompts the user for a string and checks it using a validation function.

    Parameters:
        prompt: Input message.
        error: Error message.
        valid: A validation function returning True/False.

    Returns:
        A valid string.
    """
    while True:
        val = input(prompt)
        if valid(val):
            return val
        print(error)


def y_or_n(prompt="Please answer yes or no: ",
           error="Invalid input. Please type yes or no."):
    """
    Prompts for a yes/no answer and returns True for yes, False for no.
    """
    while True:
        val = input(prompt).strip().lower()
        if val in ("y", "yes"):
            return True
        elif val in ("n", "no"):
            return False
        else:
            print(error)


def select_item(prompt="Select an item: ",
                error="Invalid selection. Try again.",
                choices=None,
                mapping=None):
    """
    Lets user select an item from a list.
    """
    if not choices:
        raise ValueError("Choices list cannot be empty.")

    lower_choices = {c.lower(): c for c in choices}

    while True:
        selection = input(prompt).strip().lower()
        if selection in lower_choices:
            return lower_choices[selection]
        elif mapping and selection in mapping:
            return mapping[selection]
        print(error)

# def select_item(prompt="Select an item: ",
#                 error="Invalid selection. Try again.",
#                 choices=None,
#                 ):
#     """
#     Lets user select an item from a list.
#     """
#
#     if not choices:
#         raise ValueError("Choices list cannot be empty.")
#
#     lower_choices = {c.lower(): c for c in choices}
#
#     while True:
#         selection = input(prompt).strip().lower()
#         if selection in lower_choices:
#             return lower_choices[selection]
#         print(error)


def input_value(value_type="string", **kwargs):
    """
    Wrapper function to call input functions by type.
    """
    if value_type == "int":
        return input_int(**kwargs)
    elif value_type == "float":
        return input_float(**kwargs)
    elif value_type == "string":
        return input_string(**kwargs)
    elif value_type == "y_or_n":
        return y_or_n(**kwargs)
    elif value_type == "select":
        return select_item(**kwargs)
    else:
        raise ValueError("Invalid type specified.")

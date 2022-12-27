# this file contains functions to validate user input as per the requireent
from view import str_format as sf
def mandatory(message):
    """This is a recursive function to be used to get input which should not be empty 
        Args:
            message(string): The message to show user to get input
        Returns:
            string/function: return input if it is not empty or call the same function if the input is empty
    """
    value = input(message)
    if not value:
        return mandatory(message)
    else:
        return value

def defined_values(message, values, required):
    """This is a recursive function to be used to get input which should be in a defined list
        Args:
            message(string): The message to show user to get input
            values(list): this should have the list of possible options for the input
            required(bool): True if the fields should be none empty, False if the value can be empty
        Returns:
            string/function: return input if it is in the given list 
    """
    value = input(message)
    values = list(map(str, values))
    # if user input should be none empty and input is not set, need to give an error message to get an input value
    if required and not value:
        print(sf.error("\nPlease enter a value, this is mandatory."))
        return defined_values(message, values, required)
    # if input has a none empty value and it is not in the given list, need to give a warning that the entered value is not in option list
    elif value and value not in values:
        print(sf.warning("\nPlease enter a value from {} ".format(", ".join(values))))
        return defined_values(message, values, required)
    else:
        return value

def fix_length_number(message, length, required):
    """This is a recursive function to be used to get input which should be a number and contains defined numbers of digits.
        comonly used in credit card numbers
        Args:
            message(string): The message to show user to get input
            length: The number of digits should be contains in the input
            required(bool): True if the fields should be none empty, False if the value can be empty
        Returns:
            number/function: return input if it is a number having the defined number of digits
    """
    try:
        value = int(input(message))
        if value and len(str(value)) != length:
            print(sf.error("\nThe number should have {} digits.".format(length)))
            return fix_length_number(message, length, required)
        else:
            return value
    except: # this is triggered if user enter some string wich can't be casted to int
        print(sf.error("\nPlease enter a number having {} digits.".format(length)))
        return fix_length_number(message, length, required)
        # raise 
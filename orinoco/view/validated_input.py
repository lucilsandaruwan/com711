from view import str_format as sf
def mandatory(message):
    value = input(message)
    if not value:
        return mandatory(message)
    else:
        return value

def defined_values(message, values, required):
    value = input(message)
    values = list(map(str, values))
    if required and not value:
        print(sf.error("\nPlease enter a value, this is mandatory."))
        return defined_values(message, values, required)
    elif value and value not in values:
        print(sf.warning("\nPlease enter a value from {} ".format(", ".join(values))))
        return defined_values(message, values, required)
    else:
        return value

def fix_length_number(message, length, required):
    try:
        value = int(input(message))
        if value and len(str(value)) != length:
            print(sf.error("\nThe number should have {} digits.".format(length)))
            return fix_length_number(message, length, required)
        else:
            return value
    except:
        print(sf.error("\nPlease enter a number having {} digits.".format(length)))
        return fix_length_number(message, length, required)
        # raise
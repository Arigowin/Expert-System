import tools.defines as td


def get_value_from_dict(fact, dictionary):
    """ get the value of the given fact from dictionary
    and add this fact to custom queries if its value is not determined
    """

    print("in get value from dict", fact)
    if fact.isdigit():
        return int(fact)

    if not fact.isupper():
        return td.Error

    val = dictionary[fact][0] if dictionary[fact][2] > 0 else td.indet
    dictionary[fact][1] = 2 if val is td.indet else dictionary[fact][1]

    return val


def fact_to_value(expr, dictionary):
    """ modify 'expr' by getting values from dictionary """

    for i, elt in enumerate(expr):

        if elt.isupper():

            if dictionary[elt][2] > 0:
                expr[i] = str(dictionary[elt][0])

    return ''.join(expr)

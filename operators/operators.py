import tools.defines as td

def logic_not(val):

    if val == td.Indet:
        return td.Indet

    return not val


def logic_and(val1, val2):

    if val1 == td.Indet or val2 == td.Indet:
        return td.Indet

    if val1 == True and val2 == True:
        return True

    return False


def logic_or(val1, val2):

    if val1 == True or val2 == True:
        return True

    if val1 == td.Indet or val2 == td.Indet:
        return td.Indet

    return False


def logic_xor(val1, val2):

    if val1 == td.Indet or val2 == td.Indet:
        return td.Indet

    if val1 == True and val2 == False:
        return True

    if val1 == False and val2 == True:
        return True

    return False


import tools.defines as td

def logic_not(val):

    if int(val) == td.Indet:
        return td.Indet

    return not int(val)


def logic_and(val):

    if len(val) < 2:
        return

    if int(val[0]) == td.Indet or int(val[1]) == td.Indet:
        return td.Indet

    if int(val[0]) == True and int(val[1]) == True:
        return True

    return False


def logic_or(val):

    if len(val) < 2:
        return

    if int(val[0]) == True or int(val[1]) == True:
        return True

    if int(val[0]) == td.Indet or int(val[1]) == td.Indet:
        return td.Indet

    return False


def logic_xor(val):

    if len(val) < 2:
        return

    if int(val[0]) == td.Indet or int(val[1]) == td.Indet:
        return td.Indet

    if int(val[0]) == True and int(val[1]) == False:
        return True

    if int(val[0]) == False and int(val[1]) == True:
        return True

    return False


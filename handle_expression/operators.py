import tools.defines as td

def logic_not(val):

    if int(val) == td.indet:
        return td.indet

    return td.true if int(val) is td.false else td.false


def logic_and(val):

    if len(val) < 2:
        return

    if int(val[0]) == td.indet or int(val[1]) == td.indet:
        return td.indet

    if int(val[0]) == td.true and int(val[1]) == td.true:
        return td.true

    return td.false


def logic_or(val):

    if len(val) < 2:
        return

    if int(val[0]) == td.true or int(val[1]) == td.true:
        return td.true

    if int(val[0]) == td.indet or int(val[1]) == td.indet:
        return td.indet

    return td.false


def logic_xor(val):

    if len(val) < 2:
        return

    if int(val[0]) == td.indet or int(val[1]) == td.indet:
        return td.indet

    if int(val[0]) == td.true and int(val[1]) == td.false:
        return td.true

    if int(val[0]) == td.false and int(val[1]) == td.true:
        return td.true

    return td.false


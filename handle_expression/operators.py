import tools.defines as td

def logic_not(val):

    if int(val) == td.v_undef:
        return td.v_undef

    return td.v_true if int(val) is td.v_false else td.v_false


def logic_and(val):

    if len(val) < 2:
        return

    if int(val[0]) == td.v_undef or int(val[1]) == td.v_undef:
        return td.v_undef

    if int(val[0]) == td.v_true and int(val[1]) == td.v_true:
        return td.v_true

    return td.v_false


def logic_or(val):

    if len(val) < 2:
        return

    if int(val[0]) == td.v_true or int(val[1]) == td.v_true:
        return td.v_true

    if int(val[0]) == td.v_undef or int(val[1]) == td.v_undef:
        return td.v_undef

    return td.v_false


def logic_xor(val):

    if len(val) < 2:
        return

    if int(val[0]) == td.v_undef or int(val[1]) == td.v_undef:
        return td.v_undef

    if int(val[0]) == td.v_true and int(val[1]) == td.v_false:
        return td.v_true

    if int(val[0]) == td.v_false and int(val[1]) == td.v_true:
        return td.v_true

    return td.v_false


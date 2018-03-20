import tools.defines as td
from dictionary.fill_dictionary import modify_dict


def logic_not(val):
    """ handle the logic NOT in the condition of the expression """

    return (td.v_undef if int(val) == td.v_undef
            else td.v_true if int(val) is td.v_false
            else td.v_false)


def logic_and(val):
    """ handle the logic AND in the condition of the expression """

    return (td.v_undef if int(val[0]) == td.v_undef or int(val[1]) == td.v_undef
            else td.v_true if int(val[0]) == td.v_true
                           and int(val[1]) == td.v_true
            else td.v_false)


def logic_or(val):
    """ handle the logic OR in the condition of the expression """

    return (td.v_true if int(val[0]) == td.v_true or int(val[1]) == td.v_true
            else td.v_undef if int(val[0]) == td.v_undef
                            or int(val[1]) == td.v_undef
            else td.v_false)


def logic_xor(val, fact, dictionary):
    """ handle the logic XOR in the condition of the expression """

    if int(val[0]) == td.v_undef and int(val[1]) == td.v_undef:
        return td.v_undef

    if int(val[0]) == int(val[1]):
        return td.v_false

    if str(td.v_true) in val:

        fact_false = fact[1] if int(val[0]) is td.v_true else fact[0]
        rlt = modify_dict(fact_false, td.v_false, dictionary, fact_false)

        return rlt if rlt is not None else td.v_true

    return td.v_undef

import tools.defines as td
from dictionary.fill_dictionary import modify_value_in_dict


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


def logic_xor(val, fact, dictionary):

    if len(val) < 2:
        return

    if int(val[0]) == td.v_undef and int(val[1]) == td.v_undef:
        return td.v_undef

    if int(val[0]) == int(val[1]):
        return td.v_false

    if str(td.v_true) in val:

        fact_false = fact[1] if int(val[0]) is td.v_true else fact[0]
        rlt = modify_value_in_dict(fact_false, td.v_false, dictionary, fact_false)
        print("in XOR - true in val [%s][%s] (%s)" % (val, type(val), dictionary[fact_false]))
        #dictionary[fact][2] = td.q_needed if dictionary[fact][2] is not td.q_initial else td.q_initial
        return rlt if rlt is not None else td.v_true

    return td.v_undef

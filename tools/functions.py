import tools.defines as td
from tools.display import display_steps
from error.error import error


def get_first_index(to_find, to_search, n=1, order=True):
    """ return the index of the first element contains in 'to_find'
    in 'to_search'
    """

    if order is False:
        to_search = to_search[::-1]

    index = -1

    for i, elt in enumerate(to_search):
        if elt in to_find:
            if n == 1:
                index = i
                break
            n -= 1

    return index if order else len(to_search) - index - 1


def print_dict(dictionary):
    """ print the whole dictionary with the values of all possible facts """

    print("\nDictionary : ")

    for elt in sorted(dictionary):
        value = ("True" if dictionary[elt][0] is td.v_true else "False"
                 if dictionary[elt][0] is td.v_false else "Undefined"
                 if dictionary[elt][0] is td.v_undef else "Bugged")
        display_steps("\t", elt, query='', dic=dictionary,
                      end_display="%s%s" % (" : ", value), sleep=False,
                      bypass=True)


def print_query(dictionary):
    """ print the facts query """

    print("\nQuery : ")

    for elt in sorted(dictionary):
        if dictionary[elt][1] is td.q_initial:
            value = ("True" if dictionary[elt][0] is td.v_true else "False"
                     if dictionary[elt][0] is td.v_false else "Undefined"
                     if dictionary[elt][0] is td.v_undef else "Bugged")
            display_steps("\t", elt, query='', dic=dictionary,
                          end_display="%s%s" % (" : ", value), sleep=False,
                          bypass=True)


def check_with_curr_value(elt, expr_lst, dic, change=False, prio=-1):
    needed_rule = [rule for rule in expr_lst if elt in rule.cc_lst]

    for rule in needed_rule:
        if rule.cdt.solver(dic) is td.v_true:
            ret = rule.cc.solver(dic, elt, prio if prio == -1 else rule.prio)
            if ret == td.v_true and change:
                dic[elt][2] = 2
            elif ret is not td.v_true:
                return False
    return True

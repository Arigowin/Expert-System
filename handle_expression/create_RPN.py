import tools.defines as td


def get_polish_notation(cdt):
    """ return the polish notation version of rule condition """

    polish_rule = ""
    ope = ""

    for elt in cdt:
        if elt.isupper():
            polish_rule += elt

        elif not ope or elt == '(':
            ope = elt + ope

        elif elt == ')':
            index = ope.find('(')
            polish_rule += ope[:index]
            ope = ope[index + 1:]

        else:
            prio = priority(elt, ope[0], td.Symbols)

            if ope[0] == '(' or prio > 0:
                ope = elt + ope

            elif prio == 0:
                polish_rule += elt

            else:
                add_to_polish, add_to_ope = split_ope(elt, ope)
                polish_rule += add_to_polish
                ope = elt + add_to_ope

    if ope:
        polish_rule += ope

    return polish_rule


def priority(symb1, symb2, order):
    """ return if symbol 1 has priority on symbol 2 """

    return order.find(symb1) - order.find(symb2)


def split_ope(to_find, ope):
    """ get the elements to add in our polish rule and the ones to keep in
    ope
    """

    for elt in ope:

        if elt is '(':
            return ope[:ope.index(elt)], ope[ope.index(elt):]

        if elt in to_find:
            return ope[:ope.index(elt) + 1], ope[ope.index(elt) + 1:]

    return ope, ""

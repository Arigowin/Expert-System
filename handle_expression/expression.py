import tools.defines as td
from classes.rule import Rule
from error.error import error


def create_rule(expr, dictionary):
    """ create a list of Rule object with all the rules needed to resolve the
    given expression
    """

    split = split_expr(expr)
    if None in split:
        error(-1)
    if '<' in split[1]:
        rules = handle_iif(expr, split, dictionary)
    else:
        rules = [Rule(expr, split, dictionary)]

    if td.Error in rules:
        error(-1)

    return rules


def split_expr(expr):
    """ split the expression in 3 part: condition, symbol, conclusion """

    cdt = expr
    symb = None
    cc = None

    if '=' in expr:
        i = expr.index('=')

        symb_beg = i - 1 if i and expr[i - 1] and expr[i - 1] is '<' else i

        if expr[i + 1] and expr[i + 2]:
            symb_end = i + 2
        else:
            error(-1)

        symb = expr[symb_beg:symb_end]
        cdt = expr[:symb_beg]
        cc = expr[symb_end:]

    return [cdt, symb, cc]


def handle_iif(expr, split_expr, dictionary):
    """ create the 4 rules related to the iif expression """

    symb = "=>"

    not_cdt = "!(%s)" % split_expr[0]
    not_cc = "!(%s)" % split_expr[2]

    rules = []
    rules.append(Rule(expr, [split_expr[0], symb, split_expr[2]], dictionary))
    rules.append(Rule(expr, [not_cdt, symb, not_cc], dictionary))
    rules.append(Rule(expr, [split_expr[2], symb, split_expr[0]], dictionary))
    rules.append(Rule(expr, [not_cc, symb, not_cdt], dictionary))

    return rules

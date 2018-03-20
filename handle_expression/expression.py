import sys

import tools.defines as td
from classes.rule import Rule


def create_rule(expr, dictionary):
    """  """

    split = split_expr(expr)

    if '<' in split[1]:
        rules = handle_iif(expr, split, dictionary)
    else:
        rules = [Rule(expr, split, dictionary)]

    if td.Error in rules:
        sys.exit()

    return rules


def split_expr(expr):
    """ split the expression in 3 part: condition, symbol, conclusion """

    if '=' in expr:
        i = expr.index('=')

        symb_beg = i - 1 if i and expr[i - 1] and expr[i - 1] is '<' else i

        if expr[i + 1] and expr[i + 2]:
            symb_end = i + 2
        else:
            sys.exit()

        symb = expr[symb_beg:symb_end]
        cdt = expr[:symb_beg]
        cc = expr[symb_end:]

    else:
        cdt = expr
        symb = None
        cc = None

    return [cdt, symb, cc]


def handle_iif(expr, split_expr, dictionary):
    """  """

    symb = "=>"

    not_cdt = "!(%s)" % split_expr[0]
    not_cc = "!(%s)" % split_expr[2]

    rules = []
    rules.append(Rule(expr, [split_expr[0], symb, split_expr[2]], dictionary))
    rules.append(Rule(expr, [not_cdt, symb, not_cc], dictionary))
    rules.append(Rule(expr, [split_expr[2], symb, split_expr[0]], dictionary))
    rules.append(Rule(expr, [not_cc, symb, not_cdt], dictionary))

    return rules


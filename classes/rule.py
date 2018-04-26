import re

from error.error import error
import tools.defines as td
from classes.condition import Condition
from classes.conclusion import Conclusion


class Rule:
    """ contain the rule and handle coherence check and modifications

    Variables:
        expr
        sub_rule
        used
        cdt
        symb
        cc
        cdt_lst
        cc_lst
        prio

    Functions:
        _check_syntax(self, split_line)
        _check_regex(self, regex, str)
        _check_expr_syntax(self, regex, strm lmodif)

    """

    __slots__ = ["expr", "sub_rule", "used", "cdt", "symb", "cc", "cdt_lst",
                 "cc_lst", "prio"]

    def __init__(self, expr, split_line, dic):
        self.expr = expr
        self.sub_rule = ''.join(split_line)
        self.used = []

        self._check_syntax(split_line)

        self.cdt = Condition(split_line[0])
        self.symb = split_line[1]
        self.cc = Conclusion(split_line[2], dic)

        self.cdt_lst = [fact for fact in self.cdt.cdt if fact.isupper()]
        self.cc_lst = [fact for fact in self.cc.cc if fact.isupper()]

        self.prio = td.m_iif if '<' in self.expr else td.m_modif

    def _check_syntax(self, split_line):
        """ launch the 'well formated' check on the three part of the rule:
        condition, symbole and conclusion
        """

        symb_reg = "^<?=>$"
        exp_reg = "^(!*[A-Z][+\|\^])*!*[A-Z]$"

        self._check_expr_syntax(exp_reg, split_line[0], split_line[0])
        self._check_regex(symb_reg, split_line[1])
        self._check_expr_syntax(exp_reg, split_line[2], split_line[2])

    def _check_regex(self, regex, string):
        """ return if the given string 'string' matches the given 'regex' """

        cdt = re.search(regex, string)
        if not cdt:
            error(-1)

    def _check_expr_syntax(self, regex, string, lmodif):
        """ check if the rule is well formated begining by the most inner
        parenthesis
        """

        if "!!" in string:
            error(-1)

        openp = string.count('(')
        closep = string.count(')')
        if openp != closep:
            error(-1)

        table = str.maketrans(dict.fromkeys("()"))
        string = string.translate(table)
        self._check_regex(regex, string)

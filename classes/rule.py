import re
import sys

import tools.defines as td
from classes.condition import Condition
from classes.conclusion import Conclusion
from dictionary.fill_dictionary import modify_value_in_dict


class Rule:
    """ contain the rule and handle coherence check and modifications

    Variables:
        cdt
        symb
        cc

    Functions:
        _check_syntax(self, split_line)
        _check_regex(self, regex, str)
        _check_cond_recu(self, regex, strm lmodif)
    """

    def __init__(self, split_line, dictionary):
        self._check_syntax(split_line)

        self.cdt = Condition(split_line[0])
        self.symb = split_line[1]
        self.cc = Conclusion(split_line[2], dictionary)

        print(split_line)


    def solver(self, dictionary):
        """ """

        cdt = self.cdt.solver(dictionary)
        if cdt is td.v_true:
            symb = td.m_iif if '<' in self.symb else td.m_modif
            cc = self.cc.solver(dictionary, symb)
            if cc is td.Error:
                return td.Error

        else:
            self._add_to_queries(self.cdt.cdt, dictionary)

        return cdt


    def _add_to_queries(self, cdt_str, dictionary):
        """ set a list of facts as queries in dictionary if not yet setted """

        for elt in cdt_str:
            if elt.isupper() and dictionary[elt][2] is not td.m_default:
                dictionary[elt][1] = td.q_needed


    def _check_syntax(self, split_line):
        """ launch the 'well formated' check on the three part of the rule:
        condition, symbole and conclusion
        """

        symb_reg = "^<?=>$"
        exp_reg = "^!?[A-Z]([+\|\^]!?[A-Z])*$"

        self._check_cond_recu(exp_reg, split_line[0], split_line[0])
        self._check_regex(symb_reg, split_line[1])
        self._check_cond_recu(exp_reg, split_line[2], split_line[2])


    def _check_regex(self, regex, str):
        """ return if the given string 'str' matches the given 'regex' """

        cdt = re.search(regex, str)
        if not cdt:
            return td.Error


    def _check_cond_recu(self, regex, str, lmodif):
        """ check if the rule is well formated begining by the most inner
        parenthesis
        """

        print( "IN REC", str)

        if '(' in str:
            popen = str.find('(')
            pclose = str.rfind(')')

            if not pclose:
                return td.Error

            self._check_cond_recu(regex, str[popen + 1:pclose], lmodif)
            str = str[:popen] + 'Z' + str[pclose + 1:]

        self._check_regex(regex, str)



#abc = Rule("(A+(D|N)^!P+)|F=>W")

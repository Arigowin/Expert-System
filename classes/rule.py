import re
import sys


class Rule:
    """ contain the rule and handle coherence check and modifications """


    def __init__(self, line):
        self._split_line(line)
        self._check_syntax(line)
        self.line = line
        print(self.line)


    def _split_line(self, line):
        """ split the rule in 3 part: condition, symbol, conclusion """

        if '=' in line:
            i = line.index('=')

            symb_beg = i - 1 if i and line[i - 1] and line[i - 1] is '<' else i

            if line[i + 1] and line[i + 2]:
                symb_end = i + 2
            else:
                print("the rule '%s' is not well formated." % line)
                sys.exit()

            self.symb = line[symb_beg:symb_end]
            self.cdt = line[:symb_beg]
            self.cc = line[symb_end:]

        else:
            self.cdt = line
            self.symb = None
            self.cc = None


    def _check_syntax(self, line):
        """ launch the 'well formated' check on the three part of the rule:
        condition, symbole and conclusion
        """

        self._check_regex('^<?=>$', self.symb, line)
        self._check_cond_recu('^!?[A-Z]([+\|\^]!?[A-Z])*$', self.cdt, line, line)
        self._check_cond_recu('^!?[A-Z]([+\|\^]!?[A-Z])*$', self.cc, line, line)


    def _check_regex(self, regex, str, line):
        """ return if the given string 'str' matches the given 'regex' """

        cdt = re.search(regex, str)
        if not cdt:
            print("the rule '%s' is not well formated." % line)
            sys.exit()


    def _check_cond_recu(self, regex, str, lmodif, line):
        """ check if the rule is well formated begining by the most inner
        parenthesis
        """

        print( "IN REC", str)

        if '(' in str:
            popen = str.find('(')
            pclose = str.rfind(')')

            if not pclose:
                print("the rule '%s' is not well formated." % line)
                sys.exit()

            self._check_cond_recu(regex, str[popen + 1:pclose], lmodif, line)
            str = str[:popen] + 'Z' + str[pclose + 1:]

        self._check_regex(regex, str, line)


    def get_polish_notation(self):
        """ return the polish notation version of self.rule condition """

        symbols = "^|+"
        self.polish_rule = ""
        ope = ""

        for elt in self:

            if elt.isupper():
                self.polish_rule += elt

            elif not ope or elt == '(':
                ope = elt + ope

            elif elt == ')':
                index = ope.find('(')
                self.polish_rule += ope[:index]
                ope = ope[index + 1:]

            else:
                prio = self._priority(elt, ope[0], symbols)

                if ope[0] == '(' or prio > 0:
                    ope = elt + ope

                elif prio == 0:
                    self.polish_rule += elt

                else:
                    add_to_polish, add_to_ope = self._split_ope(elt, ope)
                    self.polish_rule += add_to_polish
                    ope = elt + add_to_ope

        if ope:
            self.polish_rule += ope

        return self.polish_rule


    def _priority(symb1, symb2, order):
        """ return if symbol 1 has priority on symbol 2 """

        return order.find(symb1) - order.find(symb2)


    def _split_ope(to_find, ope):
        #cf convention sur pep8
        """ get the elements to add in our polish rule and the ones to keep in
        ope
        """

        for elt in ope:

            if elt is '(':
                return ope[:ope.index(elt)], ope[ope.index(elt):]

            if elt in to_find:
                return ope[:ope.index(elt) +1], ope[ope.index(elt) +1:]

        return ope, ""


#abc = Rule("(A+(D|N)^!P+)|F=>W")

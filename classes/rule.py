import re
import sys



class Rule:


    def __init__(self, line):
        self.__split_line(line)
        self.__check_syntax(line)


    def _split_line(self, line):
        """ split the rule in 3 part: condition, symbol, conclusion """

        if '=' in line:
            index = line.index('=')

            symb_beg = index - 1 if index and line[index - 1] and line[index - 1] is '<' else index

            if line[index + 1] and line[index + 2]:
                symb_end = index + 2 # indexes are` included at begining and excluded at end
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
            condition, symbole and conclusion """

        self.__check_regex('^<?=>$', self.symb, line)
        self.__check_cond_recu('^!?[A-Z]([+\|\^]!?[A-Z])*$', self.cdt, line, line)
        self.__check_cond_recu('^!?[A-Z]([+\|\^]!?[A-Z])*$', self.cc, line, line)


    def _check_regex(self, regex, str, line):
        """ return if the given string 'str' matches the given 'regex' """

        cdt = re.search(regex, str)
        if not cdt:
            print("the rule '%s' is not well formated." % line)
            sys.exit()


    def _check_cond_recu(self, regex, str, modif_line, line):
        """ check if the rule is well formated begining by the innerest parenthesis """

        print  "IN REC", str

        if '(' in str:
            open_parent = str.find('(')
            close_parent = str.rfind(')')

            if not close_parent:
                print("the rule '%s' is not well formated." % line)
                sys.exit()

            self.__check_cond_recu(regex, str[open_parent + 1:close_parent], modif_line, line)
            str = str[:open_parent] + 'Z' + str[close_parent + 1:]

        self.__check_regex(regex, str, line)


    def _get_polish_notation(self):
        """ return the polish notation version of self.rule condition """

        order = "+|^"
        tmp_ope = ""

        for elt in self.cdt:

            if elt.isupper():
            if elt not in symbols:
            elif tmp_ope == "" or self.__priority(tmp_ope[0], elt) == False:
            elif
                tmp_ope = elt + tmp_ope
            else:
                self.polish_rule = tmp_ope + self.polish_rule
                tmp_ope = elt
        order = "+|^"
        return order.find(symb1) < order.find(symb2):


    def __priority(symb1, symb2, order):
        """ return if symbol 1 has priority on symbol 2 """

        return order.find(symb1) - order.find(symb2)

#abc = Rule("(A+(D|N)^!P+)|F=>W")

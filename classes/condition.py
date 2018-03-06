import operators.operators as op
import tools.defines as td

class Condition:
    """ handle all the modfications and specifications of condition """

    def __init__(self, cdt):
        self.cdt = cdt
        print("cdt : " + self.cdt)
        self._get_polish_notation(cdt)
        self.pmodif = self.polish_rule
        print("RPN : " + self.polish_rule)


    def polish_solver(self, dictionary):
        """ find the result of the given RPN expression """

#        print("cdt : " + self.cdt)
#        print("RPN : " + self.polish_rule)

        sym, fact, start, end = self._get_sub_exp()
#        print("sym[%s], fact[%s], start[%s], end[%s]" % (sym, fact, start, end))

        val1 = self._get_value(fact[0], dictionary)
        val2 = self._get_value(fact[1], dictionary)

        func_tbl = { '^': op.logic_xor(val1, val2),
                     '|': op.logic_or(val1, val2),
                     '+': op.logic_and(val1, val2) }

        rlt = 0 if func_tbl[sym] == False else 1 if func_tbl[sym] == True else td.Indet
        self.pmodif = start + str(rlt) + end

#        print("polish_solver : " + self.pmodif)
        for elt in td.Symbols:
            if elt in self.pmodif:
                self.polish_solver(dictionary)


    def _get_sub_exp(self):
        """ """

        for elt in self.pmodif:

            if elt in "^|+":

                i = self.pmodif.index(elt)

                if self.pmodif[i - 2] is not '!':
                    fact = [self.pmodif[i - 2] if self.pmodif[i - 3] is not '!'
                                               else self.pmodif[i - 3:i - 1],
                            self.pmodif[i - 1]]

                else:
                    fact = [self.pmodif[i - 3] if self.pmodif[i - 4] is not '!'
                                               else self.pmodif[i - 4:i - 2],
                           self.pmodif[i - 2:i]]


                start = self.pmodif[:i - (len(fact[0]) + len(fact[1]))]
                end = self.pmodif[i + 1:]

                return self.pmodif[i], fact, start, end

#       ERROR
        return None


    def _get_value(self, fact, dictionary):
        """ return the value of 'fact' from 'dictionary' """

        if fact.isdigit():
            return int(fact)

        if '!' in fact:
            return op.logic_not(dictionary[fact[1]][0])

        return dictionary[fact][0]




    def _get_polish_notation(self, cdt):
        """ return the polish notation version of self.rule condition """

        self.polish_rule = ""
        ope = ""

        for elt in cdt:

            if elt.isupper() or elt is '!':
                self.polish_rule += elt

            elif not ope or elt == '(':
                ope = elt + ope

            elif elt == ')':
                index = ope.find('(')
                self.polish_rule += ope[:index]
                ope = ope[index + 1:]

            else:
                prio = self._priority(elt, ope[0], td.Symbols)

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


    def _priority(self, symb1, symb2, order):
        """ return if symbol 1 has priority on symbol 2 """

        return order.find(symb1) - order.find(symb2)


    def _split_ope(self, to_find, ope):
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

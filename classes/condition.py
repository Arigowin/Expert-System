import operators.operators as op
import tools.defines as td

class Condition:
    """ handle all the modfications and specifications of condition """

    def __init__(self, cdt):
        self.cdt = cdt
        print("\ncdt : " + self.cdt)
        self._get_polish_notation(cdt)
        self.pmodif = self.polish_rule
        print("RPN : " + self.polish_rule)


    def polish_solver(self, dictionary):
        """ find the result of the given RPN expression """

#        print("cdt : " + self.cdt)
#        print("RPN : " + self.polish_rule)

        sym, fact, start, end = self._get_sub_exp()
        #print("sym[%s], fact[%s], start[%s], end[%s]" % (sym, fact, start, end))

        val = self._get_value(fact, dictionary)

        func_tbl = {
                    '^': op.logic_xor(val),
                    '|': op.logic_or(val),
                    '+': op.logic_and(val),
                    '!': op.logic_not(val)
                   }

        # as rlt is a boolean, we need to get the correct int value for
        # the equations to be performed
        rlt = 0 if func_tbl[sym] == False \
              else 1 if func_tbl[sym] == True \
              else td.Indet

        self.pmodif = start + str(rlt) + end

#        print("polish_solver : " + self.pmodif)
        for elt in td.Symbols:
            if elt in self.pmodif:
                self.polish_solver(dictionary)


    def _get_sub_exp(self):
        """ split pmodif to get the fist operation to do -fact and symbol- and
        the 2 leftovers
        """

        for elt in self.pmodif:

            if elt in td.Symbols:

                i = self.pmodif.index(elt)

                fact_start = i - 2
                if self.pmodif[i] is '!':
                    fact_start = i - 1

                return self.pmodif[i], self.pmodif[fact_start:i], \
                       self.pmodif[:fact_start], self.pmodif[i+1 :]

#       ERROR
        return None


    def _get_value(self, fact, dictionary):
        """ return the value of 'fact' from 'dictionary' """

        rlt = ""

        for elt in fact:
            if elt.isdigit():
                rlt += elt
            else:
                rlt += str(dictionary[elt][0])

        return rlt


    def _get_polish_notation(self, cdt):
        """ return the polish notation version of self.rule condition """

        self.polish_rule = ""
        ope = ""

        for elt in cdt:

            if elt.isupper():
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

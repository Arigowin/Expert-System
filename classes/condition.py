import tools.defines as td
from tools.functions import print_dict
import handle_expression.operators as op
from handle_expression.create_RPN import get_polish_notation

class Condition:
    """ handle all the modfications and specifications of condition

    Variables:
        cdt
        polish_rule
        pmodif

    Function:
    """

    def __init__(self, cdt):
        self.cdt = cdt
        print("cdt : " + self.cdt)
        self.polish_rule = get_polish_notation(cdt)
        print("RPN : " + self.polish_rule)


    def solver(self, dictionary):
        """ find the result of the given RPN expression """

        self.pmodif = self.polish_rule
        self._recu_solver(dictionary)
        print("LOGIQUEMENT LA DERNIERE VALEUR DS CDT", self.pmodif)

        return int(self.pmodif)

    def _recu_solver(self, dictionary):
        print("cdt : " + self.cdt)
        print("RPN : " + self.polish_rule)

        if len(self.pmodif) == 1:
            self.pmodif = self._get_value(self.pmodif, dictionary)
            return None

        sym, fact, start, end = self._get_sub_exp()
        print("sym[%s], fact[%s], start[%s], end[%s]" % (sym, fact, start, end))

        val = self._get_value(fact, dictionary)

        func_tbl = {
                    '^': op.logic_xor(val),
                    '|': op.logic_or(val),
                    '+': op.logic_and(val),
                    '!': op.logic_not(val)
                   }

        self.pmodif = start + str(func_tbl[sym]) + end

        print("recu solver : " + self.pmodif)
        for elt in td.Symbols:
            if elt in self.pmodif:
                self._recu_solver(dictionary)



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

        print('ERROR')
        return None, None, None, None


# OUT OF THE CLASS!!!!!
    def _get_value(self, fact, dictionary):
        """ return the value of 'fact' from 'dictionary' """

        rlt = ""

        for elt in fact:
            if elt.isdigit():
                rlt += elt
            else:
                rlt += str(dictionary[elt][0])

        return rlt


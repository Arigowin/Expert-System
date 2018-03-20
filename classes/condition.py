import tools.defines as td
from tools.functions import print_dict
import handle_expression.operators as op
from handle_expression.create_RPN import get_polish_notation
from dictionary.check_dictionary import get_value_from_dict


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
        self.polish_rule = get_polish_notation(cdt)


    def solver(self, dictionary):
        """ find the result of the given RPN expression """

        self.pmodif = self.polish_rule
        self._recu_solver(dictionary)

        return int(self.pmodif)

    def _recu_solver(self, dictionary):

        if len(self.pmodif) == 1:
            self.pmodif = self._get_value(self.pmodif, dictionary)
            return None

        sym, fact, start, end = self._get_sub_exp()

        val = self._get_value(fact, dictionary)

        func_tbl = {'|': op.logic_or,
                    '+': op.logic_and,
                    '!': op.logic_not}

        if sym is '^':
            self.pmodif = start + str(op.logic_xor(val, fact, dictionary)) + end
        else:
            self.pmodif = start + str(func_tbl[sym](val)) + end

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
                       self.pmodif[:fact_start], self.pmodif[i+1:]

        return None, None, None, None


# OUT OF THE CLASS!!!!!
    def _get_value(self, fact, dictionary):
        """ return the value of 'fact' from 'dictionary' """

        rlt = ""

        cc_list = [fact for fact in dictionary
                        if dictionary[fact][1] is not td.q_unused]
        for elt in fact:
            ret_val = str(get_value_from_dict(elt, dictionary))

            print("ELT (%s) ret val (%s) rlt (%s) cc list (%s)" % (elt, ret_val, rlt, cc_list))
            print("cdt elif", int(ret_val) is td.v_undef, elt in cc_list)
            rlt += elt if elt.isdigit() else ret_val if int(ret_val) == td.v_undef and elt in cc_list else str(dictionary[elt][0])
            #if elt.isdigit():
            #    print("digit")
            #    rlt += elt
            #elif ret_val == td.v_undef and elt in cc_list:
            #    print("cc list")
            #    rlt += ret_val
            #else:
            #    print("else")
            #    rlt += str(dictionary[elt][0])



        return rlt



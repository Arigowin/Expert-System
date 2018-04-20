import tools.defines as td
from tools.functions import print_dict
from handle_expression.create_RPN import get_polish_notation
from dictionary.check_dictionary import get_value_from_dict
from dictionary.fill_dictionary import modify_dict


class Condition:
    """ handle all the modfications and specifications of condition

    Variables:
        cdt
        rpn_rule
        pmodif

    Function:
        solver
        _recu_solver
        _get_sub_exp
        _get_value
        _logic_not
        _logic_and
        _logic_or
        _logic_xor

    """

    __slots__ = "cdt", "rpn_rule", "pmodif"

    def __init__(self, cdt):
        self.cdt = cdt
        self.rpn_rule = get_polish_notation(cdt)


    def solver(self, dic):
        """ find the result of the given RPN expression """

        self.pmodif = self.rpn_rule
        self._recu_solver(dic)

        return int(self.pmodif)


    def _recu_solver(self, dic):
        """ """
        
        if len(self.pmodif) == 1:
            self.pmodif = self._get_value(self.pmodif, dic)
            return None

        sym, fact, start, end = self._get_sub_exp()

        val = self._get_value(fact, dic)

        func_tbl = {'|': self._logic_or,
                    '+': self._logic_and,
                    '!': self._logic_not}

        if sym is '^':
            self.pmodif = start + str(self._logic_xor(val, fact, dic)) + end
        else:
            self.pmodif = start + str(func_tbl[sym](val)) + end

        for elt in td.Symbols:
            if elt in self.pmodif:
                self._recu_solver(dic)


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

                return (self.pmodif[i], self.pmodif[fact_start:i],
                        self.pmodif[:fact_start], self.pmodif[i+1:])

        return None, None, None, None


    def _get_value(self, fact, dic):
        """ return the value of 'fact' from 'dictionary' """

        rlt = ""
        cc_list = [fact for fact in dic if dic[fact][1] is not td.q_unused]
        for elt in fact:

            ret_val = str(get_value_from_dict(elt, dic))
            rlt += (elt if elt.isdigit()
                    else ret_val if int(ret_val) == td.v_undef
                        and elt in cc_list
                    else str(dic[elt][0]))

        return rlt


    def _logic_not(self, val):
        """ handle the logic NOT in the condition of the expression """

        return (td.v_undef if int(val) == td.v_undef
                else td.v_true if int(val) is td.v_false
                else td.v_false)


    def _logic_and(self, val):
        """ handle the logic AND in the condition of the expression """

        return (td.v_undef if int(val[0]) == td.v_undef or int(val[1]) == td.v_undef
                else td.v_true if int(val[0]) == td.v_true
                               and int(val[1]) == td.v_true
                else td.v_false)


    def _logic_or(self, val):
        """ handle the logic OR in the condition of the expression """

        return (td.v_true if int(val[0]) == td.v_true or int(val[1]) == td.v_true
                else td.v_undef if int(val[0]) == td.v_undef
                                or int(val[1]) == td.v_undef
                else td.v_false)


    def _logic_xor(self, val, fact, dic):
        """ handle the logic XOR in the condition of the expression """

        if int(val[0]) == td.v_undef and int(val[1]) == td.v_undef:
            return td.v_undef

        if int(val[0]) == int(val[1]):
            return td.v_false

        if str(td.v_true) in val:

            fact_false = fact[1] if int(val[0]) is td.v_true else fact[0]

            if fact_false not in [elt for elt in dic if dic[elt][1] is not td.q_unused]:
                rlt = modify_dict(fact_false, td.v_false, dic, fact_false)
            else:
                rlt = modify_dict(fact_false, td.v_undef, dic, fact_false)
                return td.v_undef if rlt is None else rlt

            return rlt if rlt is not None else td.v_true

        return td.v_undef

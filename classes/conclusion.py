import re

import tools.defines as td
import handle_expression.operators as op
from tools.functions import get_first_index
from handle_expression.create_RPN import get_polish_notation
from dictionary.check_dictionary import get_value_from_dict, fact_to_value
from dictionary.fill_dictionary import modify_value_in_dict


class Conclusion:
    """

    Variables:
        cc
        rpolish

    Functions:
    """


    def __init__(self, cc, dictionary):
        self.cc = cc
        self.rpolish = get_polish_notation(cc)[::-1]
        self._fill_dictionary(dictionary)


    def solver(self, dictionary, symb):
        """ """

        rpolish_cpy = self.rpolish
        rpolish_cpy = fact_to_value(list(rpolish_cpy), dictionary)
        print("solv2", rpolish_cpy)
        rlt = self._recu_solver(dictionary, rpolish_cpy, td.v_true, symb)
        print("last rlt : ", rlt)

        return rlt


    def _recu_solver(self, dictionary, rpolish_cpy, wanted, symb):
        """ recursive function to call the correct operator function """

        print("recu_solver", rpolish_cpy)
        rpolish_lst = []
        if get_first_index(td.Symbols[:-1], rpolish_cpy) is not -1:
            rpolish_lst = self._split_rpolish(rpolish_cpy)
        elif rpolish_cpy[0] is '!':
            rpolish_lst = ['!', rpolish_cpy[1:]]
        elif rpolish_cpy[0].isupper():
            if wanted is td.v_true and modify_value_in_dict(rpolish_cpy[0],
                                     td.v_true, dictionary, symb) is not None:
                return td.Error
            return get_value_from_dict(rpolish_cpy[0], dictionary)

        print("recu fct after split ", rpolish_cpy, rpolish_lst)

        if rpolish_cpy[0] is '^':
            rlt = self._logic_xor(dictionary, rpolish_lst, wanted, symb)

        elif rpolish_cpy[0] is '|':
            rlt = self._logic_or(dictionary, rpolish_lst, wanted, symb)

        elif rpolish_cpy[0] is '+':
            rlt = self._logic_and(dictionary, rpolish_lst, wanted, symb)

        elif rpolish_cpy[0] is '!':
            rlt = self._logic_not(dictionary, rpolish_lst, wanted, symb)

        else:
            rlt = get_value_from_dict(rpolish_cpy[0], dictionary)

        print("rlt rcu : ", rlt)
        return rlt



    def _logic_xor(self, dictionary, rpolish_lst, wanted, symb):
        """ """

        print("- LOGIC XOR -")
        val = [-1, -1]
        for i, elt in enumerate(rpolish_lst[1:]):
            if len(elt) > 1:
                val[i] = self._recu_solver(dictionary, elt, wanted, symb)
            else:
                val[i] = get_value_from_dict(elt, dictionary)

        if -1 in val:
            return td.Error

        if wanted is td.v_true:
            if val[0] != val[1] and td.v_indet not in val:
                return wanted
            if val[0] == val[1] and val[0] is not td.v_indet:
                print("ERROR")
                return td.Error
            if val[0] == val[1]:
                return td.v_indet

            melt = 1 if val[0] is td.v_indet else 2
            value = td.v_false if td.v_true in val else td.v_true
            if modify_value_in_dict(rpolish_lst[melt], value, dictionary, symb) is not None:
                return td.Error

            return wanted

        if wanted is td.v_false:
            if val[0] != val[1] and td.v_indet not in val:
                print("ERROR")
                return td.Error
            if val[0] == val[1] and td.v_indet not in val:
                return wanted
            if val[0] == val[1] and td.v_indet in val:
                return td.v_indet

            melt = 1 if val[0] is td.v_indet else 2
            value = td.v_false if td.v_false in val else td.v_true
            if modify_value_in_dict(rpolish_lst[melt], value, dictionary, symb) is not None:
                return td.Error

            return wanted


    def _logic_or(self, dictionary, rpolish_lst, wanted, symb):
        """ """

        print("- LOGIC OR -")
        val = [-1, -1]
        for i, elt in enumerate(rpolish_lst[1:]):
            if len(elt) > 1:
                val[i] = self._recu_solver(dictionary, elt, wanted, symb)
            else:
                val[i] = get_value_from_dict(elt, dictionary)

        print("val in OR after for", val)
        if wanted is td.v_true:
            print("if wanted true and one val true")
            if td.v_true in val:
                # set le 2eme a indet
                return td.v_true

            if val.count(td.v_false) == 1:
                if val[0] is td.v_false and modify_value_in_dict(rpolish_lst[2],
                                         td.v_true, dictionary, symb) is not None:
                        return td.Error
                elif modify_value_in_dict(rpolish_lst[1], td.v_true, dictionary, symb) is not None:
                        return td.Error
                return td.v_true

            if val.count(td.v_indet) == 2:
                print("in OR [%s][%s]" % (val, self.cc))
                input()
                if modify_value_in_dict(rpolish_lst[1], td.v_indet, dictionary, symb) is not None:
                        return td.Error
                if modify_value_in_dict(rpolish_lst[2], td.v_indet, dictionary, symb) is not None:
                        return td.Error
                return td.v_indet

            if val.count(td.v_false) == 2:
                print("ERROR")
                return td.Error

        if wanted is td.v_false:
            if td.v_true in val:
                print("ERROR")
                return td.Error

            for elt in rpolish_lst[1:]:
                if modify_value_in_dict(elt, td.v_false, dictionary, symb) is not None:
                        return td.Error
                return td.v_true

            return td.v_false



    def _logic_and(self, dictionary, rpolish_lst, wanted, symb):
        """ """

        print("- LOGIC AND -")
        val = [-1, -1]
        for i, elt in enumerate(rpolish_lst[1:]):

            if len(elt) > 1:
                val[i] = self._recu_solver(dictionary, elt, wanted, symb)

            elif elt.isupper():
                if modify_value_in_dict(elt, wanted, dictionary, symb) is not None:
                    print("in ret ERROR add", elt, wanted, symb, dictionary[elt])
                    return td.Error
                val[i] = wanted

            else:
                val[i] = int(elt)

        if td.v_indet in val:
            # si on revient ici et que c'est indet ca veux dire qu'il faut determiner les valeurs par une autre equation
            return td.v_indet

        if val.count(wanted) is not 2:
            print("1 ERROR - incoherence")
            return td.Error

        return wanted


    def _logic_not(self, dictionary, rpolish_lst, wanted, symb):
        """ """

        print("- LOGIC NOT -")
        inv_rlt = op.logic_not(wanted)

        if len(rpolish_lst[1]) > 1:
            val = op.logic_not(self._recu_solver(dictionary, rpolish_lst[1], inv_rlt, symb))

        elif rpolish_lst[1].isupper():
            if modify_value_in_dict(rpolish_lst[1], wanted, dictionary, symb) is not None:
                return td.Error
            val = inv_rlt

        else:
            val = op.logic_not(rpolish_lst[1])

        if val is not wanted:
            print("2 ERROR - incoherence", val)
            return td.Error

        return val


    def _split_rpolish(self, rpolish_cpy):
        """ """

        print("in split : ", rpolish_cpy)
        if get_first_index(td.Symbols[:-1], rpolish_cpy[1:]) is -1:
            match = re.match("([+|^])(!?[A-Z0-2])(!?[A-Z0-2])", rpolish_cpy)

            if match.lastindex == 3:
                return [match.group(1), match.group(2), match.group(3)]

        if rpolish_cpy[0] is '!' and not rpolish_cpy[1].isupper():
            return [rpolish_cpy[0], rpolish_cpy[1:]]
        rpolish_lst = [rpolish_cpy[0]]
        b = False

        index = -1
        for i, elt in enumerate(rpolish_cpy[1:]):

#            print(i, elt)
            if elt in "^|+" and b is True:
                index = i + 1
                break

            elif elt.isupper() or elt.isdigit():
                b = True

        if index is not -1:
            rpolish_lst.extend((rpolish_cpy[1:index], rpolish_cpy[index:]))

        return rpolish_lst


    def _fill_dictionary(self, dictionary):

        for elt in self.rpolish:
            if elt.isupper() and dictionary[elt][2] is td.m_default:
                dictionary[elt][1] = td.q_needed

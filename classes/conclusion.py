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


    def solver(self, dictionary, query, symb):
        """ """

        rpolish_cpy = self.rpolish
        rpolish_cpy = fact_to_value(list(rpolish_cpy), dictionary)
        rlt = self._recu_solver(dictionary, rpolish_cpy, td.v_true, query, symb)
        print("CONCLUSION last rlt : ", rlt)

        return rlt


    def _recu_solver(self, dictionary, rpolish_cpy, wanted, query, symb):
        """ recursive function to call the correct operator function """

        rpolish_lst = []

        if get_first_index(td.Symbols[:-1], rpolish_cpy) is not -1:
            rpolish_lst = self._split_rpolish(rpolish_cpy)
        elif rpolish_cpy[0] is '!':
            rpolish_lst = ['!', rpolish_cpy[1:]]
        elif rpolish_cpy[0].isupper():
            if wanted is td.v_true and modify_value_in_dict(rpolish_cpy[0],
                                     td.v_true, dictionary, query, symb) is not None:
                return td.Error
            return get_value_from_dict(rpolish_cpy[0], dictionary)

        func_tbl = {'^': self._logic_xor,
                    '|': self._logic_or,
                    '+': self._logic_and,
                    '!': self._logic_not}

        if rpolish_cpy[0] in '^|+!':
            rlt = func_tbl[rpolish_cpy[0]](dictionary, rpolish_lst, wanted, query, symb)

        else:
            rlt = get_value_from_dict(rpolish_cpy[0], dictionary)

        print("----- end recu ", rlt)
        return rlt



    def _logic_xor(self, dictionary, rpolish_lst, wanted, query, symb):
        """ """

        val = [-1, -1]
        for i, elt in enumerate(rpolish_lst[1:]):
            if len(elt) > 1:
                val[i] = self._recu_solver(dictionary, elt, wanted, query, symb)
            else:
                val[i] = get_value_from_dict(elt, dictionary)

        if -1 in val:
            return td.Error

        if wanted is td.v_true:
            if val[0] != val[1] and td.v_indet not in val:
                return wanted
            if val[0] == val[1] and val[0] is not td.v_indet:
                return td.Error
            if val[0] == val[1]:
                return td.v_indet

            melt = 1 if val[0] is td.v_indet else 2
            value = td.v_false if td.v_true in val else td.v_true
            if modify_value_in_dict(rpolish_lst[melt], value, dictionary, query, symb) is not None:
                return td.Error

            return wanted

        if wanted is td.v_false:
            if val[0] != val[1] and td.v_indet not in val:
                return td.Error
            if val[0] == val[1] and td.v_indet not in val:
                return wanted
            if val[0] == val[1] and td.v_indet in val:
                return td.v_indet

            melt = 1 if val[0] is td.v_indet else 2
            value = td.v_false if td.v_false in val else td.v_true
            if modify_value_in_dict(rpolish_lst[melt], value, dictionary, query, symb) is not None:
                return td.Error

            return wanted


    def _logic_or(self, dictionary, rpolish_lst, wanted, query, symb):
        """ """

        val = [-1, -1]
        for i, elt in enumerate(rpolish_lst[1:]):
            if len(elt) > 1:
                val[i] = self._recu_solver(dictionary, elt, wanted, query, symb)
            else:
                val[i] = get_value_from_dict(elt, dictionary)

        if wanted is td.v_true:

            if td.v_true in val:
                return td.v_true

            if val.count(td.v_false) == 1:
                if val[0] is td.v_false:

                    if modify_value_in_dict(rpolish_lst[2], td.v_true, dictionary, query, symb) is not None:
                        return td.Error

                elif modify_value_in_dict(rpolish_lst[1], td.v_true, dictionary, query, symb) is not None:
                    return td.Error

                return td.v_true

            if val.count(td.v_indet) == 2:
                if modify_value_in_dict(rpolish_lst[1], td.v_indet, dictionary, query, symb) is not None:
                    return td.Error

                if modify_value_in_dict(rpolish_lst[2], td.v_indet, dictionary, query, symb) is not None:
                    return td.Error

                return td.v_indet

            if val.count(td.v_false) == 2:
                return td.Error

        if wanted is td.v_false:
            if td.v_true in val:
                return td.Error

            for elt in rpolish_lst[1:]:
                if modify_value_in_dict(elt, td.v_false, dictionary, query, symb) is not None:
                    return td.Error
                return td.v_true

            return td.v_false


    def _logic_and(self, dictionary, rpolish_lst, wanted, query, symb):
        """ """

        #print("- LOGIC AND -")
        val = [-1, -1]
        for i, elt in enumerate(rpolish_lst[1:]):

            if len(elt) > 1:
                val[i] = self._recu_solver(dictionary, elt, wanted, query, symb)

            elif elt.isupper():
                if modify_value_in_dict(elt, wanted, dictionary, query, symb) is not None:
                    return td.Error
                val[i] = wanted

            else:
                val[i] = int(elt)

        if td.v_indet in val:
            return td.v_indet

        if val.count(wanted) is not 2:
            return td.Error

        return wanted


    def _logic_not(self, dictionary, rpolish_lst, wanted, query, symb):
        """ """

        inv_rlt = op.logic_not(wanted)

        print("IN LOGIC NOT", rpolish_lst, wanted)
        if len(rpolish_lst[1]) > 1:
            val = self._recu_solver(dictionary, rpolish_lst[1], inv_rlt, query, symb)
            print("END IF RECU LOGIC NOT", rpolish_lst[1], val)

        elif rpolish_lst[1].isupper():
            if modify_value_in_dict(rpolish_lst[1], inv_rlt, dictionary, query, symb) is not None:
                print(">>>> YEP")
                return td.Error
            val = inv_rlt

        else:
            val = rpolish_lst[1]

        print("++++ in not val/wanted", val, wanted)

        if val is wanted:
            print("NOOOOOOOOOP!!!")
            return td.Error

        return val


    def _split_rpolish(self, rpolish_cpy):
        """ """

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
            if elt.isupper() and dictionary[elt][2] is td.m_default and dictionary[elt][1] is not td.q_initial:
                dictionary[elt][1] = td.q_needed

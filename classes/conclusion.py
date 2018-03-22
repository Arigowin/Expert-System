import re

import tools.defines as td
import handle_expression.operators as op
from error.error import error
from tools.functions import get_first_index
from handle_expression.create_RPN import get_polish_notation
from dictionary.check_dictionary import get_value_from_dict, fact_to_value
from dictionary.fill_dictionary import modify_dict
from tools.custom_return import enable_ret, cust_ret


class Conclusion:
    """

    Variables:
        cc
        rpolish

    Functions:
        solver
        _recu_solver
        _split_rpolish
        _fill_dict
        _logic_not
        _logic_and
        _logic_or
        _logic_xor

    """


    def __init__(self, cc, dic):

        self.cc = cc
        self.rpolish = get_polish_notation(cc)[::-1]
        self._fill_dict(dic)


    def solver(self, dic, query, symb):
        """ call the recursive solver function """

        #print("in CC SOLVER query (%s) symb (%s) RPN (%s)" % (query, symb, self.rpolish))
        rpolish_cpy = self.rpolish

        rlt = self._recu_solver(dic, rpolish_cpy, td.v_true, query, symb)
        #print("CONCLUSION last rlt : ", rlt)

        return rlt


    @enable_ret
    def _recu_solver(self, dic, rpolish_cpy, wanted, query, symb):
        """ recursive function to call the correct operator function """

        rpolish_lst = []

        if get_first_index(td.Symbols[:-1], rpolish_cpy) is not -1:
            rpolish_lst = self._split_rpolish(rpolish_cpy)

        elif rpolish_cpy[0] is '!':
            rpolish_lst = ['!', rpolish_cpy[1:]]

        elif rpolish_cpy[0].isupper():
            if wanted is td.v_true:
                ret = modify_dict(rpolish_cpy[0], td.v_true, dic, query, symb)
                #if ret is not None:
                #    return ret
                cust_ret(ret) if ret is not None else None

            return get_value_from_dict(rpolish_cpy[0], dic)

        func_tbl = {'^': self._logic_xor,
                    '|': self._logic_or,
                    '+': self._logic_and,
                    '!': self._logic_not}

        if rpolish_cpy[0] in '^|+!':
            rlt = func_tbl[rpolish_cpy[0]](dic, rpolish_lst, wanted, query, symb)

        else:
            rlt = get_value_from_dict(rpolish_cpy[0], dic)

        return rlt


    @enable_ret
    def _logic_xor(self, dic, rpolish_lst, wanted, query, symb):
        """ handle the logic XOR in the conclusion of the expression """

        val = [-1, -1]
        for i, elt in enumerate(rpolish_lst[1:]):

            if len(elt) > 1:
                val[i] = self._recu_solver(dic, elt, wanted, query, symb)
            else:
                val[i] = get_value_from_dict(elt, dic)

        if -1 in val:
            return td.Error

        if wanted is td.v_true:

            if val[0] != val[1] and td.v_undef not in val:
                return wanted
            if val[0] == val[1] and val[0] is not td.v_undef:
                return td.Error
            if val[0] == val[1]:
                ret = modify_dict(rpolish_lst[1], td.v_undef, dic, query, symb)
                #if ret is not None:
                #    return ret
                cust_ret(ret) if ret is not None else None

                ret = modify_dict(rpolish_lst[2], td.v_undef, dic, query, symb)
                return td.v_undef if ret is None else ret

            melt = 1 if val[0] is td.v_undef else 2
            value = td.v_false if td.v_true in val else td.v_true
            ret = modify_dict(rpolish_lst[melt], value, dic, query, symb)
            #if ret is not None:
            #    return ret
            cust_ret(ret) if ret is not None else None

            return wanted

        if wanted is td.v_false:
            if val[0] != val[1] and td.v_undef not in val:
                return td.Error
            if val[0] == val[1] and td.v_undef not in val:
                return wanted
            if val[0] == val[1] and td.v_undef in val:
                return td.v_undef

            melt = 1 if val[0] is td.v_undef else 2
            value = td.v_false if td.v_false in val else td.v_true
            ret = modify_dict(rpolish_lst[melt], value, dic, query, symb)
            cust_ret(ret) if ret is not None else None
            #if ret is not None:
            #    return ret

            return wanted


    @enable_ret
    def _logic_or(self, dic, rpolish_lst, wanted, query, symb):
        """ handle the logic OR in the conclusion of the expression """

        val = [-1, -1]
        for i, elt in enumerate(rpolish_lst[1:]):
            if len(elt) > 1:
                val[i] = self._recu_solver(dic, elt, wanted, query, symb)
            else:
                val[i] = get_value_from_dict(elt, dic)

        if wanted is td.v_true:

            if td.v_true in val:
                return td.v_true

            if val.count(td.v_false) == 1:

                if val[0] is td.v_false:
                    ret = modify_dict(rpolish_lst[2], td.v_true, dic, query, symb)
                    cust_ret(ret) if ret is not None else None
                    #if ret is not None:
                    #    return ret

                else:
                    ret = modify_dict(rpolish_lst[1], td.v_true, dic, query, symb)
                    cust_ret(ret) if ret is not None else None
                    #if ret is not None:
                    #    return ret

                return td.v_true

            if val.count(td.v_undef) == 2:
                ret = modify_dict(rpolish_lst[1], td.v_undef, dic, query, symb)
                cust_ret(ret) if ret is not None else None
                #if ret is not None:
                #    return ret

                rlt = modify_dict(rpolish_lst[2], td.v_undef, dic, query, symb)
                cust_ret(ret) if ret is not None else None
                #if ret is not None:
                #    return ret

                return td.v_undef

            if val.count(td.v_false) == 2:
                return td.Error

        if wanted is td.v_false:
            if td.v_true in val:
                return td.Error

            val = [-1, -1]
            for i, elt in enumerate(rpolish_lst[1:]):
                rlt = modify_dict(elt, td.v_false, dic, query, symb)
                val[i] = rlt if rlt is not None else dic[elt][0]

            return wanted if val.count(wanted) == 2 else val[0 if val[0] < 0 else 1]


    def _logic_and(self, dic, rpolish_lst, wanted, query, symb):
        """ handle the logic AND in the conclusion of the expression """

        val = [-1, -1]
        if len(rpolish_lst[1]) == 1 and len(rpolish_lst[2]) == 1:

            for i, fact in enumerate(rpolish_lst[1:]):

                if fact.isupper():
                    rlt = modify_dict(fact, wanted, dic, query, symb)
                    val[i] = rlt if rlt is not None else dic[fact][0]

                elif rpolish_lst[i + 1] != wanted:
                    val[i] = error(-6)
                    ### TO DO !! return check_error(dic, , wanted)

            return wanted if val.count(wanted) == 2 else val[0 if val[0] < 0 else 1]

        val = [-1, -1]
        for i, elt in enumerate(rpolish_lst[1:]):

            if len(elt) > 1:
                val[i] = self._recu_solver(dic, elt, wanted, query, symb)

            elif elt.isupper():
                rlt = modify_dict(elt, wanted, dic, query, symb)
                val[i] = rlt if rlt is not None else dic[elt][0]

            else:
                val[i] = int(elt)

        return wanted if val.count(wanted) == 2 else val[0 if val[0] < 0 else 1]


    @enable_ret
    def _logic_not(self, dic, rpolish_lst, wanted, query, symb):
        """ handle the logic NOT in the conclusion of the expression """

        inv_rlt = op.logic_not(wanted)

        if len(rpolish_lst[1]) > 1:
            val = self._recu_solver(dic, rpolish_lst[1], inv_rlt, query, symb)

        elif rpolish_lst[1].isupper():

            ret = modify_dict(rpolish_lst[1], inv_rlt, dic, query, symb)
            cust_ret(ret) if ret is not None else None
            #if ret is not None:
            #    return ret
            # val = inv_rlt
            val = wanted

        else:
            val = rpolish_lst[1]

        if int(val) != int(wanted):
            return error(-6)

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
        b, index = False, -1
        for i, elt in enumerate(rpolish_cpy[1:]):

            if elt in "^|+" and b is True:
                index = i + 1
                break

            elif elt.isupper() or elt.isdigit():
                b = True

        if index is not -1:
            rpolish_lst.extend((rpolish_cpy[1:index], rpolish_cpy[index:]))

        return rpolish_lst


    def _fill_dict(self, dic):
        """ """

        for elt in self.rpolish:
            if elt.isupper() and dic[elt][2] is td.m_default and dic[elt][1] is not td.q_initial:
                dic[elt][1] = td.q_needed

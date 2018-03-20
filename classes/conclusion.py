import re

import tools.defines as td
import handle_expression.operators as op
from error.error import error
from tools.functions import get_first_index
from handle_expression.create_RPN import get_polish_notation
from dictionary.check_dictionary import get_value_from_dict, fact_to_value
from dictionary.fill_dictionary import modify_value_in_dict
from tools.custom_return import enable_ret, cust_ret


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

        #print("in CC SOLVER query (%s) symb (%s) RPN (%s)" % (query, symb, self.rpolish))
        rpolish_cpy = self.rpolish
#        rpolish_cpy = fact_to_value(list(rpolish_cpy), dictionary)
        rlt = self._recu_solver(dictionary, rpolish_cpy, td.v_true, query, symb)
        #print("CONCLUSION last rlt : ", rlt)

        return rlt

    # !!!!!!!!!!! pb in XOR? undef not set

    def _recu_solver(self, dictionary, rpolish_cpy, wanted, query, symb):
        """ recursive function to call the correct operator function """

        rpolish_lst = []

        #print("--------------- BEFORE CALL rpolish(%s)" % rpolish_cpy)
        if get_first_index(td.Symbols[:-1], rpolish_cpy) is not -1:
            rpolish_lst = self._split_rpolish(rpolish_cpy)

        elif rpolish_cpy[0] is '!':
            rpolish_lst = ['!', rpolish_cpy[1:]]

        elif rpolish_cpy[0].isupper():
            if wanted is td.v_true:
                rlt = modify_value_in_dict(rpolish_cpy[0], td.v_true, dictionary,
                                       query, symb)
                if rlt is not None:
                    return rlt
            return get_value_from_dict(rpolish_cpy[0], dictionary)

        func_tbl = {'^': self._logic_xor,
                    '|': self._logic_or,
                    '+': self._logic_and,
                    '!': self._logic_not}

        if rpolish_cpy[0] in '^|+!':
            rlt = func_tbl[rpolish_cpy[0]](dictionary, rpolish_lst, wanted, query, symb)

        else:
            rlt = get_value_from_dict(rpolish_cpy[0], dictionary)

        return rlt


    @enable_ret
    def _logic_xor(self, dictionary, rpolish_lst, wanted, query, symb):
        """ """

        #print("-- IN XOR --", query, wanted, rpolish_lst, symb)
        val = [-1, -1]
        for i, elt in enumerate(rpolish_lst[1:]):
            if len(elt) > 1:
                val[i] = self._recu_solver(dictionary, elt, wanted, query, symb)
            else:
                val[i] = get_value_from_dict(elt, dictionary)

        #print(" XOR-after for", query, wanted, rpolish_lst, symb, val)
        if -1 in val:
            return td.Error

        if wanted is td.v_true:
            if val[0] != val[1] and td.v_undef not in val:
                return wanted
            if val[0] == val[1] and val[0] is not td.v_undef:
                return td.Error
            if val[0] == val[1]:
                ret = modify_value_in_dict(rpolish_lst[1], td.v_undef, dictionary, query, symb)
                if ret is not None:
                    return ret
                #cust_ret(ret) if ret is not None else None
                ret = modify_value_in_dict(rpolish_lst[2], td.v_undef, dictionary, query, symb)
                return td.v_undef if ret is None else ret

            melt = 1 if val[0] is td.v_undef else 2
            value = td.v_false if td.v_true in val else td.v_true
            ret = modify_value_in_dict(rpolish_lst[melt], value, dictionary, query, symb)
            if ret is not None:
                return ret
            #cust_ret(ret) if ret is not None else None

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
            ret = modify_value_in_dict(rpolish_lst[melt], value, dictionary, query, symb)
            if ret is not None:
                return ret

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

                    ret = modify_value_in_dict(rpolish_lst[2], td.v_true, dictionary, query, symb)
                    if ret is not None:
                        return ret
                    #if modify_value_in_dict(rpolish_lst[2], td.v_true, dictionary, query, symb) is not None:
                    #    return td.Error

                else:
                    rlt = modify_value_in_dict(rpolish_lst[1], td.v_true, dictionary, query, symb)
                    if rlt is not None:
                        return rlt

                return td.v_true

            if val.count(td.v_undef) == 2:
                rlt = modify_value_in_dict(rpolish_lst[1], td.v_undef, dictionary, query, symb)
                if rlt is not None:
                    return rlt

                rlt = modify_value_in_dict(rpolish_lst[2], td.v_undef, dictionary, query, symb)
                if rlt is not None:
                    return rlt

                return td.v_undef

            if val.count(td.v_false) == 2:
                return td.Error

        if wanted is td.v_false:
            if td.v_true in val:
                return td.Error

            val = [-1, -1]
            for i, elt in enumerate(rpolish_lst[1:]):
                rlt = modify_value_in_dict(elt, td.v_false, dictionary, query, symb)

                val[i] = rlt if rlt is not None else dictionary[elt][0]

            return wanted if val.count(wanted) == 2 else val[0 if val[0] < 0 else 1]


    def _logic_and(self, dictionary, rpolish_lst, wanted, query, symb):
        """ """

        #print("FIRST IF", rpolish_lst)
        val = [-1, -1]
        if len(rpolish_lst[1]) == 1 and len(rpolish_lst[2]) == 1:
            print("FIRST IF", rpolish_lst)
            for i, fact in enumerate(rpolish_lst[1:]):
                #print("FACT???", fact)

                if fact.isupper():
                    rlt = modify_value_in_dict(fact, wanted, dictionary, query, symb)
                    #print("rlt", rlt)
                    val[i] = rlt if rlt is not None else dictionary[fact][0]

                elif rpolish_lst[i + 1] != wanted:
                    val[i] = error(-6)
                    #            return check_error(dictionary, , wanted)



            return wanted if val.count(wanted) == 2 else val[0 if val[0] < 0 else 1]

        val = [-1, -1]
        #print(">>>>>>>>>>>>>>>>>> IN ADD CC", rpolish_lst)
        for i, elt in enumerate(rpolish_lst[1:]):
            print("NOT FIRST IF")

            if len(elt) > 1:
                val[i] = self._recu_solver(dictionary, elt, wanted, query, symb)

            elif elt.isupper():
                #print("ELIF => wanted(%s)" % wanted)
                rlt = modify_value_in_dict(elt, wanted, dictionary, query, symb)
                val[i] = rlt if rlt is not None else dictionary[elt][0]

            else:
                val[i] = int(elt)

        return wanted if val.count(wanted) == 2 else val[0 if val[0] < 0 else 1]


    def _logic_not(self, dictionary, rpolish_lst, wanted, query, symb):
        """ """

        print("FIRST IF", rpolish_lst)
        inv_rlt = op.logic_not(wanted)

        if len(rpolish_lst[1]) > 1:
            val = self._recu_solver(dictionary, rpolish_lst[1], inv_rlt, query, symb)

        elif rpolish_lst[1].isupper():
            rlt = modify_value_in_dict(rpolish_lst[1], inv_rlt, dictionary, query, symb)
            if rlt is not None:
                return rlt
            val = inv_rlt

        else:
            val = rpolish_lst[1]


        if int(val) == int(wanted):
            return error(-6)

        return val


    def _split_rpolish(self, rpolish_cpy):
        """ """

        ##print("SPILT POLISH", rpolish_cpy)
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

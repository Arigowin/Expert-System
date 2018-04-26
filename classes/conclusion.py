import tools.defines as td
from tools.functions import get_first_index
from handle_expression.create_RPN import get_polish_notation
from dictionary.check_dictionary import get_value_from_dict, fact_to_value
from dictionary.fill_dictionary import modify_dict
from tools.custom_return import enable_ret, cust_ret


class Conclusion:
    """
    the class that handle the conclusion side of the expression

    Variables:

        cc     variable holding the conclusion side of the expression
        r_rpn  custum 'reverse reverse polish notation'
               to ease conclusion solve

    Methods:

        solver        public method to launch the conclusion solver method
        _recu_solver  recursive method to call the correct operator method
        _logic_xor    logic xor handler for the conclusion side
        _logic_or     logic or handler for the conclusion side
        _logic_and    logic and handler for the conclusion side
        _logic_not    logic not handler for the conclusion side
        _not          return the NOT value
        _split_r_rpn  split our custum RPN into subgroups
        _fill_dict    call the modify_dict method for all the given facts

    """

    __slots__ = "cc", "r_rpn"

    def __init__(self, cc, dic):

        self.cc = cc
        self.r_rpn = get_polish_notation(cc)[::-1]
        self._fill_dict(dic)

    def solver(self, dic, query, symb):
        """ public method to launch the conclusion solver function """

        r_rpn_cpy = self.r_rpn

        rlt = self._recu_solver(dic, r_rpn_cpy, td.v_true, query, symb)

        return rlt

    @enable_ret
    def _recu_solver(self, dic, r_rpn_cpy, wanted, query, symb):
        """ recursive function to call the correct operator function """

        r_rpn_lst = []

        if get_first_index(td.Symbols, r_rpn_cpy) is not -1:
            r_rpn_lst = self._split_r_rpn(r_rpn_cpy)

        elif r_rpn_cpy[0].isupper():
            ret = modify_dict(r_rpn_cpy[0], wanted, dic, query, symb)
            cust_ret(ret) if ret is not None else None

            return get_value_from_dict(r_rpn_cpy[0], dic)

        func_tbl = {'^': self._logic_xor,
                    '|': self._logic_or,
                    '+': self._logic_and,
                    '!': self._logic_not}

        if r_rpn_cpy[0] in '^|+!':
            rlt = func_tbl[r_rpn_cpy[0]](dic, r_rpn_lst, wanted, query, symb)

        else:
            rlt = get_value_from_dict(r_rpn_cpy[0], dic)

        return rlt

    @enable_ret
    def _logic_xor(self, dic, r_rpn_lst, wanted, query, symb):
        """ handle the logic XOR in the conclusion of the expression """

        val = fact_to_value(r_rpn_lst[1:], dic)

        if (-1 not in val and 2 not in val
                and ((wanted is td.v_true and val[0] == val[1])
                     or (wanted is td.v_false and val[0] != val[1]))):

            if query in r_rpn_lst:
                elts = []
                for elt in list(r_rpn_lst[1:]):
                    for letter in elt:
                        if letter.isupper():
                            elts += letter

                ret = modify_dict(elts, td.v_bugged, dic, query, symb)

                return -2

        i = 1
        while i < 3:
            to_give = td.v_undef
            if wanted is not td.v_undef:
                other_val = val[0 if i == 2 else 1]

                if other_val == td.v_undef and other_val == -1:
                    to_give = td.v_undef
                elif wanted == other_val and other_val != -1:
                    to_give = td.v_false
                elif val.count(-1) == 0 and other_val is not td.v_undef:
                    to_give = td.v_true

                wanted == (other_val and -1 not in val,
                           val.count(-1) != 2 and -1 not in val)

            if len(r_rpn_lst[i]) > 1:
                tmp = self._recu_solver(dic, r_rpn_lst[i],
                                        to_give, query, symb)

            elif r_rpn_lst[i].isupper():
                ret = modify_dict(r_rpn_lst[i], to_give, dic, query, symb)
                cust_ret(ret) if ret is not None else None
                tmp = to_give

            if tmp != val[i - 1]:
                val[i - 1] = tmp
                i = 0

            i += 1

        if (val.count(td.v_undef) == 0
                and ((wanted is td.v_true and val[0] != val[1])
                     or (wanted is td.v_false and val[0] == val[1]))):
            return wanted

        elif (val.count(td.v_undef) == 0
                and ((wanted is td.v_true and val[0] == val[1])
                     or (wanted is td.v_false and val[0] != val[1]))):

            elts = set([elt for elt in list(r_rpn_lst[1:]) if elt.isupper()])
            ret = modify_dict(elts, td.v_bugged, dic, query, symb)

            return -2

        elif (val.count(td.v_undef) == 1 and len(r_rpn_lst[1]) == 1
              and len(r_rpn_lst[2]) == 1):
            to_give = (td.v_true if (wanted is td.v_true and td.v_false in val)
                       or (wanted is td.v_false and td.v_true in val)
                       else td.v_false)

            ret = modify_dict(r_rpn_lst[1 + val.index(td.v_undef)], to_give,
                              dic, query, symb)

            return wanted if ret is None else ret

        return td.v_undef

    @enable_ret
    def _logic_or(self, dic, r_rpn_lst, wanted, query, symb):
        """ handle the logic OR in the conclusion of the expression """

        val = fact_to_value(r_rpn_lst[1:], dic)
        if ((wanted is td.v_false and td.v_true in val)
                or (wanted is td.v_true and val.count(td.v_false) == 2)):
            if query in r_rpn_lst:
                elts = []
                for elt in list(r_rpn_lst[1:]):
                    for letter in elt:
                        if letter.isupper():
                            elts += letter

                ret = modify_dict(elts, td.v_bugged, dic, query, symb)

                return -2

        i = 1
        while i < 3:
            to_give = td.v_undef
            if wanted is not td.v_undef:
                other_val = val[0 if i == 2 else 1]
                to_give = (td.v_true if wanted is td.v_true
                           and other_val is td.v_false
                           else td.v_false if wanted is td.v_false
                           else td.v_undef)

            if len(r_rpn_lst[i]) > 1:
                tmp = self._recu_solver(dic, r_rpn_lst[i],
                                        to_give, query, symb)

            if len(r_rpn_lst[i]) == 1 and r_rpn_lst[i].isupper():
                ret = modify_dict(r_rpn_lst[i], to_give, dic, query, symb)
                cust_ret(ret) if ret is not None else None
                tmp = dic[r_rpn_lst[i]][0]

            if tmp != val[i - 1]:
                val[i - 1] = tmp
                i = 0

            i += 1

        return (wanted if val.count(wanted) == 2
                or (val.count(wanted) == 1 and wanted is td.v_true)
                else td.v_undef)

    def _logic_and(self, dic, r_rpn_lst, wanted, query, symb):
        """ handle the logic AND in the conclusion of the expression """

        val = fact_to_value(r_rpn_lst[1:], dic)
        if ((wanted is td.v_true and td.v_false in val)
                or (wanted is td.v_false and val.count(td.v_true) == 2)):

            if query in r_rpn_lst:
                not_wanted = (td.v_true if wanted is td.v_false
                              else td.v_false if wanted is td.v_true
                              else td.v_undef)

                tmp = ''.join(elt for i, elt in enumerate(r_rpn_lst[1:])
                              if val[i] is not_wanted)

                bug = set([elt for elt in tmp if elt.isupper()])

                ret = modify_dict(bug, td.v_bugged, dic, query, symb)

                und = set([elt for elt in tmp if elt.isupper()
                           and elt not in bug])

                ret = modify_dict(und, td.v_undef, dic, query, symb)

                return -2

        for i, elt in enumerate(r_rpn_lst[1:]):
            if len(elt) > 1:
                other_val = val[0 if i == 1 else 1]

                to_give = td.v_undef
                if wanted is td.v_true:
                    to_give = wanted
                elif wanted is td.v_false and other_val is td.v_true:
                    to_give = td.v_false

                val[i] = self._recu_solver(dic, elt, to_give, query, symb)

            else:
                value = (td.v_true if wanted is td.v_true
                         else td.v_false if wanted is td.v_false
                         and val[0 if i == 1 else 1] is td.v_true
                         else td.v_undef)
                ret = modify_dict(elt, value, dic, query, symb)
                cust_ret(ret) if ret is not None else None
        return (td.v_false if val.count(td.v_false) > 0 else td.v_undef
                if val.count(td.v_undef) > 0 else td.v_true)

    @enable_ret
    def _logic_not(self, dic, r_rpn_lst, wanted, query, symb):
        """ handle the logic NOT in the conclusion of the expression """

        inv_rlt = self._not(wanted) if wanted < 2 else td.v_undef

        if len(r_rpn_lst[1]) > 1:
            val = self._recu_solver(dic, r_rpn_lst[1], inv_rlt, query, symb)
            val = (td.v_true if val == td.v_false
                   else td.v_false if val == td.v_true else val)

        elif r_rpn_lst[1].isupper():

            if dic[r_rpn_lst[1]][2] >= symb:
                val = (dic[r_rpn_lst[1]][0]
                       if dic[r_rpn_lst[1]][0] is not td.v_undef else inv_rlt)

                ret = modify_dict(r_rpn_lst[1], val, dic, query, symb)
                cust_ret(ret) if ret is not None else None

                val = (td.v_true if val is td.v_false
                       else td.v_false if val is td.v_true else td.v_undef)

            else:
                ret = modify_dict(r_rpn_lst[1], inv_rlt, dic, query, symb)
                cust_ret(ret) if ret is not None else None
                val = wanted

        else:
            val = r_rpn_lst[1]

        if (int(val) != int(wanted) and wanted is not td.v_undef
                and int(val) >= 0
                and int(val) is not td.v_undef
                and (len(r_rpn_lst[1]) > 1 or dic[r_rpn_lst[1]][2] <= symb)):

            elts = set([elt for elt in ''.join(r_rpn_lst[1]) if elt.isupper()])
            ret = modify_dict(elts, td.v_bugged, dic, query, symb)
            return -2

        return val

    def _not(self, val):
        """ return the NOT value """

        return (td.v_undef if int(val) == td.v_undef
                else td.v_true if int(val) is td.v_false
                else td.v_false)

    def _split_r_rpn(self, r_rpn_cpy):
        """ split the RPN expression to handle each part separately """

        op, index = [], 0
        for i, elt in enumerate(r_rpn_cpy):

            if elt in "^|+":
                op.append(2)
            elif elt is '!':
                op.append(1)
            else:
                if len(op) == 1 and index == 0:
                    index = i + 1

                op[-1] -= 1

                while op and op[-1] == 0:
                    op.remove(op[-1])

                    if (len(op) > 0):
                        op[-1] -= 1
                    if len(op) == 1 and index == 0:
                        index = i + 1

        return ([r_rpn_cpy[0], r_rpn_cpy[1:]] if r_rpn_cpy[0] == '!'
                else [r_rpn_cpy[0], r_rpn_cpy[1:index], r_rpn_cpy[index:]])

    def _fill_dict(self, dic):
        """ fill the dictionary with the newly found values """

        for elt in self.r_rpn:
            if (elt.isupper() and dic[elt][2] is td.m_default
                    and dic[elt][1] is not td.q_initial):
                dic[elt][1] = td.q_needed

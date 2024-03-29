import copy

import tools.defines as td
import tools.functions as tf
from classes.enum import Btype
from tools.display import display_steps
from error.error import error


class _BNode:
    """ A node containing either a condition expression or a conclusion fact

    Variables:
        btype
        rule
        query
        children
        value

    Functions:
        get_value_cdt_solver

    """

    __slots__ = "btype", "rule", "query", "children", "value"

    def __init__(self, dic, btype, rule=None, query=None):

        self.btype = btype
        self.rule = rule
        self.query = query
        self.children = []

        if self.btype is Btype.CDT:
            self.value = self.get_value_cdt_solver(dic)
        else:
            self.value = dic[query][0]

    def get_value_cdt_solver(self, dic):
        self.value = self.rule.cdt.solver(dic)
        return self.value


class Btree:
    """

    Variables:
        _query
        _root

    Functions:
        recu_launcher
        _recu
        _node_cdt
        _node_cc
        _cc_solver_checker
        _node_checking
        _tree_skimming
        _new_node

    """

    __slots__ = "_query", "_root"

    def __init__(self, dic, rule_lst, query):
        self._query = query

        _, self._root = self._new_node(dic, Btype.CC, query=query)

    def recu_launcher(self, dic, rule_lst, prev_rule=None):
        """ launch the main recursive loop """

        return self._recu(dic, rule_lst, self._root, prev_rule)

    def _recu(self, dic, rule_lst, curr_bnode, prev_rule):
        """ specify which element is needed in a specific bnode """

        if curr_bnode.query:
            display_steps("\nFinding the value of ", curr_bnode.query, query=curr_bnode.query, dic=dic)

        if curr_bnode.btype is Btype.CC:
            self._node_cc(dic, curr_bnode, rule_lst, prev_rule)
            return dic[curr_bnode.query][0]

        return self._node_cdt(dic, curr_bnode, rule_lst, prev_rule)

    def _node_cdt(self, dic, curr_bnode, rule_lst, prev_rule):
        """ """

        val = curr_bnode.value
        if val is td.v_undef:
            for fact in curr_bnode.rule.cdt_lst:
                if dic[fact][1] < 2:
                    child_node, curr_bnode = self._new_node(dic,
                                                            btype=Btype.CC,
                                                            query=fact,
                                                            tree=curr_bnode)

                    self._recu(dic, rule_lst, child_node, prev_rule)
                    if dic[fact][2] is td.m_default:
                        dic[fact][2] = td.m_iif

            curr_bnode.get_value_cdt_solver(dic)

        return val

    def _node_cc(self, dic, curr_bnode, rule_lst, prev_rule):
        """ """

        query = curr_bnode.query

        if dic[query][2] <= 0 or dic[query][0] is td.v_undef:
            needed_rule = dict((rule, -1) for rule in rule_lst if
                               query in rule.cc_lst and rule is not prev_rule)

            display_steps("Rules containing ", "%s: " % query, ", ".join([rule.expr for rule in needed_rule]), "\n", query=curr_bnode.query, dic=dic)

            if len(needed_rule) == 0:
                display_steps("\tNo rule for", " %s" % curr_bnode.query, query=curr_bnode.query, dic=dic)

            for rule in needed_rule:
                if query not in rule.used:
                    child_node, curr_bnode = self._new_node(dic,
                                                            btype=Btype.CDT,
                                                            rule=rule,
                                                            tree=curr_bnode)

                    rule.used.append(query)
                    ret_recu = self._recu(dic, rule_lst, child_node, prev_rule)

                    needed_rule[rule] = ret_recu

            for node in curr_bnode.children:

                if node.value is td.v_true:
                    val_cc = self._cc_solver_checker(dic, rule_lst, node.rule,
                                                     query, node.rule.prio)
                    node.rule.used.append(query)

                    if ((val_cc is td.v_undef or val_cc < 0)
                        and ('^' in node.rule.cc.cc or '|' in node.rule.cc.cc
                             or "!+" in node.rule.cc.r_rpn)
                            or dic[query][2] is td.m_nset):
                        cc_lst = (node.rule.cc_lst if node.rule.cc_lst[0]
                                  is not query
                                  else node.rule.cc_lst[::-1])

                        cust_rule_lst = [rule for rule in rule_lst if rule.expr
                                         is not node.rule.expr]
                        for elt in cc_lst:
                            if dic[elt][0] is not td.v_bugged:
                                display_steps("\nWe need to know the value of", " %s" % elt, query=curr_bnode.query, dic=dic)

                                new_tree = Btree(dic, cust_rule_lst, elt)
                                new_tree.recu_launcher(dic, cust_rule_lst,
                                                       curr_bnode.rule)

                                value = ("True" if dic[elt][0] is td.v_true
                                         else "False" if dic[elt][0] is td.v_false
                                         else "Not define" if dic[elt][0] is
                                              td.v_undef
                                         else "Bugged")
                                display_steps("\tNewly found value for", " %s: " % elt, end_display=value, query=curr_bnode.query, dic=dic)

                        if (dic[query][0] is not td.v_bugged
                                and node.rule.prio > dic[query][2]):
                            dic[query][2] = node.rule.prio

                        self._cc_solver_checker(dic, rule_lst, node.rule,
                                                query, node.rule.prio)
            if len([key for key, value in needed_rule.items()
                    if value is td.v_undef]):
                self._node_checking(dic, list(map(list, needed_rule.items())),
                                    rule_lst, query)

        else:
            if tf.check_with_curr_value(curr_bnode.query, rule_lst, dic, True, 2):
                display_steps("\tValue of", " %s already known.\n" % curr_bnode.query, query=curr_bnode.query, dic=dic)
            elif dic[curr_bnode.query][0] is td.v_bugged:
                error(-2)
                display_steps("\tNewly found value for", " %s: " % curr_bnode.query, end_display="Bugged", query=curr_bnode.query, dic=dic)


    def _cc_solver_checker(self, dic, rule_lst, curr_rule, query, prio):

        bck_dic = copy.deepcopy(dic)

        if curr_rule.prio is 1:
            display_steps("\tNext expression containing", " %s, from rule %s: %s" % (query, curr_rule.expr, curr_rule.sub_rule), query=query, dic=dic)
        else:
            display_steps("\tNext expression containing", " %s: %s" % (query, curr_rule.expr), query=query, dic=dic)

        ret = curr_rule.cc.solver(dic, query, prio)
        if ret == -2 or (ret is td.v_bugged and bck_dic[query][0] is not td.v_bugged):
            return error(-2, " - on rule: %s" % curr_rule.expr)

        if bck_dic != dic:
            new_lst = [elt for elt in rule_lst if query in elt.expr]

            for elt in new_lst:
                if elt.prio is 1:
                    display_steps("\tNext expression containing", " %s, from rule %s: %s" % (query, elt.expr, elt.sub_rule), query=query, dic=dic)
                else:
                    display_steps("\tNext expression containing", " %s: %s" % (query, elt.expr), query=query, dic=dic)

                if elt.cdt.solver(dic) is td.v_true:
                    tmp = elt.cc.solver(dic, query, elt.prio)
                    if tmp == -2 or (tmp is td.v_bugged and bck_dic[query][0] is not td.v_bugged):
                        return error(-2, " - on rule: %s" % elt.expr)

                    if elt == curr_rule:
                        ret = tmp

        display_steps("\t\tExpression with the newly found values: ", "%s" % curr_rule.expr, query=query, dic=dic)
        return ret

    def _node_checking(self, dic, sorted_rule, rule_lst, query):
        """ check if rules that contain the requested fact in cc can be
        determined
        """

        i = 0
        bck_sorted = sorted_rule.copy()

        while i in range(len(sorted_rule)):

            if sorted_rule[i][1] is td.v_undef:
                val = -1
                ret = self._tree_skimming(dic, rule_lst,
                                          sorted_rule[i][0].cdt_lst)
                a = sorted_rule[i][0].cdt.solver(dic)

                if ret and a is td.v_true:
                    val = self._cc_solver_checker(dic, rule_lst,
                                                  sorted_rule[i][0],
                                                  query,
                                                  sorted_rule[i][0].prio)

                if val != sorted_rule[i][1]:
                    sorted_rule[i][1] = val

            if td.v_undef not in [elt[1] for elt in sorted_rule]:
                break

            i += 1

            if i == len(sorted_rule) and bck_sorted != sorted_rule:
                bck_sorted = sorted_rule
                i = 0

    def _tree_skimming(self, dic, rule_lst, cdt_lst):
        """ skim the tree to check every child node """

        ret = False

        for elt in cdt_lst:
            if dic[elt][0] is td.v_undef or dic[elt][2] <= 0:
                new_tree = Btree(dic, rule_lst, elt)
                new_tree.recu_launcher(dic, rule_lst)
                ret = True

        return ret

    def _new_node(self, dic, btype, rule=None, query=None, tree=None):
        """ create a new child node to be attach to the tree """

        if not tree:
            child = _BNode(dic, btype, rule, query)

            return None, child

        child = _BNode(dic, btype, rule, query)
        tree.children.append(child)

        return child, tree

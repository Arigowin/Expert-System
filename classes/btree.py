import tools.defines as td
from classes.enum import Btype
from error.error import error
from tools.custom_return import enable_ret, cust_ret
from tools.functions import print_dict


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
        _node_checking
        _tree_skimming
        _new_node

    """

    __slots__ = "_query", "_root"


    def __init__(self, dic, rule_lst, query):
        self._query = query

        needed_rule = [rule for rule in rule_lst if query in rule.cc_lst]
        _, self._root = self._new_node(dic, Btype.CC, query=query)


    def recu_launcher(self, dic, rule_lst, prev_rule=None):
        """ """

        print("\nRECU LAUNCHER START", self._root.query)
        print_dict(dic)

        ret = self._recu(dic, rule_lst, self._root, prev_rule)

        return ret


    def _recu(self, dic, rule_lst, curr_bnode, prev_rule):
        """ specify which element is needed in a specific bnode """

        print(" -- RECU -- ")

        if curr_bnode.btype is Btype.CC:
            self._node_cc(dic, curr_bnode, rule_lst, prev_rule)
            return dic[curr_bnode.query][0]

        return self._node_cdt(dic, curr_bnode, rule_lst, prev_rule)


    def _node_cdt(self, dic, curr_bnode, rule_lst, prev_rule):
        """ """

        print(" -- NODE CDT -- ", curr_bnode.rule.expr, curr_bnode.query)

        val = curr_bnode.value
        if val is td.v_undef:
            for fact in curr_bnode.rule.cdt_lst:
                if dic[fact][1] < 2:
                    child_node, curr_bnode = self._new_node(dic,
                                                           btype=Btype.CC,
                                                           query=fact,
                                                           tree=curr_bnode)

                    ret_cdt = self._recu(dic, rule_lst, child_node, prev_rule)
                    print(" -- DEPIL CDT --", curr_bnode.rule.cdt_lst, fact)
                    if dic[fact][2] is td.m_default:
                        dic[fact][2] = td.m_iif

            curr_bnode.get_value_cdt_solver(dic)

        return val


    def _node_cc(self, dic, curr_bnode, rule_lst, prev_rule):
        """ """

        print(" -- NODE CC -- ", curr_bnode.query, dic[curr_bnode.query])

        query = curr_bnode.query

        if dic[query][2] <= 0 or dic[query][0] is td.v_undef:
            needed_rule = dict((rule, -1) for rule in rule_lst if
                          query in rule.cc_lst and rule is not prev_rule)

            for rule in needed_rule:
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx", rule.expr, rule.cdt.solver(dic))
                if query not in rule.used:
                    child_node, curr_bnode = self._new_node(dic,
                                                            btype=Btype.CDT,
                                                            rule=rule,
                                                            tree=curr_bnode)

                    rule.used.append(query)
                    ret_recu = self._recu(dic, rule_lst, child_node, prev_rule)

                    print(" -- DEPIL CC --", ret_recu)
                    needed_rule[rule] = ret_recu

            for node in curr_bnode.children:
                print("NODE EXPR", node.rule.expr)
                if node.value is td.v_true:
                    val_cc = node.rule.cc.solver(dic, query, node.rule.prio)
                    node.rule.used.append(query)

                    if ((val_cc is td.v_undef or val_cc < 0)
                         and ('^' in node.rule.cc.cc or '|' in node.rule.cc.cc or "!+" in node.rule.cc.r_rpn)
                         or dic[query][2] is td.m_nset):
                        cc_lst = (node.rule.cc_lst if node.rule.cc_lst[0]
                                                    is not query
                                  else node.rule.cc_lst[::-1])

                        cust_rule_lst = [rule for rule in rule_lst if rule.expr is not node.rule.expr]
                        for elt in cc_lst:
                            print("\nSTART NEW TREE CC", elt)

                            new_tree = Btree(dic, cust_rule_lst, elt)
                            new_tree.recu_launcher(dic, cust_rule_lst, curr_bnode.rule)
                            print("\nEND NEW TREE CC", elt)


                        if dic[query][0] is not td.v_bugged and node.rule.prio > dic[query][2]:
                            dic[query][2] = node.rule.prio

                        node.rule.cc.solver(dic, query, node.rule.prio)

            if len([key for key, value in needed_rule.items() if value is td.v_undef]):
                ret = self._node_checking(dic, list(map(list, needed_rule.items())), rule_lst, query)


    def _node_checking(self, dic, sorted_rule, rule_lst, query):
        """ check if rules that contain the requested fact in cc can be
        determined
        """

        print(" -- NODE CHECK -- ")

        i = 0
        bck_sorted = sorted_rule.copy()

        while i in range(len(sorted_rule)):
            print("_node_checking ", [(elt[0].expr, elt[1]) for elt in sorted_rule], (sorted_rule[i][0].expr, sorted_rule[i][1]))

            if sorted_rule[i][1] is td.v_undef:
                val = -1
                ret = self._tree_skimming(dic, rule_lst, sorted_rule[i][0].cdt_lst)
                a = sorted_rule[i][0].cdt.solver(dic)
                print("BAC", ret, a, sorted_rule[i][0].cdt_lst)
                if ret and a is td.v_true:
                    val = sorted_rule[i][0].cc.solver(dic, query, sorted_rule[i][0].prio)

                if val != sorted_rule[i][1]:
                    sorted_rule[i][1] = val

            if td.v_undef not in [elt[1] for elt in sorted_rule]:
                print("break")
                break

            i += 1

            if i == len(sorted_rule) and bck_sorted != sorted_rule:
                bck_sorted = sorted_rule
                i = 0


    def _tree_skimming(self, dic, rule_lst, cdt_lst):
        """ skim the tree to check every child node """

        print("-- TREE SKIM --")
        b = False

        for elt in cdt_lst:
            # if dic[elt][2] is td.m_default:
                print("\nSTART NEW TREE", elt)
                new_tree = Btree(dic, rule_lst, elt)
                ret = new_tree.recu_launcher(dic, rule_lst)
                print("val from new Tree", ret)
                print("\nEND NEW TREE", elt)
                b = True

        return b


    def _new_node(self, dic, btype, rule=None, query=None, tree=None):
        """ create a new child node to be attach to the tree """

        if not tree:
            child = _BNode(dic, btype, rule, query)

            return None, child

        child = _BNode(dic, btype, rule, query)
        tree.children.append(child)

        return child, tree

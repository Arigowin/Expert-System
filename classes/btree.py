import tools.defines as td
from classes.enum import Btype
from error.error import error
from tools.custom_return import enable_ret, cust_ret


#### modifier dico par dic

class _BNode:
    """ A node containing either a condition expression or a conclusion fact """

    __slots__ = "btype", "rule", "query", "children", "value"

    def __init__(self, dico, btype, rule=None, query=None):

        #if query and rule:
        #    ##print("ERROR!!!!!!!!!!! BNODE INIT")

        self.btype = btype
        self.rule = rule
        self.query = query
        self.children = []

        if self.btype is Btype.CDT:
            self.value = self.rule.cdt.solver(dico)
        else:
            self.value = dico[query][0]


class Btree:
    """ """

    __slots__ = "_query", "_root"


    def __init__(self, dico, rule_lst, query):
        self._query = query

        needed_rule = [rule for rule in rule_lst if query in rule.cc_lst]
        _, self._root = self._new_node(dico, Btype.CC, query=query)


    def recu_launcher(self, dico, rule_lst, prev_rule=None):
        """ """

        print("RECU LAUNCHER START", self._root.query)

        ret = self._recu(dico, rule_lst, self._root, prev_rule)

        ##print("RECU LAUNCHER EXIT", self._root.query, "\n")
        return ret


    def _recu(self, dico, rule_lst, curr_bnode, prev_rule):
        """ specify which element is needed in a specific bnode """
        print(" -- RECU -- ")

        if curr_bnode.btype is Btype.CC:

            self._node_cc(dico, curr_bnode, rule_lst, prev_rule)
            return dico[curr_bnode.query][0]

        return self._node_cdt(dico, curr_bnode, rule_lst, prev_rule)


    def _node_cdt(self, dico, curr_bnode, rule_lst, prev_rule):
        """ """

        print(" -- NODE CDT -- ", curr_bnode.rule.expr, curr_bnode.query)

        val = curr_bnode.value
        if val is td.v_undef:

           for fact in curr_bnode.rule.cdt_lst:

               if dico[fact][1] < 2:
                   child_node, curr_bnode = self._new_node(dico,
                                                           btype=Btype.CC,
                                                           query=fact,
                                                           tree=curr_bnode)

                   ret_cdt = self._recu(dico, rule_lst, child_node, prev_rule)
                   print(" -- DEPIL CDT --")

           return curr_bnode.rule.cdt.solver(dico)

        return val


    def _node_cc(self, dico, curr_bnode, rule_lst, prev_rule):
        print(" -- NODE CC -- ", curr_bnode.query, dico[curr_bnode.query])
        query = curr_bnode.query
        val = dico[query][0]

        if dico[query][2] <= 0 or dico[query][0] is td.v_undef:

            needed_rule = dict((rule, -1) for rule in rule_lst if
                          query in rule.cc_lst and rule is not prev_rule)

            for rule in needed_rule:

                if query not in rule.used:
                    child_node, curr_bnode = self._new_node(dico,
                                                            btype=Btype.CDT,
                                                            rule=rule,
                                                            tree=curr_bnode)

                    rule.used.append(query)
                    ret_recu = self._recu(dico, rule_lst, child_node, prev_rule)

                    print(" -- DEPIL CC --", ret_recu)
                    needed_rule[rule] = ret_recu

            for rule in needed_rule:

                print("in 2nd for", rule.expr, needed_rule[rule], rule.prio)
                if needed_rule[rule] is td.v_true:

                    val_cc = rule.cc.solver(dico, query, rule.prio)
                    #print("VAL CC", query,  val_cc, dico[query][2])
                    rule.used.append(query)

                    if ((val_cc is td.v_undef or val_cc < 0)
                         and ('^' in rule.cc.cc or '|' in rule.cc.cc)
                         or dico[query][2] == -1):

                        cc_lst = rule.cc_lst if rule.cc_lst[0] is not query else rule.cc_lst[::-1]
                        cc_lst.remove(query)

                        for elt in cc_lst:

                            new_tree = Btree(dico, rule_lst, elt)
                            new_tree.recu_launcher(dico, rule_lst, curr_bnode.rule)

                        if dico[query][0] is not td.v_bugged and rule.prio > dico[query][2]:
                            dico[query][2] = rule.prio

                        rule.cc.solver(dico, query, rule.prio)

            if len([key for key, value in needed_rule.items() if value is td.v_undef]):
                ret = self._node_checking(dico, list(map(list, needed_rule.items())), curr_bnode)



    def _node_checking(self, dico, sorted_rule, curr_bnode):
        """ check if rules that contain the requested fact in cc can be
        determined
        """

        print(" -- NODE CHECK -- ", curr_bnode, curr_bnode.rule)#, curr_bnode.rule.expr)
        i = 0
        bck_sorted = sorted_rule.copy()

        while i in range(len(sorted_rule)):
            if sorted_rule[i][1] is td.v_undef:

                val = self._tree_skimming(dico, curr_bnode)
                if val != sorted_rule[i][1]:
                    sorted_rule[i][1] = val

            if td.v_undef not in sorted_rule:
                break

            i += 1

            if i == len(sorted_rule) and bck_sorted != sorted_rule:
                bck_sorted = sorted_rule
                i = 0


    def _tree_skimming(self, dico, curr_bnode):
        """ skim the tree to check every child node """

        print("-- TREE SKIM --", curr_bnode.btype,  curr_bnode.query if curr_bnode.query else curr_bnode.rule.cc.cc)

        for child in curr_bnode.children:
            print(child.query)

            if child.btype is Btype.CDT and child.value is td.v_undef:
                val = child.rule.cdt.solver(dico)
                if val and val == child.value:
                    self._tree_skimming(dico, child)

            elif child.btype is Btype.CC and child.value is td.v_undef:
                print("child rule  (%s)" % child.rule)
                self._tree_skimming(dico, child)
                #if dico[child.query][0] is td.v_undef or dico[child.query][2] < child.rule.prio:
                #    child.rule.cc.solver(dico, child.query, child.rule.prio)
                #    if dico[child.query][0] == child.value:
                #        self._tree_skimming(dico, child)


    def _new_node(self, dico, btype, rule=None, query=None, tree=None):
        """ create a new child node to be attach to the tree """

        if not tree:
            child = _BNode(dico, btype, rule, query)

            return None, child

        child = _BNode(dico, btype, rule, query)
        tree.children.append(child)

        return child, tree


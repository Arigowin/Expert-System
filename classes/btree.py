import tools.defines as td
from classes.enum import Btype
from error.error import error
from dictionary.fill_dictionary import modify_value_in_dict
from tools.custom_return import enable_ret, cust_ret


class _BNode:
    """ """

    __slots__ = "btype", "rule", "query", "children", "value"

    def __init__(self, dictionary, btype, rule=None, query=None):

        #if query and rule:
        #    ##print("ERROR!!!!!!!!!!! BNODE INIT")

        self.btype = btype
        self.rule = rule
        self.query = query
        self.children = []

        if self.btype is Btype.CDT:
            self.value = self.rule.cdt.solver(dictionary)
        else:
            self.value = dictionary[query][0]


class Btree:
    """ """

    __slots__ = "_query", "_root"

    def __init__(self, dictionary, rule_lst, query):
        self._query = query

        # self._rule_lst = rule_lst  # => cf si on la garde en variable

        needed_rule = [rule for rule in rule_lst if query in rule.cc_lst]
        _, self._root = self._create_bnode(dictionary, Btype.CC, query=query)

    def recu_launcher(self, dictionary, rule_lst, prev_rule=None):
        """ """

        ##print("RECU LAUNCHER START", self._root.query)
        ret = self._recu(dictionary, rule_lst, self._root, prev_rule)
        ##print("RECU LAUNCHER EXIT", self._root.query, "\n")
        return ret

    @enable_ret
    def _recu(self, dictionary, rule_lst, curr_bnode, prev_rule):
        """ specify which element is needed in a specific bnode """
        ##print(" -- RECU -- ")

        if curr_bnode.btype is Btype.CC:
            self._node_cc(dictionary, curr_bnode, rule_lst, prev_rule)
            return dictionary[curr_bnode.query][0]

        return self._node_cdt(dictionary, curr_bnode, rule_lst, prev_rule)


    def _node_cdt(self, dictionary, curr_bnode, rule_lst, prev_rule):
        ##print(" -- NODE CDT -- ", curr_bnode.rule.expr, curr_bnode.query)

        val = curr_bnode.value
        ##print("VAL IN CDT", val)

        if val is td.v_undef:
           ##print("VAL IN CDT IF 1", val)

           for fact in curr_bnode.rule.cdt_lst:
               ##print("FACT in CDT FOR", fact, dictionary[fact][1])
               if dictionary[fact][1] < 2:
                   child_node, curr_bnode = \
                       self._create_bnode(dictionary,
                                          btype=Btype.CC,
                                          query=fact,
                                          tree=curr_bnode)

                   ##print("BEFORE RECU CDT")
                   ret_cdt = self._recu(dictionary, rule_lst, child_node, prev_rule)
                   ##print(" -- DEPIL CDT --")

           return curr_bnode.rule.cdt.solver(dictionary)
        ##print("END CDT", val)

        return val


    def _node_cc(self, dictionary, curr_bnode, rule_lst, prev_rule):
        ##print(" -- NODE CC -- ", curr_bnode.query)
        query = curr_bnode.query
        val = dictionary[query][0]

        if val is not td.v_true and val is not td.v_bugged and (dictionary[query][2] <= 0 or dictionary[query][0] is td.v_undef):

            needed_rule = dict((rule, -1) for rule in rule_lst if
                          query in rule.cc_lst and rule is not prev_rule)

            #i = 0
            #while i in range(len(needed_rule)):
            for rule in needed_rule:
                ##print("rule (%s)" % rule.expr)

                child_node, curr_bnode = \
                   self._create_bnode(dictionary,
                                      btype=Btype.CDT,
                                      rule=rule,
                                      tree=curr_bnode)

                ret_recu = self._recu(dictionary, rule_lst, child_node, prev_rule)
                ##print(" -- DEPIL CC --", )
                needed_rule[rule] = ret_recu

            for rule in needed_rule:

                ##print("in 2nd for", rule.expr, needed_rule[rule])
                if needed_rule[rule] is td.v_true:

                    val_cc = rule.cc.solver(dictionary, query, rule.prio)
                    ##print("VAL CC", query,  val_cc, dictionary[query][2])
                    rule.used.append(query)
                    if (val_cc is td.v_undef or val_cc < 0) \
                       and ('^' in rule.cc.cc or '|' in rule.cc.cc): # and dictionary[query][2] == -1:

                        ##print("not here??????????????")
                        cc_lst = rule.cc_lst if rule.cc_lst[0] is not query else rule.cc_lst[::-1]
                        #bck_used = rule.used.copy()
                        #rule.used = []

                        cc_lst.remove(query)

                        for elt in cc_lst:
                            new_tree = Btree(dictionary, rule_lst, elt)
                            new_tree.recu_launcher(dictionary, rule_lst, curr_bnode.rule)

                        rule.cc.solver(dictionary, query, rule.prio)
                        #rule.used.copy()

            ##print(" >> BEFORE new fct << ", [key for key, value in needed_rule.items() if value is td.v_undef])

            # on check si il y a un undef dans la liste des retours
            #   si non: pas de pb rien a faire
            #   si oui
            if len([key for key, value in needed_rule.items() if value is td.v_undef]):
                ret = self._node_checking(dictionary, list(map(list, needed_rule.items())), curr_bnode)


               #if rule.used.count(query) == 2:
               ##if query in rule.used:
               #    return error(-6)


    def _node_checking(self, dictionary, sorted_rule, curr_bnode):
        """ check if rules that contain the requested fact in cc can be
        determined
        """

        ##print(" -- NODE CHECK -- ", curr_bnode, curr_bnode.rule)#, curr_bnode.rule.expr)
        i = 0
        bck_sorted = sorted_rule.copy()

        while i in range(len(sorted_rule)):
            if sorted_rule[i][1] is td.v_undef:

                val = self._tree_skimming(dictionary, curr_bnode)
                if val != sorted_rule[i][1]:
                    sorted_rule[i][1] = val

            if td.v_undef not in sorted_rule:
                break

            i += 1

            if i == len(sorted_rule) and bck_sorted != sorted_rule:
                bck_sorted = sorted_rule
                i = 0


    def _tree_skimming(self, dictionary, curr_bnode):
        """ skim the tree to check every child node """

        for child in curr_bnode.children:

            if child.btype is Btype.CDT and child.value is td.v_undef:
                val = child.rule.cdt.solver(dictionary)
                if val == child.value:
                    self._tree_skimming(dictionary, child)

            elif child.btype is Btype.CC and child.value is td.v_undef:
                if dictionary[child.query][0] is td.v_undef or dictionary[child.query][2] < child.rule.prio:
                    child.rule.cc.solver(dictionary, child.query, child.rule.prio)
                    if dictionary[child.query][0] == child.value:
                        self._tree_skimming(dictionary, child)


    def _create_bnode(self, dictionary, btype, rule=None, query=None, tree=None):
        """ create a new child node to be attach to the tree """

        ###print("ENTER BNODE", query, rule, btype)

        if not tree:
            child = _BNode(dictionary, btype, rule, query)

            ###print("EXIT BNODE", child.value, child.query, "\n")

            return None, child

        child = _BNode(dictionary, btype, rule, query)
        tree.children.append(child)

        ###print("EXIT BNODE", child.value, child.query, "\n")

        return child, tree


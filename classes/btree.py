import tools.defines as td
from classes.enum import Btype
from error.error import error
from dictionary.fill_dictionary import modify_value_in_dict
from tools.custom_return import enable_ret, cust_ret


class _BNode:
    """ """

    __slots__ = "_needed_rule", "btype", "curr_rule", "expand_fact",\
                "children", "value"

    def __init__(self, dictionary, query, btype=Btype.FACT, rule=None,
                 needed_rule=None):

        if query and rule:
            print("ERROR!!!!!!!!!!! BNODE INIT")

        self._needed_rule = needed_rule
        self.btype = btype
        self.curr_rule = rule
        self.expand_fact = query
        self.children = []

        if self.curr_rule:
            self.value = self.curr_rule.cdt.solver(dictionary)
        else:
            self.value = dictionary[query][0]


class Btree:
    """ """

    __slots__ = "_query", "_root"

    def __init__(self, dictionary, rule_lst, query):
        self._query = query

        # self._rule_lst = rule_lst  # => cf si on la garde en variable

        needed_rule = [rule for rule in rule_lst if query in rule.cc_lst]
        _, self._root = self._create_bnode(dictionary, query,
                                           needed_rule=needed_rule)

    def recu_launcher(self, dictionary, rule_lst):
        """ """

        #print("RECU LAUNCHER START", self._root.expand_fact)
        ret = self._recu(dictionary, rule_lst, curr_bnode=self._root)
        #print("RECU LAUNCHER EXIT", self._root.expand_fact, "\n")
        return ret

    @enable_ret
    def _recu(self, dictionary, rule_lst, curr_bnode):
        """ specify which element is needed in a specific bnode """

        if curr_bnode.btype is Btype.FACT:
            self._node_cc(dictionary, curr_bnode, rule_lst)
            return dictionary[curr_bnode.expand_fact][0]

        return self._node_cdt(dictionary, curr_bnode, rule_lst)



    def _node_cc(self, dictionary, curr_bnode, rule_lst):
        query = curr_bnode.expand_fact
        val = dictionary[query][0]

        if val is not td.v_true and val is not td.v_bugged and dictionary[query][2] <= 0:

            needed_rule = dict((rule, -1) for rule in rule_lst if
                          query in rule.cc_lst)

            for rule in needed_rule:

               child_node, curr_bnode = \
                   self._create_bnode(dictionary,
                                      rule=rule,
                                      tree=curr_bnode,
                                      btype=Btype.EXPR)

               ret_recu = self._recu(dictionary, rule_lst, child_node)
               needed_rule[rule] = ret_recu

            for rule in needed_rule:
               if needed_rule[rule] is td.v_true:
                   ret_solv = rule.cc.solver(dictionary, query, rule.prio)


    def _node_cdt(self, dictionary, curr_bnode, rule_lst):

        val = curr_bnode.value

        if val is td.v_undef:

           for fact in curr_bnode.curr_rule.cdt_lst:
               if dictionary[fact][2] <= 0:
                   child_node, curr_bnode = \
                       self._create_bnode(dictionary,
                                          fact,
                                          tree=curr_bnode,
                                          btype=Btype.FACT)

                   ret_cdt = self._recu(dictionary, rule_lst, child_node)

           return curr_bnode.curr_rule.cdt.solver(dictionary)

        return val


    def _create_bnode(self, dictionary, query=None, rule=None, needed_rule=None,
                      tree=None, btype=Btype.FACT):
        """ create a new child node to be attach to the tree """

        #print("ENTER BNODE", query, rule, btype)

        if not tree:
            child = _BNode(dictionary, query, btype, rule=rule,
                           needed_rule=needed_rule)

            #print("EXIT BNODE", child.value, child.expand_fact, "\n")

            return None, child

        child = _BNode(dictionary, query, btype, rule=rule,
                       needed_rule=needed_rule)
        tree.children.append(child)

        #print("EXIT BNODE", child.value, child.expand_fact, "\n")

        return child, tree


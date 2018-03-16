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

        print("RECU LAUNCHER START", self._root.expand_fact)
        ret = self._recu(dictionary, rule_lst, curr_bnode=self._root)
        print("RECU LAUNCHER EXIT", self._root.expand_fact, "\n")
        return ret

    @enable_ret
    def _recu(self, dictionary, rule_lst, curr_bnode):
        """ specify which element is needed in a specific bnode """


        print("\t\tRECU", curr_bnode.expand_fact, curr_bnode.curr_rule.expr if curr_bnode.curr_rule else None)

        ret, value, true_lst = [], [], []

        query = curr_bnode.expand_fact if curr_bnode.btype is Btype.FACT \
            else curr_bnode.curr_rule

        # ------------------------------------------------------------------------------------------------------------------------------------
        # si on resoud sur une cc
        if curr_bnode.btype is Btype.FACT:

            val = dictionary[query][0]

            print("RECU IF", val, query)

            if val is not td.v_true and val is not td.v_bugged and dictionary[query][2] <= 0:

                needed_rule = [rule for rule in rule_lst if
                               query in rule.cc_lst]

                for rule in needed_rule:

                    print("*******BEFORE TYPE SET", rule.cdt_lst)
                    _type = Btype.FACT if len(rule.cdt_lst) == 1 else Btype.EXPR

                    child_query = rule.cdt_lst[0] if _type == Btype.FACT\
                        else None

                    child_node, curr_bnode = \
                        self._create_bnode(dictionary,
                                           child_query,
                                           rule=rule,
                                           tree=curr_bnode,
                                           btype=_type)

                    print("AFTER CREATE BNODE -----------------------", rule.expr)

                    # ****************************************************************************************************************************
                    ret_recu = self._recu(dictionary, rule_lst, child_node)

                    if ret_recu is td.v_true:
                        ret_solv = curr_bnode.curr_rule.cc.solver(dictionary)
                        if ret_recu >= 0:
                            value += dictionary[query][0]

                # END FOR
                print("---- END FOR IF", ret)

        # ------------------------------------------------------------------------------------------------------------------------------------
        # si on resoud sur une cdt
        else:  # if curr_bnode.btype is Btype.EXPR
            print("RECU ELSE")

            val = query.value

            if val is td.v_undef:

                for fact in curr_bnode.curr_rule.cdt_lst:
                    if dictionary[fact][2] <= 0:
                        child_node, curr_bnode = \
                            self._create_bnode(dictionary,
                                               fact,
                                               tree=curr_bnode,
                                               btype=Btype.FACT)

                    # ****************************************************************************************************************************

                        ret_cdt = self._recu(dictionary, rule_lst, child_node)
                        if ret_cdt is td.v_true:
                            true_lst += child_node.curr_expr

                        print("RECU TOTO ELSE", query, ret, child_node.expand_fact, child_node.btype)

                for expr in true_lst:
                    expr.cc.solver(dictionary, curr_bnode.expand_fact, expr.prio)

                # END FOR
                print("END FOR ELSE", ret)

            else:
                return val

        return dictionary[curr_bnode.expand_fact][0]


    def _create_bnode(self, dictionary, query, rule=None, needed_rule=None,
                      tree=None, btype=Btype.FACT):
        """ create a new child node to be attach to the tree """

        print("ENTER BNODE", query, rule, btype)

        if not tree:
            child = _BNode(dictionary, query, btype, rule=rule,
                           needed_rule=needed_rule)

            print("EXIT BNODE", child.value, child.expand_fact, "\n")

            return None, child

        child = _BNode(dictionary, query, btype, rule=rule,
                       needed_rule=needed_rule)
        tree.children.append(child)

        print("EXIT BNODE", child.value, child.expand_fact, "\n")

        return child, tree

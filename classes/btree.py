import tools.defines as td
from classes.enum import Btype
from classes.condition import Condition

class _BNode:
    """ """

    #__slots__ = "children", "value", "curr_rule", "_curr_rule", "expand_fact", "_needed_rule", "bytpe"


    def __init__(self, dictionary, query, btype=Btype.FACT, rule=None,
                 needed_rule=None):
        if query and rule:
            print("ERROR!!!!!!!!!!! BNODE INIT")

        self._curr_rule = rule
        self._needed_rule = needed_rule
        self.btype = btype
        self.curr_rule = rule
        self.expand_fact = query
        self.children = []
        if self.curr_rule:
            self.value = self.curr_rule.cdt.slover(dictionary)
        print("BNODE INIT")


class Btree:
    """ """

    __slots__ = "curr_query", "_root", "_query", "_rule_lst"


    def __init__(self, dictionary, rule_lst, query):
        self._query = query
        # self._rule_lst = rule_lst  # => cf si on la garde en variable
        needed_rule = [rule for rule in rule_lst if query in rule.cc_lst]
        _, self._root = self._create_bnode(dictionary, query,
                                        needed_rule=needed_rule)


    def recu_launcher(self, dictionary, expr_lst):
        """ """
        ret = self._recu(dictionary, expr_lst, curr_bnode=self._root)


    def _recu(self, dictionary, expr_lst, curr_bnode):
        """ specify which element is needed in a specific bnode """

        print(curr_bnode.btype)
        query = curr_bnode.expand_fact.cdt if curr_bnode.btype is Btype.FACT \
                                           else curr_bnode.curr_rule
        if curr_bnode.btype is Btype.FACT:
            val = dictionary[query][0]

            if val is not td.v_true and val is not td.v_bugged and \
               dictionary[query][2]:
                needed_rule = [expr for expr in expr_lst if query in expr.cc_lst]
                for expr in needed_rule:
                    _type = Btype.FACT if len(expr.cdt_lst) == 1 else Btype.EXPR
                    query, expr = (expr.cdt_lst[0], None) if _type == Btype.FACT\
                                  else (None, expr)
                    expr_child, curr_bnode = self._create_bnode(dictionary,
                                             query, expr, tree=curr_bnode,
                                             btype=_type)
                    ret = self._recu(dictionary, expr_lst, expr_child)

        else:  # if curr_bnode.btype is Btype.EXPR
            val = query.solver(dictionary)

            if val is not td.v_true and val is not td.v_bugged:

                for fact in curr_bnode.curr_rule.cdt_lst:
                    if dictionary[fact][2] <= 0:
                        expr_child, curr_bnode = self._create_bnode(dictionary,
                                                 fact, tree=curr_bnode,
                                                 btype=Btype.FACT)
                        ret = self._recu(dictionary, expr_lst, expr_child)

        if val is td.v_bugged:
            return error(-8)

        return val if val is td.v_true else ret


    def _create_bnode(self, dictionary, query, expr=None, rule=None,
                      needed_rule=None, tree=None, btype=Btype.FACT):
        """ create a new child node to be attach to the tree """

        print("ENTER BNODE", query, expr, btype)
        if not tree:
            return None, _BNode(dictionary, query=query, expr=expr, rule=rule,
                                needed_rule=needed_rule)

        child = _BNode(dictionary, query=query, expr=expr, rule=rule,
                       needed_rule=needed_rule)
        tree.children.append(child)

        print("EXIT BNODE", child.value, child.expand_fact)

        return child, tree


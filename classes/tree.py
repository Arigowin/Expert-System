from tools.defines import *
from rule import Rule


class Node:


    def __init__(self, fact=None, value=Indet, neg=0, operator=None):

        self.fact = fact
        self.value = value

        self.neg = neg
        self.operator = operator

        self.right = None
        self.left = None



class Tree:


    def __init__(self, query):

        self.rule = Rule.polish
        _, _, operator = self._polish_rule_handler()
        self.tree = Node(index=0, fact=query, operator=operator)
        default = 'a'


    def insert(self, value=Indet):
        """ insert a new object 'Node' on the left then on right of our tree """

        fact, neg, operator = self._polish_rule_handler()

        if self.right is None:
            self.right = Node(fact=fact, value=value, neg=neg, operator=operator)
            if fact is None:
                self.insert()
            else:
                return

        if self.left is None:
            self.left = Node(fact=fact, value=value, neg=neg, operator=operator)
            if fact is None:
                self.insert()
            else:
                return


    def _polish_rule_handler(self):
        """ fonction to get the first element of the polish rule string
            remove it from the string and return it """

        index = 0 if self.rule[0] not '!' else 1
        neg = 0 if self.rule[0] not '!' else 1

        current = self.rule[index]
        self.rule = self.rule[index + 1:]

        fact = current if current.isupper() else None
        operator = None if current.isupper() else current

        return fact, neg, operator





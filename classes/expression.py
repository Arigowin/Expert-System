import tools.defines as td
from classes.rule import Rule

class Expression:
    """

    Variables:
        line: extracted expression from file
        rules: list of Rule extracted from line

    Function:
        _split_line(self, line)
        _create_rule_list(self, line, dictionary)
        _handle_iif(self, split_line)
    """


    def __init__(self, line, dictionary):

        self.line = line
        self._create_rule_list(line, dictionary)
        self.usable = True


    def solver(self, dictionary, query):
        """ """

        ret = td.Error
        for rule in self.rules:
            ret = rule.solver(dictionary, query)
            if ret is td.v_false:
                lst = [elt for elt in self.cdt if elt.isupper()
                       and dictionary[elt][2] is td.m_default]
                if len(lst) == 0:
                    self.usable = False

        return ret


    def _split_line(self, line):
        """ split the expression in 3 part: condition, symbol, conclusion """

        if '=' in line:
            i = line.index('=')

            symb_beg = i - 1 if i and line[i - 1] and line[i - 1] is '<' else i

            if line[i + 1] and line[i + 2]:
                symb_end = i + 2
            else:
                sys.exit()

            self.symb = line[symb_beg:symb_end]
            self.cdt = line[:symb_beg]
            self.cc = line[symb_end:]

        else:
            self.cdt = line
            self.symb = None
            self.cc = None


    def _create_rule_list(self, line, dictionary):
        """  """

        self._split_line(line)
        split_line = [self.cdt, self.symb, self.cc]

        if '<' in split_line[1]:
            self._handle_iif(split_line, dictionary)
        else:
            self.rules = [Rule(split_line, dictionary)]

        if td.Error in self.rules:
            sys.exit()


    def _handle_iif(self, split_line, dictionary):
        """  """

        symb = "=>"

        not_cdt = "!(%s)" % self.cdt
        not_cc = "!(%s)" % self.cc

        self.rules = []
        self.rules.append(Rule([self.cdt, symb, self.cc], dictionary))
        self.rules.append(Rule([not_cdt, symb, not_cc], dictionary))
        self.rules.append(Rule([self.cc, symb, self.cdt], dictionary))
        self.rules.append(Rule([not_cc, symb, not_cdt], dictionary))

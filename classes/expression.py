import tools.defines as td
from classes.rule import Rule

class Expression:
    """

    Variables:
        line: extracted expression from file
        rules: list of Rule extracted from line

    Function:
        _split_line(self, line)
        _toto(self, line)
        _handle_iif(self, split_line)
    """


    def __init__(self, line):

        print("\n[%s]" % line)

        self.line = line
        self._toto(line)


    def _split_line(self, line):
        """ split the expression in 3 part: condition, symbol, conclusion """

        if '=' in line:
            i = line.index('=')

            symb_beg = i - 1 if i and line[i - 1] and line[i - 1] is '<' else i

            if line[i + 1] and line[i + 2]:
                symb_end = i + 2
            else:
                print("the rule '%s' is not well formated." % line)
                sys.exit()

            symb = line[symb_beg:symb_end]
            cdt = line[:symb_beg]
            cc = line[symb_end:]

        else:
            cdt = line
            symb = None
            cc = None

        return [cdt, symb, cc]


    def _toto(self, line):
        """  """

        split_line = self._split_line(line)

        if '<' in split_line[1]:
            self._handle_iif(split_line)
        else:
            self.rules = [Rule(split_line)]

        if td.Error in self.rules:
            print("the rule '%s' is not well formated." % line)
            sys.exit()


    def _handle_iif(self, split_line):
        """  """

        symb = "=>"

        cdt = split_line[0]
        cc = split_line[2]

        not_cdt = "!(%s)" % split_line[0]
        not_cc = "!(%s)" % split_line[2]

        self.rules = []
        self.rules.append(Rule([cdt, symb, cc]))
        self.rules.append(Rule([not_cdt, symb, not_cc]))
        self.rules.append(Rule([cc, symb, cdt]))
        self.rules.append(Rule([not_cc, symb, not_cdt]))

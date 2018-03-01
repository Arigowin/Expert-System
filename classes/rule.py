import re
import sys
#  cdt = re.search()
#       symb = re.search(v'^<?=>$', self.symb)
class Rule:

    def __init__(self, line):
        self.__split_line(line)
        self.__check_syntax(line)

    def __split_line(self, line):

        if '=' in line:
            index = line.index('=')

            symb_beg = index - 1 if index and line[index - 1] and line[index - 1] is '<' else index

            if line[index + 1] and line[index + 2]:
                symb_end = index + 2 # indexes are` included at begining and excluded at end
            else:
                print("the rule '%s' is not well formated." % line)
                sys.exit()

            self.symb = line[symb_beg:symb_end]
            self.cdt = line[:symb_beg]
            self.cc = line[symb_end:]

        else:
            self.cdt = line
            self.symb = None
            self.cc = None


    def __check_syntax(self, line):
        self.__check_regex('^<?=>$', self.symb, line)
        self.__check_cond_recu('^!?[A-Z]([+\|\^]!?[A-Z])*$', self.cdt, line, line)
        self.__check_cond_recu('^!?[A-Z]([+\|\^]!?[A-Z])*$', self.cc, line, line)


    def __check_regex(self, regex, str, line):
        print "in check regex", str
        cdt = re.search(regex, str)
        if not cdt:
            print("the rule '%s' is not well formated." % line)
            sys.exit()


    def __check_cond_recu(self, regex, str, modif_line, line):
        print  "IN REC", str

        if '(' in str:
            open_parent = str.find('(')
            close_parent = str.rfind(')')

            if not close_parent:
                print("the rule '%s' is not well formated." % line)
                sys.exit()

            self.__check_cond_recu(regex, str[open_parent + 1:close_parent], modif_line, line)
            str = str[:open_parent] + 'Z' + str[close_parent + 1:]
            print "after modif, line (%s)" % str

        self.__check_regex(regex, str, line)





#abc = Rule("(A+(D|N)^!P+)|F=>W")

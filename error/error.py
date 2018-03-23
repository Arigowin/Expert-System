import sys


def error_tbl(code, msg=""):
    """ set an error table to be called by the error handler to get the correct
    error messages and return

    In the following table:
        key: error code
        value[0]: error message
        value[1]: exit boolean

    """

    error_tbl = {# rule inconstitiency but priority say we modify
                 3: ["Try to modify value set in dico but prio say it's oki => modif", False],  # prio dico < prio current

                 # rule inconstitiency and priority say we can't modify
                 4: ["Try to modify value set in dico, but OK => not modif%s", False],  # prio dico > prio current

                 # rule inconsistiency and prio can't decied wich is true => BUGGED
                 5: ["Cannot modify value with same priority %s", False],  # prio dico == prio current

                 # endless loop between the rules
                 6: ["Problem of consistency between the rules %s", False],


                 1: ["Input file not well formatted %s", True],
                 8: ["trucmuche bugge", True],
                 7: ["Notre machin il est tout casse.... :( %s", False]}

    return error_tbl[code]


def error(code, msg=""):
    """ display error message, return specific error code and exit if needed """

    err_lst = error_tbl(abs(code), msg)

    print("EXPERT SYSTEM - %d - Error: %s" % (abs(code), err_lst[0]))

    if err_lst[1]:
        sys.exit(abs(code))

    return code


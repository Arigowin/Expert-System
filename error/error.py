import sys

def error_tbl(code, msg=""):
    """ set an error table to be called by the error handler to get the correct
    error messages and return

    In the folowing table:
        key: error code
        value[0]: error message
        value[1]: exit boolean
    """

    error_tbl = {2: ["Cannot modify value already set %s" % msg, False],
                 3: ["Cannot modify value with lower priority %s" % msg, False], # prio dico < prio current
                 4: ["Cannot modify value with highter priority %s" % msg, False], # prio dico > prio current
                 5: ["Cannot modify value with same priority %s" % msg, False], # prio dico == prio current
                 6: ["Problem of constitiency in the rules %s" % msg, False],
                 1: ["Input file not well formated %s" % msg, True],
                 7: ["Notre machin il est tout casse.... :( %s" % msg, False]}

    return error_tbl[code]


def error(code, msg=""):
    """ display error message, return specific error code and exit if needed """

    err_lst = error_tbl(abs(code), msg)

    print(err_lst[0])

    if err_lst[1]:
        sys.exit(abs(code))

    return code


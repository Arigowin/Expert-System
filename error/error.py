import sys


def error_tbl(code, msg=""):
    """ set an error table to be called by the error handler to get the correct
    error messages and return

    In the following table:
        key: error code
        value[0]: error message
        value[1]: exit boolean

    """

    error_tbl = {
        2: ["Problem of consistency between the rules%s" % msg, False],
        1: ["Input file not well formatted%s" % msg, True],
    }

    return error_tbl[code]


def error(code, msg=""):
    """ display error message, return specific error code and exit if needed
    """

    err_lst = error_tbl(abs(code), msg)

    print("\nEXPERT SYSTEM - Error: %s\n" % err_lst[0], file=sys.stderr)

    if err_lst[1]:
        sys.exit(abs(code))

    return code

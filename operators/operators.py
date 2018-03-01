Inde = -1


def logic_not(val):

    return not val


def logic_and(val_1, val_2):

    if val_1 is True and val_2 is True:
        return True

    return False


def logic_or(val_1, val_2):

    if val_1 is True or val_2 is True:
        return True

    return False


def logic_xor(val_1, val_2):

    if val_1 is True and val_2 is False:
        return True

    if val_1 is False and val_2 is True:
        return True

    return False


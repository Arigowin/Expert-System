from tools.functions import get_first_index


def test(rpolish_cpy):
    op, index = [], 0

    for i, elt in enumerate(rpolish_cpy):

        print("FOR", op, elt)
        while op and op[-1] == 0:
            op.remove(op[-1])
            op[-1] -= 1
        print("WHILE", op, elt)

        if elt in "^|+":
            op.append(2)
        elif elt is '!':
            op.append(1)
        else:
       # if elt.isupper():
            op[-1] -= 1

        print("SUM", sum(op), op)
        if sum(op) == 0:
            index = i
        print("END FOR", op, elt)

    print("after FOR", op, index, op)
    #if op == [1, 0]:
    if len(op) > 1 and sum(op) / (len(op) - 1) == 1:
        index = get_first_index("^|+!", rpolish_cpy, op.count(1), False)
        print("TOTO")

    print("END", index)
    return ([rpolish_cpy[0], rpolish_cpy[1:]] if rpolish_cpy[0] == '!'
            else [rpolish_cpy[0], rpolish_cpy[1:index], rpolish_cpy[index:]])

if __name__ == '__main__':
    a = test("+P^Q!P")
    print(a)

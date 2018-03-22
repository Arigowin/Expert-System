
def test(string):
    lst = []
    op = []

    lst.append(string[0])  # add ^

    for i, elt in enumerate(string):

        if op and op[-1] == 0:
            op.remove(op[-1])
            op[-1] -= 1

        if elt in "^|+":
            op.append(2)
        if elt is '!':
            op.append(1)

        if elt.isupper():
            op[-1] -= 1

        print("op", op)

    return lst

if __name__ == '__main__':
    print(test("^|!U+TSR"))

import sys
from subprocess import Popen, PIPE

print("\n", __file__)
arg = sys.argv
i = 1

if (len(arg) > 1):
    i = int(arg[1])

for i in range(i):
    process = Popen(["python3", "main.py", "tests/thomas/testBasiquesReverse.txt"], stdout=PIPE)

    (ret, err) = process.communicate()

    exit_code = process.wait()

    if str(ret).find("[A:[1, ") == -1:
        print("Diff on A")
        b = True
    if str(ret).find("[B:[1, ") == -1:
        print("Diff on B")
        b = True
    if str(ret).find("[C:[1, ") == -1:
        print("Diff on C")
        b = True
    if str(ret).find("[D:[2, ") == -1:
        print("Diff on D")
        b = True
    if str(ret).find("[E:[2, ") == -1:
        print("Diff on E")
        b = True
    if str(ret).find("[F:[0, ") == -1:
        print("Diff on F")
        b = True
    if str(ret).find("[G:[0, ") == -1:
        print("Diff on G")
        b = True
    if str(ret).find("[H:[2, ") == -1:
        print("Diff on H")
        b = True
    if str(ret).find("[I:[1, ") == -1:
        print("Diff on I")
        b = True
    if str(ret).find("[J:[1, ") == -1:
        print("Diff on J")
        b = True
    if str(ret).find("[K:[0, ") == -1:
        print("Diff on K")
        b = True
    if str(ret).find("[L:[1, ") == -1:
        print("Diff on L")
        b = True
    if str(ret).find("[M:[0, ") == -1:
        print("Diff on M")
        b = True
    if str(ret).find("[N:[0, ") == -1:
        print("Diff on N")
        b = True
    if str(ret).find("[O:[1, ") == -1:
        print("Diff on O")
        b = True
    if str(ret).find("[P:[1, ") == -1:
        print("Diff on P")
        b = True
    if str(ret).find("[Q:[1, ") == -1:
        print("Diff on Q")
        b = True
    if str(ret).find("[R:[1, ") == -1:
        print("Diff on R")
        b = True
    if str(ret).find("[S:[2, ") == -1:
        print("Diff on S")
        b = True
    if str(ret).find("[T:[2, ") == -1:
        print("Diff on T")
        b = True
    if str(ret).find("[U:[1, ") == -1:
        print("Diff on U")
        b = True
    if str(ret).find("[V:[0, ") == -1:
        print("Diff on V")
        b = True
    if str(ret).find("[W:[0, ") == -1:
        print("Diff on W")
        b = True
    if str(ret).find("[X:[0, ") == -1:
        print("Diff on X")
        b = True
    if str(ret).find("[Y:[0, ") == -1:
        print("Diff on Y")
        b = True
    if str(ret).find("[Z:[0, ") == -1:
        print("Diff on Z")
        b = True

    if b is True:
        print(ret)
        break

    print("%d " % (i + 1), end='', flush=True)

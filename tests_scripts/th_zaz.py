import sys
from subprocess import Popen, PIPE

print("\n", __file__)
arg = sys.argv
i = 1

if (len(arg) > 1):
    i = int(arg[1])

tmp = {'A': "[A:[1,",
       'B': "[B:[1,",
       'C': "[C:[1,",
       'D': "[D:[1,",
       'E': "[E:[0,",
       'F': "[F:[0,",
       'G': "[G:[1,",
       'H': "[H:[0,",
       'I': "[I:[0,",
       'J': "[J:[0,",
       'K': "[K:[0,",
       'L': "[L:[0,",
       'M': "[M:[0,",
       'N': "[N:[0,",
       'O': "[O:[1,",
       'P': "[P:[2,",
       'Q': "[Q:[0,",
       'R': "[R:[0,",
       'S': "[S:[0,",
       'T': "[T:[0,",
       'U': "[U:[0,",
       'V': "[V:[0,",
       'W': "[W:[0,",
       'X': "[X:[1,",
       'Y': "[Y:[0,",
       'Z': "[Z:[0,"}

for i in range(i):
    process = Popen(["python3", "main.py", "tests/thomas/testZaz.txt"], stdout=PIPE)

    (ret, err) = process.communicate()

    exit_code = process.wait()

    b = False
    for k in tmp:
        if str(ret).find(tmp[k]) == -1:
            print("Diff on", k)
            b = True

    if b is True:
        print(ret)
        break

    print("%d " % (i + 1), end='', flush=True)
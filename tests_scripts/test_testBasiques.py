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
       'D': "[D:[2,",
       'E': "[E:[2,",
       'F': "[F:[0,",
       'G': "[G:[0,",
       'H': "[H:[2,",
       'I': "[I:[1,",
       'J': "[J:[1,",
       'K': "[K:[0,",
       'L': "[L:[1,",
       'M': "[M:[0,",
       'N': "[N:[0,",
       'O': "[O:[1,",
       'P': "[P:[1,",
       'Q': "[Q:[1,",
       'R': "[R:[1,",
       'S': "[S:[2,",
       'T': "[T:[2,",
       'U': "[U:[1,",
       'V': "[V:[0,",
       'W': "[W:[0,",
       'X': "[X:[0,",
       'Y': "[Y:[0,",
       'Z': "[Z:[0,"}

for i in range(i):
    process = Popen(["python3", "main.py", "tests/thomas/testBasiques.txt"], stdout=PIPE)

    (ret, err) = process.communicate()

    exit_code = process.wait()

    b = False
    for k, v in enumerate(tmp):
        if str(ret).find(v) == -1:
            print("Diff on", k)
            b = True

    if b is True:
        print(ret)
        break

    print("%d " % (i + 1), end='', flush=True)

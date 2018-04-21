import sys
from subprocess import Popen, PIPE

print("\n", __file__)
arg = sys.argv
i = 1

if (len(arg) > 1):
    i = int(arg[1])

tmp = {'A': "[A:[1,",
       'B': "[B:[0,",
       'C': "[C:[0,",
       'D': "[D:[1,",
       'E': "[E:[2,",
       'F': "[F:[2,",
       'G': "[G:[1,",
       'H': "[H:[1,",
       'I': "[I:[1,",
       'J': "[J:[1,",
       'K': "[K:[2,",
       'L': "[L:[2,",
       'M': "[M:[1,",
       'N': "[N:[0,",
       'O': "[O:[1,",
       'P': "[P:[1,",
       'Q': "[Q:[0,",
       'R': "[R:[0,",
       'S': "[S:[0,",
       'T': "[T:[0,",
       'U': "[U:[0,",
       'V': "[V:[0,",
       'W': "[W:[0,",
       'X': "[X:[0,",
       'Y': "[Y:[0,",
       'Z': "[Z:[0,"}

for i in range(i):
    process = Popen(["python3", "main.py", "tests/thomas/trucmalfait.txt"], stdout=PIPE)

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
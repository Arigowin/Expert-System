import sys
from subprocess import Popen, PIPE

print("\n", __file__)
arg = sys.argv
i = 1

if (len(arg) > 1):
    i = int(arg[1])

tmp = {'A': "A : True",
       'B': "B : True",
       'C': "C : True",
       'D': "D : Undefined",
       'E': "E : Undefined",
       'F': "F : False",
       'G': "G : False",
       'H': "H : Undefined",
       'I': "I : True",
       'J': "J : True",
       'K': "K : False",
       'L': "L : True",
       'M': "M : False",
       'N': "N : False",
       'O': "O : True",
       'P': "P : True",
       'Q': "Q : True",
       'R': "R : True",
       'S': "S : Undefined",
       'T': "T : Undefined",
       'U': "U : True",
       'V': "V : False",
       'W': "W : False",
       'X': "X : False",
       'Y': "Y : False",
       'Z': "Z : False"}

for i in range(i):
    process = Popen(["python3", "expert_system.py", "-cdv", "tests/thomas/testBasiquesReverse.txt"], stdout=PIPE)

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

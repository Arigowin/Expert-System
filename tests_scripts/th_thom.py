import sys
from subprocess import Popen, PIPE

print("\n", __file__)
arg = sys.argv
i = 1

if (len(arg) > 1):
    i = int(arg[1])

tmp = {'A': "A : True",
       'B': "B : False",
       'C': "C : True",
       'D': "D : False",
       'E': "E : False",
       'F': "F : False",
       'G': "G : True",
       'H': "H : False",
       'I': "I : False",
       'J': "J : False",
       'K': "K : False",
       'L': "L : False",
       'M': "M : False",
       'N': "N : False",
       'O': "O : False",
       'P': "P : False",
       'Q': "Q : False",
       'R': "R : False",
       'S': "S : False",
       'T': "T : False",
       'U': "U : False",
       'V': "V : False",
       'W': "W : False",
       'X': "X : False",
       'Y': "Y : False",
       'Z': "Z : False"}

for i in range(i):
    process = Popen(["python3", "expert_system.py", "-cdv", "tests/thomas/testThom.txt"], stdout=PIPE)

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

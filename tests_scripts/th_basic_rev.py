import os
from subprocess import Popen, PIPE

print("\n", __file__)
for i in range(100):
    process = Popen(["python3", "main.py", "tests/thomas/testBasiques.txt"], stdout=PIPE)
    (ret, err) = process.communicate()
    exit_code = process.wait()
    if (str(ret).find("[A:[1, 2, ") == -1 or
        str(ret).find("[B:[1, 2, ") == -1 or
        str(ret).find("[C:[1, 2, ") == -1 or
        str(ret).find("[D:[2, 2, ") == -1 or
        str(ret).find("[E:[2, 2, ") == -1 or
        str(ret).find("[F:[0, 2, ") == -1 or
        str(ret).find("[G:[0, 2, ") == -1 or
        str(ret).find("[H:[2, 2, ") == -1 or
        str(ret).find("[I:[1, 2, ") == -1 or
        str(ret).find("[J:[1, 2, ") == -1 or
        str(ret).find("[K:[0, 2, ") == -1 or
        str(ret).find("[L:[1, 2, ") == -1 or
        str(ret).find("[M:[0, 2, ") == -1 or
        str(ret).find("[N:[0, 2, ") == -1 or
        str(ret).find("[O:[1, 2, ") == -1 or
        str(ret).find("[P:[1, 2, ") == -1 or
        str(ret).find("[Q:[1, 2, ") == -1 or
        str(ret).find("[R:[1, 2, ") == -1 or
        str(ret).find("[S:[0, 2, ") == -1 or
        str(ret).find("[T:[0, 2, ") == -1 or
        str(ret).find("[U:[0, 2, ") == -1 or
        str(ret).find("[V:[0, 2, ") == -1 or
        str(ret).find("[W:[0, 2, ") == -1 or
        str(ret).find("[X:[0, 2, ") == -1 or
        str(ret).find("[Y:[0, 2, ") == -1 or
        str(ret).find("[Z:[0, 2, ") == -1):
        print("ET NOP!")
        print(ret)
        break
    print("%d " % i, end='')



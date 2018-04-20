import os
print("\n", __file__)
from subprocess import Popen, PIPE


for i in range(100):
    process = Popen(["python3", "main.py", "tests/ex/ex1.es"], stdout=PIPE)
    (ret, err) = process.communicate()
    exit_code = process.wait()
    if (str(ret).find("[A:[1, ") == -1 or
        str(ret).find("[B:[1, ") == -1 or
        str(ret).find("[C:[0, ") == -1 or
        str(ret).find("[D:[1, ") == -1 or
        str(ret).find("[E:[1, ") == -1 or
        str(ret).find("[F:[1, ") == -1 or
        str(ret).find("[G:[1, ") == -1 or
        str(ret).find("[H:[1, ") == -1 or
        str(ret).find("[I:[1, ") == -1 or
        str(ret).find("[J:[1, ") == -1 or
        str(ret).find("[K:[1, ") == -1 or
        str(ret).find("[L:[1, ") == -1 or
        str(ret).find("[M:[1, ") == -1 or
        str(ret).find("[N:[1, ") == -1 or
        str(ret).find("[O:[1, ") == -1 or
        str(ret).find("[P:[1, ") == -1 or
        str(ret).find("[Q:[0, ") == -1 or
        str(ret).find("[R:[0, ") == -1 or
        str(ret).find("[S:[0, ") == -1 or
        str(ret).find("[T:[0, ") == -1 or
        str(ret).find("[U:[0, ") == -1 or
        str(ret).find("[V:[0, ") == -1 or
        str(ret).find("[W:[0, ") == -1 or
        str(ret).find("[X:[0, ") == -1 or
        str(ret).find("[Y:[0, ") == -1 or
        str(ret).find("[Z:[0, ") == -1):
        print("ET NOP!")
        print(ret)
        break
    print("%d " % i, end='')



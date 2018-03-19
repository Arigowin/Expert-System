import os
from subprocess import Popen, PIPE


for i in range(1000):
    process = Popen(["python3", "main.py", "tests/example_input.txt"], stdout=PIPE)
    (ret, err) = process.communicate()
    exit_code = process.wait()
    if (str(ret).find("[A:[1, ") == -1 or
        str(ret).find("[B:[1, ") == -1 or
        str(ret).find("[C:[1, ") == -1 or
        str(ret).find("[D:[1, ") == -1 or
        str(ret).find("[E:[1, ") == -1 or
        str(ret).find("[G:[1, ") == -1 or
        str(ret).find("[H:[1, ") == -1 or
        str(ret).find("[Y:[1, ") == -1 or
        str(ret).find("[Z:[1, ") == -1 or
        str(ret).find("[X:[2, ") == -1 or
        str(ret).find("[V:[2, ") == -1):
        print("ET NOP!")
        print(ret)
        break
    print(i)


from solver.main_solver import main_loop
from input_file.input import main_input
from tools.functions import print_dict

dictionary, rules = main_input()
main_loop(rules, dictionary)

print_dict(dictionary)
#print("OK END!")


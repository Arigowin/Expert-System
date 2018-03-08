from solver.main_solver import main_loop
from input_file.input import main_input

dictionary, rules = main_input()
main_loop(rules, dictionary)


#!../venv/bin/python

from enum import Enum
import os
from unittest import result
import minizinc
import utils
from matplotlib import pyplot as plt
import sys
import getopt

SOLVER = "chuffed"
INSTANCE_NUMBER = 12

class Solver(Enum):
    CHUFFED = "chuffed"
    GECODE = "gecode"


def solve(solver_type: Solver = Solver.CHUFFED, instance_number: int = 1, model_path: str = 'VLSIdesign.mzn', visualize: bool = False, intermediate_solutions: bool = False) -> minizinc.Result:
    # Create a MiniZinc model
    model = minizinc.Model()

    # Load the model from a file
    with open(model_path, 'r') as f:
        model.add_string(f.read())

    # Load the data-instance from a file
    dzn_file_path = os.path.join('dzn_instances', f'ins-{instance_number}.dzn')
    full_dzn_file_path = os.path.join(os.getcwd(), dzn_file_path)
    with open(full_dzn_file_path, 'r') as f:
        model.add_string(f.read())

    # Transform Model into a instance
    solver = minizinc.Solver.lookup(solver_type.value)
    inst = minizinc.Instance(solver, model)

    # Solve the instance
    result = inst.solve(intermediate_solutions=False)
    str_res = str(result).strip().split('\n')
    parsed_res = utils.parse_result(str_res)
    
    if visualize:
        utils.visualize_output(parsed_res)

    return result

def main(argv):
    model = 'VLSIdesign.mzn'
    solver = "chuffed"
    range = "1-5"

    try:
      opts, args = getopt.getopt(argv, "hm:s:r:", ["help", "model=", "solver=", "range="])
    except getopt.GetoptError:
      print('usage: ./minizinc_solver.py -m <model_path> -s <chuffed|gecode> -r <range>')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print('usage: ./minizinc_solver.py -m <model_path> -s <chuffed|gecode> -r <range>')
         sys.exit()
      elif opt in ("-m", "--model"):
         model = arg
      elif opt in ("-s", "--solver"):
         solver = arg
      elif opt in ("-r", "--range"):
        range = arg
    
    print(model, solver, range)

if __name__ == "__main__":
    main(sys.argv[1:])
    # for i in range(1, 10):
    #     output_file = f"./cp_solutions/sol_ins-{i}.txt"
    #     result = solve(instance_number = i, visualize=False)
    #     output = f"{result}\n{result.statistics}"
    #     utils.write_output_to_file(output_file, output)
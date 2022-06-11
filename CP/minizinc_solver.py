#!../venv/bin/python

from enum import Enum
import os
from unittest import result
import minizinc
import utils
from matplotlib import pyplot as plt
import sys
import getopt
import time
import signal

SOLVER = "chuffed"
INSTANCE_NUMBER = 12

class Solver(Enum):
    CHUFFED = "chuffed"
    GECODE = "gecode"

def solve(solver_type: Solver = Solver.CHUFFED, instance_number: int = 1, model_type: str = "VLSIdesign", visualize: bool = False, intermediate_solutions: bool = False) -> minizinc.Result:
    # Model path
    model_path = f'./models/{model_type}.mzn'

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

def parse_args(argv):
    model_type = 'VLSIdesign'
    solver = Solver.CHUFFED
    start = 1
    stop = 40
    output_to_file = True

    try:
      opts, args = getopt.getopt(argv, "hm:s:r:o", ["help", "model=", "solver=", "range=", "output-file"])
    except getopt.GetoptError:
      print('usage: ./minizinc_solver.py -m <model_type> -s <chuffed|gecode> -r <range>')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print('usage: ./minizinc_solver.py -m <model_type> -s <chuffed|gecode> -r <range>')
         sys.exit()
      elif opt in ("-m", "--model"):
         model_type = arg
      elif opt in ("-o", "--output-file"):
         output_to_file = True
      elif opt in ("-s", "--solver"):
        if (arg == "chuffed"):
            solver = Solver.CHUFFED
        elif (arg == "gecode"):
            solver = Solver.GECODE
        else:
            print("Not accepted solver, using default Chuffed")
      elif opt in ("-r", "--range"):
        range_split = arg.split("-")
        try:
            start, stop = int(range_split[0]), int(range_split[1])
        except:
            print("Error parsing range, example usage: ./minizinc_solver.py -r  6-9")
    
    print(f"Solving instances from {start} to {stop}\nUsing solver: {solver.value}\nUsing model: {model_type}\n")
    return model_type, solver, start, stop, output_to_file

def parse_statistics(statistics):
    n_solutions = statistics.get('nSolutions')
    failures = statistics.get('failures')
    time = statistics.get('time')
    solve_time = statistics.get('solveTime')

    stats = [time, solve_time, failures, n_solutions]
    stats = [str(x) for x in stats]
    return " ".join(stats)

def handler(signum, frame):
    raise Exception("end of time")

if __name__ == "__main__":
    model_type, solver, start, stop, output_to_file = parse_args(sys.argv[1:])
    for i in range(start, stop+1):
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(60*5) #5 min timeout
        print("start instance: ", i)
        try:
            result = solve(solver, instance_number = i, model_type=model_type, visualize=False)
            stats = parse_statistics(result.statistics)
            output = f"{result}\n{stats}"

            if (output_to_file):
                output_file = f"./cp_solutions/{model_type}/sol_ins-{i}.txt"
                utils.write_output_to_file(output_file, output)
            else:
                print(output)    
        except Exception:
            if (output_to_file):
                output = 60*5
                output_file = f"./cp_solutions/{model_type}/sol_ins-{i}.txt"
                utils.write_output_to_file(output_file, str(output))
            continue

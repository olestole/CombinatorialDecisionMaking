from enum import Enum
import os
import minizinc
import utils
from matplotlib import pyplot as plt

SOLVER = "chuffed"
INSTANCE_NUMBER = 12

class Solver(Enum):
    CHUFFED = "chuffed"
    GECODE = "gecode"


def solve(solver_type: Solver = Solver.CHUFFED, instance_number: int = 1, model_path: str = 'VLSIdesign.mzn', visualize: bool = False, intermediate_solutions: bool = False) -> None:
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

    print(result.statistics, "\n")
    print(result)

for i in range(1, 9):
    solve(instance_number = i, visualize=True)
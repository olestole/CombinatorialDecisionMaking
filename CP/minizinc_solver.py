from enum import Enum
import os
from unittest import result
import minizinc
import utils
from matplotlib import pyplot as plt

SOLVER = "chuffed"
INSTANCE_NUMBER = 12

class Solver(Enum):
    CHUFFED = "chuffed"
    GECODE = "gecode"

class Model(Enum):
    NORMAL = "VLSIdesign"
    ROTATION = "VLSIdesign_rotation"
    NORMAL_OPTIMIZED = "VLSIdesign_optimized"
    ROTATION_OPTIMIZED = "VLSIdesign_rotation_optimized"

def solve(solver_type: Solver = Solver.CHUFFED, instance_number: int = 1, model_type: Model = Model.NORMAL, visualize: bool = False, intermediate_solutions: bool = False) -> minizinc.Result:
    # Model path
    model_path = f'CP/{model_type.value}.mzn'

    # Create a MiniZinc model
    model = minizinc.Model()

    # Load the model from a file
    with open(model_path, 'r') as f:
        model.add_string(f.read())

    # Load the data-instance from a file
    dzn_file_path = os.path.join('CP/dzn_instances', f'ins-{instance_number}.dzn')
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

for i in range(1, 10):
    model_type = Model.NORMAL
    output_file = f"CP/cp_solutions/{model_type.value}/sol_ins-{i}.txt"
    result = solve(instance_number = i, visualize=False, model_type=model_type)
    output = f"{result}\n{result.statistics}"
    utils.write_output_to_file(output_file, output)
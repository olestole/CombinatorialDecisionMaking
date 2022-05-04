import os
import minizinc
import utils
from matplotlib import pyplot as plt

SOLVER = "chuffed"
INSTANCE_NUMBER = 12

# Create a MiniZinc model
model = minizinc.Model()

# Load the model from a file
model_file_path = 'VLSIdesign.mzn'
with open(model_file_path, 'r') as f:
    model.add_string(f.read())

# Load the data-instance from a file
dzn_file_path = os.path.join('dzn_instances', f'ins-{INSTANCE_NUMBER}.dzn')
full_dzn_file_path = os.path.join(os.getcwd(), dzn_file_path)
with open(full_dzn_file_path, 'r') as f:
    model.add_string(f.read())

# Transform Model into a instance
solver = minizinc.Solver.lookup(SOLVER)
inst = minizinc.Instance(solver, model)

# Solve the instance
result = inst.solve(intermediate_solutions=False)
str_res = str(result).strip().split('\n')
parsed_res = utils.parse_result(str_res)
utils.visualize_output(parsed_res)

print(result.statistics, "\n")
print(result)
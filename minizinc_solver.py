import minizinc
import utils


# Create a MiniZinc model
model = minizinc.Model()
utils.create_model(model)

# Transform Model into a instance
gecode = minizinc.Solver.lookup("gecode")
inst = minizinc.Instance(gecode, model)
inst["w"], inst["n"], inst["dims"] = utils.parse_instance()

# Solve the instance
result = inst.solve(intermediate_solutions=True)
for i in range(len(result)):
    print(result[i])
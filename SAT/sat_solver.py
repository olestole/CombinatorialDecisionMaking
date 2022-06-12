from itertools import combinations, chain
import numpy as np
from z3 import *
import utils
import SAT_constraints
import logging

ALL_SOLUTIONS = False
ROTATION = False
VISUALIZE = True
BREAK_SYMMETRY = True

# Define your preferred logging level
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

WIDTH = 0
HEIGHT = 1

def coherent_cicuits(bool_vars, dims, n, w, upper_bound):
    constraints = []
    for c in range(1, n + 1):
        c_constraints = []
        height = dims[c - 1][HEIGHT]
        width = dims[c - 1][WIDTH]
        for x in range(w - (width - 1)):
            for y in range(upper_bound - (height - 1)):
                temp = [bool_vars[x+i][y+j][c] for i in range(0, width) for j in range(0, height)]
                # temp2 = And([Not(bool_vars[x+i][y+j][c]) for i in range(0, width) for j in range(0, height) if bool_vars[x+i][y+j][c] not in temp])
                # cons = Or(Not(bool_vars[x][y][c]), And(temp))
                # c_constraints.append(And(And(temp), temp2))
                c_constraints.append(And(temp))
        # constraints.append(Or(c_constraints))  
        ex = SAT_constraints.exactly_one_seq(c_constraints, f"Hello_{c}")
        constraints.append(ex)
              
    return And(constraints)

def coherent_cicuits_rotation(bool_vars, dims, n, w, upper_bound):
# Ensures that the circuits are connected
    constraints = []
    for c in range(1, n + 1):
        c_constraints = []
        height = dims[c - 1][HEIGHT]
        width = dims[c - 1][WIDTH]
        if upper_bound < height: 
            logging.info(f"l ({upper_bound}) is less than hight ({height}) of block {c}, so the block {c} must be rotated.")
            # Block is to high for the lower bound. Have to check if it can be rotated.
            if ((upper_bound >= width) and (height <= w)): 
                # Block fits if it is rotated. have to add only rotated posiiton to constraints.
                rotated = [And([bool_vars[x+j][y+i][c] for i in range(width) for j in range(height)]) for x in range(w - (height - 1)) for y in range(upper_bound - (width - 1)) ] 
                ex = SAT_constraints.exactly_one_seq(rotated, f"coherent_{c}")
                constraints.append(ex)
            else: 
                logging.info(f"l ({upper_bound}) is less than hight ({height}) of block {c}, and it's height ({height}) is greater than w ({w}). Block {c} it can not be rotated, and l must increase ")
        else:
            for x in range(w - (width - 1)):
                for y in range(upper_bound - (height - 1)):
                    normal = []
                    rotated = []
                    # Should it be strictly less than or less than and equal here?
                    rotation_possible = ((x+height) < w) and ((y+width) < upper_bound) and (width != height)
                    for i in range(width):
                        for j in range(height):
                            normal.append(bool_vars[x+i][y+j][c])
                            if rotation_possible: 
                                rotated.append(bool_vars[x+j][y+i][c])
                    
                    c_constraints.append(And(normal))
                    if len(rotated)>0:
                        c_constraints.append(And(rotated))
            # constraints.append(Or(c_constraints))  
            ex = SAT_constraints.exactly_one_seq(c_constraints, f"coherent_{c}")
            constraints.append(ex)
              
    return And(constraints)

def create_contraints(w, n, dims, upper_bound, rotation):
    s = Solver()
    s.set("timeout", 25 * 1000) # If the solver takes longer than 20 seconds, to try next lower bound.

    # Model the problem
    v = [[[Bool(f"v_{x}_{y}_{c}") for c in range(0, n + 1)] for y in range(upper_bound)] for x in range(w)]
    
    # At most one circuit in each grid cell
    for x in range(w):
        for y in range(upper_bound):
            predicate = v[x][y]
            s.add(SAT_constraints.at_most_one_seq(predicate, f"valid_cell_{x}_{y}"))    
    
    # Ensure the right amount of empty cells -> Ensures that each circuit don't expand more than their dimension
    total_white_cells = (upper_bound * w) - sum(dims[:, WIDTH] * dims[:, HEIGHT])
    if total_white_cells > 0:
        predicate = [v[x][y][0] for x in range(w) for y in range(upper_bound)]
        s.add(SAT_constraints.exactly_k_seq(predicate, total_white_cells, f"white_cells_{x}_{y}_{0}"))
    if rotation:
        s.add(coherent_cicuits_rotation(v, dims, n, w, upper_bound))
    else:
        s.add(coherent_cicuits(v, dims, n, w, upper_bound))
    
    return s, v

def compute_lb(w, dims, roation):
    n_rows = math.ceil(sum(dims[:, WIDTH]) / w)
    sorted_heights = sorted(dims[:, HEIGHT])
    lb = np.sum(sorted_heights[:n_rows])
    if roation:
        l = lb
    else:
        l = lb if lb >= max(dims[:, HEIGHT]) else max(dims[:, HEIGHT])
    
    return l

def compute_solution(model: ModelRef, v, w, n, l):
    sol = []

    for x in range(w):
        sol.append([])
        for y in range(l):
            found_circuit = False
            for c in range(1, n + 1):
                if model.evaluate(v[x][y][c]):
                    found_circuit = True
                    sol[x].append(c)
            if not found_circuit:
                sol[x].append(0)
    return sol

def all_smt(s, initial_terms, l, w, n, break_symmetry):
    # https://stackoverflow.com/questions/11867611/z3py-checking-all-solutions-for-equation/70656700#70656700
    logging.info(f"Looking for all solutions for l= {l}") 
    numb_solutions = 1
    def all_smt_rec(terms, l, numb_solutions, w, n, break_symmetry):    
        if sat == s.check():
            # logging.info(f"Have found {numb_solutions} solution(s) for l= {l}") 
            numb_solutions += 1
            m = s.model()
            yield m
            const = [] 
            for term in terms:
                if m.eval(term, model_completion=True):
                    const.append(Not(term))
                    #term_splitted = term.split("_")
                    #term_if_flipped_over_vertical_axis = f"v_{w-int(term_splitted[1])}_{term_splitted[2]}_{term_splitted[2]}"
                    #s.add()
                else:
                    const.append(term)
            s.add(Or(const))


            if break_symmetry:
                # No symmetry over vertical axis:
                symmetry_x_cons = []
                for i in range(l*(n+1)): # All terms with x=0 
                    opposite_term = terms[-l*(n+1)+i] # Term on opposite side of vertical axis
                    if m.eval(terms[i], model_completion=True):
                        symmetry_x_cons.append(opposite_term)
                    else:
                        symmetry_x_cons.append(Not(opposite_term))
                    if m.eval(opposite_term, model_completion=True):
                        symmetry_x_cons.append(terms[i])
                    else:
                        symmetry_x_cons.append(Not(terms[i]))
                    
                equal_circuits_on_max_x = And(symmetry_x_cons)
                s.add(Not(equal_circuits_on_max_x))


                # No symmetry over horizontal axis:
                symmetry_y_cons = []
                all_term_w_x_zero = [terms[i:i+n+1] for i in range(0, len(terms), l*(n+1))]
                all_term_w_x_zero = np.array(all_term_w_x_zero).flatten()

                all_term_w_x_l = [terms[i:i+n+1] for i in range(((l-1)*(n+1)), len(terms), l*(n+1))]
                all_term_w_x_l = np.array(all_term_w_x_l).flatten()

                for i in range(len(all_term_w_x_zero)): # All terms with x=0 
                    opposite_term = all_term_w_x_l[i] # Term on opposite side of vertical axis
                    if m.eval(all_term_w_x_zero[i], model_completion=True):
                        symmetry_y_cons.append(opposite_term)
                    else:
                        symmetry_y_cons.append(Not(opposite_term))
                    if m.eval(opposite_term, model_completion=True):
                        symmetry_x_cons.append(all_term_w_x_zero[i])
                    else:
                        symmetry_x_cons.append(Not(all_term_w_x_zero[i]))
                equal_circuits_on_max_y = And(symmetry_y_cons)
                s.add(Not(equal_circuits_on_max_y))


            yield from all_smt_rec(terms, l, numb_solutions, w, n, break_symmetry)
 
    yield from all_smt_rec(list(initial_terms), l, numb_solutions, w, n, break_symmetry)

def vlsi_design_one_solution(instance_number: int, visualize = True, rotation=True) -> None:
    file_path = f"../instances/ins-{instance_number}.txt"
    w, n, dims = utils.read_output(file_path)
    l = compute_lb(w, dims, rotation)
    logging.info(f"Trying with l= {l}")
    s, v = create_contraints(w, n, dims, l, rotation)

    while(not s.check()==sat):
        l += 1
        logging.info(f"Trying again with l= {l}")
        s, v = create_contraints(w, n, dims, l, rotation)

    model = s.model()
    sol = compute_solution(model, v, w, n, l)
    if visualize:
        utils.visualize_w_color_rotation(sol, w, len(sol[0]), dims, title=f"Instance {instance_number}, l={l}")
    return w, n, l, dims, sol, s

def vlsi_design_all_solutions(instance_number: int, visualize, rotation=True, break_symmetry=True) -> None:
    file_path = f"../instances/ins-{instance_number}.txt"
    w, n, dims = utils.read_output(file_path)
    l = compute_lb(w, dims, rotation)
    logging.info(f"Trying with l= {l}")
    s, v = create_contraints(w, n, dims, l, rotation)

    while(not s.check()==sat):
        l += 1
        logging.info(f"Trying again with l= {l}")
        s, v = create_contraints(w, n, dims, l, rotation)


    logging.info(f"Found one solution for l= {l}")
       
    flattened_v = np.array(v).flatten()
    solutionGenerator = all_smt(s, flattened_v, l, w, n, break_symmetry)
    solutions = [compute_solution(model, v, w, n, l) for model in solutionGenerator]
    logging.info(f"Found {len(solutions)} solutions with length l = {l}")
    if visualize:
        for sol in solutions:
            utils.visualize_w_color_rotation(sol, w, len(sol[0]), dims, title=f"Instance {instance_number}, l={l}")
    return w, n, l, dims, solutions, s

def vlsi_design(instance_number: int, visualize = True, allSolutions=True, rotation=True, break_symmetry=True) -> None:
    if allSolutions:
        return vlsi_design_all_solutions(instance_number, visualize, rotation, break_symmetry)
    else:
        return vlsi_design_one_solution(instance_number, visualize, rotation)

def make_solution_str(w, l, n, dims, sol):
    str = f"{w} {l}\n{n}\n"

    pos = {}
    for x in range(w):
      for y in range(l-1, 0, -1):
          c = sol[x][y]

          if c != 0 and c not in pos:
              pos[c] = [x, (l-1) - y]

              numb = sol[x].count(c)
              if numb != dims[c-1][1]:
                  pos[c].append("R")
          
    for i in range(n):
      rotated = 0
      if (len(pos.get(i + 1)) > 2):
        rotated = 1
      str += f"{dims[i][WIDTH + rotated]} {dims[i][HEIGHT - rotated]} {pos.get(i + 1)[0]} {pos.get(i + 1)[1]}\n"

    str += "\n"  
    return str

def parse_statistics(statistics):
    # We don't have n_solutions, failures or solve_time in SAT as in CP. Only record time.
    time = statistics.get_key_value('time')

    stats = [time]
    stats = [str(x) for x in stats]
    return " ".join(stats)

# Parse the solution to correct output form
def output_results(w, l, n, dims, sol, s):
    str = ""
    if len(np.array(sol).shape) == 3:
        for j in range(len(sol)):
            str += make_solution_str(w, l, n, dims, sol[j])
    else:
        str = make_solution_str(w, l, n, dims, sol)
    
    str += f"{parse_statistics(s.statistics())}"
    return str


def main():
    i = sys.argv[1]
    print(f"Instance {i}")
    output_file = f"./sat_solutions/sol_ins_no_rotation_20s-{i}.txt"
    logging.info(f"Running file {output_file}")
    w, n, l, dims, sol, s = vlsi_design(i, allSolutions=ALL_SOLUTIONS, rotation=ROTATION, visualize=VISUALIZE, break_symmetry=BREAK_SYMMETRY)

    output = output_results(w, l, n, dims, sol, s) 
    utils.write_output_to_file(output_file, output)

if __name__ == "__main__":
    main()
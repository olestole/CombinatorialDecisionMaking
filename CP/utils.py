import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

def parse_result(output):
    arr = []
    for line in output:
        elm = line.strip().split(' ')
        int_elm = [int(elm) for elm in elm]
        arr.append(int_elm)
    return arr

def visualize_output(output):
    w = output[0][0]
    l = output[0][1]
    n = output[1][0]

    colors = np.array(['red', 'green', 'blue', 'yellow', 'orange', 'pink', 'purple', 'brown']*(math.ceil(n/8)))

    fig = plt.figure(figsize=(w/2, l/2))
    ax = fig.gca()
    ax.set_xticks(np.arange(0, w+1, 1))
    ax.set_yticks(np.arange(0, l+1, 1))
    plt.grid()
    for i, [width, height, x, y] in enumerate(np.array(output[2:])):
        rect = patches.Rectangle((x, y), width, height, linewidth=3, edgecolor='black', facecolor=colors[i])
        ax.add_patch(rect)
    plt.show()
    return fig

def parse_instance(instance_dir = 'instances', filename = "ins-1.txt"):
    instance_dir = 'instances'
    directory_path = os.path.join(os.getcwd(), instance_dir)
    file_path = os.path.join(directory_path, filename)

    with open(file_path, 'r') as f:
            data = f.readlines()
            data = [x.strip() for x in data]
            data = [x.split(' ') for x in data]
            data = [[int(y) for y in x] for x in data]
            w = data[0][0]
            n = data[1][0]
            data = data[2:]
    return w, n, data
        
def create_model(model, new_string=None):
    if new_string:
        model.add_string(new_string)
        return
    model.add_string("""
include "globals.mzn";

int: w;
int: n;

int: width = 1;
int: height = 2;

set of int: CIRCUITS = 1..n;
array[CIRCUITS, 1..2] of int: dims;

int: upper_bound = sum(i in CIRCUITS)(dims[i, height]);

array[CIRCUITS] of var 0..w: pos_x;
array[CIRCUITS] of var 0..upper_bound: pos_y;

var 0..upper_bound: l;

constraint
  l = max(i in CIRCUITS)(
    pos_y[i] + dims[i, height]
  );

constraint
  forall(i in CIRCUITS)(
    pos_x[i] + dims[i, width] <= w
  );
  
 constraint
  forall(i in CIRCUITS)(
    forall(j in CIRCUITS where i != j)(
      not overlapping(i,j)
    )
  );

solve minimize l;

predicate x_overlapping(var int:i, var int:j) = 
   pos_x[i] + dims[i, width] > pos_x[j] /\ pos_x[j] + dims[j, width] > pos_x[i];
   
predicate y_overlapping(var int:i, var int:j) = 
   pos_y[i] + dims[i, height] > pos_y[j] /\ pos_y[j] + dims[j, height] > pos_y[i];
   
predicate overlapping(var int:i, var int:j) = 
   x_overlapping(i, j) /\ y_overlapping(i, j);

output 
  ["\(w) \(l)\\n"] ++
  ["\(n)\\n"] ++
  [show(dims[i, width]) ++ " " ++ show(dims[i, height]) ++ " " ++ show(pos_x[i]) ++ " " ++ show(pos_y[i]) ++ "\\n" | i in CIRCUITS];
""")

def write_output_to_file(file_path, output):
    with open(file_path, "w") as f:
        f.write(output)
        f.write("\n")
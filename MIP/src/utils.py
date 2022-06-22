import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math


def read_output(filename):
    arr = []
    with open(filename) as f:
        for line in f:
            elm = line.strip().split(' ')
            int_elm = [int(elm) for elm in elm]
            arr.append(int_elm)
    
    w = arr[0][0]
    n = arr[1][0]
    dims = np.array(arr[2:])
    return w, n, dims

def visualize_output(output, dims, instance_number):
    w = output[0][0]
    l = output[0][1]
    n = output[1][0]

    colors = np.array(['red', 'green', 'blue', 'yellow', 'orange', 'pink', 'purple', 'brown']*(math.ceil(n/8)))


    fig = plt.figure(figsize=(w/2, l/2))
    fig.suptitle(f"Instance {instance_number}")
    ax = fig.gca()
    ax.set_xticks(np.arange(0, w+1, 1))
    ax.set_yticks(np.arange(0, l+1, 1))
    plt.grid()
    for i, [width, height, x, y] in enumerate(np.array(output[2:])):
        rect = patches.Rectangle((x, y), width, height, linewidth=3, edgecolor='black', facecolor=colors[i])
        ax.add_patch(rect)
        if (width != dims[i, 0]):
            ax.text(x+width/2-0.7, y+height/2, 'Rotated')
    plt.show()
    return fig

def write_output_to_file(file_path, output):
    with open(file_path, "w") as f:
        f.write(output)
        f.write("\n")

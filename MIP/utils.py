import numpy as np

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
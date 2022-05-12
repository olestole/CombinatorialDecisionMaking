import matplotlib.pyplot as plt
import numpy as np

def display_sudoku(sol, w, l):
    fig, ax = plt.subplots(figsize=(4, 4))
    for x in range(w):
        for y in range(l):
            v = sol[x][y] # Mulig y, x
            s = " "
            if v > 0:
                s = str(v)
            ax.text(x+0.5, (l-0.5)-y, s, va='center', ha='center')
        ax.set_xlim(0, w)
    ax.set_ylim(0, l)
    ax.set_xticks(np.arange(w))
    ax.set_yticks(np.arange(l))
    ax.grid()
    plt.show()

def display_sudoku_with_rotation(sol, w, l, dims):
    fig, ax = plt.subplots(figsize=(4, 4))
    for x in range(w):
        for y in range(l):
            v = sol[x][y] # Mulig y, x
            s = " "
            if v > 0:
                numb = sol[x].count(v)
                if numb != dims[v-1][1]:
                    s = str(v)+"_r"
                else:
                    s = str(v)
            ax.text(x+0.5, (l-0.5)-y, s, va='center', ha='center')
        ax.set_xlim(0, w)
    ax.set_ylim(0, l)
    ax.set_xticks(np.arange(w))
    ax.set_yticks(np.arange(l))
    ax.grid()
    plt.show()
    
def read_output(filename):
    arr = []
    with open(filename) as f:
        for line in f:
            elm = line.strip().split(' ')
            int_elm = [int(elm) for elm in elm]
            arr.append(int_elm)
    return arr
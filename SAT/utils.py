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

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

table = np.random.randint(2, size=(480, 640))
kernel = np.ones((3,3))
rule = np.array([0,0,0,0,1,0,1,1,1,1])

fig = plt.figure(figsize=(6.4,4.8),dpi=100)
im = plt.imshow(table, animated=True)

def update(_):
    padded = np.pad(table, 1)
    for i in range(table.shape[0]):
        for j in range(table.shape[1]):
            table[i][j] = rule[np.sum(padded[i:i+3, j:j+3] * kernel, dtype=np.int32)]
    im.set_array(table)

anim = FuncAnimation(fig, update, frames=400, interval=1.0/60, blit=False)
anim.save("cell_automata.gif", writer="imagemagick")

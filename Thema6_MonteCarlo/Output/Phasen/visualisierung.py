""" 
Skript zur Visualisierung der harten Stäbchen
in Python 3

Erwartet: 
horizontal.csv
vertikal.csv
mit Spalten: x,y

in CSV: Kommentare mit # erlaubt
"""

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import numpy as np


ROD_LENGTH = 8   # Rod length L
ROD_WIDTH = 1   # Rod width 1

LATTICE_WIDTH = 64  # Lattice Width M


# --------------------------------------------------------------------------- load data
print("Loading data")
hor_arr = np.loadtxt("horizontal.csv", delimiter=',')
ver_arr = np.loadtxt("vertical.csv", delimiter=',')
print("Data loaded")



# --------------------------------------------------------------------------- prepare plot
fig, axs = plt.subplots()

# Format limits and aspect ratio
axs.set_xlim(0,LATTICE_WIDTH)
axs.set_ylim(0,LATTICE_WIDTH)
axs.set_aspect("equal")

# create rectangle patches for horizontal rods
hor_rods = []
for rod_pos in hor_arr:
    hor_rods.append(patches.Rectangle(rod_pos, ROD_LENGTH, ROD_WIDTH, 
                                      linewidth=1, edgecolor="black", facecolor="red"))
    
    # check if rod is at the edge of the lattice and place it 64 units further left
    if rod_pos[0] + ROD_LENGTH > LATTICE_WIDTH:
        hor_rods.append(patches.Rectangle((rod_pos[0]-LATTICE_WIDTH, rod_pos[1]), ROD_LENGTH, ROD_WIDTH, 
                                      linewidth=1, edgecolor="black", facecolor="red"))

# create rectangle patches for horizontal rods
ver_rods = []
for rod_pos in ver_arr:
    ver_rods.append(patches.Rectangle(rod_pos, ROD_WIDTH, ROD_LENGTH,
                                      linewidth=1, edgecolor="black", facecolor="blue"))
    
    # check if rod is at the edge of the lattice and place it 64 units further down
    if rod_pos[1] + ROD_LENGTH > LATTICE_WIDTH:
        ver_rods.append(patches.Rectangle((rod_pos[0], rod_pos[1]-LATTICE_WIDTH), ROD_WIDTH, ROD_LENGTH,
                                      linewidth=1, edgecolor="black", facecolor="blue"))

# add rectangles to plot
for rod in hor_rods:
    axs.add_patch(rod)
    
for rod in ver_rods:
    axs.add_patch(rod)
    
# --------------------------------------------------------------------------- save plot

plt.savefig("visualization.png", dpi=300)
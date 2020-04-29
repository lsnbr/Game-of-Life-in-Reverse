import numpy as np

from gol_tools import *
from square_cell import SquareCell, merge_quad
from square_tree import SquareTree



def quad_gen(goal):

    height, width = goal.shape
    tree = SquareTree(goal.shape)
    init_cells = np.ndarray(goal.shape, dtype=Squarecell)
    # dict of all kid of 3x3 predecessors of a single on/off cell
    pre = singleCellPredecessorsStrict()

    # populate init_cells
    for row in range(height):
        for col in range(width):

            pass
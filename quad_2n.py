import numpy as np

from gol_tools import *
from square_cell import SquareCell




def quad_2n(goal):
    '''
    Finds all predecessors of a given 2^n by 2^n goal pattern

    First fills an array (same shape of goal) with SquareCell objects, 
    each with precalculated 3x3 predecessors of single cells as stored pattern.
    If the cell is on the rim or at a corner it gets a subset of the predecessors, 
    such that the corresponding rim is dead after one generation.

    Then 2x2 SquareCell objects get merged to a new SquareCell object,
    and we get a new SquareCell array 1/4 the size of the previous.

    That process is iterated until the array consists of just one SquareCell object,
    which now holds all valid predecessors to the goal pattern.
    '''

    width = goal.shape[0]           # side length of goal pattern
    log_two = len(bin(width)) - 3   # log base 2 of side length

    new_cells = np.ndarray(shape=(width, width), dtype=SquareCell)

    # dict of all kid of 3x3 predecessors of a single on/off cell
    pre = singleCellPredecessorsStrict()



    # initialize first newCell[,]
    print(f'Level {log_two}...')

    for row in range(width):
        for col in range(width):

            pos = col % 2
            status = ['off', 'on'][goal[row, col]]

            if row == 0:
                if col == 0:           new_cells[row, col] = SquareCell(pre[status + '_tl'], pos)
                elif col == width - 1: new_cells[row, col] = SquareCell(pre[status + '_tr'], pos)
                else:                  new_cells[row, col] = SquareCell(pre[status + '_t'], pos)
            elif row == width - 1:
                if col == 0:           new_cells[row, col] = SquareCell(pre[status + '_dl'], pos)
                elif col == width - 1: new_cells[row, col] = SquareCell(pre[status + '_dr'], pos)
                else:                  new_cells[row, col] = SquareCell(pre[status + '_d'], pos)
            else:
                if col == 0:           new_cells[row, col] = SquareCell(pre[status + '_l'], pos)
                elif col == width - 1: new_cells[row, col] = SquareCell(pre[status + '_r'], pos)
                else:                  new_cells[row, col] = SquareCell(pre[status], pos)


    # main merging loop of SquareCells
    for level in range(log_two - 1, -1, -1):
        print(f'Level {level}...')

        old_cells = new_cells
        width = 2 ** level
        new_cells = np.ndarray(shape=(width, width), dtype=SquareCell)

        for row in range(width):
            oldRow = row * 2
            for col in range(width):
                oldCol = col * 2
                new_cells[row, col] = SquareCell.merge(
                                            col % 2, 'quad',
                                            old_cells[oldRow    , oldCol], old_cells[oldRow    , oldCol + 1],
                                            old_cells[oldRow + 1, oldCol], old_cells[oldRow + 1, oldCol + 1])

    return new_cells[0, 0].pats













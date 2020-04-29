import numpy as np

from gol_tools import *




class SquareCell:
    '''Represents a 2^n by 2^2 cell'''

    def __init__(self, pats: [np.ndarray], pos: int) -> None :
        '''
        constructs a hash table with the left/top rim as keys
        pos = position in its 2x2 square: 0 is left, 1 is right, 2 is down
        '''

        self.hashs = {}
        self.pats = pats

        if pos == 1:
            for p in pats:
                h = left2(p).tostring()
                if h in self.hashs:
                    self.hashs[h].append(p)
                else:
                    self.hashs[h] = [p]
        elif pos == 2:
            for p in pats:
                h = top2(p).tostring()
                if h in self.hashs:
                    self.hashs[h].append(p)
                else:
                    self.hashs[h] = [p]





def merge_quad(tl: SquareCell, tr: SquareCell, dl: SquareCell, dr: SquareCell, pos: int) -> SquareCell:
    '''takes 4 SquareCell objects and creates a new one out of all possible combinations'''

    tops = []
    downs = []
    quads = []

    # tops
    for left_cell in tl.pats:
        h = right2(left_cell).tostring()
        if h in tr.hashs:
            for reight_cell in tr.hashs[h]:
                tops.append(merge_halves_horizontal(left_cell, reight_cell))

    # downs
    for left_cell in dl.pats:
        h = right2(left_cell).tostring()
        if h in dr.hashs:
            for reight_cell in dr.hashs[h]:
                downs.append(merge_halves_horizontal(left_cell, reight_cell))
    downs = SquareCell(downs, 2)

    # quads
    for top_cell in tops:
        h = down2(top_cell).tostring()
        if h in downs.hashs:
            for down_cell in downs.hashs[h]:
                quads.append(merge_halves_vertical(top_cell, down_cell))

    return SquareCell(quads, pos)




def merge_halves_horizontal(le, re):
    return np.hstack((le[:, :-1], re[:, 1:]))

def merge_halves_vertical(up, do):
    return np.vstack((up[:-1, :], do[1:, :]))
import numpy as np

from gol_tools import *




class SquareCell:
    '''Represents a 2^n by 2^2 cell'''

    def __init__(self, pats: [np.ndarray], pos: int) -> None :
        '''
        constructs a hash table with the left/top rim as keys
                                               3
        pos = position in its 2x2 square:    0   1
                                               2
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





def merge(pos: int, kind: str, c1: SquareCell, c2: SquareCell, c3: SquareCell = None, c4: SquareCell = None) -> SquareCell:
    '''
    takes 2 or 4 SquareCell objects and creates a new one out of all possible combinations
    
    kinds:    'vertical':  c1      'horizontal':  c1 c2      'quad':  c1 c2
                           c2                                         c3 c4
    '''

    if kind == 'vertical':
        pairs = []
        for top_cell in c1.pats:
            h = down2(top_cell).tostring()
            if h in c2.hashs:
                for down_cell in c2.hashs[h]:
                    pairs.append(merge_halves_vertical(top_cell, down_cell))
        return SquareCell(pairs, pos)

    # tops
    tops = []
    for left_cell in c1.pats:
        h = right2(left_cell).tostring()
        if h in c2.hashs:
            for reight_cell in c2.hashs[h]:
                tops.append(merge_halves_horizontal(left_cell, reight_cell))
    if kind == 'horizontal': return SquareCell(tops, pos)

    # downs
    downs = []
    for left_cell in c3.pats:
        h = right2(left_cell).tostring()
        if h in c4.hashs:
            for reight_cell in c4.hashs[h]:
                downs.append(merge_halves_horizontal(left_cell, reight_cell))
    downs = SquareCell(downs, 2)

    # quads
    quads = []
    for top_cell in tops:
        h = down2(top_cell).tostring()
        if h in downs.hashs:
            for down_cell in downs.hashs[h]:
                quads.append(merge_halves_vertical(top_cell, down_cell))
    if kind == 'quad': return SquareCell(quads, pos)




def merge_halves_horizontal(le, re):
    return np.hstack((le[:, :-1], re[:, 1:]))

def merge_halves_vertical(up, do):
    return np.vstack((up[:-1, :], do[1:, :]))
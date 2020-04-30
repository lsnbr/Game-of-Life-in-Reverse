import numpy as np

from gol_tools import *




class SquareCell:
    '''Represents a 2^n by 2^2 cell'''


    def __init__(self, pats, pos):
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



    @classmethod
    def merge(cls, pos, kind, c1, c2, c3 = None, c4 = None):
        '''
        takes 2 or 4 SquareCell objects and creates a new one out of all possible combinations
        
        kinds:    'vertical':  c1      'horizontal':  c1 c2      'quad':  c1 c2
                            c2                                         c3 c4
        '''

        if kind == 'vertical':
            tops, downs = c1.pats, c2
        else:
            # tops
            tops = []
            for left_cell in c1.pats:
                h = right2(left_cell).tostring()
                if h in c2.hashs:
                    for reight_cell in c2.hashs[h]:
                        tops.append(merge_halves_horizontal(left_cell, reight_cell))
            if kind == 'horizontal': return cls(tops, pos)
            
            # downs
            downs = []
            for left_cell in c3.pats:
                h = right2(left_cell).tostring()
                if h in c4.hashs:
                    for reight_cell in c4.hashs[h]:
                        downs.append(merge_halves_horizontal(left_cell, reight_cell))
            downs = cls(downs, 2)

        # quads or vertical
        quads = []
        for top_cell in tops:
            h = down2(top_cell).tostring()
            if h in downs.hashs:
                for down_cell in downs.hashs[h]:
                    quads.append(merge_halves_vertical(top_cell, down_cell))
        return cls(quads, pos)
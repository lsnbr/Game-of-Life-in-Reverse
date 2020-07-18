import numpy as np

from gol_tools import *
from square_cell import SquareCell
from square_tree import SquareTree

from typing import List, Tuple
Life = np.ndarray


def quad_gen(goal: Life) -> List[Life]:
    '''generalized verion of quad_2n, works for mxn with 1 <= m,n'''

    # tree structure of pattern to merge
    tree = SquareTree(goal.shape)
    # general dimensions of input pattern
    height, width = goal.shape
    # dict of all kid of 3x3 predecessors of a single on/off cell
    pre = single_cell_predecessors()


    def tree_merge(twig: SquareTree, cord: Tuple[int, int], pos: int) -> SquareCell:
        '''recursive merging according to tree structure of rectangles'''
        
        if twig.type == 'leaf':
            status = ['off', 'on'][goal[cord]]
            row_pos = ('t' if cord[0] == 0 else '') + ('d' if cord[0] == height - 1 else '')
            col_pos = ('l' if cord[1] == 0 else '') + ('r' if cord[1] == width - 1 else '')
            return SquareCell(pre[status + row_pos + col_pos], pos)

        off_height, off_width = twig.tl.shape

        if twig.type == 'vertical':
            top = tree_merge(twig.tl, cord, 3)
            down = tree_merge(twig.dl, (cord[0] + off_height, cord[1]), 2)
            return SquareCell.merge(pos, 'vertical', top, down)

        top_left = tree_merge(twig.tl, cord, 0)
        top_right = tree_merge(twig.tr, (cord[0], cord[1] + off_width), 1)
        if twig.type == 'horizontal':
            return SquareCell.merge(pos, 'horizontal', top_left, top_right)
        
        down_left = tree_merge(twig.dl, (cord[0] + off_height, cord[1]), 0)
        down_right = tree_merge(twig.dr, (cord[0] + off_height, cord[1] + off_width), 1)
        return SquareCell.merge(pos, 'quad', top_left, top_right, down_left, down_right)
        

    result = tree_merge(tree, (0, 0), 0)
    return result.pats
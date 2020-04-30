import numpy as np

from gol_tools import *
from square_cell import SquareCell
from square_tree import SquareTree



def quad_gen(goal):

    tree = SquareTree(goal.shape)
    height, width = goal.shape
    # dict of all kid of 3x3 predecessors of a single on/off cell
    pre = singleCellPredecessorsStrict()


    def tree_merge(twig, cord, pos):
        
        if twig.type == 'leaf':
            status = ['off', 'on'][goal[cord]]
            if cord[0] == 0:
                if cord[1] == 0:           return SquareCell(pre[status + '_tl'], pos)
                elif cord[1] == width - 1: return SquareCell(pre[status + '_tr'], pos)
                else:                      return SquareCell(pre[status + '_t'], pos)
            elif cord[0] == height - 1:
                if cord[1] == 0:           return SquareCell(pre[status + '_dl'], pos)
                elif cord[1] == width - 1: return SquareCell(pre[status + '_dr'], pos)
                else:                      return SquareCell(pre[status + '_d'], pos)
            else:
                if cord[1] == 0:           return SquareCell(pre[status + '_l'], pos)
                elif cord[1] == width - 1: return SquareCell(pre[status + '_r'], pos)
                else:                      return SquareCell(pre[status], pos)

        off_height, off_width = twig.tl.shape

        if twig.type == 'vertical':
            top = tree_merge(twig.tl, cord, 3)
            down = tree_merge(twig.dl, (cord[0] + off_height, cord[1]), 2)
            return SquareCell.merge(pos, 'vertical', top, down)

        if twig.type == 'horizontal':
            left = tree_merge(twig.tl, cord, 0)
            right = tree_merge(twig.tr, (cord[0], cord[1] + off_width), 1)
            return SquareCell.merge(pos, 'horizontal', left, right)

        else:
            top_left = tree_merge(twig.tl, cord, 0)
            top_right = tree_merge(twig.tr, (cord[0], cord[1] + off_width), 1)
            down_left = tree_merge(twig.dl, (cord[0] + off_height, cord[1]), 0)
            down_right = tree_merge(twig.dr, (cord[0] + off_height, cord[1] + off_width), 1)
            return SquareCell.merge(pos, 'quad', top_left, top_right, down_left, down_right)


    result = tree_merge(tree, (0, 0), 0)
    return result.pats
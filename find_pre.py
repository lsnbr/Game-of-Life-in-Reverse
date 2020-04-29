import numpy as np

from gol_tools import *
from quad_2n import quad_2n
from quad_gen import quad_gen



goal8 = np.array(list(bin(31 ** 13)[3:]), dtype = np.int8).reshape(8,8)
goal_rnd = create_rnd((8,8), 0.6)
goal = goal_rnd

pred = quad_gen(goal)
#pred = quad_2n(goal)

print_life(goal, title=f'Goal pattern {goal.shape[0]}x{goal.shape[1]}')
print_life(pred[0], title=f'{len(pred)} predecessors')
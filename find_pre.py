import numpy as np

from gol_tools import *
from quad_2n import quad_2n



goal8 = np.array(list(bin(31 ** 13)[3:]), dtype = np.int8).reshape(8,8)
goal = create_rnd((8,8), 0.8)

pred = quad_2n(goal)

print_life(goal, title='Goal pattern')
print_life(pred[0], title=f'{len(pred)} predecessors')
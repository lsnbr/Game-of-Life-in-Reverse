import numpy as np

from speed import profile
from gol_tools import *

from quad_2n     import quad_2n
from quad_2n_one import quad_2n_one





rand_goal = create_rnd((4,4), 0.5)
test_goal = np.array(list(bin(31 ** 13)[3:]), dtype = np.int8).reshape(8,8)
goal = rand_goal


@profile()
def test_speed(goal):
    return quad_2n(goal)

preds = test_speed(goal)




print_life(preds[0], title=f'number of predecessors: {len(preds)}')
print_life(pad(goal), title='goal pattern padded')
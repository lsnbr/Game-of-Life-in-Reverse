import numpy as np

from gol_tools import *
from quad_2n import quad_2n
from quad_gen import quad_gen
from speed import profile



goal8 = np.array(list(bin(31 ** 13)[3:]), dtype = np.int8).reshape(8,8)
goal_rnd = create_rnd((4,4), 0.1)
goal_2n = create_rnd((8,8), 0.7)
goal_sm = np.array([[0,1,0,1,0]
                   ,[0,1,0,1,0]
                   ,[0,0,0,0,0]
                   ,[1,0,0,0,1]
                   ,[0,1,1,1,0]], dtype=np.int8)
goal_4 = pad(np.ones((2,2), dtype=np.int8))


goal = goal_4

@profile()
def test_pre(g):
    return quad_gen(g)
    #return quad_2n(g)

pred = test_pre(goal)

print_life(goal, title=f'Goal pattern {goal.shape[0]}x{goal.shape[1]}')
print_life(pred[4459], title=f'{len(pred)} predecessors')
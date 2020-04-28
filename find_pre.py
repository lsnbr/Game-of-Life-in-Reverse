import numpy as np

from gol_tools import *
from quad_2n import quad_2n




goal = create_rnd((4,4))

pred = quad_2n(goal)

print_life(*pred[:min(len(pred), 4)])
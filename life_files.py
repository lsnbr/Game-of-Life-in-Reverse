import numpy as np
from itertools import product
import re

import gol_tools as gol

Life = np.ndarray



def to_life106(life: Life) -> str:
    file = '#Life 1.06'
    file += '\n' + '\n'.join(f'{r} {c}' for r, c in product(*map(range, life.shape)) if life[r, c])
    return file


def from_life106(file: str) -> Life:
    if not re.match(r'#Life 1\.06\n(\n-?\d+ -?\d+)*', file):
        raise Exception('Invalid file format')
    coords = {tuple(map(int, row.split())) for row in file.split('\n')[1:]}
    if not coords:
        return np.zeros((1,1), dtype=np.int8)
    min_x = min(coords, key=lambda x: x[0])[0]
    max_x = max(coords, key=lambda x: x[0])[0]
    min_y = min(coords, key=lambda x: x[1])[1]
    max_y = max(coords, key=lambda x: x[1])[1]
    life = np.zeros((max_x - min_x + 1, max_y - min_y + 1), dtype=np.int8)
    for x, y in coords:
        life[x - min_x, y - min_y] = 1
    return life



def to_life105(life: Life) -> str:
    file = '#Life 1.05'


def from_life105(file: str) -> Life:
    pass
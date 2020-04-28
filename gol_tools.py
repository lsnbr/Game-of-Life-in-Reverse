import numpy as np
from random import random







def create_rnd(size: (int, int), density: float = 0.5) -> np.ndarray:

    return np.array([[1 if random() < density else 0 for _ in range(size[1])] for _ in range(size[0])]
                    ,dtype = np.int8)





def pad(life: np.ndarray) -> np.ndarray:

    zrow = np.zeros(life.shape[1] + 2, dtype=np.int8)
    zcol = np.zeros(life.shape[0], dtype=np.int8)
    return np.vstack((zrow.copy()
                     ,np.column_stack((zcol.copy(), life, zcol.copy()))
                     ,zrow.copy()))




def print_life(*lifes: (np.ndarray), title: str = 'Great pattern') -> None:
    
    print()
    if len(lifes) == 1:
        print(title)
        for r in lifes[0]:
            print(' '.join(map(lambda c: ['.', 'O'][c], r)))
    else:
        for i, life in enumerate(lifes):
            print(title, i + 1)
            for r in life:
                print(' '.join(map(lambda c: ['.', 'O'][c], r)))
            if i < len(lifes) - 1:
                print()




def next_gen(oldL: np.ndarray) -> np.ndarray:

    newL = np.zeros(oldL.shape, dtype=np.int8)
    oldL = pad(oldL)
    for r in range(1, oldL.shape[0] - 1):
        for c in range(1, oldL.shape[1] - 1):
            near = oldL[r-1 : r+2, c-1 : c+2].sum() - oldL[r, c]
            if near == 3 or (near == 2 and oldL[r, c]):
                newL[r-1, c-1] = 1
    return newL





def singleCellPredecessorsStrict() -> {str: [np.ndarray]}:

    pre_on = []
    pre_off = []
    pre_top_on = []
    pre_top_off = []
    pre_top_left_on = []
    pre_top_left_off = []

    for i in range(512, 1024):

        pat0 = np.array(list(bin(i)[3:]), dtype=np.int8).reshape(3,3)
        pat1 = next_gen(pat0)

        if pat1[1, 1]:
            pre_on.append(pat0)
            if not (pat1[0, 0] or pat1[0, 1] or pat1[0, 2]):
                pre_top_on.append(pat0)
                if not (pat1[1, 0] or pat1[2, 0]):
                    pre_top_left_on.append(pat0)
        else:
            pre_off.append(pat0)
            if not (pat1[0, 0] or pat1[0, 1] or pat1[0, 2]):
                pre_top_off.append(pat0)
                if not (pat1[1, 0] or pat1[2, 0]):
                    pre_top_left_off.append(pat0)

    return {'on': pre_on, 'on_t': pre_top_on, 'on_tl': pre_top_left_on
           ,'off': pre_off, 'off_t': pre_top_off, 'off_tl': pre_top_left_off
           ,'on_d': rot_twice(pre_top_on), 'on_l': rot_counter(pre_top_on), 'on_r': rot_clock(pre_top_on)
           ,'off_d': rot_twice(pre_top_off), 'off_l': rot_counter(pre_top_off), 'off_r': rot_clock(pre_top_off)
           ,'on_tr': rot_clock(pre_top_left_on), 'on_dr': rot_twice(pre_top_left_on), 'on_dl': rot_counter(pre_top_left_on)
           ,'off_tr': rot_clock(pre_top_left_off), 'off_dr': rot_twice(pre_top_left_off), 'off_dl': rot_counter(pre_top_left_off)}




def flip_row(pats):
    return list(map(np.flipud, pats))
def flip_col(pats):
    return list(map(np.fliplr, pats))
def transpose(pats):
    return list(map(lambda a: a.T, pats))
def rot_counter(pats):
    return list(map(lambda a: np.rot90(a).copy(), pats))
def rot_clock(pats):
    return list(map(lambda a: np.rot90(a, 3).copy(), pats))
def rot_twice(pats):
    return list(map(lambda a: np.rot90(a, 2).copy(), pats))



def right2(grid):
    return grid[:, -2:]
def left2(grid):
    return grid[:, :2]
def top2(grid):
    return grid[:2, :]
def down2(grid):
    return grid[-2:, :]

def mid(grid):
    return grid[2:-2, 2:-2]




def map2d(fun, mat: np.ndarray, n_type = None) -> np.ndarray:

    if n_type:
        n_mat = np.ndarray(mat.shape, n_type)
    else:
        n_mat = np.ndarray(mat.shape)
    for r in range(mat.shape[0]):
        for c in range(mat.shape[1]):
            n_mat[r, c] = fun(mat[r, c])
    return n_mat











def run_gens(life: np.ndarray, gens: int, print_final: bool = False, print_all: bool = False) -> np.ndarray:

    for _ in range(gens):
        if print_all: print_life(life)
        life = next_gen(life)
    if print_final: print_life(life)
    return life





def singleCellPredecessors() -> ([np.ndarray], [np.ndarray]):

    #ind_on, ind_off = 0, 0
    pred0, pred1 = [], []

    for i in range(512, 1024):
        pattern = np.array(list(bin(i)[3:]), dtype=np.int8).reshape(3,3)
        if next_gen(pattern)[1, 1] == 1:
            pred1.append(pattern)
        else:
            pred0.append(pattern)

    return pred0, pred1





def avg_density(size: (int, int), density: float, n_gens: int, tries: int = 10) -> (float, float, float):
    '''return (avg_density, lowest_density, highest_density)'''

    total_cells = size[0] * size[1]
    total = 0
    lowest = total_cells
    highest = 0
    for _ in range(tries):
        end_pat = run_gens(create_rnd(size, density), n_gens, print_final=False)
        on_cells = end_pat.sum()
        total += on_cells
        if on_cells < lowest: lowest = on_cells
        elif on_cells > highest: highest = on_cells
    return total / (total_cells * tries), lowest / total_cells, highest / total_cells
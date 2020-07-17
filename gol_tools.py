import numpy as np
from random import random

from typing import (
    List, Tuple, Dict,
    Iterable, Callable,
    Optional, Any
)
Life = np.ndarray



def create_rnd(size: Tuple[int, int], density: float = 0.5) -> Life:
    '''create a size[0] by size[1] pattern with given density of live cells'''

    return np.array(
        [[1 if random() < density else 0 for _ in range(size[1])] for _ in range(size[0])],
        dtype = np.int8
    )



def pad(life: Life) -> Life:
    '''surround a pattern with a 1 thick layer of dead cells'''

    zrow = np.zeros(life.shape[1] + 2, dtype=np.int8)
    zcol = np.zeros(life.shape[0], dtype=np.int8)
    return np.vstack((
        zrow.copy(),
        np.column_stack((zcol.copy(), life, zcol.copy())),
        zrow.copy()
    ))



def print_life(*lifes: Life, title: Optional[str] = None) -> None:
    '''print a pattern where 'O'=alive and '.'=dead'''
    
    print()
    if len(lifes) == 1:
        if title is not None: print(title)
        for r in lifes[0]:
            print(' '.join(map(lambda c: ['.', 'O'][c], r)))
    else:
        for i, life in enumerate(lifes):
            if title is not None: print(title, i + 1)
            for r in life:
                print(' '.join(map(lambda c: ['.', 'O'][c], r)))
            if i < len(lifes) - 1:
                print()



def next_gen(oldL: Life, geometry: str = 'Hard Edges') -> Life:
    '''
    compute the GoL successor function with a certain geometry

    geometry == 'Hard Edges':      cells on the rim have fewer neighboors
    geometry == 'Torus':    grid wraps around on the edges
    '''

    newL = np.zeros(oldL.shape, dtype=np.int8)
    if geometry == 'Hard Edges':
        oldL = pad(oldL)
    elif geometry == 'Torus':
        top, bottom = oldL[0, :], oldL[-1, :]
        tl, tr, bl, br = oldL[0, 0], oldL[0, -1], oldL[-1, 0], oldL[-1, -1]
        oldL = np.column_stack((oldL[:, -1], oldL, oldL[:, 0]))
        oldL = np.row_stack((
            np.hstack((br, bottom, bl)),
            oldL,
            np.hstack((tr, top, tl))
        ))
    else:
        raise Exception(f"No such geometry '{geometry}' is supported.")

    for r in range(1, oldL.shape[0] - 1):
        for c in range(1, oldL.shape[1] - 1):
            near = oldL[r-1 : r+2, c-1 : c+2].sum() - oldL[r, c]
            if near == 3 or (near == 2 and oldL[r, c]):
                newL[r-1, c-1] = 1
    return newL



def single_cell_predecessors() -> Dict[str, List[Life]]:
    '''compute all kind of predecessors of a single cell'''

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

    return {'on': pre_on, 'ont': pre_top_on, 'ontl': pre_top_left_on
           ,'off': pre_off, 'offt': pre_top_off, 'offtl': pre_top_left_off
           ,'ond': rot_twice(pre_top_on), 'onl': rot_counter(pre_top_on), 'onr': rot_clock(pre_top_on)
           ,'offd': rot_twice(pre_top_off), 'offl': rot_counter(pre_top_off), 'offr': rot_clock(pre_top_off)
           ,'ontr': rot_clock(pre_top_left_on), 'ondr': rot_twice(pre_top_left_on), 'ondl': rot_counter(pre_top_left_on)
           ,'offtr': rot_clock(pre_top_left_off), 'offdr': rot_twice(pre_top_left_off), 'offdl': rot_counter(pre_top_left_off)}



def flip_row(pats: Iterable[Life]) -> List[Life]:
    return list(map(np.flipud, pats))

def flip_col(pats: Iterable[Life]) -> List[Life]:
    return list(map(np.fliplr, pats))

def transpose(pats: Iterable[Life]) -> List[Life]:
    return list(map(lambda a: a.T, pats))

def rot_counter(pats: Iterable[Life]) -> List[Life]:
    return list(map(lambda a: np.rot90(a).copy(), pats))

def rot_clock(pats: Iterable[Life]) -> List[Life]:
    return list(map(lambda a: np.rot90(a, 3).copy(), pats))

def rot_twice(pats: Iterable[Life]) -> List[Life]:
    return list(map(lambda a: np.rot90(a, 2).copy(), pats))


def merge_halves_horizontal(le: Life, re: Life) -> Life:
    return np.hstack((le[:, :-1], re[:, 1:]))

def merge_halves_vertical(up: Life, do: Life) -> Life:
    return np.vstack((up[:-1, :], do[1:, :]))

def right2(grid: Life) -> Life:
    return grid[:, -2:]

def left2(grid: Life) -> Life:
    return grid[:, :2]

def top2(grid: Life) -> Life:
    return grid[:2, :]

def down2(grid: Life) -> Life:
    return grid[-2:, :]

def mid(grid: Life) -> Life:
    return grid[2:-2, 2:-2]



def map2d(fun: Callable, mat: Life, n_type: Any = None) -> Life:
    '''like the built in map function, just for np 2d arrays'''

    if n_type:
        n_mat = np.ndarray(mat.shape, n_type)
    else:
        n_mat = np.ndarray(mat.shape)
    for r in range(mat.shape[0]):
        for c in range(mat.shape[1]):
            n_mat[r, c] = fun(mat[r, c])
    return n_mat



def test_if_pre(preds: List[Life], goal: Life) -> int:
    '''test if all pattern in preds are predecessors of goal and returns amount of false tests'''

    c = 0
    goal = pad(goal)
    for p in [preds] if isinstance(preds, np.ndarray) else preds:
        if not np.array_equal(next_gen(p), goal):
            c += 1
    return c



def run_gens(life: Life, gens: int, geometry='Hard Edges', print_final: bool = False, print_all: bool = False) -> Life:
    '''compute a future generation'''

    for _ in range(gens):
        if print_all: print_life(life)
        life = next_gen(life, geometry=geometry)
    if print_final: print_life(life)
    return life



def avg_density(
    size: Tuple[int, int],
    density: float,
    n_gens: int,
    sample_size: int = 32
) -> Tuple[float, float, float]:
    '''return (avg_density, lowest_density, highest_density)'''

    total_cells = size[0] * size[1]
    total = 0
    lowest = total_cells
    highest = 0
    for _ in range(sample_size):
        end_pat = run_gens(create_rnd(size, density), n_gens, print_final=False)
        on_cells = end_pat.sum()
        total += on_cells
        if on_cells < lowest: lowest = on_cells
        elif on_cells > highest: highest = on_cells
    return total / (total_cells * sample_size), lowest / total_cells, highest / total_cells
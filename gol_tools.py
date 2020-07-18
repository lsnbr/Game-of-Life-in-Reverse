import numpy as np
from random import random
from math import inf

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

    geometry == 'Hard Edges':   cells on the rim have fewer neighboors
    geometry == 'Torus':        grid wraps around on the edges
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


def shrink(life: Life) -> Life:
    '''shrinks a pattern to the smallest bounding box'''

    new_life = life
    while 0 not in new_life.shape and new_life[0, :].sum() == 0:
        new_life = new_life[1:, :]
    while 0 not in new_life.shape and new_life[-1, :].sum() == 0:
        new_life = new_life[:-1, :]
    while 0 not in new_life.shape and new_life[:, 0].sum() == 0:
        new_life = new_life[:, 1:]
    while 0 not in new_life.shape and new_life[:, -1].sum() == 0:
        new_life = new_life[:, :-1]
    return np.zeros((1,1), dtype=np.int8) if 0 in new_life.shape else new_life.copy()



def single_cell_predecessors() -> Dict[str, List[Life]]:
    '''compute all kind of predecessors of a single cell'''

    on,                off                = [], []
    top_on,            top_off            = [], []
    top_left_on,       top_left_off       = [], []
    top_left_right_on, top_left_right_off = [], []
    top_down_on,       top_down_off       = [], []
    center_on,         center_off         = [], []

    for i in range(512, 1024):

        pat0 = np.array(list(bin(i)[3:]), dtype=np.int8).reshape(3,3)
        pat1 = next_gen(pat0)

        if pat1[1, 1]:
            on.append(pat0)
            if pat1[0, 0] + pat1[0, 1] + pat1[0, 2] == 0:
                top_on.append(pat0)
                if pat1[2, 0] + pat1[2, 1] + pat1[2, 2] == 0:
                    top_down_on.append(pat0)
                if pat1[1, 0] + pat1[2, 0] == 0:
                    top_left_on.append(pat0)
                    if pat1[1, 2] + pat1[2, 2] == 0:
                        top_left_right_on.append(pat0)
                        if pat1[2, 1] == 0:
                            center_on.append(pat0)

        else:
            off.append(pat0)
            if pat1[0, 0] + pat1[0, 1] + pat1[0, 2] == 0:
                top_off.append(pat0)
                if pat1[2, 0] + pat1[2, 1] + pat1[2, 2] == 0:
                    top_down_off.append(pat0)
                if pat1[1, 0] + pat1[2, 0] == 0:
                    top_left_off.append(pat0)
                    if pat1[1, 2] + pat1[2, 2] == 0:
                        top_left_right_off.append(pat0)
                        if pat1[2, 1] == 0:
                            center_off.append(pat0)

    return {
        'on':     on,                             'off':     off,

        'ont':    top_on,                         'offt':    top_off,
        'ond':    rot_twice(top_on),              'offd':    rot_twice(top_off),
        'onl':    rot_counter(top_on),            'offl':    rot_counter(top_off),
        'onr':    rot_clock(top_on),              'offr':    rot_clock(top_off),

        'ontl':   top_left_on,                    'offtl':   top_left_off,
        'ontr':   rot_clock(top_left_on),         'offtr':   rot_clock(top_left_off),
        'ondl':   rot_counter(top_left_on),       'offdl':   rot_counter(top_left_off),
        'ondr':   rot_twice(top_left_on),         'offdr':   rot_twice(top_left_off),

        'ontlr':  top_left_right_on,              'offtlr':  top_left_right_off,
        'ondlr':  rot_twice(top_left_right_on),   'offdlr':  rot_twice(top_left_right_off),
        'ontdl':  rot_counter(top_left_right_on), 'offtdl':  rot_counter(top_left_right_off),
        'ontdr':  rot_clock(top_left_right_on),   'offtdr':  rot_clock(top_left_right_off),

        'ontd':   top_down_on,                    'offtd':   top_down_off,
        'onlr':   rot_clock(top_down_on),         'offlr':   rot_clock(top_down_off),
        
        'ontdlr': center_on,                      'offtdlr': center_off
    }



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



def filter_least_cells(lifes: Iterable[Life]) -> List[Life]:
    '''return all lifes that have the least amount of on cells'''

    filtered = []
    c_min = inf
    for life in lifes:
        c = life.sum()
        if c < c_min:
            filtered = [life]
            c_min = c
        elif c == c_min:
            filtered.append(life)
    return filtered



def filter_most_cells(lifes: Iterable[Life]) -> List[Life]:
    '''return all lifes that have the most amount of on cells'''

    filtered = []
    c_max = -inf
    for life in lifes:
        c = life.sum()
        if c > c_max:
            filtered = [life]
            c_max = c
        elif c == c_max:
            filtered.append(life)
    return filtered



def bounding_box(life: Life) -> Tuple[int, int]:
    '''return the size of the bounding box (rows x cols)'''

    h, w = life.shape
    r0, c0 = 0, 0 
    r1, c1 = h - 1, w - 1
    while r0 < h - 1 and life[r0, :].sum() == 0: r0 += 1
    while r1 > 0     and life[r1, :].sum() == 0: r1 -= 1
    while c0 < w - 1 and life[:, c0].sum() == 0: c0 += 1
    while c1 > 0     and life[:, c1].sum() == 0: c1 -= 1
    return max(1, r1 - r0 + 1), max(1, c1 - c0 + 1)


def filter_bounding_box(lifes: Iterable[Life]) -> List[Life]:
    '''return all lifes with the smallest bounding box'''

    filtered = []
    bb_min = inf
    for life in lifes:
        r, c = bounding_box(life)
        bb = r * c
        if bb < bb_min:
            filtered = [life]
            bb_min = bb
        elif bb == bb_min:
            filtered.append(life)
    return filtered



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
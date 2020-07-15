import tkinter as tk
import numpy as np

import gol_tools as gol

from typing import Tuple, Optional
Life = np.ndarray



class LifeCanvas(tk.Canvas):

    def __init__(self, life: Optional[Life] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        if life is not None:
            self.life = life

    @property
    def rows(self) -> int:
        return self.life.shape[0]

    @property
    def cols(self) -> int:
        return self.life.shape[1]

    @property
    def life(self) -> Life:
        try:
            return self._life
        except AttributeError:
            raise Exception('No Life pattern is set yet.')

    @life.setter
    def life(self, life: Life) -> None:
        self._life = life
        self.update(self._life)


    def update(self, life: Life) -> None:
        cell_width  = int(self['width']) / self.cols
        cell_height = int(self['height']) / self.rows
        self.delete(tk.ALL)
        for r in range(self.rows):
            for c in range(self.cols):
                self.create_rectangle(
                    r * cell_width,     c * cell_height,
                    (r+1) * cell_width, (c+1) * cell_height,
                    fill=['black', 'white'][self.life[r, c]],
                )


    def random(self, size: Tuple[int, int], density: float = 0.5) -> None:
        self.life = gol.create_rnd(size, density)


    def clean(self, size: Tuple[int, int]) -> None:
        self.life = np.zeros(size, dtype=np.int8)


    def next_gen(self, step: int = 1, geometry: str = 'Hard Edges') -> None:
        self.life = gol.run_gens(
            life=self.life,
            gens=step,
            geometry=geometry
        )
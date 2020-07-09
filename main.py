import gol_tools as gol

import tkinter as tk
import numpy as np

from typing import Optional
Life = np.ndarray



class GoLApp:

    def __init__(self) -> None:
        self.width, self.height = 512, 512
        self.life = None
        self.life_size = (20, 20)
        self.is_in_loop = False
        self.app = tk.Tk()
        self.app.title('Game of Life in Reverse')

        self.btn_nextgen = tk.Button(
            master=self.app,
            text='Next Gen',
            command=self.update_life,
            pady=5, padx=5,
        )
        self.btn_looplife = tk.Button(
            master=self.app,
            text='Start Loop',
            command=self.control_loop_life,
            pady=5, padx=5,
        )
        self.btn_resetlife = tk.Button(
            master=self.app,
            text='Reset',
            command=lambda: self.update_life(gol.create_rnd(self.life_size, 0.3)),
            pady=5, padx=5,
        )
        self.btn_nextgen.grid(row=0, column=0, sticky='we')
        self.btn_looplife.grid(row=0, column=1, sticky='we')
        self.btn_resetlife.grid(row=0, column=2, sticky='we')

        self.cnv_life = tk.Canvas(
            master=self.app,
            width=self.width,
            height=self.height,
        )
        self.cnv_life.grid(row=1, column=0, columnspan=3)

        self.update_life(gol.create_rnd(self.life_size, 0.3))
        self.app.mainloop()


    def update_life(self, new_life: Optional[Life] = None) -> None:
        self.life = gol.next_gen(self.life) if new_life is None else new_life
        rows, cols = self.life.shape
        cell_width, cell_height = self.width / cols, self.height / rows
        self.cnv_life.delete(tk.ALL)
        for r in range(rows):
            for c in range(cols):
                self.cnv_life.create_rectangle(
                    r * cell_width, c * cell_height,
                    (r+1) * cell_width, (c+1) * cell_height,
                    fill=['black', 'white'][self.life[r, c]],
                )


    def control_loop_life(self) -> None:
        if not self.is_in_loop:
            self.is_in_loop = True
            self.btn_looplife.configure(text='Stop Loop')
            self.loop_life()
        else:
            self.is_in_loop = False
            self.btn_looplife.configure(text='Start Loop')


    def loop_life(self) -> None:
        if self.is_in_loop:
            self.update_life()
            self.app.after(100, self.loop_life)



app = GoLApp()
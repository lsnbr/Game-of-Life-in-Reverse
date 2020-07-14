import gol_tools as gol

import tkinter as tk
import numpy as np

from typing import Optional, Tuple
Life = np.ndarray



class GoLApp:

    def __init__(self) -> None:
        self.width, self.height = 512, 512
        self.life = None
        self.is_in_loop = False

        self.root = tk.Tk()
        self.root.title('Game of Life in Reverse')
        self.create_menubar()

        self.cnv_life = self.create_canvas_life()
        self.controls_left = self.create_controls_left()

        self.cnv_life.grid(row=0, column=0)
        self.controls_left.grid(row=1, column=0, sticky='nswe')

        self.update_life(gol.create_rnd(self.start_size, self.density))
        self.root.mainloop()

    
    @property
    def start_size(self) -> Tuple[int, int]:
        return (
            min(32, max(1, self.var_rows.get())),
            min(32, max(1, self.var_cols.get()))
        )

    @property
    def density(self) -> float:
        return min(1, max(0, self.var_density.get() / 100))


    def create_menubar(self) -> None:
        self.menu = tk.Menu(master=self.root)

        self.menu_file = tk.Menu(master=self.menu, tearoff=0)
        self.menu_file.add_command(label='Import', command=lambda: print('Import'))
        self.menu_file.add_command(label='Export', command=lambda: print('Export'))
        self.menu_file.add_separator()
        self.menu_file.add_command(label='Quit', command=self.root.destroy)

        self.menu_settings = tk.Menu(master=self.menu, tearoff=0)
        self.menu_geometry = tk.Menu(master=self.menu_settings, tearoff=0)
        self.var_geometry = tk.StringVar()
        self.var_geometry.set('Hard Edges')
        self.menu_geometry.add_radiobutton(
            label='Hard Edges',
            value='Hard Edges',
            variable=self.var_geometry)
        self.menu_geometry.add_radiobutton(
            label='Torus',
            value='Torus',
            variable=self.var_geometry)
        self.menu_settings.add_cascade(label='Geometry', menu=self.menu_geometry)

        self.menu.add_cascade(label='File', menu=self.menu_file)
        self.menu.add_cascade(label='Settings', menu=self.menu_settings)

        self.root.config(menu=self.menu)


    def create_controls_left(self) -> tk.Frame:
        frame_ctrl = tk.Frame(master=self.root)

        self.btn_nextgen = tk.Button(
            master=frame_ctrl,
            text='Next Gen',
            command=self.update_life,
            pady=5, padx=5)
        self.btn_looplife = tk.Button(
            master=frame_ctrl,
            text='Start Loop',
            command=self.control_loop_life,
            pady=5, padx=5)
        self.btn_clear = tk.Button(
            master=frame_ctrl,
            text='Clear',
            command=lambda: self.update_life(np.zeros(self.start_size, dtype=np.int8)),
            pady=5, padx=5)
        self.btn_random = tk.Button(
            master=frame_ctrl,
            text='Random',
            command=lambda: self.update_life(gol.create_rnd(self.start_size, self.density)),
            pady=5, padx=5)
        self.btn_nextgen.grid  (row=0, column=0, sticky='we')
        self.btn_looplife.grid (row=0, column=1, sticky='we')
        self.btn_clear.grid    (row=0, column=2, sticky='we')
        self.btn_random.grid   (row=0, column=3, sticky='we')

        self.label_stepsize = tk.Label(
            master=frame_ctrl,
            text='Step Size')
        self.scale_stepsize = tk.Scale(
            master=frame_ctrl,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL)
        self.scale_stepsize.set(1)
        self.scale_stepsize.grid(row=1, column=0)
        self.label_stepsize.grid(row=2, column=0)

        self.label_loopspeed = tk.Label(
            master=frame_ctrl,
            text='Speed')
        self.scale_loopspeed = tk.Scale(
            master=frame_ctrl,
            from_=50,
            to=2000,
            resolution=50,
            orient=tk.HORIZONTAL)
        self.scale_loopspeed.set(200)
        self.scale_loopspeed.grid(row=1, column=1)
        self.label_loopspeed.grid(row=2, column=1)

        self.var_rows, self.var_cols = tk.IntVar(), tk.IntVar()
        self.var_rows.set(8)
        self.var_cols.set(8)
        self.frame_rowxcol = tk.Frame(master=frame_ctrl)
        self.entry_rows = tk.Entry(
            master=self.frame_rowxcol,
            textvariable=self.var_rows,
            justify=tk.CENTER,
            width=8)
        self.entry_cols = tk.Entry(
            master=self.frame_rowxcol,
            textvariable=self.var_cols,
            justify=tk.CENTER,
            width=8)
        self.label_cxr = tk.Label(master=self.frame_rowxcol, text='x')
        self.entry_rows.grid(row=0, column=0)
        self.label_cxr.grid(row=0, column=1)
        self.entry_cols.grid(row=0, column=2)
        self.label_rowxcol = tk.Label(master=frame_ctrl, text='Size')
        self.frame_rowxcol.grid(row=1, column=2)
        self.label_rowxcol.grid(row=2, column=2)

        self.var_density = tk.IntVar()
        self.var_density.set(50)
        self.frame_density = tk.Frame(master=frame_ctrl)
        self.entry_density = tk.Entry(
            master=self.frame_density,
            textvariable=self.var_density,
            justify=tk.CENTER)
        self.label_percentage = tk.Label(master=self.frame_density, text='%')
        self.entry_density.grid(row=0, column=0)
        self.label_percentage.grid(row=0, column=1)
        self.label_density = tk.Label(master=frame_ctrl, text='Density')
        self.frame_density.grid(row=1, column=3)
        self.label_density.grid(row=2, column=3)

        return frame_ctrl


    def create_canvas_life(self) -> tk.Canvas:
        cnv = tk.Canvas(
            master=self.root,
            width=self.width,
            height=self.height,
        )
        return cnv


    def update_life(self, new_life: Optional[Life] = None) -> None:
        if new_life is None:
            self.life = gol.run_gens(
                life=self.life,
                gens=self.scale_stepsize.get(),
                geometry=self.var_geometry.get()
            )
        else:
            self.life = new_life
        rows, cols = self.life.shape
        cell_width, cell_height = self.width / cols, self.height / rows

        self.cnv_life.delete(tk.ALL)
        for r in range(rows):
            for c in range(cols):
                self.cnv_life.create_rectangle(
                    r * cell_width,     c * cell_height,
                    (r+1) * cell_width, (c+1) * cell_height,
                    fill=['black', 'white'][self.life[r, c]],
                )


    def control_loop_life(self) -> None:
        if self.is_in_loop:
            self.is_in_loop = False
            self.btn_looplife.configure(text='Start Loop')
        else:
            self.is_in_loop = True
            self.btn_looplife.configure(text='Stop Loop')
            self.loop_life()


    def loop_life(self) -> None:
        if self.is_in_loop:
            self.update_life()
            self.root.after(self.scale_loopspeed.get(), self.loop_life)



app = GoLApp()
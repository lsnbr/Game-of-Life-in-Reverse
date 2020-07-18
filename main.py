'''
todo:
- resizable canvas
- proogress indicator / algorithm visualization / log-life switch
- life 1.05 format
'''

from life_canvas import LifeCanvas
from life_files import *
from reverse_quad_gen import quad_gen
import gol_tools as gol

import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import os

from typing import Optional, Tuple, List
Life = np.ndarray



class GoLApp:

    filetypes = (
        ('Life 1.06', '*.life'),
        ('Life 1.05', '*.lif'),
    )

    def __init__(self) -> None:
        self.width, self.height = 420, 420
        self.is_in_loop = False

        self.root = tk.Tk()
        self.root.title('Game of Life in Reverse')

        self.controls_left    = self.create_controls_left()
        self.cnv_life_main    = self.create_life_main()
        self.controls_right   = self.create_controls_right()
        self.cnv_life_reverse = self.create_life_reverse()

        for r in range(2):
            self.root.rowconfigure(r, weight=1)
        for c in range(2):
            self.root.columnconfigure(c, weight=1)

        self.cnv_life_main.grid    (row=0, column=0, sticky='nswe')
        self.controls_left.grid    (row=1, column=0, sticky='nswe', padx=5, pady=2)
        self.cnv_life_reverse.grid (row=0, column=1, sticky='nswe')
        self.controls_right.grid   (row=1, column=1, sticky='ns'  , padx=5, pady=2)

        self.create_menubar()
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

    @property
    def stepsize(self) -> int:
        return self.scale_stepsize.get()

    @property
    def geometry(self) -> str:
        return self.var_geometry.get()

    @property
    def loopspeed(self) -> int:
        return self.scale_loopspeed.get()

    @property
    def reversed_lifes(self) -> List[Life]:
        if not hasattr(self, '_reversed_lifes'):
            self.reversed_lifes = []
        return self._reversed_lifes

    @reversed_lifes.setter
    def reversed_lifes(self, lifes: List[Life]) -> None:
        self._reversed_lifes = lifes
        if self.reversed_lifes:
            self.cnv_life_reverse.life = self.reversed_lifes[0]
        else:
            self.cnv_life_reverse.delete(tk.ALL)

        self.reversed_amount = len(self.reversed_lifes)
        self.var_reverse_count.set(1 if self.reversed_amount > 0 else 0)
        self.label_reverse.config(text=f'{self.reversed_amount} predecessors found.')
        self.spinbox_reverse.config(
            from_= 1 if self.reversed_amount > 0 else 0,
            to=self.reversed_amount
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
            self.cnv_life_main.next_gen(step=self.stepsize, geometry=self.geometry)
            self.root.after(self.loopspeed, self.loop_life)


    def reverse_life(self) -> None:
        if self.cnv_life_main.rows not in range(1, 17) or self.cnv_life_main.cols not in range(1, 17):
            messagebox.showerror(message='Reversing is only supported for\n1 <= rows <= 16\n1 <= cols <= 16')
            return
        self.reversed_lifes = quad_gen(self.cnv_life_main.life)


    def update_cnv_reversed(self, *_, **__) -> None:
        if not self.reversed_lifes:
            self.cnv_life_reverse.delete(tk.ALL)
        else:
            n = min(self.reversed_amount, max(1, self.var_reverse_count.get()))
            self.cnv_life_reverse.life = self.reversed_lifes[n - 1]


    def reverse_to_active(self) -> None:
        try:
            self.cnv_life_main.life = self.cnv_life_reverse.life
            self.var_rows.set(self.cnv_life_main.rows)
            self.var_cols.set(self.cnv_life_main.cols)
        except:
            pass


    def shrink_life(self) -> None:
        self.cnv_life_main.shrink()
        self.var_rows.set(self.cnv_life_main.rows)
        self.var_cols.set(self.cnv_life_main.cols)


    def export_file(self) -> None:
        with filedialog.asksaveasfile(
            mode='w',
            initialdir=os.getcwd(),
            defaultextension=GoLApp.filetypes[:1],
            filetypes=GoLApp.filetypes[:1]
        ) as file:

            ext = os.path.splitext(file.name)[1]
            to_save = self.cnv_life_main.life
            if ext == '.life':
                file.write(to_life106(to_save))
            elif ext == '.lif':
                file.write(to_life105(to_save))


    def import_file(self) -> None:
        with filedialog.askopenfile(
            mode='r',
            initialdir=os.getcwd(),
            filetypes=GoLApp.filetypes
        ) as file:

            ext = os.path.splitext(file.name)[1]
            if ext in ('.lif', '.life'):
                content = file.read()
                header = content.split('\n', 1)[0]
                if header == '#Life 1.05':
                    new_life = from_life105(content)
                elif header == '#Life 1.06':
                    new_life = from_life106(content)
                else:
                    raise Exception('Bad File.')
            
            self.cnv_life_main.life = new_life


    def filter_reversed(self, f: str) -> None:
        if   f == 'Fewest Alive Cells':
            self.reversed_lifes = gol.filter_least_cells(self.reversed_lifes)
        elif f == 'Most Alive Cells':
            self.reversed_lifes = gol.filter_most_cells(self.reversed_lifes)
        elif f == 'Smallest Bounding Box':
            self.reversed_lifes = gol.filter_bounding_box(self.reversed_lifes)
        else:
            raise Exception(f'No such filter option \'{f}\' is supported.')


    def create_life_main(self) -> LifeCanvas:
        cnv = LifeCanvas(
            master=self.root,
            width=self.width,
            height=self.height,
        )
        cnv.random(self.start_size, density=self.density)
        cnv.make_clickable()
        return cnv

    
    def create_life_reverse(self) -> LifeCanvas:
        cnv = LifeCanvas(
            master=self.root,
            width=self.width,
            height=self.height,
        )
        return cnv


    def create_menubar(self) -> None:
        self.menu = tk.Menu(master=self.root)

        # File Menu
        self.menu_file = tk.Menu(master=self.menu, tearoff=0)
        self.menu_file.add_command(label='Import', command=self.import_file)
        self.menu_file.add_command(label='Export', command=self.export_file)
        self.menu_file.add_separator()
        self.menu_file.add_command(label='Quit', command=self.root.destroy)

        # Settings Menu
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

        # Edit Menu
        self.menu_edit = tk.Menu(master=self.menu, tearoff=0)
        self.menu_edit.add_command(label='Reversed -> Active', command=self.reverse_to_active)
        self.menu_edit.add_command(label='Shrink Pattern', command=self.shrink_life)
        self.menu_filter = tk.Menu(master=self.menu_edit, tearoff=0)
        self.menu_filter.add_command(
            label='Fewest Alive Cells',
            command=lambda: self.filter_reversed('Fewest Alive Cells'))
        self.menu_filter.add_command(
            label='Most Alive Cells',
            command=lambda: self.filter_reversed('Most Alive Cells'))
        self.menu_filter.add_command(
            label='Smallest Bounding Box',
            command=lambda: self.filter_reversed('Smallest Bounding Box'))
        self.menu_edit.add_cascade(label='Filter Results', menu=self.menu_filter)

        # Build main menu
        self.menu.add_cascade(label='File', menu=self.menu_file)
        self.menu.add_cascade(label='Settings', menu=self.menu_settings)
        self.menu.add_cascade(label='Edit', menu=self.menu_edit)

        self.root.config(menu=self.menu)


    def create_controls_left(self) -> tk.Frame:
        frame_ctrl = tk.Frame(master=self.root)

        # Four buttons in row 0
        self.btn_nextgen = tk.Button(
            master=frame_ctrl,
            text='Next Gen',
            command=lambda: self.cnv_life_main.next_gen(self.stepsize, self.geometry),
            pady=5, padx=5)
        self.btn_looplife = tk.Button(
            master=frame_ctrl,
            text='Start Loop',
            command=self.control_loop_life,
            pady=5, padx=5)
        self.btn_clear = tk.Button(
            master=frame_ctrl,
            text='Clear',
            command=lambda: self.cnv_life_main.clean(self.start_size),
            pady=5, padx=5)
        self.btn_random = tk.Button(
            master=frame_ctrl,
            text='Random',
            command=lambda: self.cnv_life_main.random(self.start_size, self.density),
            pady=5, padx=5)
        
        self.btn_nextgen.grid  (row=0, column=0, sticky='nswe')
        self.btn_looplife.grid (row=0, column=1, sticky='nswe')
        self.btn_clear.grid    (row=0, column=2, sticky='nswe')
        self.btn_random.grid   (row=0, column=3, sticky='nswe')

        # Label + Scale for controlling stepsize
        self.label_stepsize = tk.Label(
            master=frame_ctrl,
            text='Step Size')
        self.scale_stepsize = tk.Scale(
            master=frame_ctrl,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL)
        self.scale_stepsize.set(1)

        self.scale_stepsize.grid(row=1, column=0, sticky='nswe')
        self.label_stepsize.grid(row=2, column=0, sticky='nswe')

        # Label + Scale for controlling loopspeed
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

        self.scale_loopspeed.grid(row=1, column=1, sticky='nswe')
        self.label_loopspeed.grid(row=2, column=1, sticky='nswe')

        # Label + Entries for controlling starting grid size
        self.var_rows, self.var_cols = tk.IntVar(), tk.IntVar()
        self.var_rows.set(6)
        self.var_cols.set(6)
        self.label_rowxcol = tk.Label(master=frame_ctrl, text='Size')
        self.frame_rowxcol = tk.Frame(master=frame_ctrl)

        self.entry_rows = tk.Entry(
            master=self.frame_rowxcol,
            textvariable=self.var_rows,
            justify=tk.CENTER,
            width=6)
        self.entry_cols = tk.Entry(
            master=self.frame_rowxcol,
            textvariable=self.var_cols,
            justify=tk.CENTER,
            width=6)
        self.label_cxr = tk.Label(master=self.frame_rowxcol, text='x')

        self.entry_rows.grid(row=0, column=0, ipady=1, sticky='we')
        self.label_cxr.grid(row=0, column=1, padx=1, sticky='we')
        self.entry_cols.grid(row=0, column=2, ipady=1, sticky='we')
        self.frame_rowxcol.rowconfigure(0, weight=1)
        for c in range(3):
            self.frame_rowxcol.columnconfigure(c, weight=1)

        self.frame_rowxcol.grid(row=1, column=2, sticky='nswe')
        self.label_rowxcol.grid(row=2, column=2, sticky='nswe')

        # Label + Entry for controlling starting cell density
        self.var_density = tk.IntVar()
        self.var_density.set(50)
        self.label_density = tk.Label(master=frame_ctrl, text='Density')
        self.frame_density = tk.Frame(master=frame_ctrl)

        self.entry_density = tk.Entry(
            master=self.frame_density,
            textvariable=self.var_density,
            justify=tk.CENTER,
            width=12)
        self.label_percentage = tk.Label(master=self.frame_density, text='%')

        self.entry_density.grid(row=0, column=0, ipady=1, padx=5, sticky='we')
        self.label_percentage.grid(row=0, column=1, sticky='we')
        self.frame_density.rowconfigure(0, weight=1)
        for c in range(2):
            self.frame_density.columnconfigure(c, weight=1)

        self.frame_density.grid(row=1, column=3, sticky='nswe')
        self.label_density.grid(row=2, column=3, sticky='nswe')

        # Final row and column config
        for r in range(3):
            frame_ctrl.rowconfigure(r, weight=1)
        for c in range(4):
            frame_ctrl.columnconfigure(c, weight=1)

        return frame_ctrl


    def create_controls_right(self) -> tk.Frame:
        frame_ctrl = tk.Frame(master=self.root)

        self.btn_reverse = tk.Button(
            master=frame_ctrl,
            text='Reverse',
            command=self.reverse_life,
            pady=5, padx=5)

        self.var_reverse_count = tk.IntVar()
        self.var_reverse_count.set(0)
        self.var_reverse_count.trace('w', self.update_cnv_reversed)
        self.spinbox_reverse = tk.Spinbox(
            master=frame_ctrl,
            from_=0,
            to=0,
            justify=tk.CENTER,
            textvariable=self.var_reverse_count,
        )

        self.label_reverse = tk.Label(
            master=frame_ctrl,
            text='No predecessors calculated yet.',
        )
            
        self.btn_reverse.grid     (row=0, column=0, sticky='nwe', padx=5)
        self.spinbox_reverse.grid (row=0, column=1, sticky='nwe', padx=5, ipady=7)
        self.label_reverse.grid   (row=0, column=2, sticky='nwe', padx=5)

        # Final row and column config
        for r in range(1):
            frame_ctrl.rowconfigure(r, weight=1)
        for c in range(3):
            frame_ctrl.columnconfigure(c, weight=1)

        return frame_ctrl




app = GoLApp()
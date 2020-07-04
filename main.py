from gol_tools import create_rnd, next_gen

import tkinter as tk


def update_gol(new_life=None):
    global life
    life = next_gen(life) if new_life is None else new_life
    for r in range(life.shape[0]):
        for c in range(life.shape[1]):
            tk.Frame(
                master=frame_gol,
                bg=['black', 'white'][life[r, c]],
            ).grid(row=r, column=c, sticky='nswe')

def loop_gol():
    update_gol()
    window.after(200, loop_gol)


window = tk.Tk()
window.title('Game of Life in Reverse')
size = (20, 20)

btn_nextgen = tk.Button(
    master=window,
    text='Next Gen',
    command=update_gol,
)
btn_nextgen.pack(fill=tk.BOTH, expand=True)
btn_startloop = tk.Button(
    master=window,
    text='Start Loop',
    command=loop_gol,
)
btn_startloop.pack(fill=tk.BOTH, expand=True)

frame_gol = tk.Frame(
    master=window,
)
frame_gol.rowconfigure(list(range(size[0])), weight=1, minsize=32)
frame_gol.columnconfigure(list(range(size[1])), weight=1, minsize=32)
frame_gol.pack(fill=tk.BOTH, expand=True)
update_gol(create_rnd(size, density=0.3))


window.mainloop()
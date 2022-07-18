from tkinter import *
from tkinter import ttk

from HAF import __version__ as HAFVersion

window = Tk()
window.title('HAF ' + HAFVersion)
window.geometry('800x600')

tabControl = ttk.Notebook(window)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text = 'Call Visualizer')
tabControl.add(tab2, text = 'Template Editor')
tabControl.pack(expand = 1, fill = 'both')

ttk.Label(
    tab1,
    text = 'TODO'
).grid(
    column = 0,
    row = 0,
    padx = 50,
    pady = 50
)
ttk.Label(
    tab2,
    text = 'TODO'
).grid(
    column = 0,
    row = 0,
    padx = 50,
    pady = 50
)

window.mainloop()

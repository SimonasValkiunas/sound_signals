import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class ChartBuilder:
    def __init__(self, xs,  ys, fig, canvas, type = "def"):
        self.xs = xs
        self.ys = ys
        self.fig = fig
        self.canvas = canvas
        self.segxs = []
        self.type = type
    
    def draw(self):
        if self.type == "def":
            for i,s in enumerate(self.ys):
                id = (100 * len(self.ys)) + 11 + i
                self.fig.add_subplot(id).plot(
                    self.xs,
                    s
                )

        if self.type == "bitmap":
            for i,s in enumerate(self.ys):
                id = (100 * len(self.ys)) + 11 + i
                ax = self.fig.add_subplot(id)
                t = np.arange(len(s[1]))
                print(s[0])
                pcm = ax.pcolormesh(t,s[0],np.log10(abs(s[2])+1))
                self.fig.colorbar(pcm, ax=ax)
        
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=1
        )


        
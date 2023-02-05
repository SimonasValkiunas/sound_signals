import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def on_click(event):
    # Code to execute on click event
    print("Mouse clicked at", event.x, event.y)

root = tk.Tk()

fig = plt.figure()
ax = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Connect the click event
canvas.mpl_connect("button_press_event", on_click)

tk.mainloop()
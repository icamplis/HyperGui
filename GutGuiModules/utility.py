from tkinter import *
from GutGuiModules.constants import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib import pyplot as plt


def init():
    root = Tk()
    root.resizable(width=False, height=False)
    root.title(WINDOW_TITLE)
    root.geometry("+0+0")
    window = Frame(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    window.pack()
    return window

def tkcolour_from_rgb(rgb):
    '''translates an rgb tuple of int to a tkinter friendly color code'''
    return "#%02x%02x%02x" % rgb

def frame_and_label(window, name, colour, row, column, rowspan, columnspan, labelspan=1):
    frame = Frame(window, bg=tkcolour_from_rgb(colour))
    frame.grid(row=row, rowspan=rowspan, column=column, columnspan=columnspan, sticky=W+E+N+S)
    label = make_label(frame, text=name, row=0, column=0, borderwidth=2, columnspan=labelspan)
    return frame, label

def make_button(window, text, command, row, column, height=1, width=10, 
    inner_padx=10, inner_pady=10, outer_padx=0, outer_pady=0, columnspan=1, rowspan=1):
    button = Button(window, text=text, command=command, padx=inner_padx, pady=inner_pady, height=height, width=width)
    button.grid(row=row, column=column, padx=outer_padx, pady=outer_pady, columnspan=columnspan, rowspan=rowspan)
    return button

def make_label(window, text, row, column,
               borderwidth=2, inner_padx=1, inner_pady=1, outer_padx=0, outer_pady=15,
               relief="solid", rowspan=1, columnspan=1, wraplength=160):
    label = Label(window, text=text, borderwidth=borderwidth, relief=relief,
                  padx=inner_padx, pady=inner_pady, wraplength=wraplength)
    label.grid(row=row, column=column, padx=outer_padx, pady=outer_pady, columnspan=columnspan, rowspan=rowspan)
    return label

def make_text(window, content, row, column, padx=10, pady=10, height=1, width=2,
              highlightthickness=0, bg="white", columnspan=1,  rowspan=1):
    text = Text(window, bg=bg, height=height, width=width, highlightthickness=highlightthickness)
    text.insert(END, content)
    text.config(state=DISABLED)
    text.grid(row=row, column=column, padx=padx, pady=pady, columnspan=columnspan, rowspan=rowspan)
    return text

def make_listbox(window, input, row, column, padx=15, pady=(0, 15),
                 highlightthickness=0, columnspan=1,  rowspan=1):
    listbox = Listbox(window, width=15, highlightthickness=highlightthickness, selectmode=SINGLE)
    listbox.grid(row=row, column=column, padx=padx, pady=pady, rowspan=rowspan, columnspan=columnspan)
    return listbox

def make_entry(window, row, column, width, columnspan=1, pady=10, 
    padx=10, highlightthickness=0, command=None):
    entry = Entry(window, width=width, highlightthickness=highlightthickness, textvariable=StringVar())
    entry.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady)
    return entry

def make_checkbox(window, text, row, column, var, columnspan=1,
                  inner_padx=1, inner_pady=1, outer_padx=0, outer_pady=0, bg="yellow", sticky=W+N+S+E):
    checkbox = Checkbutton(window, text=text, variable=var, padx=inner_padx, pady=inner_pady, bg=bg, width=2)
    checkbox.grid(row=row, column=column, padx=outer_padx, pady=outer_pady, sticky=sticky, columnspan=columnspan)
    return checkbox

def make_graph(master, x_vals, y_vals, row, column, x_size, y_size, colour, x_upper=None, x_lower=None, y_upper=None, y_lower=None, inner_pady=0, inner_padx=0, rowspan=1, columnspan=1):
    figure = Figure(figsize=(x_size, y_size))
    axes = figure.add_subplot(111)
    axes.plot(x_vals, y_vals)
    figure.patch.set_facecolor(rgb_to_rgba(colour))
    figure.set_tight_layout(True)
    axes.set_xlim(left=x_lower, right=x_upper)
    axes.set_ylim(bottom=y_lower, top=y_upper)
    canvas = FigureCanvasTkAgg(figure, master=master)
    canvas.draw()
    canvas.get_tk_widget().grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, ipady=inner_pady, ipadx=inner_padx)
    return canvas

def rgb_to_rgba(rgb):
    r = rgb[0]/255
    g = rgb[1]/255
    b = rgb[2]/255
    return (r, g, b)





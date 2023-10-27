import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

color_codes = {
    "black": (0, None),
    "brown": (1, 1),
    "red": (2, 2),
    "orange": (3, 0.05),
    "yellow": (4, 0.02),
    "green": (5, 0.5),
    "blue": (6, 0.25),
    "violet": (7, 0.1),
    "gray": (8, 0.01),
    "white": (9, None),
    "gold": (None, 5),
    "silver": (None, 10),
}

def calculate_resistance():
    band1_color = band1_combobox.get()
    band2_color = band2_combobox.get()
    band3_color = band3_combobox.get()
    band4_color = band4_combobox.get()

    notation = notation_combobox.get()

    resistance = 0  # Initialize with a default value

    if notation == "4 Bands":
        if band1_color == '' or band2_color == '' or band3_color == '' or band4_color == '':
            resistance_label.config(text="Resistance: N/A")
            tolerance_label.config(text="Tolerance: N/A")
            return

        resistance = (color_codes[band1_color][0] * 10 + color_codes[band2_color][0]) * 10 ** color_codes[band3_color][
            0]
        tolerance = str(color_codes[band4_color][1]) + "%"
    elif notation == "5 Bands":
        band5_color = band5_combobox.get()

        if band1_color == '' or band2_color == '' or band3_color == '' or band4_color == '' or band5_color == '':
            resistance_label.config(text="Resistance: N/A")
            tolerance_label.config(text="Tolerance: N/A")
            return

        resistance = (color_codes[band1_color][0] * 100 + color_codes[band2_color][0] * 10 + color_codes[band3_color][
            0]) * 10 ** color_codes[band4_color][0]
        tolerance = str(color_codes[band5_color][1]) + "%"

    resistance_label.config(text=f"Resistance: {resistance:.2f} Ω")
    tolerance_label.config(text=f"Tolerance: {tolerance}")

root = tk.Tk()
# setting window size
width = 600
height = 500
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)

root.title("Resistor Calculator")
root.resizable(width=False, height=False)

notation_combobox = ttk.Combobox(root, values=["4 Bands", "5 Bands"])
notation_combobox.current(1)
notation_combobox.place(x=310, y=60, width=170, height=32)

notation_label=tk.Label(root)
ft = tkFont.Font(family='Times',size=16)
notation_label["font"] = ft
notation_label["fg"] = "#333333"
notation_label["justify"] = "center"
notation_label["text"] = "Number of Bands: "
notation_label.place(x=100,y=60,width=163,height=36)

band1_label = tk.Label(root)
ft = tkFont.Font(family='Times', size=16)
band1_label["font"] = ft
band1_label["fg"] = "#333333"
band1_label["justify"] = "center"
band1_label["text"] = "Band 1"
band1_label.place(x=110, y=140, width=158, height=32)

band2_label = tk.Label(root)
ft = tkFont.Font(family='Times', size=16)
band2_label["font"] = ft
band2_label["fg"] = "#333333"
band2_label["justify"] = "center"
band2_label["text"] = "Band 2"
band2_label.place(x=110, y=190, width=158, height=32)

band3_label = tk.Label(root)
ft = tkFont.Font(family='Times', size=16)
band3_label["font"] = ft
band3_label["fg"] = "#333333"
band3_label["justify"] = "center"
band3_label["text"] = "Band 3"
band3_label.place(x=110, y=240, width=158, height=32)

band4_label = tk.Label(root)
ft = tkFont.Font(family='Times', size=16)
band4_label["font"] = ft
band4_label["fg"] = "#333333"
band4_label["justify"] = "center"
band4_label["text"] = "Band 4"
band4_label.place(x=110, y=290, width=158, height=32)

band5_label = tk.Label(root)
ft = tkFont.Font(family='Times', size=16)
band5_label["font"] = ft
band5_label["fg"] = "#333333"
band5_label["justify"] = "center"
band5_label["text"] = "Band 5"
band5_label.place(x=110, y=340, width=158, height=32)

resistance_label = tk.Label(root)
ft = tkFont.Font(family='Times', size=14)
resistance_label["font"] = ft
resistance_label["fg"] = "#333333"
resistance_label["justify"] = "center"
resistance_label["text"] = "Resistance:"
resistance_label.place(x=80, y=410, width=320, height=32)

tolerance_label = tk.Label(root)
ft = tkFont.Font(family='Times', size=14)
tolerance_label["font"] = ft
tolerance_label["fg"] = "#333333"
tolerance_label["justify"] = "center"
tolerance_label["text"] = "Tolerance:"
tolerance_label.place(x=360, y=410, width=180, height=30)

band1_combobox = ttk.Combobox(root, values=list(color_codes.keys()))
band1_combobox.place(x=310, y=140, width=170, height=32)

band2_combobox = ttk.Combobox(root, values=list(color_codes.keys()))
band2_combobox.place(x=310, y=190, width=170, height=32)

band3_combobox = ttk.Combobox(root, values=list(color_codes.keys()))
band3_combobox.place(x=310, y=240, width=170, height=32)

band4_combobox = ttk.Combobox(root, values=list(color_codes.keys()))
band4_combobox.place(x=310, y=290, width=170, height=32)

band5_combobox = ttk.Combobox(root, values=list(color_codes.keys()))
band5_combobox.place(x=310, y=340, width=170, height=32)

calculate_button = ttk.Button(root, text="Calculate", command=calculate_resistance)
calculate_button["text"] = "Calculate"
calculate_button.place(x=270, y=460, width=100, height=32)


def handle_notation_selection(event):
    selected_option = notation_combobox.get()
    if selected_option == "5 Bands":
        band5_label.place(x=110, y=340, width=158, height=32)
        band5_combobox.place(x=310, y=340, width=170, height=32)
    else:
        band5_label.place_forget()
        band5_combobox.place_forget()


notation_combobox.bind("<<ComboboxSelected>>", handle_notation_selection)

root.mainloop()

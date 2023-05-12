import tkinter as tk
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

    if notation == "4-band":
        if band1_color == '' or band2_color == '' or band3_color == '' or band4_color == '':
            resistance_label.config(text="Resistance: N/A")
            tolerance_label.config(text="Tolerance: N/A")
            return

        resistance = (color_codes[band1_color][0] * 10 + color_codes[band2_color][0]) * 10 ** color_codes[band3_color][
            0]
        tolerance = str(color_codes[band4_color][1]) + "%"
    elif notation == "5-band":
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
root.title("Resistor Calculator")
root.geometry(f"310x420")

logo_file = "icon.png"
if os.path.exists(logo_file):
    logo = PhotoImage(file=logo_file)
    root.wm_iconphoto(True, logo)

# Style
## Define font size
fnt_size = 16
style = ttk.Style(root)
style.configure('.', font=('Arial', fnt_size))

notation_label = ttk.Label(root, text="Notation:")
notation_label.grid(row=0, column=0, padx=10, pady=40, sticky=tk.W)

notation_combobox = ttk.Combobox(root, values=["4-band", "5-band"])
notation_combobox.current(1)
notation_combobox.grid(row=0, column=1, padx=10, pady=40)

band1_label = ttk.Label(root, text="Band 1:")
band1_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

band1_combobox = ttk.Combobox(root, values=list(color_codes.keys()))
band1_combobox.grid(row=1, column=1, padx=10, pady=5)

band2_label = ttk.Label(root, text="Band 2:")
band2_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

band2_combobox = ttk.Combobox(root, values=list(color_codes.keys()))
band2_combobox.grid(row=2, column=1, padx=10, pady=5)

band3_label = ttk.Label(root, text="Band 3:")
band3_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

band3_combobox = ttk.Combobox(root, values=list(color_codes.keys()))
band3_combobox.grid(row=3, column=1, padx=10, pady=5)

band4_label = ttk.Label(root, text="Band 4:")
band4_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

band4_combobox = ttk.Combobox(root, values=list(color_codes.keys()))
band4_combobox.grid(row=4, column=1, padx=10, pady=5)

band5_label = ttk.Label(root, text="Band 5:")
band5_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

band5_combobox = ttk.Combobox(root, values=list(color_codes.keys()))
band5_combobox.grid(row=5, column=1, padx=10, pady=5)

calculate_button = ttk.Button(root, text="Calculate", command=calculate_resistance)
calculate_button.grid(row=6, columnspan=2, padx=10, pady=5)

resistance_label = ttk.Label(root, text="Resistance:")
resistance_label.grid(row=7, columnspan=2, padx=10, pady=5)

tolerance_label = ttk.Label(root, text="Tolerance:")
tolerance_label.grid(row=8, columnspan=2, padx=10, pady=5)


def handle_notation_selection(event):
    selected_option = notation_combobox.get()
    if selected_option == "5-band":
        band5_label.grid()
        band5_combobox.grid()
    else:
        band5_label.grid_remove()
        band5_combobox.grid_remove()


notation_combobox.bind("<<ComboboxSelected>>", handle_notation_selection)

root.mainloop()

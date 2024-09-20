import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import messagebox

# Color codes dictionary
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


# Font initialization for labels
def initialize_font(size=16):
    return tkFont.Font(family='Times', size=size)


# Helper function to format resistance values
def format_resistance(value):
    if value >= 1e6:
        return f"{value / 1e6:.2f} MΩ"
    elif value >= 1e3:
        return f"{value / 1e3:.2f} kΩ"
    else:
        return f"{value:.2f} Ω"


# Resistance calculation function
def calculate_resistance():
    band1_color = band1_combobox.get()
    band2_color = band2_combobox.get()
    band3_color = band3_combobox.get()
    band4_color = band4_combobox.get()
    notation = notation_combobox.get()

    if notation == "4 Bands":
        if not all([band1_color, band2_color, band3_color, band4_color]):
            resistance_label.config(text="Resistance: N/A")
            tolerance_label.config(text="Tolerance: N/A")
            resistance_range_label.config(text="")
            return

        resistance = (color_codes[band1_color][0] * 10 + color_codes[band2_color][0]) * 10 ** color_codes[band3_color][
            0]
        tolerance = color_codes[band4_color][1]
    elif notation == "5 Bands":
        band5_color = band5_combobox.get()

        if not all([band1_color, band2_color, band3_color, band4_color, band5_color]):
            resistance_label.config(text="Resistance: N/A")
            tolerance_label.config(text="Tolerance: N/A")
            resistance_range_label.config(text="")
            return

        resistance = (color_codes[band1_color][0] * 100 + color_codes[band2_color][0] * 10 + color_codes[band3_color][
            0]) * 10 ** color_codes[band4_color][0]
        tolerance = color_codes[band5_color][1]

    # Display resistance and tolerance
    formatted_resistance = format_resistance(resistance)
    resistance_label.config(text=f"Resistance: {formatted_resistance}")
    tolerance_label.config(text=f"Tolerance: ±{tolerance}%")

    # Calculate the potential resistance range
    min_resistance = resistance * (1 - tolerance / 100)
    max_resistance = resistance * (1 + tolerance / 100)

    # Display resistance range
    resistance_range_label.config(
        text=f"Resistance Range: {format_resistance(min_resistance)} - {format_resistance(max_resistance)}"
    )


# Menu bar functions
def show_help():
    help_text = (
        "Resistor Calculator Usage:\n\n"
        "1. Select the number of bands on your resistor (4 or 5).\n"
        "2. For each band, select the corresponding color from the dropdown menus.\n"
        "   - Band 1: First significant figure.\n"
        "   - Band 2: Second significant figure.\n"
        "   - Band 3 (only for 5-band resistors): Third significant figure.\n"
        "   - Band 4: Multiplier.\n"
        "   - Band 5: Tolerance (if 5 bands).\n"
        "3. Press the 'Calculate' button to view the resistance and tolerance.\n\n"
        "How to Determine the First Color Band:\n"
        "- The first band is typically located closer to one end of the resistor.\n"
        "- The tolerance band (gold, silver, or none) is usually separated by more space from the other bands and is often positioned on the far right.\n"
        "- Hold the resistor so that the tolerance band is on the right. The first color band will be on the far left.\n"
        "- For resistors with 5 bands, the first three bands represent significant figures, and the last two are the multiplier and tolerance.\n\n"
    )
    messagebox.showinfo("Help - Resistor Calculator", help_text)


def show_about():
    about_text = (
        "Resistor Calculator v2.012\n\n"
        "Developed by Kaotick Jay\n"
        "GitHub: https://github.com/kaotickj\n"
        "Website: https://kdgwebsolutions.com\n"
    )
    messagebox.showinfo("About", about_text)


# Initialize tkinter root
root = tk.Tk()
width, height = 600, 550
screenwidth, screenheight = root.winfo_screenwidth(), root.winfo_screenheight()
alignstr = f'{width}x{height}+{(screenwidth - width) // 2}+{(screenheight - height) // 2}'
root.geometry(alignstr)
root.title("Resistor Calculator")
root.resizable(width=False, height=False)

# Menu bar creation
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Usage Instructions", command=show_help)

about_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="About this program", command=show_about)

# Combobox for notation selection (4 or 5 bands)
notation_combobox = ttk.Combobox(root, values=["4 Bands", "5 Bands"])
notation_combobox.current(0)
notation_combobox.place(x=310, y=60, width=170, height=32)

notation_label = tk.Label(root, text="Number of Bands:", font=initialize_font(16), fg="#333333", justify="center")
notation_label.place(x=100, y=60, width=163, height=36)

# Labels and comboboxes for each band
band_labels = ["Band 1", "Band 2", "Band 3", "Band 4", "Band 5"]
band_comboboxes = {}

for i, band in enumerate(band_labels[:4]):  # Only set up the first 4 bands by default
    label = tk.Label(root, text=band, font=initialize_font(16), fg="#333333", justify="center")
    label.place(x=110, y=140 + 50 * i, width=158, height=32)

    combobox = ttk.Combobox(root, values=list(color_codes.keys()))
    combobox.place(x=310, y=140 + 50 * i, width=170, height=32)
    band_comboboxes[band] = combobox

# Reference to each combobox
band1_combobox = band_comboboxes["Band 1"]
band2_combobox = band_comboboxes["Band 2"]
band3_combobox = band_comboboxes["Band 3"]
band4_combobox = band_comboboxes["Band 4"]

# Band 5 components (hidden on startup)
band5_label = tk.Label(root, text="Band 5", font=initialize_font(16), fg="#333333", justify="center")
band5_combobox = ttk.Combobox(root, values=list(color_codes.keys()))

# Label for displaying resistance
resistance_label = tk.Label(root, text="Resistance:", font=initialize_font(14), fg="#333333", justify="center")
resistance_label.place(x=80, y=410, width=320, height=32)

# Label for displaying tolerance
tolerance_label = tk.Label(root, text="Tolerance:", font=initialize_font(14), fg="#333333", justify="center")
tolerance_label.place(x=360, y=410, width=180, height=30)

# New label for showing the resistance range, centered in the main window
resistance_range_label = tk.Label(root, text="", font=("Arial", 12), justify="center")
resistance_range_label.place(x=150, y=450, width=300, height=32)

# Button for triggering the calculation
calculate_button = ttk.Button(root, text="Calculate", command=calculate_resistance)
calculate_button.place(x=270, y=490, width=100, height=30)


# Event listener for combobox change
def on_notation_change(event):
    if notation_combobox.get() == "5 Bands":
        band5_label.place(x=110, y=340, width=158, height=32)
        band5_combobox.place(x=310, y=340, width=170, height=32)
    else:
        band5_label.place_forget()
        band5_combobox.place_forget()


notation_combobox.bind("<<ComboboxSelected>>", on_notation_change)

# Run the tkinter main loop
root.mainloop()

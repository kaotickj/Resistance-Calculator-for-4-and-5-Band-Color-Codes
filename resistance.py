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

# Tooltip class
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify="left",
                         background="#ffffe0", relief="solid", borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

# Font initialization for labels
def initialize_font(size=16):
    return tkFont.Font(family='Arial', size=size)

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
            resistance_label.config(text="")
            tolerance_label.config(text="")
            resistance_range_label.config(text="")
            return

        resistance = (color_codes[band1_color][0] * 10 + color_codes[band2_color][0]) * 10 ** color_codes[band3_color][0]
        tolerance = color_codes[band4_color][1]
    elif notation == "5 Bands":
        band5_color = band5_combobox.get()

        if not all([band1_color, band2_color, band3_color, band4_color, band5_color]):
            resistance_label.config(text="")
            tolerance_label.config(text="")
            resistance_range_label.config(text="")
            return

        resistance = (color_codes[band1_color][0] * 100 + color_codes[band2_color][0] * 10 + color_codes[band3_color][0]) * 10 ** color_codes[band4_color][0]
        tolerance = color_codes[band5_color][1]

    formatted_resistance = format_resistance(resistance)
    resistance_label.config(text=f"Resistance: {formatted_resistance}", fg="blue")
    tolerance_label.config(text=f"Tolerance: ±{tolerance}%", fg="blue")

    min_resistance = resistance * (1 - tolerance / 100)
    max_resistance = resistance * (1 + tolerance / 100)

    resistance_range_label.config(
        text=f"Resistance Range: {format_resistance(min_resistance)} - {format_resistance(max_resistance)}",
        fg="blue"
    )

# Menu bar functions
def show_help():
    help_text = (
        "Resistor Calculator Usage:\n\n"
        "1. Select the number of bands on your resistor (4 or 5).\n"
        "\n"
        "For 4-Band Resistors:\n"
        "2. Select the corresponding color for each band from the dropdown menus:\n"
        "   - Band 1: First significant figure.\n"
        "   - Band 2: Second significant figure.\n"
        "   - Band 3: Multiplier.\n"
        "   - Band 4: Tolerance.\n"
        "\n"
        "For 5-Band Resistors:\n"
        "2. Select the corresponding color for each band from the dropdown menus:\n"
        "   - Band 1: First significant figure.\n"
        "   - Band 2: Second significant figure.\n"
        "   - Band 3: Third significant figure.\n"
        "   - Band 4: Multiplier.\n"
        "   - Band 5: Tolerance.\n"
        "\n"
        "3. Press the 'Calculate' button to view the resistance and tolerance.\n\n"
        "How to Determine the First Color Band:\n"
        "- The first band is typically located closer to one end of the resistor.\n"
        "- The tolerance band (gold, silver, or none) is usually separated by more space from the other bands and is often positioned on the far right.\n"
        "- Hold the resistor so that the tolerance band is on the right. The first color band will be on the far left.\n"
        "- For resistors with 5 bands, the first three bands represent significant figures, while the last two are the multiplier and tolerance.\n\n"
    )

    messagebox.showinfo("Help - Resistor Calculator", help_text)

def show_about():
    about_text = (
        "Resistor Calculator v2.1.12\n\n"
        "Developed by KaotickJ\n"
        "https://github.com/kaotickj\n"
    )
    messagebox.showinfo("About", about_text)

# Initialize tkinter root
root = tk.Tk()
width, height = 600, 600
screenwidth, screenheight = root.winfo_screenwidth(), root.winfo_screenheight()
alignstr = f'{width}x{height}+{(screenwidth - width) // 2}+{(screenheight - height) // 2}'
root.geometry(alignstr)
root.title("Ω Resistor Calculator")
root.configure(bg="#f0f0f0")
root.resizable(width=False, height=False)

# Top label with colored background
header_label = tk.Label(root, text="Ω Resistor Color Code Calculator", font='Arial 14 bold', bg="#f0f0f0", fg="blue", padx=10, pady=5)
header_label.place(relx=0.5, rely=0.055, anchor='center')

# Menu bar creation
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

help_menu = tk.Menu(menu_bar, tearoff=0, bg="green", fg="white")
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Usage Instructions", command=show_help)

about_menu = tk.Menu(menu_bar, tearoff=0, bg="green", fg="white")
menu_bar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="About this program", command=show_about)

# Combobox for notation selection (4 or 5 bands)
notation_combobox = ttk.Combobox(root, values=["4 Bands", "5 Bands"])
notation_combobox.current(0)
notation_combobox.place(x=310, y=60, width=170, height=32)
ToolTip(notation_combobox, "Select the number of bands on your resistor.")

notation_label = tk.Label(root, text="Number of Bands:", font=initialize_font(16), fg="#333333", bg="#f0f0f0")
notation_label.place(x=100, y=60, width=170, height=36)
ToolTip(notation_label, "Number of color bands on the resistor.")

# Labels and comboboxes for each band
band_labels = ["Band 1", "Band 2", "Band 3", "Band 4", "Band 5"]
band_comboboxes = {}

for i, band in enumerate(band_labels[:4]):  # Only set up the first 4 bands by default
    label = tk.Label(root, text=band, font=initialize_font(16), fg="#333333", bg="#f0f0f0")
    label.place(x=110, y=140 + 50 * i, width=158, height=32)
    ToolTip(label, f"Select color for {band}.")

    combobox = ttk.Combobox(root, values=list(color_codes.keys()))
    combobox.place(x=310, y=140 + 50 * i, width=170, height=32)
    band_comboboxes[band] = combobox
    ToolTip(combobox, f"Select color for {band}.")

# Reference to specific band comboboxes
band1_combobox = band_comboboxes["Band 1"]
band2_combobox = band_comboboxes["Band 2"]
band3_combobox = band_comboboxes["Band 3"]
band4_combobox = band_comboboxes["Band 4"]

# Additional band 5 setup (for 5-band notation)
band5_label = tk.Label(root, text="Band 5", font=initialize_font(16), fg="#333333", bg="#f0f0f0")
band5_combobox = ttk.Combobox(root, values=list(color_codes.keys()))

ToolTip(band5_label, "Select color for Band 5 (tolerance).")
ToolTip(band5_combobox, "Select color for Band 5 (tolerance).")

# Result labels for resistance and tolerance
resistance_label = tk.Label(root, text="", font=initialize_font(14), fg="blue", bg="#f0f0f0", justify="center")
resistance_label.place(x=110, y=400, width=400, height=32)

tolerance_label = tk.Label(root, text="", font=initialize_font(14), fg="blue", bg="#f0f0f0", justify="center")
tolerance_label.place(x=110, y=440, width=400, height=32)

resistance_range_label = tk.Label(root, text="", font=initialize_font(14), fg="blue", bg="#f0f0f0", justify="center")
resistance_range_label.place(x=110, y=470, width=400, height=32)

# Calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate_resistance, font=initialize_font(14), bg="green", fg="white")
calculate_button.place(x=230, y=520, width=150, height=36)

# Event handler for updating band comboboxes
def update_band_comboboxes(event):
    if notation_combobox.get() == "4 Bands":
        band5_label.place_forget()
        band5_combobox.place_forget()
    else:
        band5_label.place(x=110, y=340, width=158, height=32)
        band5_combobox.place(x=310, y=340, width=170, height=32)

# Bind the event to the notation combobox
notation_combobox.bind("<<ComboboxSelected>>", update_band_comboboxes)

# Start the application
update_band_comboboxes(None)  # Initial call to set up the UI correctly
root.mainloop()

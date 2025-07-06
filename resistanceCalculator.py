import sys
import os
import ctypes
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QMessageBox,
    QVBoxLayout, QWidget, QGridLayout, QMenuBar, QMenu, QHBoxLayout, QFrame
)
from PyQt6.QtGui import QAction, QFont, QIcon
from PyQt6.QtCore import Qt

# Define color groups
significant_colors = {
    "black": 0, "brown": 1, "red": 2, "orange": 3, "yellow": 4,
    "green": 5, "blue": 6, "violet": 7, "gray": 8, "white": 9
}

multiplier_colors = {
    "black": 0, "brown": 1, "red": 2, "orange": 3, "yellow": 4,
    "green": 5, "blue": 6, "violet": 7, "gray": 8, "white": 9,
    "gold": -1, "silver": -2
}

tolerance_colors = {
    "brown": 1, "red": 2, "green": 0.5, "blue": 0.25,
    "violet": 0.1, "gray": 0.01, "gold": 5, "silver": 10
}

tempco_colors = {
    "brown": 100, "red": 50, "orange": 15, "yellow": 25,
    "blue": 10, "violet": 5
}

color_text_overrides = {
    "black": "white", "blue": "white", "brown": "white", "violet": "white",
    "gray": "black", "white": "black", "red": "white", "green": "white",
    "orange": "black", "yellow": "black", "gold": "black", "silver": "black"
}

def format_resistance(value):
    if value >= 1e6:
        return f"{value / 1e6:.2f} MΩ"
    elif value >= 1e3:
        return f"{value / 1e3:.2f} kΩ"
    else:
        return f"{value:.2f} Ω"

def set_taskbar_icon(window, icon_path):
    # Load icon using Windows API for taskbar icon
    LoadImage = ctypes.windll.user32.LoadImageW
    LR_LOADFROMFILE = 0x00000010
    IMAGE_ICON = 1

    hicon = LoadImage(None, icon_path, IMAGE_ICON, 0, 0, LR_LOADFROMFILE)
    if hicon == 0:
        print("Failed to load icon for taskbar.")
        return

    hwnd = int(window.winId())

    WM_SETICON = 0x80
    ICON_SMALL = 0
    ICON_BIG = 1

    ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)
    ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)

class ResistorCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        # Get the path to icon.ico inside the bundled app
        if getattr(sys, 'frozen', False):
            # Running in a PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        icon_path = os.path.join(base_path, "icon.ico")

        self.setWindowIcon(QIcon(icon_path))
        set_taskbar_icon(self, icon_path)  # Explicitly set taskbar icon on Windows

        self.setWindowTitle("Resistor Color Code Calculator")
        self.setGeometry(100, 100, 650, 620)
        self.setFixedSize(650, 620)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QComboBox {
                padding: 3px;
                border: 1px solid #ccc;
                border-radius: none;
            }
            QPushButton {
                border-radius: 0;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: #2e8b57;
            }
            QLabel.output-label {
                border: 1px solid #aaa;
                border-radius: 6px;
                padding: 6px;
                background-color: #fff;
            }
            QLabel.title-label {
                border: 1px solid #bbb;
                border-radius: 8px;
                background-color: #e6e6e6;
                color: #2a2a2a;
                padding: 10px;
            }
        """)

        font = QFont("Arial", 13)

        outer_frame = QFrame()
        outer_frame.setStyleSheet("background-color: white; border: 2px solid #ccc;")
        outer_layout = QVBoxLayout(outer_frame)
        outer_layout.setContentsMargins(24, 24, 24, 24)
        outer_layout.setSpacing(8)

        self.setCentralWidget(outer_frame)

        title = QLabel("Ω Resistor Color Code Calculator")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFixedSize(400, 50)
        title.setProperty("class", "title-label")
        outer_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(6)
        form_layout.setVerticalSpacing(4)
        outer_layout.addLayout(form_layout)

        self.band_combos = {}
        self.band_labels = {}
        self.total_bands = 6
        band_names = [f"Band {i+1}" for i in range(self.total_bands)]

        for i, name in enumerate(band_names):
            label = QLabel(name)
            label.setFont(font)
            self.band_labels[name] = label
            combo = QComboBox()
            combo.currentTextChanged.connect(lambda _, b=name: self.update_combo_style(b))
            self.band_combos[name] = combo
            form_layout.addWidget(label, i, 0)
            form_layout.addWidget(combo, i, 1)

        self.notation_combo = QComboBox()
        self.notation_combo.addItems(["4 Bands", "5 Bands", "6 Bands"])
        self.notation_combo.currentTextChanged.connect(self.update_band_visibility)
        form_layout.addWidget(QLabel("Number of Bands"), self.total_bands, 0)
        form_layout.addWidget(self.notation_combo, self.total_bands, 1)

        self.preview_frame = QFrame()
        self.preview_frame.setFixedSize(340, 40)
        self.preview_frame.setStyleSheet("background-color: #fdf6e3; border: 2px solid #888; border-radius: 20px;")
        self.preview_band_layout = QHBoxLayout(self.preview_frame)
        self.preview_band_layout.setContentsMargins(16, 4, 16, 4)
        self.preview_band_layout.setSpacing(10)
        self.preview_color_frames = [QFrame() for _ in range(6)]

        for frame in self.preview_color_frames:
            frame.setFixedSize(8, 30)
            frame.setStyleSheet("background-color: none; border-left: 2px solid transparent;")
            self.preview_band_layout.addWidget(frame)

        outer_layout.addWidget(self.preview_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        self.output_frame = QFrame()
        self.output_frame.setStyleSheet("border: 1px solid #aaa; border-radius: 8px;")
        self.output_frame.setVisible(False)
        output_layout = QVBoxLayout(self.output_frame)
        output_layout.setContentsMargins(10, 6, 10, 6)

        self.resistance_label = QLabel("")
        self.tolerance_label = QLabel("")
        self.range_label = QLabel("")
        self.tempco_label = QLabel("")  # New label for temperature coefficient

        for lbl in [self.resistance_label, self.tolerance_label, self.range_label, self.tempco_label]:
            lbl.setFont(QFont("Arial", 14, QFont.Weight.Medium))
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setProperty("class", "output-label")
            output_layout.addWidget(lbl)

        outer_layout.addWidget(self.output_frame)

        calc_button = QPushButton("Calculate")
        calc_button.setFont(font)
        calc_button.setStyleSheet("background-color: #006400; color: white; border-radius: 0;")
        calc_button.clicked.connect(self.calculate_resistance)
        outer_layout.addWidget(calc_button)

        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)

        help_menu = QMenu("Help", self)
        about_menu = QMenu("About", self)
        menu_bar.addMenu(help_menu)
        menu_bar.addMenu(about_menu)

        usage_action = QAction("Usage Instructions", self)
        usage_action.triggered.connect(self.show_help)
        help_menu.addAction(usage_action)

        about_action = QAction("About this program", self)
        about_action.triggered.connect(self.show_about)
        about_menu.addAction(about_action)

        self.update_band_visibility(self.notation_combo.currentText())

    def update_band_visibility(self, notation):
        band_count = {"4 Bands": 4, "5 Bands": 5, "6 Bands": 6}[notation]
        for i in range(self.total_bands):
            name = f"Band {i+1}"
            show = i < band_count
            self.band_labels[name].setVisible(show)
            self.band_combos[name].setVisible(show)
            self.preview_color_frames[i].setVisible(show)
            combo = self.band_combos[name]
            combo.clear()

            if notation == "4 Bands":
                if i in [0, 1]:
                    combo.addItems(significant_colors.keys())
                elif i == 2:
                    combo.addItems(multiplier_colors.keys())
                elif i == 3:
                    combo.addItems(tolerance_colors.keys())
            elif notation == "5 Bands":
                if i in [0, 1, 2]:
                    combo.addItems(significant_colors.keys())
                elif i == 3:
                    combo.addItems(multiplier_colors.keys())
                elif i == 4:
                    combo.addItems(tolerance_colors.keys())
            elif notation == "6 Bands":
                if i in [0, 1, 2]:
                    combo.addItems(significant_colors.keys())
                elif i == 3:
                    combo.addItems(multiplier_colors.keys())
                elif i == 4:
                    combo.addItems(tolerance_colors.keys())
                elif i == 5:
                    combo.addItems(tempco_colors.keys())

            if combo.count() > 0:
                combo.setCurrentIndex(0)
                self.update_combo_style(name)

        self.resistance_label.setText("")
        self.tolerance_label.setText("")
        self.range_label.setText("")
        self.tempco_label.setText("")  # Clear tempco label
        self.tempco_label.setVisible(False)
        self.output_frame.setVisible(False)

    def update_combo_style(self, band_name):
        index = int(band_name.split()[-1]) - 1
        combo = self.band_combos[band_name]
        color_name = combo.currentText()
        if color_name:
            text_color = color_text_overrides.get(color_name, "black")
            combo.setStyleSheet(f"background-color: {color_name}; color: {text_color};")
            self.preview_color_frames[index].setStyleSheet(f"background-color: {color_name}; border-left: 2px solid black;")

    def calculate_resistance(self):
        notation = self.notation_combo.currentText()
        try:
            if notation == "4 Bands":
                b1 = significant_colors[self.band_combos["Band 1"].currentText()]
                b2 = significant_colors[self.band_combos["Band 2"].currentText()]
                mult = 10 ** multiplier_colors[self.band_combos["Band 3"].currentText()]
                tol = tolerance_colors[self.band_combos["Band 4"].currentText()]
                resistance = (b1 * 10 + b2) * mult
                tempco_str = ""
                self.tempco_label.setVisible(False)

            elif notation == "5 Bands":
                b1 = significant_colors[self.band_combos["Band 1"].currentText()]
                b2 = significant_colors[self.band_combos["Band 2"].currentText()]
                b3 = significant_colors[self.band_combos["Band 3"].currentText()]
                mult = 10 ** multiplier_colors[self.band_combos["Band 4"].currentText()]
                tol = tolerance_colors[self.band_combos["Band 5"].currentText()]
                resistance = (b1 * 100 + b2 * 10 + b3) * mult
                tempco_str = ""
                self.tempco_label.setVisible(False)

            else:  # 6 Bands
                b1 = significant_colors[self.band_combos["Band 1"].currentText()]
                b2 = significant_colors[self.band_combos["Band 2"].currentText()]
                b3 = significant_colors[self.band_combos["Band 3"].currentText()]
                mult = 10 ** multiplier_colors[self.band_combos["Band 4"].currentText()]
                tol = tolerance_colors[self.band_combos["Band 5"].currentText()]
                tempco = tempco_colors[self.band_combos["Band 6"].currentText()]
                resistance = (b1 * 100 + b2 * 10 + b3) * mult
                tempco_str = f"Temperature Coefficient: {tempco} ppm/°C"
                self.tempco_label.setVisible(True)

            self.resistance_label.setText(f"Resistance: {format_resistance(resistance)}")
            self.tolerance_label.setText(f"Tolerance: ±{tol}%")
            min_r = resistance * (1 - tol / 100)
            max_r = resistance * (1 + tol / 100)
            self.range_label.setText(f"Range: {format_resistance(min_r)} - {format_resistance(max_r)}")

            self.tempco_label.setText(tempco_str)
            self.output_frame.setVisible(True)
        except Exception:
            self.resistance_label.setText("Invalid selection.")
            self.tolerance_label.setText("")
            self.range_label.setText("")
            self.tempco_label.setText("")
            self.tempco_label.setVisible(False)
            self.output_frame.setVisible(False)

    def show_help(self):
        QMessageBox.information(self, "Help - Usage Instructions", """
        1. Select number of bands (4, 5, or 6).

        4-Band:
        Band 1-2: Significant digits
        Band 3: Multiplier
        Band 4: Tolerance

        5-Band:
        Band 1-3: Significant digits
        Band 4: Multiplier
        Band 5: Tolerance

        6-Band:
        Band 1-3: Significant digits
        Band 4: Multiplier
        Band 5: Tolerance
        Band 6: Temperature Coefficient (ignored in calculation)
        """)

    def show_about(self):
        QMessageBox.information(self, "About", "Resistor Calculator v2.3.1\n\nDeveloped by KaotickJ\nhttps://github.com/kaotickj")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResistorCalculator()
    window.show()
    sys.exit(app.exec())

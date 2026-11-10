import sys
import os
import ctypes

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QComboBox,
    QPushButton,
    QMessageBox,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QMenu,
    QHBoxLayout,
    QFrame,
    QSizePolicy,
    QDialog,
)
from PyQt6.QtGui import QAction, QFont, QIcon
from PyQt6.QtCore import Qt


# ============================================================
# Resistor data
# ============================================================

significant_colors = {
    "black": 0,
    "brown": 1,
    "red": 2,
    "orange": 3,
    "yellow": 4,
    "green": 5,
    "blue": 6,
    "violet": 7,
    "gray": 8,
    "white": 9,
}

multiplier_colors = {
    "black": 0,
    "brown": 1,
    "red": 2,
    "orange": 3,
    "yellow": 4,
    "green": 5,
    "blue": 6,
    "violet": 7,
    "gray": 8,
    "white": 9,
    "gold": -1,
    "silver": -2,
}

tolerance_colors = {
    "brown": 1,
    "red": 2,
    "green": 0.5,
    "blue": 0.25,
    "violet": 0.1,
    "gray": 0.01,
    "gold": 5,
    "silver": 10,
}

tempco_colors = {
    "brown": 100,
    "red": 50,
    "orange": 15,
    "yellow": 25,
    "blue": 10,
    "violet": 5,
}


# CSS colors are kept separate from resistor names so the
# appearance is consistent across platforms.
DISPLAY_COLORS = {
    "black": "#17191d",
    "brown": "#795548",
    "red": "#d64545",
    "orange": "#f28c28",
    "yellow": "#f2cf43",
    "green": "#36965b",
    "blue": "#3478c9",
    "violet": "#8255b8",
    "gray": "#9ca3af",
    "white": "#f3f4f6",
    "gold": "#d4af37",
    "silver": "#c0c0c0",
}

LIGHT_TEXT_COLORS = {
    "black",
    "brown",
    "red",
    "green",
    "blue",
    "violet",
}


# ============================================================
# Helpers
# ============================================================

def format_resistance(value):
    """Return resistance using a sensible engineering unit."""
    abs_value = abs(value)

    if abs_value >= 1e9:
        return f"{value / 1e9:.2f} GΩ"
    if abs_value >= 1e6:
        return f"{value / 1e6:.2f} MΩ"
    if abs_value >= 1e3:
        return f"{value / 1e3:.2f} kΩ"

    return f"{value:.2f} Ω"


def resource_path(filename):
    """Return a resource path that works normally and with PyInstaller."""
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, filename)


def set_windows_taskbar_icon(window, icon_path):
    """Set native Windows taskbar icon when running on Windows."""
    if sys.platform != "win32":
        return

    if not os.path.exists(icon_path):
        return

    try:
        load_image = ctypes.windll.user32.LoadImageW

        LR_LOADFROMFILE = 0x00000010
        IMAGE_ICON = 1
        WM_SETICON = 0x0080
        ICON_SMALL = 0
        ICON_BIG = 1

        hicon = load_image(
            None,
            icon_path,
            IMAGE_ICON,
            0,
            0,
            LR_LOADFROMFILE,
        )

        if not hicon:
            return

        hwnd = int(window.winId())

        ctypes.windll.user32.SendMessageW(
            hwnd, WM_SETICON, ICON_SMALL, hicon
        )
        ctypes.windll.user32.SendMessageW(
            hwnd, WM_SETICON, ICON_BIG, hicon
        )

    except Exception:
        # QIcon still provides the normal application icon.
        pass


# ============================================================
# Main window
# ============================================================

class ResistorCalculator(QMainWindow):

    def __init__(self):
        super().__init__()

        self.total_bands = 6
        self.band_combos = {}
        self.band_labels = {}
        self.band_role_labels = {}

        self.setup_window()
        self.setup_ui()
        self.setup_menu()
        self.apply_theme()

        self.update_band_visibility(
            self.notation_combo.currentText()
        )


    # --------------------------------------------------------
    # Window
    # --------------------------------------------------------

    def setup_window(self):
        self.setWindowTitle("Resistor Color Code Calculator")
        self.resize(760, 720)
        self.setMinimumSize(760, 1000)

        icon_path = resource_path("icon.ico")

        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            set_windows_taskbar_icon(self, icon_path)


    # --------------------------------------------------------
    # UI construction
    # --------------------------------------------------------

    def setup_ui(self):
        central = QWidget()
        central.setObjectName("centralWidget")

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(32, 26, 32, 28)
        main_layout.setSpacing(20)

        self.setCentralWidget(central)

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)

        title = QLabel("Resistor Color Code")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel(
            "Calculate resistance, tolerance and temperature coefficient"
        )
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        main_layout.addLayout(header_layout)

        # ----------------------------------------------------
        # Band count selector
        # ----------------------------------------------------

        mode_card = QFrame()
        mode_card.setObjectName("card")

        mode_layout = QHBoxLayout(mode_card)
        mode_layout.setContentsMargins(20, 14, 20, 14)

        mode_label = QLabel("Resistor type")
        mode_label.setObjectName("sectionLabel")

        self.notation_combo = QComboBox()
        self.notation_combo.setObjectName("modeCombo")
        self.notation_combo.addItems(
            ["4 Bands", "5 Bands", "6 Bands"]
        )
        self.notation_combo.setMinimumWidth(160)

        self.notation_combo.currentTextChanged.connect(
            self.update_band_visibility
        )

        mode_layout.addWidget(mode_label)
        mode_layout.addStretch()
        mode_layout.addWidget(self.notation_combo)

        main_layout.addWidget(mode_card)

        # ----------------------------------------------------
        # Band selection card
        # ----------------------------------------------------

        bands_card = QFrame()
        bands_card.setObjectName("card")

        bands_layout = QVBoxLayout(bands_card)
        bands_layout.setContentsMargins(20, 18, 20, 20)
        bands_layout.setSpacing(14)

        bands_heading = QLabel("Color Bands")
        bands_heading.setObjectName("cardTitle")

        bands_layout.addWidget(bands_heading)

        self.form_layout = QGridLayout()
        self.form_layout.setHorizontalSpacing(16)
        self.form_layout.setVerticalSpacing(10)
        self.form_layout.setColumnStretch(1, 1)

        bands_layout.addLayout(self.form_layout)

        for i in range(self.total_bands):
            name = f"Band {i + 1}"

            number_label = QLabel(name)
            number_label.setObjectName("bandNumber")

            role_label = QLabel("")
            role_label.setObjectName("bandRole")

            label_container = QWidget()
            label_layout = QVBoxLayout(label_container)
            label_layout.setContentsMargins(0, 0, 0, 0)
            label_layout.setSpacing(1)
            label_layout.addWidget(number_label)
            label_layout.addWidget(role_label)

            combo = QComboBox()
            combo.setMinimumHeight(38)
            combo.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed,
            )

            combo.currentTextChanged.connect(
                lambda _, band=name: self.band_changed(band)
            )

            self.band_labels[name] = label_container
            self.band_role_labels[name] = role_label
            self.band_combos[name] = combo

            self.form_layout.addWidget(label_container, i, 0)
            self.form_layout.addWidget(combo, i, 1)

        main_layout.addWidget(bands_card)

        # ----------------------------------------------------
        # Resistor preview
        # ----------------------------------------------------

        preview_card = QFrame()
        preview_card.setObjectName("card")

        preview_layout = QVBoxLayout(preview_card)
        preview_layout.setContentsMargins(20, 16, 20, 20)
        preview_layout.setSpacing(12)

        preview_heading = QLabel("Preview")
        preview_heading.setObjectName("cardTitle")

        preview_layout.addWidget(preview_heading)

        preview_container = QWidget()

        resistor_layout = QHBoxLayout(preview_container)
        resistor_layout.setContentsMargins(30, 8, 30, 8)
        resistor_layout.setSpacing(0)

        left_lead = QFrame()
        left_lead.setObjectName("lead")
        left_lead.setFixedHeight(4)

        right_lead = QFrame()
        right_lead.setObjectName("lead")
        right_lead.setFixedHeight(4)

        self.preview_frame = QFrame()
        self.preview_frame.setObjectName("resistorBody")
        self.preview_frame.setFixedSize(390, 70)

        self.preview_band_layout = QHBoxLayout(
            self.preview_frame
        )
        self.preview_band_layout.setContentsMargins(
            34, 7, 34, 7
        )
        self.preview_band_layout.setSpacing(20)

        self.preview_color_frames = []

        for _ in range(6):
            band = QFrame()
            band.setFixedSize(16, 56)
            band.setObjectName("resistorBand")

            self.preview_color_frames.append(band)
            self.preview_band_layout.addWidget(band)

        resistor_layout.addWidget(left_lead, 1)
        resistor_layout.addWidget(self.preview_frame)
        resistor_layout.addWidget(right_lead, 1)

        preview_layout.addWidget(preview_container)

        main_layout.addWidget(preview_card)

        # ----------------------------------------------------
        # Results
        # ----------------------------------------------------

        self.output_frame = QFrame()
        self.output_frame.setObjectName("resultCard")

        output_layout = QVBoxLayout(self.output_frame)
        output_layout.setContentsMargins(24, 18, 24, 20)
        output_layout.setSpacing(7)

        result_heading = QLabel("Calculated Value")
        result_heading.setObjectName("resultHeading")
        result_heading.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.resistance_label = QLabel("—")
        self.resistance_label.setObjectName("resistanceValue")
        self.resistance_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.tolerance_label = QLabel("")
        self.tolerance_label.setObjectName("resultDetail")
        self.tolerance_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.range_label = QLabel("")
        self.range_label.setObjectName("resultDetail")
        self.range_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.tempco_label = QLabel("")
        self.tempco_label.setObjectName("resultDetail")
        self.tempco_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        output_layout.addWidget(result_heading)
        output_layout.addWidget(self.resistance_label)
        output_layout.addWidget(self.tolerance_label)
        output_layout.addWidget(self.range_label)
        output_layout.addWidget(self.tempco_label)

        main_layout.addWidget(self.output_frame)

        # ----------------------------------------------------
        # Calculate button
        # ----------------------------------------------------

        self.calc_button = QPushButton("Calculate")
        self.calc_button.setObjectName("primaryButton")
        self.calc_button.setMinimumHeight(46)
        self.calc_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        self.calc_button.clicked.connect(
            self.calculate_resistance
        )

        main_layout.addWidget(self.calc_button)


    # --------------------------------------------------------
    # Menu
    # --------------------------------------------------------

    def setup_menu(self):
        menu_bar = self.menuBar()

        help_menu = QMenu("Help", self)
        menu_bar.addMenu(help_menu)

        usage_action = QAction(
            "Usage Instructions", self
        )
        usage_action.triggered.connect(self.show_help)

        about_action = QAction(
            "About Resistor Calculator", self
        )
        about_action.triggered.connect(self.show_about)

        help_menu.addAction(usage_action)
        help_menu.addSeparator()
        help_menu.addAction(about_action)


    # --------------------------------------------------------
    # Theme
    # --------------------------------------------------------

    def apply_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #111318;
            }

            QWidget#centralWidget {
                background-color: #111318;
            }

            QLabel {
                color: #e8eaed;
                font-family: "Segoe UI", "Arial";
            }

            QLabel#title {
                color: #f4f6f8;
                font-size: 28px;
                font-weight: 700;
            }

            QLabel#subtitle {
                color: #8f98a6;
                font-size: 13px;
            }

            QFrame#card {
                background-color: #1a1d24;
                border: 1px solid #292e38;
                border-radius: 12px;
            }

            QLabel#cardTitle,
            QLabel#sectionLabel {
                color: #f0f2f5;
                font-size: 14px;
                font-weight: 600;
            }

            QLabel#bandNumber {
                color: #e8eaed;
                font-size: 13px;
                font-weight: 600;
            }

            QLabel#bandRole {
                color: #7f8998;
                font-size: 11px;
            }

            QComboBox {
                background-color: #242832;
                color: #f1f3f5;
                border: 1px solid #343a46;
                border-radius: 7px;
                padding: 7px 12px;
                font-size: 13px;
            }

            QComboBox:hover {
                border: 1px solid #596273;
            }

            QComboBox:focus {
                border: 1px solid #56a36c;
            }

            QComboBox::drop-down {
                border: none;
                width: 30px;
            }

            QComboBox QAbstractItemView {
                background-color: #242832;
                color: #f1f3f5;
                border: 1px solid #343a46;
                selection-background-color: #39764b;
                selection-color: white;
                outline: 0;
            }

            QFrame#resistorBody {
                background-color: #d6c69f;
                border: 2px solid #91856b;
                border-radius: 28px;
            }

            QFrame#lead {
                background-color: #707782;
                border: none;
            }

            QFrame#resultCard {
                background-color: #171d19;
                border: 1px solid #31523a;
                border-radius: 12px;
            }

            QLabel#resultHeading {
                color: #8fa898;
                font-size: 12px;
                font-weight: 600;
            }

            QLabel#resistanceValue {
                color: #71cf8b;
                font-size: 27px;
                font-weight: 700;
            }

            QLabel#resultDetail {
                color: #c5cec8;
                font-size: 13px;
            }

            QPushButton#primaryButton {
                background-color: #39764b;
                color: white;
                border: 1px solid #498c5d;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton#primaryButton:hover {
                background-color: #438958;
                border-color: #5ca870;
            }

            QPushButton#primaryButton:pressed {
                background-color: #326841;
            }

            QMenuBar {
                background-color: #16191f;
                color: #cbd0d8;
                border-bottom: 1px solid #292e38;
                padding: 3px;
            }

            QMenuBar::item {
                background: transparent;
                padding: 6px 10px;
            }

            QMenuBar::item:selected {
                background-color: #292e38;
                border-radius: 4px;
            }

            QMenu {
                background-color: #20242c;
                color: #e5e7eb;
                border: 1px solid #343a46;
                padding: 5px;
            }

            QMenu::item {
                padding: 7px 28px 7px 10px;
            }

            QMenu::item:selected {
                background-color: #39764b;
                color: white;
            }

            QToolTip {
                background-color: #242832;
                color: #ffffff;
                border: 1px solid #444b58;
                padding: 5px;
            }
        """)


    # --------------------------------------------------------
    # Band configuration
    # --------------------------------------------------------

    def update_band_visibility(self, notation):
        band_count = {
            "4 Bands": 4,
            "5 Bands": 5,
            "6 Bands": 6,
        }[notation]

        roles = self.get_band_roles(notation)

        for i in range(self.total_bands):
            name = f"Band {i + 1}"
            visible = i < band_count

            self.band_labels[name].setVisible(visible)
            self.band_combos[name].setVisible(visible)
            self.preview_color_frames[i].setVisible(visible)

            if not visible:
                continue

            self.band_role_labels[name].setText(roles[i])

            combo = self.band_combos[name]

            combo.blockSignals(True)
            combo.clear()

            if notation == "4 Bands":
                if i in (0, 1):
                    combo.addItems(significant_colors.keys())
                elif i == 2:
                    combo.addItems(multiplier_colors.keys())
                elif i == 3:
                    combo.addItems(tolerance_colors.keys())

            elif notation == "5 Bands":
                if i in (0, 1, 2):
                    combo.addItems(significant_colors.keys())
                elif i == 3:
                    combo.addItems(multiplier_colors.keys())
                elif i == 4:
                    combo.addItems(tolerance_colors.keys())

            else:
                if i in (0, 1, 2):
                    combo.addItems(significant_colors.keys())
                elif i == 3:
                    combo.addItems(multiplier_colors.keys())
                elif i == 4:
                    combo.addItems(tolerance_colors.keys())
                elif i == 5:
                    combo.addItems(tempco_colors.keys())

            combo.blockSignals(False)

            if combo.count():
                combo.setCurrentIndex(0)
                self.update_combo_style(name)

        self.tempco_label.setVisible(
            notation == "6 Bands"
        )

        # Calculate immediately so the result panel is never empty.
        self.calculate_resistance()


    def get_band_roles(self, notation):
        if notation == "4 Bands":
            return [
                "1st significant digit",
                "2nd significant digit",
                "Multiplier",
                "Tolerance",
            ]

        if notation == "5 Bands":
            return [
                "1st significant digit",
                "2nd significant digit",
                "3rd significant digit",
                "Multiplier",
                "Tolerance",
            ]

        return [
            "1st significant digit",
            "2nd significant digit",
            "3rd significant digit",
            "Multiplier",
            "Tolerance",
            "Temperature coefficient",
        ]


    # --------------------------------------------------------
    # Color handling
    # --------------------------------------------------------

    def band_changed(self, band_name):
        self.update_combo_style(band_name)

        # Modern UI behavior: update the result immediately.
        self.calculate_resistance()


    def update_combo_style(self, band_name):
        index = int(band_name.split()[-1]) - 1
        combo = self.band_combos[band_name]

        color_name = combo.currentText()

        if not color_name:
            return

        background = DISPLAY_COLORS.get(
            color_name, "#242832"
        )

        text_color = (
            "#ffffff"
            if color_name in LIGHT_TEXT_COLORS
            else "#151515"
        )

        combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {background};
                color: {text_color};
                border: 1px solid #4a505c;
                border-radius: 7px;
                padding: 7px 12px;
                font-size: 13px;
                font-weight: 600;
            }}

            QComboBox:hover {{
                border: 1px solid #7c8492;
            }}

            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}

            QComboBox QAbstractItemView {{
                background-color: #242832;
                color: #f1f3f5;
                border: 1px solid #343a46;
                selection-background-color: #39764b;
                selection-color: white;
            }}
        """)

        self.preview_color_frames[index].setStyleSheet(
            f"""
            background-color: {background};
            border: 1px solid rgba(0, 0, 0, 90);
            border-radius: 2px;
            """
        )


    # --------------------------------------------------------
    # Calculation
    # --------------------------------------------------------

    def calculate_resistance(self):
        notation = self.notation_combo.currentText()

        try:
            if notation == "4 Bands":
                b1 = significant_colors[
                    self.band_combos["Band 1"].currentText()
                ]
                b2 = significant_colors[
                    self.band_combos["Band 2"].currentText()
                ]

                multiplier = 10 ** multiplier_colors[
                    self.band_combos["Band 3"].currentText()
                ]

                tolerance = tolerance_colors[
                    self.band_combos["Band 4"].currentText()
                ]

                resistance = (
                    b1 * 10 + b2
                ) * multiplier

                tempco = None

            elif notation == "5 Bands":
                b1 = significant_colors[
                    self.band_combos["Band 1"].currentText()
                ]
                b2 = significant_colors[
                    self.band_combos["Band 2"].currentText()
                ]
                b3 = significant_colors[
                    self.band_combos["Band 3"].currentText()
                ]

                multiplier = 10 ** multiplier_colors[
                    self.band_combos["Band 4"].currentText()
                ]

                tolerance = tolerance_colors[
                    self.band_combos["Band 5"].currentText()
                ]

                resistance = (
                    b1 * 100 +
                    b2 * 10 +
                    b3
                ) * multiplier

                tempco = None

            else:
                b1 = significant_colors[
                    self.band_combos["Band 1"].currentText()
                ]
                b2 = significant_colors[
                    self.band_combos["Band 2"].currentText()
                ]
                b3 = significant_colors[
                    self.band_combos["Band 3"].currentText()
                ]

                multiplier = 10 ** multiplier_colors[
                    self.band_combos["Band 4"].currentText()
                ]

                tolerance = tolerance_colors[
                    self.band_combos["Band 5"].currentText()
                ]

                tempco = tempco_colors[
                    self.band_combos["Band 6"].currentText()
                ]

                resistance = (
                    b1 * 100 +
                    b2 * 10 +
                    b3
                ) * multiplier

            minimum = resistance * (
                1 - tolerance / 100
            )

            maximum = resistance * (
                1 + tolerance / 100
            )

            self.resistance_label.setText(
                format_resistance(resistance)
            )

            self.tolerance_label.setText(
                f"Tolerance   ±{tolerance:g}%"
            )

            self.range_label.setText(
                "Range   "
                f"{format_resistance(minimum)}  –  "
                f"{format_resistance(maximum)}"
            )

            if tempco is not None:
                self.tempco_label.setText(
                    f"Temperature coefficient   "
                    f"{tempco} ppm/°C"
                )
                self.tempco_label.setVisible(True)
            else:
                self.tempco_label.clear()
                self.tempco_label.setVisible(False)

        except (KeyError, ValueError):
            self.resistance_label.setText("—")
            self.tolerance_label.setText("")
            self.range_label.setText("")
            self.tempco_label.setText("")


    # --------------------------------------------------------
    # Dialogs
    # --------------------------------------------------------
    def show_help(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Usage Instructions")
        dialog.setFixedSize(520, 520)
        dialog.setModal(True)

        if not self.windowIcon().isNull():
            dialog.setWindowIcon(self.windowIcon())

        dialog.setStyleSheet("""
            QDialog {
                background-color: #1a1d24;
            }

            QLabel#helpTitle {
                color: #f4f6f8;
                font-family: "Segoe UI", "Arial";
                font-size: 20px;
                font-weight: 700;
            }

            QLabel#helpIntro {
                color: #aab2bd;
                font-family: "Segoe UI", "Arial";
                font-size: 13px;
            }

            QLabel#helpHeading {
                color: #71cf8b;
                font-family: "Segoe UI", "Arial";
                font-size: 14px;
                font-weight: 700;
            }

            QLabel#helpText {
                color: #d2d6dc;
                font-family: "Segoe UI", "Arial";
                font-size: 13px;
            }

            QLabel#helpFooter {
                color: #8f98a6;
                font-family: "Segoe UI", "Arial";
                font-size: 12px;
            }

            QFrame#helpDivider {
                background-color: #343a46;
                border: none;
                max-height: 1px;
            }

            QPushButton {
                background-color: #39764b;
                color: white;
                border: 1px solid #498c5d;
                border-radius: 7px;
                padding: 8px 24px;
                font-family: "Segoe UI", "Arial";
                font-size: 13px;
                font-weight: 600;
                min-width: 80px;
            }

            QPushButton:hover {
                background-color: #438958;
                border-color: #5ca870;
            }

            QPushButton:pressed {
                background-color: #326841;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(30, 26, 30, 24)
        layout.setSpacing(8)

        title = QLabel("Usage Instructions")
        title.setObjectName("helpTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        intro = QLabel(
            "Select the resistor type, then choose the color "
            "of each band."
        )
        intro.setObjectName("helpIntro")
        intro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        intro.setWordWrap(True)

        divider = QFrame()
        divider.setObjectName("helpDivider")
        divider.setFrameShape(QFrame.Shape.HLine)

        layout.addWidget(title)
        layout.addWidget(intro)
        layout.addSpacing(8)
        layout.addWidget(divider)
        layout.addSpacing(8)

        # 4-band instructions
        heading_4 = QLabel("4-Band Resistor")
        heading_4.setObjectName("helpHeading")

        text_4 = QLabel(
            "Bands 1–2:  Significant digits\n"
            "Band 3:       Multiplier\n"
            "Band 4:       Tolerance"
        )
        text_4.setObjectName("helpText")

        layout.addWidget(heading_4)
        layout.addWidget(text_4)
        layout.addSpacing(8)

        # 5-band instructions
        heading_5 = QLabel("5-Band Resistor")
        heading_5.setObjectName("helpHeading")

        text_5 = QLabel(
            "Bands 1–3:  Significant digits\n"
            "Band 4:       Multiplier\n"
            "Band 5:       Tolerance"
        )
        text_5.setObjectName("helpText")

        layout.addWidget(heading_5)
        layout.addWidget(text_5)
        layout.addSpacing(8)

        # 6-band instructions
        heading_6 = QLabel("6-Band Resistor")
        heading_6.setObjectName("helpHeading")

        text_6 = QLabel(
            "Bands 1–3:  Significant digits\n"
            "Band 4:       Multiplier\n"
            "Band 5:       Tolerance\n"
            "Band 6:       Temperature coefficient"
        )
        text_6.setObjectName("helpText")

        layout.addWidget(heading_6)
        layout.addWidget(text_6)

        layout.addStretch()

        footer = QLabel(
            "The calculated resistance updates automatically "
            "whenever a band color is changed."
        )
        footer.setObjectName("helpFooter")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setWordWrap(True)

        close_button = QPushButton("Close")
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button.clicked.connect(dialog.accept)

        layout.addWidget(footer)
        layout.addSpacing(8)
        layout.addWidget(
            close_button,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        dialog.exec()

    def show_about(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("About Resistor Calculator")
        dialog.setFixedSize(420, 310)
        dialog.setModal(True)

        if not self.windowIcon().isNull():
            dialog.setWindowIcon(self.windowIcon())

        dialog.setStyleSheet("""
            QDialog {
                background-color: #1a1d24;
            }

            QLabel#aboutTitle {
                color: #f4f6f8;
                font-family: "Segoe UI", "Arial";
                font-size: 20px;
                font-weight: 700;
            }

            QLabel#aboutVersion {
                color: #71cf8b;
                font-family: "Segoe UI", "Arial";
                font-size: 13px;
                font-weight: 600;
            }

            QLabel#aboutText {
                color: #c5cbd3;
                font-family: "Segoe UI", "Arial";
                font-size: 13px;
            }

            QLabel#aboutLink {
                color: #71cf8b;
                font-family: "Segoe UI", "Arial";
                font-size: 13px;
            }

            QFrame#aboutDivider {
                background-color: #343a46;
                border: none;
                max-height: 1px;
            }

            QPushButton {
                background-color: #39764b;
                color: white;
                border: 1px solid #498c5d;
                border-radius: 7px;
                padding: 8px 24px;
                font-family: "Segoe UI", "Arial";
                font-size: 13px;
                font-weight: 600;
                min-width: 80px;
            }

            QPushButton:hover {
                background-color: #438958;
                border-color: #5ca870;
            }

            QPushButton:pressed {
                background-color: #326841;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(30, 26, 30, 24)
        layout.setSpacing(8)

        title = QLabel("Resistor Color Code Calculator")
        title.setObjectName("aboutTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        version = QLabel("Version 3.0")
        version.setObjectName("aboutVersion")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)

        divider = QFrame()
        divider.setObjectName("aboutDivider")
        divider.setFrameShape(QFrame.Shape.HLine)

        developer = QLabel("Developed by KaotickJ")
        developer.setObjectName("aboutText")
        developer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        github = QLabel(
            '<a href="https://github.com/kaotickj">'
            'github.com/kaotickj</a>'
        )
        github.setObjectName("aboutLink")
        github.setAlignment(Qt.AlignmentFlag.AlignCenter)
        github.setOpenExternalLinks(True)
        github.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextBrowserInteraction
        )

        close_button = QPushButton("Close")
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button.clicked.connect(dialog.accept)

        layout.addWidget(title)
        layout.addWidget(version)
        layout.addSpacing(8)
        layout.addWidget(divider)
        layout.addSpacing(12)
        layout.addWidget(developer)
        layout.addWidget(github)
        layout.addStretch()
        layout.addWidget(
            close_button,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        dialog.exec()


# ============================================================
# Application
# ============================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setApplicationName(
        "Resistor Color Code Calculator"
    )
    app.setOrganizationName("KaotickJ")

    # Fusion gives much more predictable cross-platform styling.
    app.setStyle("Fusion")

    window = ResistorCalculator()
    window.show()

    sys.exit(app.exec())


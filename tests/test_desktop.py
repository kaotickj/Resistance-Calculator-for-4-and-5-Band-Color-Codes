"""Exercise the actual Qt calculator; set QT_QPA_PLATFORM=offscreen for CI."""
import importlib.util
import os
from pathlib import Path
import sys
import unittest
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtCore import QTimer

source = Path(os.environ.get('RESISTOR_SOURCE', 'resistanceCalculator.py')).resolve()
spec = importlib.util.spec_from_file_location('resistanceCalculator', source)
calculator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calculator)

class CalculatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.window = calculator.ResistorCalculator()
        self.window.show()
        self.app.processEvents()

    def tearDown(self):
        self.window.close()
        self.app.processEvents()

    def select(self, count, colors):
        self.window.notation_combo.setCurrentText(f'{count} Bands')
        for i, color in enumerate(colors, 1):
            self.window.band_combos[f'Band {i}'].setCurrentText(color)
        self.window.calc_button.click()
        self.app.processEvents()

    def test_four_band(self):
        self.select(4, ['yellow', 'violet', 'red', 'gold'])
        self.assertEqual(self.window.resistance_label.text(), '4.70 kΩ')
        self.assertEqual(self.window.tolerance_label.text(), 'Tolerance   ±5%')
        self.assertEqual(self.window.range_label.text(), 'Range   4.46 kΩ  –  4.93 kΩ')
        self.assertTrue(self.window.tempco_label.isHidden())

    def test_five_band_and_subohm(self):
        self.select(5, ['brown', 'black', 'black', 'red', 'brown'])
        self.assertEqual(self.window.resistance_label.text(), '10.00 kΩ')
        self.assertEqual(self.window.tolerance_label.text(), 'Tolerance   ±1%')
        self.select(4, ['yellow', 'violet', 'silver', 'silver'])
        self.assertEqual(self.window.resistance_label.text(), '0.47 Ω')

    def test_six_band_and_repeated_mode_switches(self):
        for count in (6, 4, 5, 6, 5, 4, 6):
            self.window.notation_combo.setCurrentText(f'{count} Bands')
            for i in range(6):
                self.assertEqual(self.window.band_combos[f'Band {i + 1}'].isHidden(), i >= count)
            self.assertNotEqual(self.window.resistance_label.text(), '—')
        self.select(6, ['brown', 'black', 'black', 'red', 'brown', 'red'])
        self.assertEqual(self.window.resistance_label.text(), '10.00 kΩ')
        self.assertEqual(self.window.tempco_label.text(), 'Temperature coefficient   50 ppm/°C')
        self.assertFalse(self.window.tempco_label.isHidden())

    def test_all_multipliers_and_tolerances(self):
        for color, exponent in calculator.multiplier_colors.items():
            self.select(4, ['brown', 'black', color, 'gold'])
            self.assertEqual(self.window.resistance_label.text(), calculator.format_resistance(10 * 10**exponent))
        for color, tolerance in calculator.tolerance_colors.items():
            self.select(5, ['brown', 'black', 'black', 'black', color])
            self.assertEqual(self.window.tolerance_label.text(), f'Tolerance   ±{tolerance:g}%')
        for color, tempco in calculator.tempco_colors.items():
            self.select(6, ['brown', 'black', 'black', 'black', 'brown', color])
            self.assertEqual(self.window.tempco_label.text(), f'Temperature coefficient   {tempco} ppm/°C')

    def test_units(self):
        for value, expected in [(0, '0.00 Ω'), (999, '999.00 Ω'), (1000, '1.00 kΩ'), (1e6, '1.00 MΩ'), (1e9, '1.00 GΩ')]:
            self.assertEqual(calculator.format_resistance(value), expected)

    def test_dialog_close_and_reopen(self):
        def dismiss():
            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, QDialog):
                    widget.reject()
        for show in (self.window.show_help, self.window.show_about) * 2:
            QTimer.singleShot(50, dismiss)
            show()
        self.assertTrue(self.window.isVisible())

    def test_icon_and_small_screen(self):
        self.assertFalse(self.window.windowIcon().isNull())
        self.window.resize(760, 720)
        self.app.processEvents()
        self.assertLessEqual(self.window.minimumHeight(), 720)

if __name__ == '__main__':
    unittest.main()

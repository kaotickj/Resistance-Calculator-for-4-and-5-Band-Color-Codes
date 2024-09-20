# Resistance Calculator for 4 and 5 Band Color Codes
![Resistance Calculator](assets/resistance.png)
 >A python resistor calculator for 4 and 5 band resistor color codes. The GUI allows users to interactively select the colors of the resistor bands through comboboxes. Each band's color selection corresponds to a specific numerical value and tolerance, defined in the color_codes dictionary.  Upon selecting the band colors, the code triggers the calculate_resistance() function, which performs the necessary calculations to determine the resistance value based on the color codes. Additionally, depending on the chosen notation (4-band or 5-band), the function calculates the tolerance value accordingly.


## Description
The Resistor Calculator is a GUI application developed in Python using Tkinter. It allows users to calculate the resistance and tolerance of resistors based on the color bands marked on them. The application supports both 4-band and 5-band resistors.

## Features
- Select the number of bands (4 or 5).
- Choose colors corresponding to the resistor's bands.
- Calculate the resistance and tolerance.
- Display the resistance range based on tolerance.

## Dependencies
- Python 3.x
- Tkinter (usually included with Python installations)

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kaotickj/resistor-calculator.git
   cd resistor-calculator
   ```

2. **Ensure Python is Installed**:
   Make sure you have Python 3.x installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

3. **Run the Application**:
   Simply run the script using Python:
   ```bash
   python resistor_calculator.py
   ```

## Usage Instructions
1. Launch the application.
2. Select the number of bands on your resistor (4 or 5) from the dropdown menu.
3. For each band, select the corresponding color from the dropdown menus.
   - **Band 1**: First significant figure.
   - **Band 2**: Second significant figure.
   - **Band 3** (only for 5-band resistors): Third significant figure.
   - **Band 4**: Multiplier.
   - **Band 5**: Tolerance (if 5 bands).
4. Press the "Calculate" button to view the resistance and tolerance.
5. The resistance range will also be displayed based on the tolerance value.

## Use Case Information
This application is ideal for electronics enthusiasts, students, and professionals who need to quickly and accurately calculate the resistance of resistors based on their color codes. It can be particularly useful in educational settings for learning about resistor color codes and tolerance values.

## About
Developed by KaotickJ.  
GitHub: [https://github.com/kaotickj](https://github.com/kaotickj?tab=repositories)  
Website: [https://kdgwebsolutions.com](https://kdgwebsolutions.com)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

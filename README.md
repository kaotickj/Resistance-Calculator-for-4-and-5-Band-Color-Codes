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

### Clone
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kaotickj/Resistance-Calculator-for-4-and-5-Band-Color-Codes.git
   cd Resistance-Calculator-for-4-and-5-Band-Color-Codes
   ```

2. **Ensure Python is Installed**:
   Make sure you have Python 3.x installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

3. **Run the Application**:
   Simply run the script using Python:
   ```bash
   python resistance.py
   ```
### Manual Download

1. **Download the Repository:**
   - Go to the [Resistance-Calculator-for-4-and-5-Band-Color-Codes](https://github.com/kaotickj/Resistance-Calculator-for-4-and-5-Band-Color-Codes) GitHub page.
   - Click on the "<> Code" button.
   - Select "Download ZIP" from the dropdown menu.
   - Save the ZIP file to your preferred location on your computer.

2. **Extract the ZIP File:**
   - Navigate to the location where you downloaded the ZIP file.
   - Right-click on the ZIP file and select "Extract All" (or a similar option depending on your operating system).
   - Choose a destination folder and extract the contents.

3. **Navigate to the Project Directory:**
   - Open your terminal or command prompt.
   - Use the `cd` command to navigate to the extracted project directory. For example:
     ```bash
     cd path/to/Resistance-Calculator-for-4-and-5-Band-Color-Codes
     ```

4. **Run the Application:**
   - Execute the following command to start the application:
     ```bash
     python resistance.py
     ```

## Usage Instructions

1. Select the number of bands on your resistor (4 or 5).

   ### For 4-Band Resistors:
   2. Select the corresponding color for each band from the dropdown menus:
      - Band 1: First significant figure.
      - Band 2: Second significant figure.
      - Band 3: Multiplier.
      - Band 4: Tolerance.

   ### For 5-Band Resistors:
   2. Select the corresponding color for each band from the dropdown menus:
      - Band 1: First significant figure.
      - Band 2: Second significant figure.
      - Band 3: Third significant figure.
      - Band 4: Multiplier.
      - Band 5: Tolerance.

3. Press the "Calculate" button to view the resistance and tolerance.

## How to Determine the First Color Band

- The first band is typically located closer to one end of the resistor.
- The tolerance band (gold, silver, or none) is usually separated by more space from the other bands and is often positioned on the far right.
- Hold the resistor so that the tolerance band is on the right. The first color band will be on the far left.
- For resistors with 5 bands, the first three bands represent significant figures, while the last two are the multiplier and tolerance.

## Use Case Information
This application is ideal for electronics enthusiasts, students, and professionals who need to quickly and accurately calculate the resistance of resistors based on their color codes. It can be particularly useful in educational settings for learning about resistor color codes and tolerance values.

## About
Developed by KaotickJ.  
GitHub: [https://github.com/kaotickj](https://github.com/kaotickj?tab=repositories)  
Website: [https://kdgwebsolutions.com](https://kdgwebsolutions.com)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

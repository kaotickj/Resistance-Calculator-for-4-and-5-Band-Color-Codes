from setuptools import setup, find_packages

setup(
    name="resistor_calculator",
    version="2.0",
    description="Resistor Color Code Calculator",
    author="Kaotick Jay",
    author_email="kaotickj@gmail.com",
    url="https://github.com/kaotickj/Resistance-Calculator-for-4-and-5-Band-Color-Codes",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.0.0"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        'console_scripts': [
            'resistor_calculator=resistor_calculator:main',  # Adjust if you have a main() function in a module
        ],
    },
)

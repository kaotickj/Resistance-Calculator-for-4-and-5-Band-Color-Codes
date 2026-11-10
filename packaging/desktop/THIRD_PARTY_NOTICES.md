# Third-party software

The application source is MIT licensed; see LICENSE. This installer distributes
application source and installation scripts, not Python, Qt, PyQt or SIP binaries.
It requires an existing 64-bit Python 3.12 and downloads the following exact wheels
directly from the official Python Package Index at installation time:

* PyQt6 6.7.1: GPL v3 or commercial Riverbank license.
  https://pypi.org/project/PyQt6/6.7.1/
  https://www.riverbankcomputing.com/software/pyqt/license
  Source: https://pypi.org/project/PyQt6/6.7.1/#files
* PyQt6-Qt6 6.7.2: Qt runtime libraries, with component-specific LGPL/GPL/commercial
  terms and third-party notices supplied by the wheel. Do not describe Qt as MIT.
  https://pypi.org/project/PyQt6-Qt6/6.7.2/
  https://www.qt.io/licensing/
  Source and corresponding licensing files: https://download.qt.io/archive/qt/6.7/6.7.2/
* PyQt6-sip 13.8.0: SIP support runtime under its supplied license notices.
  https://pypi.org/project/PyQt6-sip/13.8.0/
  Source: https://pypi.org/project/PyQt6-sip/13.8.0/#files
* Python 3.12 is installed separately under the Python Software Foundation License.
  https://docs.python.org/3.12/license.html

Installed distribution metadata and license files are retained in the private
virtual environment. Inno Setup is the Windows installer build tool, not a Qt
license exception: https://jrsoftware.org/files/is/license.txt

These are source installers, not standalone frozen executables or PEX files.
If you redistribute a built virtual environment or frozen Qt/PyQt application,
you must separately satisfy all applicable redistribution and corresponding-source
obligations. Upstream links alone do not replace those obligations.

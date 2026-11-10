Resistor Color Code Calculator 3.0.0

These are per-user SOURCE INSTALLERS, not standalone portable apps. No admin
privileges are required. Installation requires internet access to pypi.org and
files.pythonhosted.org and an existing 64-bit Python 3.12.

Windows: install Python 3.12 from python.org with the Python launcher, then run
ResistorCalculator-3.0.0-windows-x86_64-setup.exe. Launch from the Start menu.
Uninstall through Windows Settings / Apps. Unsigned installer: Windows may show
an unknown-publisher warning. No signing certificate is bundled.

Linux x86_64: Python 3.12 and its venv package are required. On Ubuntu 24.04:
  sudo apt install python3.12-venv libegl1 libopengl0 libxcb-cursor0 libxkbcommon-x11-0
A working desktop/display server is required for normal use. Other distributions
may need equivalent Qt xcb/graphics libraries. Qt wheels require a compatible
glibc Linux distribution (the pinned Qt wheel is manylinux_2_28 x86_64).
Extract the tar.gz, then run:
  sh install.sh
Launch using the applications menu or:
  ~/.local/share/resistor-calculator/3.0.0/launch.sh
Uninstall:
  sh ~/.local/share/resistor-calculator/3.0.0/uninstall.sh
Install to a different location with: sh install.sh --target /full/path

Dependencies are pinned in requirements.txt and downloaded directly from PyPI.
The installer never changes the system Python environment. Dependency download
failure removes the incomplete runtime; the installation log is kept in the
parent directory as resistor-calculator-install.log. Remove an existing version
before reinstalling to the same path. See THIRD_PARTY_NOTICES.md for licenses.

CI checks mathematics, 4/5/6-band transitions and offscreen Qt UI startup on
Windows and Linux, including the installed source. Offscreen tests are not a
substitute for a manual real-desktop visual inspection or a signed release.

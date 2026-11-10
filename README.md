# Resistor Color Code Calculator

Development version 3.0.0 supports Android, Windows and Linux, with 4-, 5- and 6-band resistance, tolerance ranges and temperature coefficients.

## Android

The native offline Java application is in [`android/`](android/README.md). It requires Android 7.0 or newer and requests no permissions. See [`android/PROVENANCE.md`](android/PROVENANCE.md) for the recovered source and historical APK checksums.

## Desktop

`resistanceCalculator.py` contains the newer v3 PyQt6 interface, recovered from the Android conversion's original-source snapshot. The older tracked files in `build/` and `dist/` are historical v1/v2 output, not the new release. Do not use those binaries to identify the current version.

The Windows EXE and Linux tar.gz are per-user source installers. They require **64-bit Python 3.12 and internet access at installation time**, and fetch pinned PyQt6 dependencies directly from PyPI. They are not standalone/offline packages. Windows installation uses the Python launcher; Linux needs Python venv and Qt graphics libraries. See [`packaging/desktop/README.txt`](packaging/desktop/README.txt) for exact setup, launch and uninstall instructions.

Source usage: install dependencies with `python -m pip install -r requirements.txt`, then run `python resistanceCalculator.py`. The broken legacy v2 `setup.py` entry point has been removed; use these supported routes.

## Development and validation

GitHub Actions on this branch builds and tests Android, and builds, installs, tests and uninstalls the Windows/Linux source installers. Desktop tests cover math, mode transitions, icons, compact screens, and repeated Help/About dialog opening/closing using offscreen Qt. The dependency-free numeric harness is in `android/tests/CoreTest.java`. Full physical-device testing is separate from build and logic checks.

The original `main` branch and local working directories are not changed by this development import. See [`PROVENANCE.md`](PROVENANCE.md).

## License

Application source: MIT, copyright Johnny Watts. Desktop PyQt6 and Qt dependencies have their own licenses; the application license does not replace their GPL/commercial and LGPL/GPL/commercial terms.

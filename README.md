# Resistor Color Code Calculator

Development version 3.0.0 supports Android, Windows and Linux, with 4-, 5- and 6-band resistance, tolerance ranges and temperature coefficients.

## Android

The native offline Java application is in [`android/`](android/README.md). It requires Android 7.0 or newer and requests no permissions. See [`android/PROVENANCE.md`](android/PROVENANCE.md) for the recovered source and historical APK checksums.

## Desktop

`resistanceCalculator.py` contains the newer v3 PyQt6 interface, recovered from the Android conversion's original-source snapshot. The older tracked files in `build/` and `dist/` are historical v1/v2 output, not the new release. Do not use those binaries to identify the current version.

Desktop installer build instructions and verified release assets are being prepared on the `development` branch. Source usage: install the dependencies in `requirements.txt`, then run `python resistanceCalculator.py`.

## Development and validation

GitHub Actions on this branch builds and tests the Android app. The dependency-free numeric harness is in `android/tests/CoreTest.java`. Full physical-device testing is separate from build and logic checks.

The original `main` branch and local working directories are not changed by this development import. See [`PROVENANCE.md`](PROVENANCE.md).

## License

Application source: MIT, copyright Johnny Watts. Desktop PyQt6 and Qt dependencies have their own licenses; the application license does not replace their GPL/commercial and LGPL/GPL/commercial terms.

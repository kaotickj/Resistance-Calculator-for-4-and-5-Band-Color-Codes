# Version 3.0.0 source recovery

The development branch is based on GitHub main commit `805fb8281118841f81a2b25ede97a3d114b4f3cb` (2025-07-06, desktop v2).

The Android project and newer desktop Python v3 source were recovered from `Resistor-Color-Code-Android-Project.zip`, created 2026-10-10. SHA-256: `590a5b5379665ac0dd3f03646042e1cbeae50de500f7dff96a2c9b4884897428`.

The archive's `original-resistanceCalculator.py` is preserved verbatim in `android/` for comparison. The root Python program imports that newer source, rather than replacing it with the older v2 copy. Its platform guard already includes the Linux/macOS taskbar fix observed in an older local working tree. Uncommitted local Python/PyInstaller files and build outputs were not copied, altered or reset.

The archive's launcher icon is identical to the repository's existing `icon.png` (Git blob `b17f63aa410727cef0f7f117284976de8e34d863`). MIT copyright attribution is retained. No signing key, password, local.properties or generated APK is committed.

The historical APK and archive have a matching application identity/version, but the original build's toolchain and signing key were not preserved with the source. This import does not claim byte-for-byte reproducibility of the historical APK. New artifacts must be built from the recorded development commit and verified separately.

Desktop release preparation fixes the forced 1000px minimum height with a scroll area, uses Qt-owned window icons instead of untyped Windows native handles, adds PNG fallback and a main() entry point. The source snapshot in android/ remains unchanged. Tests and installer scripts document these scoped packaging/startup changes.

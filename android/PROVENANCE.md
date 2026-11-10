# Android source and APK provenance

Recovered source archive: `Resistor-Color-Code-Android-Project.zip` (2026-10-10), SHA-256 `590a5b5379665ac0dd3f03646042e1cbeae50de500f7dff96a2c9b4884897428`.

Historical APK: `Resistor-Color-Code.apk` (139752 bytes), SHA-256 `8ee84dc43ebe9c792440a68f7b7a5fb4024c6829c5e364d5b8ef34fb916bc8f3`.

Inspected historical APK manifest: `com.kaotickj.resistorcalculator`, versionCode 1, versionName `3.0-android`, minSdk 24, targetSdk 34, compileSdk 35. No uses-permission declarations.

Its signing certificate is `CN=Android Debug,O=Android,C=US`, SHA-256 `b02d19d3c5af914c2c26f3285cfd3c861d7ba07158252c098c00ecad8ac18681`. The historical file is debug-signed, not a production identity. Its old report stated 80 calculation checks passed, without physical-device testing.

The development release increments versionCode to 2 and versionName to `3.0.0`. A new production signing identity will not install as an update over the historical debug APK. Uninstall the debug build first; later releases must use the same production key and a higher versionCode.

Build artifacts are unsigned until an explicitly authorized signing step verifies them. The key is never stored in this repository. Source/APK equivalence is established for each new build by its recorded commit; the historical APK is not claimed to be a reproducible build of the archive.

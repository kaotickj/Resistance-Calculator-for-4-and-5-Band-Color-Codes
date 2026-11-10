# Resistor Color Code Calculator for Android

Native Java adaptation of Kaotick Jay's PyQt6 application. It supports 4-, 5- and 6-band calculations, tolerance/minimum/maximum values, temperature coefficients, live preview, Help and About, fully offline with no permissions.

## Build

Requires JDK 17, Gradle 8.10.2 and Android SDK 35 / Build Tools 35.0.0. From this directory:

```sh
gradle --no-daemon :app:lint :app:assembleRelease
```

The resulting `app/build/outputs/apk/release/app-release-unsigned.apk` requires signing before installation. No production key is included. The repository's `Build resistor release` Actions workflow runs from `development` and uploads an explicitly unsigned artifact pending authorized signing.

## Logic tests

```sh
mkdir -p out
javac -encoding UTF-8 -d out app/src/main/java/com/kaotickj/resistorcalculator/ResistorCore.java tests/CoreTest.java
java -cp out CoreTest
```

The test harness has 80 assertions. Build and logic checks do not constitute physical-device tests.

## Install compatibility

Android 7.0+ (API 24), package `com.kaotickj.resistorcalculator`. Version 3.0.0 uses versionCode 2. The old October APK used a debug certificate. A release signed with a different certificate requires uninstalling that old build first. See [provenance](PROVENANCE.md).

## License

MIT; see `LICENSE`. Original developer: Kaotick Jay, https://github.com/kaotickj.

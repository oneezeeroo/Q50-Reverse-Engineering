# Minimal Q50 RPM app example

This directory contains an intentionally small, source-only educational example. It is based on the observed application-side approach used by the working Red Sport reference app: a normal Android activity, IVI manifest metadata, and `SensorManager` access to a vehicle signal.

It is **not** a ready-to-install package and is not presented as a complete Q50 application toolchain.

```text
normal Android Activity
        |
        v
IVI metadata in AndroidManifest.xml
        |
        v
SensorManager
        |
        v
vehicle sensor events
```

The example watches **sensor type 13**, which was treated as RPM by the reference app examined in this project. That mapping may differ across software revisions, model years, trims, or vehicle configurations.

## What is included

```text
AndroidManifest.xml
src/com/example/q50sample/MainActivity.java
```

The example does **not** include:

- an Android build project or Gradle configuration
- an EPK builder
- vehicle-specific key material
- recovered Infiniti files
- a prebuilt APK
- a prebuilt EPK
- installation or compatibility validation

APK building, signing, EPK packaging, compatibility checks, USB handling, and device installation are separate research tasks covered conceptually by the rest of this repository.

## What the manifest demonstrates

The manifest keeps the parts observed as useful in the working reference application:

- API 10 compatibility
- normal `MAIN` / `LAUNCHER` activity
- landscape orientation
- IVI metadata
- `com.ygomi.permission.IVI_CAN_READ`

The stock HomeScreen was observed reading application metadata, including `ivi.isDistractive`.

## What `MainActivity` demonstrates

The Java example:

1. obtains Android's `SensorManager`,
2. looks up sensor type 13,
3. registers a listener, and
4. displays the latest value from `SensorEvent.values[0]`.

That is the same broad Android mechanism used by the working reference app, reduced to one signal for clarity.

## What this proves

- The observed vehicle-data path can be represented with ordinary Android sensor APIs.
- A minimal example can document the application shape without distributing proprietary files or a turnkey installer.

## Important

Use this research code only with systems you own or are authorized to test. Sensor IDs, metadata behavior, permissions, and IVI installation policy may differ between software revisions and vehicle configurations.

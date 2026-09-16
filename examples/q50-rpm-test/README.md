# Minimal Q50 app example

This is intentionally a small source example, not a ready-to-flash package.

The point is to show the basic shape of a Q50-compatible Android app based on what I found in the working Red Sport application:

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

The example only watches **sensor type 13**, which is the RPM sensor observed in the reference app.

It does not include:

- an EPK builder
- vehicle-specific key material
- recovered Infiniti files
- a prebuilt APK
- a prebuilt EPK

You still need to understand the Android build process and the EPK research in the rest of this repo.

## Files

```text
AndroidManifest.xml
src/com/example/q50sample/MainActivity.java
```

## What the manifest demonstrates

The manifest keeps the parts that were useful in the working reference application:

- API 10 compatibility
- normal MAIN / LAUNCHER activity
- landscape orientation
- IVI metadata
- `com.ygomi.permission.IVI_CAN_READ`

The stock HomeScreen was observed reading application metadata, including `ivi.isDistractive`.

## What MainActivity demonstrates

The Java example does three things:

1. gets Android's `SensorManager`
2. finds sensor type 13
3. displays the latest RPM value from `SensorEvent.values[0]`

That is basically the same Android mechanism the working Red Sport app uses for live vehicle data, just stripped down to one signal.

## Important

This is research code for systems you own or have permission to test.

Sensor IDs and IVI behavior may differ between software revisions, model years, or vehicle configurations.

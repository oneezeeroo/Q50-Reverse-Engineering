# Research log

This is a running record of the project, grouped by investigation area rather than by date. It records the evidence that shaped the current model and keeps unresolved questions visible.

## Getting a usable picture of the system

The first problem was identifying the platform. The Q50 IVI is not a normal Android head unit: the recovered image shows a Linux-oriented side and a modified Android environment. The Android side contains applications and IVI-facing code, while the division of responsibility between the two sides remains incomplete.

Once that was clear, the investigation shifted away from treating the system like a phone or tablet and toward the Q50-specific application and USB path.

## Finding the EPK code

The first major lead was the Connexis EPK code:

```text
com.connexis.ivi.utils.epk
com.connexis.ivi.utils.epk.v1
com.connexis.ivi.utils.epk.v2
com.connexis.ivi.utils.epk.v2_2
com.connexis.ivi.utils.epk.v2_3
```

From there, the parser, version handling, envelope fields, payload blocks, encryption helpers, and AppsManager USB path were traced in the available decompiled software.

## Mapping EPK v2

The v2 envelope contains:

```text
magic
version
payload type
block count
wrapped-key length
256-byte wrapped-key field
```

Each payload block then stores a fixed-width filename, encrypted length, and encrypted file data. The implementation uses RSA to wrap temporary symmetric key material and AES-CBC for file payloads.

A small independent parser was written to reproduce the observed structure outside the original code. It is intentionally read-only and does not require device-specific keys.

## Testing against a real working package

A known working community EPK was used as a reference instead of relying only on decompiled factory code. It parsed as:

```text
EPK version: 2
payload type: 2
block count: 1
payload: APK
```

Recovering the APK provided a concrete example of what a custom Q50 application looks like on the stock system.

## What the working APK showed

The app targets API 10, uses a normal `MAIN` / `LAUNCHER` activity, and does not request the Android system UID.

It includes IVI-specific metadata, and the stock HomeScreen code was observed reading at least one of those values directly.

The APK is signed like a normal third-party Android application rather than an obvious OEM system package. This describes the examined sample and does not settle all package-manager policy questions.

## Vehicle data

The largest app-side finding was how the reference dashboard reads the car. It does not parse raw CAN frames itself. Instead, it uses:

```text
SensorManager
  -> getSensorList(...)
  -> registerListener(...)
  -> onSensorChanged(...)
  -> SensorEvent.values[]
```

The reference app exposed a useful group of vehicle sensor IDs, including RPM, coolant, oil temperature, oil pressure, speed, throttle, G-force, gear, power, and TPMS. Those mappings are documented in [sensor-map.md](sensor-map.md).

## What this proves

- The investigation has moved from broad platform identification to concrete parser, package, APK, and sensor observations.
- The EPK structure can be examined independently without publishing sensitive inputs.
- A minimal Android example can document the observed application-side sensor path without pretending to be a complete install pipeline.

## Current next step

The next practical step is to build a very small API-10-compatible app that explores three separate questions:

1. whether it can be packaged through the same EPK/USB path,
2. whether it appears correctly in the IVI launcher,
3. whether it reads selected live sensors.

The first build should remain simple. Install, launch, and data access should be evaluated independently before adding UI or extra features.

## Still open

- hardware verification across software revisions and vehicle configurations
- exact EPK signature and verification boundaries
- payload-type semantics beyond the observed sample
- required permissions and sensor indexes
- the final Linux/Android responsibility split

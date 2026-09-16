# Research log

This is my running record of the project, grouped by what I investigated instead of by date.

## Getting a usable picture of the system

The first problem was figuring out what kind of platform I was actually dealing with.

The Q50 IVI is not a normal Android head unit. The recovered image shows a Linux-oriented side and a modified Android environment. The Android side contains the apps and a lot of the IVI-facing code, while other system work appears to happen outside of it.

Once that was clear, I stopped treating the system like a normal phone or tablet and started following the Q50-specific install path instead.

## Finding the EPK code

The first major lead was the Connexis EPK code:

```text
com.connexis.ivi.utils.epk
com.connexis.ivi.utils.epk.v1
com.connexis.ivi.utils.epk.v2
com.connexis.ivi.utils.epk.v2_2
com.connexis.ivi.utils.epk.v2_3
```

From there I traced the parser, version handling, envelope fields, payload blocks, encryption helpers, and the AppsManager USB path.

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

Each payload block then stores a fixed-width filename, encrypted length, and encrypted file data.

The implementation uses RSA for wrapping a temporary symmetric key and AES-CBC for file payloads.

I wrote a small independent parser to make sure the format could be reproduced outside of the original code.

## Testing against a real working package

The next step was using a known working community EPK as a reference instead of relying only on decompiled factory code.

That package parsed as:

```text
EPK version: 2
payload type: 2
block count: 1
payload: APK
```

Recovering the APK gave me a real example of what a custom Q50 app looks like.

## What the working APK showed

The app targets API 10, uses a normal `MAIN` / `LAUNCHER` activity, and does not request the Android system UID.

It includes IVI-specific metadata, and the stock HomeScreen code was observed reading at least one of those values directly.

The APK is also signed like a normal third-party Android application rather than an obvious OEM system package.

## Vehicle data

The biggest app-side finding was how the reference dashboard reads the car.

It does not parse raw CAN frames itself.

Instead it uses:

```text
SensorManager
  -> getSensorList(...)
  -> registerListener(...)
  -> onSensorChanged(...)
  -> SensorEvent.values[]
```

From there I was able to map a useful group of vehicle sensor IDs, including RPM, coolant, oil temperature, oil pressure, speed, throttle, G-force, gear, power, and TPMS.

Those mappings are documented in [sensor-map.md](sensor-map.md).

## Next practical test

The next step is to build a very small API-10-compatible app that does three things:

1. installs through the same EPK/USB path,
2. appears correctly in the IVI launcher,
3. reads a few live sensors.

The first build will stay simple on purpose. I want to prove install, launch, and data access before spending time on UI or extra features.

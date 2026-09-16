# Vehicle sensor map

One of the most useful findings came from a working third-party Q50 dashboard app.

Instead of decoding raw CAN frames inside the app, it uses Android's normal `SensorManager` API. The app enumerates sensors, registers a `SensorEventListener`, and reads values from `SensorEvent.values[]`.

This indicates that at least part of the vehicle data is exposed to Android applications by the IVI layer. It does not establish that every vehicle or software revision exposes the same set of sensors.

## Observed sensor types

| Sensor type | Vehicle value |
| ---: | --- |
| 12 | Torque |
| 13 | Engine RPM |
| 14 | Coolant temperature |
| 15 | Oil temperature |
| 16 | Oil pressure |
| 17 | Vehicle speed |
| 20 | Lateral G |
| 21 | Longitudinal G |
| 22 | Gear |
| 23 | Throttle |
| 32 | Power |
| 36 | TPMS front-right |
| 37 | TPMS front-left |
| 38 | TPMS rear-right |
| 39 | TPMS rear-left |

The reference app also treats sensors as likely vehicle sensors when the vendor string contains `YGOMI`, the sensor name contains `VS_ID`, or the type falls in the 12–53 range. That is the reference app's heuristic, not a platform-wide definition.

## Conversions used by the reference app

These are the conversions used by the working app examined:

- speed: raw × `0.621371` = mph
- torque: raw × `0.7375621` = lb-ft
- coolant/oil temperature: raw Celsius converted to Fahrenheit
- oil pressure: raw × `145.0377` = psi

The app keeps the full `values[]` array for each sensor. It normally uses index 0, but can select another index for certain signals.

## Minimal Android pattern

The basic read path is the normal Android sensor API:

```java
SensorManager sm = (SensorManager) getSystemService(SENSOR_SERVICE);

for (Sensor s : sm.getSensorList(Sensor.TYPE_ALL)) {
    sm.registerListener(listener, s, SensorManager.SENSOR_DELAY_GAME);
}
```

Then:

```java
public void onSensorChanged(SensorEvent event) {
    int type = event.sensor.getType();
    float[] values = event.values;
}
```

The repository's [minimal RPM example](../examples/q50-rpm-test/README.md) uses sensor type 13 because that was the simplest signal observed in the reference app.

## What this proves

- The reference app obtains vehicle values through Android sensor events.
- A useful group of vehicle signals can be mapped from sensor type IDs in that app.
- Raw CAN decoding is not required in the reference application's app-side data path.

## Still needs hardware verification

Do not assume every Q50 software revision behaves exactly the same. Open verification areas include:

- model-year differences
- engine and trim differences
- alternate indexes inside `SensorEvent.values[]`
- sensors missing on specific vehicles
- permissions actually required by each signal
- units, scaling, and update behavior outside the examined reference app

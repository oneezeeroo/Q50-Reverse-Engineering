# Vehicle sensor map

One of the most useful findings came from a working third-party Q50 dashboard app.

Instead of decoding raw CAN frames inside the app, it uses Android's normal `SensorManager` API. The app enumerates sensors, registers a `SensorEventListener`, and reads values from `SensorEvent.values[]`.

That means at least part of the vehicle data is already being exposed to Android apps by the IVI layer.

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

The reference app also treats sensors as likely vehicle sensors when the vendor string contains `YGOMI`, the sensor name contains `VS_ID`, or the type falls in the 12–53 range.

## Conversions used by the reference app

These are the conversions used by the working app I inspected:

- speed: raw × 0.621371 = mph
- torque: raw × 0.7375621 = lb-ft
- coolant/oil temperature: raw Celsius converted to Fahrenheit
- oil pressure: raw × 145.0377 = psi

The app keeps the full `values[]` array for each sensor. It normally uses index 0, but it can select another index for certain signals.

## Minimal Android pattern

The basic read path is just the normal Android sensor API:

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

For a first custom app, sensor type 13 for RPM is probably the simplest thing to test.

## Still needs hardware verification

I would not assume every Q50 software revision behaves exactly the same.

Things still worth checking:

- model-year differences
- engine/trim differences
- alternate indexes inside `SensorEvent.values[]`
- which sensors are missing on certain cars
- which permissions are actually required

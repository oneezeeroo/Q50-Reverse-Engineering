package com.example.q50sample;

import android.app.Activity;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends Activity implements SensorEventListener {

    // Sensor ID observed as RPM in the working Red Sport app.
    private static final int SENSOR_RPM = 13;

    private SensorManager sensorManager;
    private Sensor rpmSensor;
    private TextView output;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        output = new TextView(this);
        output.setTextSize(34);
        output.setText("Waiting for RPM sensor...");
        setContentView(output);

        sensorManager =
                (SensorManager) getSystemService(SENSOR_SERVICE);

        if (sensorManager != null) {
            rpmSensor =
                    sensorManager.getDefaultSensor(SENSOR_RPM);
        }
    }

    @Override
    protected void onResume() {
        super.onResume();

        if (sensorManager == null || rpmSensor == null) {
            output.setText("RPM sensor not found");
            return;
        }

        sensorManager.registerListener(
                this,
                rpmSensor,
                SensorManager.SENSOR_DELAY_GAME
        );
    }

    @Override
    protected void onPause() {
        super.onPause();

        if (sensorManager != null) {
            sensorManager.unregisterListener(this);
        }
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        if (event.sensor.getType() != SENSOR_RPM) {
            return;
        }

        if (event.values == null || event.values.length == 0) {
            return;
        }

        float rpm = event.values[0];
        output.setText("RPM: " + Math.round(rpm));
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        // Nothing needed for this test.
    }
}

# CAN Capture & Native Tune-Switching Roadmap

## Goal

Determine how the Q50 changes vehicle states from the factory infotainment system, then compare that behavior with EcuTek/RaceROM map switching.

The long-term target is a native infotainment app that can request tune-map changes without requiring a phone or the EcuTek Bluetooth interface for routine map switching.

> Current phase is **passive observation only**. Do not transmit arbitrary CAN frames until the relevant buses, messages, and safety behavior are understood.

---

## Phase 1 — Build the CAN Monitoring Setup

### Hardware to acquire

- [ ] SocketCAN-compatible USB-to-CAN interface
  - CANable / CANable 2.0 class device
  - CANtact-class interface is another option
- [ ] OBD-II breakout cable or breakout box
  - Makes passive access easier and avoids repeatedly probing vehicle wiring
- [ ] USB cable required by the selected CAN interface
- [ ] Laptop for capture/analysis
- [ ] Optional second CAN interface for later multi-bus comparison
- [ ] Optional bench power supply / spare infotainment harness for off-car testing

### Software to install

Most of the software required for the first phase is free.

- [ ] SavvyCAN — visual CAN capture and frame analysis
- [ ] Linux SocketCAN utilities (`can-utils`)
- [ ] Wireshark with SocketCAN support
- [ ] Python 3
- [ ] python-can
- [ ] Git for keeping capture notes/scripts versioned

### Initial validation

- [ ] Confirm the CAN adapter is recognized by the laptop
- [ ] Confirm passive receive-only capture works
- [ ] Determine which CAN bus/buses are visible from the diagnostic connector
- [ ] Record interface bitrate/configuration
- [ ] Save a short baseline capture with no controls being touched

---

## Phase 2 — Use Factory Drive Modes as the Known Reference

The stock infotainment already changes drive modes, giving us a known event originating from the factory UI.

### Capture sequence

Create a timestamped capture containing:

- [ ] 20–30 seconds untouched baseline
- [ ] Standard → Sport
- [ ] Sport → Standard
- [ ] Standard → Sport
- [ ] Sport → Standard
- [ ] Standard → Personal
- [ ] Personal → Standard

Repeat the sequence multiple times.

### Analysis

- [ ] Identify arbitration IDs that change at each drive-mode transition
- [ ] Identify bytes/bits that consistently track the selected mode
- [ ] Separate command/request frames from broadcast state/status frames
- [ ] Determine whether the relevant traffic is visible from OBD-II
- [ ] Document candidate IDs and byte positions
- [ ] Create a small script to compare capture windows around marked events

### Deliverable

A documented path resembling:

```
Infotainment UI
      ↓
Infotainment/Linux vehicle service
      ↓
Vehicle network
      ↓
Drive-mode controller / ECU
```

We do **not** assume the screen directly sends raw CAN.

---

## Phase 3 — Capture RaceROM Map Switching

Once the vehicle is running an EcuTek/RaceROM calibration with multiple maps:

### Factory-control capture

- [ ] Record baseline traffic
- [ ] Perform Map 1 → Map 2 using the supported steering-wheel/control method
- [ ] Map 2 → Map 3
- [ ] Map 3 → Map 4
- [ ] Return to Map 1
- [ ] Repeat each transition several times

### Questions to answer

- [ ] Does the ECU receive a dedicated map-selection message?
- [ ] Is RaceROM simply interpreting normal cruise-control button states?
- [ ] Is the current map broadcast anywhere on the vehicle network?
- [ ] Which ECU/module owns the final state?

---

## Phase 4 — Compare Against ECU Connect

Only after the passive CAN workflow is understood:

- [ ] Obtain/access an EcuTek ECU Connect interface
- [ ] Capture Map 1 → Map 2 from the official ECU Connect workflow
- [ ] Repeat the same transition several times
- [ ] Compare vehicle-bus traffic with the steering-wheel method
- [ ] Determine whether ECU Connect uses:
  - normal CAN frames
  - diagnostic requests
  - a proprietary EcuTek/RaceROM command
  - a combination of the above
- [ ] Inspect the Android ECU Connect application separately for Bluetooth/protocol clues if needed

### Key question

Does the Bluetooth dongle contain required proprietary logic, or is it primarily translating a phone command into a vehicle-side request that the infotainment could eventually reproduce?

---

## Phase 5 — Trace the Infotainment Vehicle Interface

Use the SD-card/head-unit research already underway.

Search the Linux/Android filesystem and binaries for:

- [ ] CAN
- [ ] SocketCAN / can0 / can1
- [ ] vehicle services
- [ ] diagnostic services
- [ ] IPC / D-Bus
- [ ] drive-mode references
- [ ] ECM / BCM references
- [ ] UART / serial bridges
- [ ] Nissan-specific vehicle APIs

Then correlate software behavior with the CAN IDs discovered during the drive-mode captures.

### Desired discovery

```
Custom EPK / Android UI
        ↓
existing Nissan IPC/API
        ↓
Linux vehicle service
        ↓
CAN gateway
        ↓
ECU
```

Reusing the factory communication path is preferable to giving the Android guest unrestricted raw CAN access.

---

## Phase 6 — Safe Bench Proof of Concept

Before any active testing on a moving vehicle:

- [ ] Reproduce the relevant communication on a bench/spare infotainment unit where possible
- [ ] Implement read-only monitoring first
- [ ] Display current drive mode / map state in a test UI
- [ ] Add explicit connection/state validation
- [ ] Add fail-closed behavior if expected ECU response is missing
- [ ] Only then investigate controlled map-selection requests

---

## Final Target

A native Q50 performance application with a flow similar to:

```
Q50 Performance App
        ↓
Factory infotainment vehicle interface
        ↓
Vehicle network / diagnostic transport
        ↓
ECU + RaceROM
        ↓
Map 1 / Map 2 / Map 3 / Map 4
```

Potential future UI:

- Current active map
- Map names supplied by the tuner
- Read-only engine parameters
- Explicit map-switch confirmation
- Connection / ECU status
- Safety lockouts

---

## Immediate Next Actions

1. [ ] Buy a compatible USB-to-CAN interface.
2. [ ] Buy an OBD-II breakout cable/box.
3. [ ] Install SavvyCAN, `can-utils`, Wireshark, Python, and python-can.
4. [ ] Verify passive CAN capture.
5. [ ] Capture the factory infotainment switching Standard/Sport/Personal modes.
6. [ ] Commit the first raw capture plus a written experiment log.
7. [ ] Analyze which IDs/bytes correlate with drive-mode changes.
8. [ ] Only after that, move to RaceROM/EcuTek map-switch captures.

---

## Research Rule

Every identified CAN ID should be treated as **unknown until repeatable evidence proves its role**. Keep raw captures, timestamps, test conditions, and conclusions separate so guesses do not become undocumented assumptions.

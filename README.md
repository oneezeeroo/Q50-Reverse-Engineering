# Q50 Reverse Engineering

<p align="center">
  <img src="assets/q50-reverse-engineering.webp" alt="Q50 Reverse Engineering project banner" width="100%">
</p>

<p align="center">
  <a href="https://github.com/oneezeeroo/Q50-Reverse-Engineering/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-2f855a" alt="MIT license"></a>
  <a href="https://github.com/oneezeeroo/Q50-Reverse-Engineering"><img src="https://img.shields.io/badge/status-active%20research-6f42c1" alt="Active research"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/tooling-Python%203-3776AB" alt="Python 3 tooling"></a>
</p>

> Independent reverse-engineering research into the Infiniti Q50 infotainment platform, its hybrid Linux/Android architecture, EPK application packages, and vehicle-data interfaces.

This project documents the process of turning a black-box automotive IVI system into a more understandable technical model. The repository focuses on evidence from decompiled software, package-format analysis, a known working third-party application, and small reproduction tools—not on publishing proprietary firmware or a turnkey installer.

## Why this project matters

Automotive infotainment systems sit at the intersection of embedded Linux, legacy Android, proprietary packaging, application security, and vehicle data. This work demonstrates how to build a useful architecture model from incomplete evidence, separate observed behavior from assumptions, and create small tools that make reverse-engineering findings reproducible without distributing sensitive device material.

## Key Findings

- The Q50 infotainment image contains a Linux-oriented side and a modified Android 2.3 environment.
- Connexis/YGOMI IVI components include an application-management stack with versioned EPK parsers.
- The traced USB path watches removable media, parses EPK packages, and passes normal payload files toward the IVI package manager.
- The observed EPK v2 envelope is 268 bytes before payload blocks and uses big-endian numeric fields.
- EPK v2 uses a hybrid encryption model: RSA-wrapped temporary key material and AES-CBC payload encryption.
- A known working community package was observed as EPK v2, payload type 2, one APK block.
- The reference APK targets Android API 10, uses a normal launcher activity, and includes IVI-specific manifest metadata.
- The reference app reads vehicle data through Android `SensorManager` rather than parsing raw CAN frames in the app.
- The reference app exposed useful mappings for RPM, temperatures, speed, throttle, torque, G-force, gear, power, and TPMS.

These findings describe the samples and software revisions examined. They are not claims that every Q50 revision behaves identically.

## Technical Highlights

- **Architecture reconstruction:** Linux/Android responsibility mapping from recovered software and observed control flow.
- **Binary format analysis:** EPK header, fixed-width fields, payload blocks, offsets, and length handling.
- **Cryptography analysis:** Separation of EPK payload encryption from APK signing; RSA/AES-CBC flow documented without publishing device keys.
- **Android internals:** API 10 compatibility, launcher behavior, IVI metadata, permissions, and `SensorManager` access.
- **Static analysis:** Tracing decompiled Java packages including `com.connexis.ivi.utils.epk` and AppsManager-related paths.
- **Reproduction tooling:** A read-only Python inspector for examining EPK structure without decrypting payloads.

## Skills Demonstrated

`reverse-engineering` · `firmware-analysis` · `embedded-systems` · `Android internals` · `binary format analysis` · `Python tooling` · `Java decompilation` · `cryptography analysis` · `automotive cybersecurity`

## Current Status

### Confirmed from the examined software and package samples

- Hybrid Linux/Android IVI architecture model.
- Versioned Connexis EPK parser packages.
- EPK v2 envelope and payload-block layout.
- Big-endian field encoding in the observed v2 implementation.
- RSA/AES-CBC hybrid encryption flow at a high level.
- API 10 launcher structure and IVI metadata in the reference APK.
- Vehicle-sensor access through Android `SensorManager` in the reference app.
- A read-only parser that reproduces the observed EPK structure.

### Observed in specific reference material

- EPK version 2, payload type 2, and one APK payload block.
- Sensor type 13 treated as RPM by the reference application.
- The reference APK using a normal developer-style v1/JAR certificate.
- Stock HomeScreen code reading at least one IVI application metadata field.

### Still being tested or mapped

- Differences across model years, trims, engines, and IVI software revisions.
- The complete meaning of EPK payload-type values.
- The exact signature and verification boundary in the install path.
- The role of the 256-byte wrapped-key field in each package variant.
- Which Android permissions and sensor indexes are required in practice.
- The final Linux/Android boundary and hardware behavior of the USB install flow.

## Want to build an app for your Q50?

Start with the intentionally small [Q50 RPM test example](examples/q50-rpm-test/README.md). It demonstrates the shape of an API-10-compatible Android application based on the observed Red Sport approach:

- a normal `MAIN` / `LAUNCHER` activity
- IVI metadata in `AndroidManifest.xml`
- `com.ygomi.permission.IVI_CAN_READ`
- Android `SensorManager`
- reading the observed RPM sensor type

**The source cannot simply be copied to a USB drive and installed.** APK building, APK signing, EPK packaging, package compatibility, and the device's installation checks are separate steps. This repository intentionally does not provide a ready-to-install APK/EPK pipeline, device-specific keys, or sensitive firmware material.

The goal is to document the architecture and give researchers enough context to build and test their own controlled tooling—not to turn the repository into a one-click installer guide.

## Repository Structure

```text
.
├── assets/
│   ├── q50-ivi-architecture.webp
│   └── q50-reverse-engineering.webp
├── docs/
│   ├── architecture.md
│   ├── custom-app-notes.md
│   ├── epk-format.md
│   ├── research-log.md
│   └── sensor-map.md
├── examples/
│   └── q50-rpm-test/
├── tools/
│   └── epk_inspect.py
├── DISCLAIMER.md
├── LICENSE
└── README.md
```

## Documentation

- [IVI architecture](docs/architecture.md) — current platform model and open boundaries.
- [EPK format notes](docs/epk-format.md) — observed v2 envelope, blocks, and encryption model.
- [Custom app notes](docs/custom-app-notes.md) — reference APK compatibility and IVI metadata.
- [Vehicle sensor map](docs/sensor-map.md) — observed sensor IDs and conversions.
- [Research log](docs/research-log.md) — how the findings were developed and what comes next.
- [Minimal Q50 app example](examples/q50-rpm-test/README.md) — educational source-only Android example.

The architecture diagram in [`assets/q50-ivi-architecture.webp`](assets/q50-ivi-architecture.webp) is the current working model; component boundaries remain subject to verification.

## Tooling

[`tools/epk_inspect.py`](tools/epk_inspect.py) is a read-only Python inspector for observed EPK v2 structures. It reports the magic, version, payload type, block count, wrapped-key length, filenames, encrypted lengths, and data offsets. It does not decrypt payloads and does not contain device keys.

## Responsible Research

Only test hardware and software you own or are authorized to examine. Avoid distributing proprietary firmware, recovered third-party APKs, private keys, passwords, VIN data, or other device-specific material. Automotive infotainment systems are real embedded systems: incompatible packages or configuration changes can leave a unit unstable or unusable.

## Scope and Disclaimer

This repository is for interoperability and reverse-engineering research on authorized systems. It is not affiliated with, sponsored by, or endorsed by Infiniti, Nissan, or their suppliers. The notes are a work in progress, and conclusions may change as additional software revisions and hardware behavior are verified.

See [DISCLAIMER.md](DISCLAIMER.md) for the full scope and safety notice.

---

**Project note:** Agentic AI was used as a research and editing assistant during parts of this project.

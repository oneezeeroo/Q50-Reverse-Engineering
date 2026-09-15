# Q50 Reverse Engineering

<p align="center">
  <img src="assets/q50-reverse-engineering.webp" alt="Q50 Reverse Engineering project banner" width="100%">
</p>

This repository documents my work reverse engineering the Infiniti Q50 infotainment system. I started with a simple question: how does this system actually package, verify, and install its applications?

That turned into a deeper look at the IVI software, the EPK package format, and the path an application appears to take before it reaches the infotainment unit.

The project is still early. I am documenting each useful finding as I go instead of waiting until everything is finished.

## What I have found so far

The Q50 infotainment platform appears to use a hybrid setup with a Linux side and a heavily modified Android 2.3 environment. The Android side is old enough that normal modern Android assumptions do not always apply, and a lot of the application handling appears to be custom to the IVI platform.

One of the more useful findings so far is the EPK handling code. Decompiled classes under `com.connexis.ivi.utils.epk` show a dedicated parser and data structures for EPK packages.

The parser exposes an envelope structure containing fields such as:

- magic code
- version
- payload type
- block count
- key size
- a 256-byte key buffer

That gives a starting point for working out how EPK files are structured and what the installer expects before accepting a package.

My current working path is:

```text
APK
  -> EPK packaging
  -> signing / verification
  -> USB manager
  -> IVI installation
```

I have not treated that flow as final yet. Part of this project is tracing each step in the code and confirming what actually happens on the hardware.

## What I am working on

The current focus is on understanding the EPK format well enough to reproduce the packaging process.

That means tracing the parser, finding where signatures or keys are checked, following references into the USB manager, and separating the Android-side logic from anything handled by the Linux side.

Once the format is understood well enough, the next step is to build small tools for inspecting and eventually creating test packages.

## Repository layout

```text
assets/
  q50-reverse-engineering.webp
  q50-ivi-architecture.webp

docs/
  architecture.md
  epk-format.md
  research-log.md
```

More code and tooling will be added as the format becomes clearer.

## Project scope

This repository is for research and documentation of hardware and software I am authorized to test.

I am not uploading the original Infiniti firmware, full decompiled source trees, private signing material, VIN data, or other proprietary vehicle data. The goal is to document the behavior I can verify and publish my own notes and tooling around it.

See [DISCLAIMER.md](DISCLAIMER.md) for more information.

## Status

Early research. The notes here will change as I confirm more of the install path and test findings against actual hardware.

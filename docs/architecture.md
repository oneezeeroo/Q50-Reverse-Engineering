# IVI architecture notes

My current model of the Q50 infotainment system is a hybrid platform with a Linux side doing much of the system-level work and a heavily modified Android 2.3 environment handling part of the application layer.

The important part for this project is that the Android environment does not behave like a normal consumer Android device. The application format, install path, and supporting services appear to be specific to the IVI platform.

I am still tracing which responsibilities sit on each side of the system, so this page is a working map rather than a finished architecture diagram.

## Android-side findings

The decompiled software contains a package named:

```text
com.connexis.ivi.utils.epk
```

There is also a versioned package:

```text
com.connexis.ivi.utils.epk.v2
```

That code contains classes for parsing EPK packages and representing parsed entries, envelopes, and payloads.

This is useful because it shows that EPK handling is built into the IVI software rather than being a generic Android APK install path.

## Working install model

The install path I am tracing currently looks like this:

```text
Application APK
      |
      v
EPK package creation
      |
      v
Signing / verification
      |
      v
USB manager
      |
      v
IVI install process
```

The exact boundary between Android and Linux is still being worked out. I do not want to label a step as Android-side or Linux-side until the code or hardware behavior confirms it.

## Questions still open

- Which component creates the final EPK file?
- What is signed, and where is the signature checked?
- What does the 256-byte key field represent?
- Which service receives an EPK from the USB manager?
- Does Linux perform any verification before Android sees the package?
- What payload types are supported?
- Are different EPK versions handled by separate parsers?

These are the areas I am tracing next.

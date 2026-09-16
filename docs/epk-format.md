# EPK format notes

EPK is the package format handled by the Q50 IVI application-management stack.

The relevant framework code includes:

```text
com.connexis.ivi.utils.epk
com.connexis.ivi.utils.epk.v1
com.connexis.ivi.utils.epk.v2
com.connexis.ivi.utils.epk.v2_2
com.connexis.ivi.utils.epk.v2_3
```

The generic wrapper checks the version and routes parsing to the matching implementation.

## EPK v2 envelope

The v2 parser and builder make the outer structure fairly clear:

| Offset | Size | Field |
| ---: | ---: | --- |
| 0x00 | 4 | ASCII magic `.epk` |
| 0x04 | 2 | version |
| 0x06 | 2 | payload type |
| 0x08 | 2 | block count |
| 0x0A | 2 | wrapped-key length |
| 0x0C | 256 | wrapped-key field |

That puts the fixed envelope size at 268 bytes.

The implementation uses Java data streams, so the numeric fields are big-endian.

## Payload blocks

Each file block is stored as:

```text
128 bytes   filename
4 bytes     encrypted payload length
N bytes     encrypted file data
```

The filename is stored as ASCII in a fixed-width field with zero padding.

## Encryption model

The v2 code uses hybrid encryption.

At a high level:

```text
temporary symmetric key
        |
        +--> wrapped with RSA
        |
        +--> used for AES-CBC payload encryption
```

The important point is that an EPK is not just a renamed ZIP file.

Device-specific key material is not included in this repo.

APK signing is also separate from the EPK encryption layer. The working third-party APK I examined had a normal Android APK signature.

## Payload type

The full meaning of every numeric payload type is still not mapped.

One known working community package was observed with:

```text
version      = 2
payload type = 2
block count  = 1
payload      = APK
```

That proves payload type 2 is used by at least one real custom application package, but I am not treating that as proof that "2 = APK" in every case.

The v2 parser separates DRM files from normal data by filename. Files ending in `.drm`, plus names such as `drm.properties` and `drm.json`, are treated as DRM data.

## USB install path

The Android-side flow I have traced so far looks like this:

```text
USB mounted
   |
   v
AppsManager / USBService
   |
   v
EPK found and parsed
   |
   v
normal data file extracted
   |
   v
APK passed to the IVI package manager
```

There are still parts of the install path I want to verify on hardware, but this is enough to start reproducing the package flow in a controlled way.

## Public tool

The repo includes a read-only inspector:

```text
tools/epk_inspect.py
```

It does not decrypt payloads and does not contain device keys.

# EPK format notes

EPK is the package format handled by the Q50 IVI application-management stack. The relevant decompiled framework code includes:

```text
com.connexis.ivi.utils.epk
com.connexis.ivi.utils.epk.v1
com.connexis.ivi.utils.epk.v2
com.connexis.ivi.utils.epk.v2_2
com.connexis.ivi.utils.epk.v2_3
```

The generic wrapper checks the version and routes parsing to a matching implementation.

## EPK v2 envelope

The v2 parser and builder make the following outer structure clear for the examined implementation:

| Offset | Size | Field |
| ---: | ---: | --- |
| `0x00` | 4 | ASCII magic `.epk` |
| `0x04` | 2 | version |
| `0x06` | 2 | payload type |
| `0x08` | 2 | block count |
| `0x0A` | 2 | wrapped-key length |
| `0x0C` | 256 | wrapped-key field |

The fixed envelope size is therefore 268 bytes. The implementation uses Java data streams, so the numeric fields are big-endian.

## Payload blocks

Each file block is stored as:

```text
128 bytes   filename
4 bytes     encrypted payload length
N bytes     encrypted file data
```

The filename is ASCII in a fixed-width, zero-padded field.

## Encryption model

The v2 code uses hybrid encryption:

```text
temporary symmetric key
        |
        +--> wrapped with RSA
        |
        +--> used for AES-CBC payload encryption
```

This is an observed implementation model, not a complete description of all EPK variants. Device-specific key material is not included in this repository.

APK signing is separate from EPK payload encryption. The working third-party APK examined in this project had a normal Android v1/JAR signature.

## Payload type

The meaning of every numeric payload type is not mapped.

One known working community package was observed with:

```text
version      = 2
payload type = 2
block count  = 1
payload      = APK
```

This proves that payload type `2` appears in at least one real custom-application package. It does not prove that `2` means APK for every package or software revision.

The v2 parser separates DRM files from normal data by filename. Files ending in `.drm`, plus names such as `drm.properties` and `drm.json`, are treated as DRM data.

## USB install path

The Android-side flow traced so far is:

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

The complete install path still needs hardware verification, but this model is sufficient to reason about the separate APK, EPK, USB, and package-manager stages.

## What this proves

- The observed EPK v2 structure can be parsed independently.
- EPK is a structured package format, not simply a renamed ZIP file.
- Payload encryption and APK signing are separate layers.
- A read-only inspector can examine package structure without decrypting payloads or publishing device keys.

## What is still unknown

- The full semantics of payload types and DRM-related files.
- The exact key-wrapping and verification behavior for every package variant.
- Whether all EPK versions share the same block layout.
- The hardware-side checks performed after USB discovery.

## Public tool

The repository includes [`tools/epk_inspect.py`](../tools/epk_inspect.py), a read-only inspector for the observed EPK v2 structure. It does not decrypt payloads and does not contain device keys.

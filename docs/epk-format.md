# EPK format notes

EPK appears to be the package format used by the IVI software for application or payload delivery.

The most useful code I have found so far is the parser implementation under:

```text
com.connexis.ivi.utils.epk.v2
```

One parsed result can contain multiple EPK entries. Each entry contains an envelope and a payload.

A simplified view of the structure is:

```text
EpkParseResult
  entries[]
    EpkEntry
      Envelope
      Payload
```

## Envelope fields

The decompiled `EpkParseResult.EpkEntry.Envelope` class exposes these fields:

```text
magic_code
version
payload_type
block_count
key_size
key[256]
```

The class stores the key buffer as a fixed 256-byte array.

At this stage, I am treating these as parser-level fields only. Their exact byte offsets and serialization order still need to be confirmed from the code that reads the package.

## What these fields may tell us

`magic_code` should help identify the beginning of an EPK structure or confirm that the parser received the expected format.

`version` suggests the package format has changed over time. The presence of a `v2` parser package supports that idea, but the exact differences between versions still need to be traced.

`payload_type` likely tells the installer how to interpret the payload. I have not mapped the numeric values yet.

`block_count` suggests the payload may be processed in blocks rather than as one continuous object.

`key_size` and the 256-byte `key` buffer are especially interesting because they may be related to package verification, encryption, signatures, or another key-based operation. I have not assigned a purpose to them yet because the surrounding code still needs to be followed.

## Current goal

The next step is to find the code that fills the envelope fields from raw bytes.

That should let me answer three important questions:

1. What is the exact EPK header layout?
2. Where does the payload begin?
3. How are keys or signatures used during parsing and installation?

Once those are known, it should be possible to write a small standalone EPK inspection tool and compare its output with the IVI parser.

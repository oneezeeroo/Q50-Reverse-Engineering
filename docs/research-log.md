# Research log

This page is my running record of the reverse engineering work. I am keeping it organized by what I investigated instead of by date.

## Getting a usable picture of the system

The first problem was figuring out what kind of platform I was dealing with.

The Q50 IVI is not a normal Android head unit. My current understanding is that it uses a Linux-based system alongside a heavily modified Android 2.3 environment. That matters because installing an app is not as simple as copying over an APK and calling the normal Android package manager.

From there, I started looking for the code responsible for whatever package format the system actually expects.

## Finding the EPK code

Searching through the decompiled software led me to the EPK utilities.

The package names immediately stood out:

```text
com.connexis.ivi.utils.epk
com.connexis.ivi.utils.epk.v2
```

The `v2` code includes an `EpkParseResult` class with a list of parsed entries. Each entry contains an envelope and a payload.

That was the first point where the package format started to become concrete instead of just being a name.

## Breaking down the envelope

The envelope object contains:

```text
m_magicCode
m_version
m_payloadType
m_blockCount
m_keySize
m_key[256]
```

This gave me a short list of fields to trace backwards into the parser.

The fixed 256-byte key buffer is one of the parts I want to understand before making assumptions about signing or encryption. The code shows that the field exists, but that alone does not tell me whether it stores a public key, signature-related data, encrypted material, or something else.

## Building the install path

The bigger goal is to understand how an application gets from an APK into something the car will accept.

The path I am currently tracing is:

```text
APK
  -> EPK packaging
  -> signing / verification
  -> USB manager
  -> IVI installation
```

The useful part about finding the parser is that I now have somewhere concrete to work from. Instead of searching the whole codebase for anything related to installation, I can follow the EPK classes outward and see what creates them, what consumes them, and what checks happen in between.

## Where the research is now

The main unknowns are still the important ones.

I need to find the code that reads the raw EPK bytes, map the header layout, identify the supported payload types, and trace how the key field is used.

After that, I want to follow the same package through the USB manager and into the install routine. That should make it possible to separate the packaging step from the verification step and eventually reproduce the format with my own tooling.

I am keeping the repo focused on findings I can trace back to code or hardware behavior. Anything that is still a guess stays labeled as one.

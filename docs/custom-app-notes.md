# Red Sport reference app notes

A known working third-party Q50 application was unpacked from a working EPK and used as a reference. It is useful because it shows what a custom application that already runs on the stock system looks like.

The observations below describe that reference APK and package, not a universal requirement for every Q50 software revision.

## Android compatibility

The APK declares:

```text
minSdkVersion    10
targetSdkVersion 10
```

The practical compatibility target is therefore Android 2.3 / API 10 behavior. The APK itself was built with modern tooling, which suggests that current development tooling may still be usable when targeting the older runtime, but that has not been established as a complete build recipe here.

## Launcher setup

The application uses a normal Android launcher activity:

```xml
<intent-filter>
    <action android:name="android.intent.action.MAIN"/>
    <category android:name="android.intent.category.LAUNCHER"/>
</intent-filter>
```

It does not declare `android:sharedUserId="android.uid.system"`. This makes the observed custom-app path look more like a normal Android application than a privileged factory component.

## IVI metadata

The working app contains IVI-specific metadata:

```xml
<meta-data android:name="ivi.isDistractive" android:value="false"/>
<meta-data android:name="ivi.shortcut" android:value="true"/>
<meta-data android:name="ivi.audio" android:value="false"/>
<meta-data android:name="ivi.autorun" android:value="false"/>
<meta-data android:name="ivi.Disclaimer" android:value="false"/>
<meta-data android:name="ivi.supportDisplay" android:value="ALL"/>
<meta-data android:name="ivi.defaultDisplay" android:value="LOWER"/>
```

The stock HomeScreen code was also observed reading `applicationInfo.metaData` and checking `ivi.isDistractive`, so these fields are not treated as arbitrary leftovers in the manifest.

The reference app also requests:

```xml
<uses-permission android:name="com.ygomi.permission.IVI_CAN_READ" />
```

## APK signing

The working APK uses a normal developer-style X.509 RSA certificate and has a valid APK v1/JAR signature, which matters because Android 2.3 understands v1 signing.

Nothing found in the reference APK suggests that a custom application must use an Infiniti or Nissan platform certificate. This is an observation about the examined APK, not a guarantee about all installation-policy checks.

## Working EPK sample

The package containing the reference app was observed as:

```text
EPK version: 2
payload type: 2
block count: 1
payload: one APK
```

These values are treated as a working example rather than a universal specification for every package type.

## What this proves

- A working third-party application can use the normal Android launcher model.
- API 10 compatibility and IVI metadata are relevant to the examined app.
- APK signing is a distinct layer from EPK packaging and encryption.

## What is still unknown

- Which metadata fields are required versus optional.
- Whether the same permission and metadata behavior applies across IVI revisions.
- Which package-manager checks occur after the APK is extracted from an EPK.
- Whether all working third-party applications use the same signing and payload arrangement.

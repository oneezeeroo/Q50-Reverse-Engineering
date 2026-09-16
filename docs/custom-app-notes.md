# Custom app notes

A known working third-party Q50 application was unpacked from a working EPK and used as a reference.

This is useful because it shows what a real custom app that already runs on the stock system looks like.

## Android version

The APK declares:

```text
minSdkVersion    10
targetSdkVersion 10
```

So the important compatibility target is Android 2.3 / API 10 behavior.

The APK itself was built with modern tooling, which is a good sign for anyone trying to build a new app today.

## Launcher setup

It uses a normal Android launcher activity:

```xml
<intent-filter>
    <action android:name="android.intent.action.MAIN"/>
    <category android:name="android.intent.category.LAUNCHER"/>
</intent-filter>
```

It does not declare `android:sharedUserId="android.uid.system"`.

That makes the custom-app path look much more like a normal Android application than a privileged factory component.

## IVI metadata

The working app contains IVI-specific metadata like this:

```xml
<meta-data android:name="ivi.isDistractive" android:value="false"/>
<meta-data android:name="ivi.shortcut" android:value="true"/>
<meta-data android:name="ivi.audio" android:value="false"/>
<meta-data android:name="ivi.autorun" android:value="false"/>
<meta-data android:name="ivi.Disclaimer" android:value="false"/>
<meta-data android:name="ivi.supportDisplay" android:value="ALL"/>
<meta-data android:name="ivi.defaultDisplay" android:value="LOWER"/>
```

The stock HomeScreen code was also observed reading `applicationInfo.metaData` and checking `ivi.isDistractive`, so these fields are not just leftovers in the manifest.

The reference app also requests:

```xml
<uses-permission android:name="com.ygomi.permission.IVI_CAN_READ"/>
```

## APK signing

The working APK uses a normal developer-style X.509 RSA certificate.

It has a valid APK v1/JAR signature, which matters because Android 2.3 understands v1 signing.

Nothing I found in the reference APK suggests that a custom application needs to be signed with an Infiniti or Nissan platform certificate.

## Working EPK sample

The package containing the reference app was:

```text
EPK version: 2
payload type: 2
block count: 1
payload: one APK
```

I am treating those values as an observed working example, not as a universal specification for every package type.

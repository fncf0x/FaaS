#!/bin/bash

mkdir ./android/frida
wget 'https://github.com/hluwa/strongR-frida-android/releases/download/14.2.18/hluda-server-14.2.18-android-x86' -P ./android/frida/
mkdir ./android/SDK
wget 'https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip' -O ./android/SDK/sdk-tools-linux-4333796.zip
cp /usr/share/zoneinfo/Europe/Paris android/timezone/Paris

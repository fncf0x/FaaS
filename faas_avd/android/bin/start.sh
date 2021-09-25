#!/bin/bash

rm -Rf /root/.android/avd/*.avd/*.lock
rm -Rf /root/.android/avd/*.avd/*.cache
adb devices | grep emulator | cut -f1 | while read device; do adb -s $device emu kill; done
emulator -avd $EMULATOR -no-audio -no-boot-anim -no-window -accel on -gpu off -skin 1440x2880 &launched=false
echo -n "Booting device: "
while [ "$launched" == false ]; do
  check=$(adb wait-for-device shell getprop sys.boot_completed | tr -d '\r')
  echo "#####  BOOTING DEVICE  #####"
  if [ "$check" == "1" ]; then
    launched=true
	echo "#####  DEVICE BOOTED! #####"
  else
    sleep 2
  fi
done
sleep 2

adb shell "settings put global window_animation_scale 0.0"
adb shell "settings put global transition_animation_scale 0.0"
adb shell "settings put global animator_duration_scale 0.0"
sleep 2
adb root
sleep 2
adb push '/frida/hluda-server-14.2.18-android-x86' '/data/local/tmp/updater'
adb shell 'chmod +x /data/local/tmp/updater'
adb shell '/data/local/tmp/updater -l 0.0.0.0 -D'&

touch /flask.log
python3 /ws/api/api.py &
tail -f /flask.log

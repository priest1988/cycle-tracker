[app]
title = Pregnancy Calculator
package.name = pregnancycalculator
package.domain = com.sergey.timoshchenko
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.4
icon.filename = icon.png
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.enable_androidx = True
android.release_artifact = apk
android.skip_update = False

[buildozer]
log_level = 2
warn_on_root = 1

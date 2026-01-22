[app]
title = Pregnancy Calculator by Sergei Timoshchenko
package.name = pregnancycalculator
package.domain = com.sergey.timoshchenko
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.2
icon.filename = icon.png
requirements = python3==3.9.17,kivy==2.2.1
orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
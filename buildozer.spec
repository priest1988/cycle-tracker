[app]
title = Pregnancy Calculator by Sergey Timoshchenko
package.name = pregnancycalculator
package.domain = com.sergey.timoshchenko
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.1
icon.filename = icon.png
requirements = python3,kivy
orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
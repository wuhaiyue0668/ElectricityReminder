[app]
title = 容大电费提醒
package.name = electricity
package.domain = org.rongda

source.dir = .
source.include_exts = py,png,jpg,kv
source.main = main.py

requirements = python3,kivy

android.api = 30
android.minapi = 21
android.permissions = INTERNET

version = 1.0
orientation = portrait

[buildozer]
log_level = 2
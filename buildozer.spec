[app]
title = 容大电费提醒
package.name = electricityreminder
package.domain = org.rongda

source.dir = .
source.include_exts = py,png,jpg,kv
source.main = main.py

requirements = python3,kivy

# Android配置 - 使用与工作流中相同的版本
android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 21.4.7075529

# 自动接受许可证
android.accept_license = True

android.permissions = INTERNET

version = 1.0
orientation = portrait

[buildozer]
log_level = 2

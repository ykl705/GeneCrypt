[app]
title = 基因密码
package.name = genecrypt
package.domain = com.genecrypt
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,wav,txt,json,xml
source.exclude_exts = spec
source.exclude_dirs = tests, __pycache__, temp_check, .github
source.exclude_patterns = *.md,*.zip,*.log,gene_game_desktop.py
version = 0.1.1

# 精简依赖，避免版本冲突
requirements = python3,kivy==2.3.0,pillow,filetype

orientation = landscape
fullscreen = 0

android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.gradle_dependencies = androidx.core:core:1.9.0
android.wakelock = True
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,VIBRATE,WAKE_LOCK
android.archs = arm64-v8a
android.allow_backup = True

# 自动接受 SDK license，避免交互式卡住
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
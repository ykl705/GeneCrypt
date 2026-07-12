[app]
title = 基因密码
package.name = genecrypt
package.domain = com.genecrypt
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,wav,txt,json
source.exclude_exts = spec
source.exclude_dirs = tests, __pycache__, temp_check, .github
source.exclude_patterns = buildozer.spec,requirements.txt,*.md,*.zip,*.log,gene_game_desktop.py,legacy_gui.py
version = 0.1.1

# 关键：确保包含所有必要依赖
requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow,pyjnius,android,plyer

orientation = landscape
fullscreen = 0

android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.gradle_dependencies = androidx.core:core:1.9.0
android.wakelock = True
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, VIBRATE, WAKE_LOCK
android.archs = arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
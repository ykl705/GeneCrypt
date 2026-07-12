[app]
title = 基因密码
package.name = genecrypt
package.domain = com.genecrypt
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,wav
source.exclude_exts = spec,txt
source.exclude_dirs = tests, __pycache__, temp_check, .github
source.exclude_patterns = buildozer.spec,requirements.txt,*.md,*.zip,*.log,gene_game_desktop.py,legacy_gui.py
version = 0.1.1
requirements = python3,kivy>=2.2.0,pillow>=9.0.0
orientation = landscape
fullscreen = 0
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.gradle_dependencies = androidx.core:core:1.9.0
android.wakelock = False
android.permissions = INTERNET
android.archs = arm64-v8a
android.manifest = <uses-feature android:glEsVersion="0x00020000" android:required="true" />
android.allow_backup = True
android.keystore =
android.keystore_alias =
android.keystore_password =

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer

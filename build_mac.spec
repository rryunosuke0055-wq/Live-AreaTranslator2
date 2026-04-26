# -*- mode: python ; coding: utf-8 -*-
"""
macOS用 PyInstaller ビルド設定
使い方: pyinstaller build_mac.spec
"""

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'Vision',
        'Quartz',
        'Foundation',
        'objc',
        'deep_translator',
        'deep_translator.google',
        'cv2',
        'numpy',
        'mss',
        'mss.darwin',
        'PySide6',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Live AreaTranslator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,   # GUIアプリなのでコンソール非表示
    target_arch=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Live AreaTranslator',
)

app = BUNDLE(
    coll,
    name='Live AreaTranslator.app',
    icon=None,   # アイコンがあれば 'icon.icns' を指定
    bundle_identifier='com.liveareatranslator.macos',
    info_plist={
        'CFBundleName': 'Live AreaTranslator',
        'CFBundleDisplayName': 'Live AreaTranslator',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSMicrophoneUsageDescription': 'Not used',
        'NSCameraUsageDescription': 'Not used',
    },
)

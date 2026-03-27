# -*- mode: python ; coding: utf-8 -*-
import sys

a = Analysis(
    ['ui/app.py'],
    pathex=['FileCompare'],
    binaries=[],
    datas=[],
    hiddenimports=['file_checker'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['unittest', 'test', 'email', 'http', 'xml', 'pydoc', 'doctest'],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data)

is_windowed = sys.platform in ('darwin', 'win32')
is_mac = sys.platform == 'darwin'

if is_mac:
    # macOS: onedir mode for .app bundle (onefile + .app is deprecated)
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='FileComparison Tool',
        debug=False,
        strip=False,
        upx=True,
        console=False,
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        name='FileComparison Tool',
    )
    app = BUNDLE(
        coll,
        name='FileComparison Tool.app',
        bundle_identifier='com.filecomparison.tool',
        info_plist={
            'NSHighResolutionCapable': True,
            'CFBundleShortVersionString': '1.0.0',
        },
    )
else:
    # Windows/Linux: single-file executable
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='FileComparison Tool',
        debug=False,
        strip=False,
        upx=True,
        console=not is_windowed,
    )

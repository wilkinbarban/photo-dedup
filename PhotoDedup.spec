# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

build_flavor = os.environ.get('PHOTO_DEDUP_BUILD_FLAVOR', 'full').strip().lower()
is_lite_build = build_flavor == 'lite'

hiddenimports = [
    'pillow_heif',
]

if not is_lite_build:
    hiddenimports += [
        'torch',
        'torchvision',
    ]

excludes = []
if is_lite_build:
    excludes += ['torch', 'torchvision']


a = Analysis(
    ['src/main/photo_dedup.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('assets',                    'assets'),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    exclude_binaries=False,
    name='PhotoDedup',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='assets/Icon.ico',
    onefile=True,
)

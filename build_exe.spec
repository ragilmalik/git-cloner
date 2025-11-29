# -*- mode: python ; coding: utf-8 -*-
"""
RagilmalikGitCloner - PyInstaller Spec File (PORTABLE VERSION WITH BUNDLED GIT)
Builds Windows executable with bundled MinGit for true portability

IMPORTANT: Run download_mingit.py first to get portable Git!

Usage:
    python download_mingit.py  # First time only
    pyinstaller build_exe.spec

Output:
    dist/RagilmalikGitCloner/
    ├── RagilmalikGitCloner.exe
    └── git_portable/  (MinGit ~50MB)
"""

import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None


a = Analysis(
    ['src/main_gui.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        # Application assets
        ('assets/icon.ico', 'assets'),
        ('assets/icon.png', 'assets'),

        # BUNDLED PORTABLE GIT (MinGit)
        # This makes the app truly portable - no Git installation needed!
        ('git_portable', 'git_portable'),
    ],
    hiddenimports=[
        # Local modules
        'url_parser',
        'git_operations',
        'report_generator',
        'error_handler',
        'git_config',

        # GUI framework
        'customtkinter',
        'darkdetect',
        'PIL',
        'PIL._tkinter_finder',

        # Git operations
        'git',
        'git.exc',
        'git.objects',
        'git.objects.submodule',
        'git.objects.submodule.base',
        'git.objects.submodule.root',

        # File parsing
        'pandas',
        'pandas._libs',
        'pandas._libs.tslibs',
        'openpyxl',
        'openpyxl.cell',
        'openpyxl.cell._writer',
        'xlrd',
        'numpy',  # Added to fix missing dependency

        # Standard library (explicit for safety)
        'csv',
        're',
        'threading',
        'datetime',
        'pathlib',
        'shutil',
        'urllib',
        'urllib.request',
        'zipfile',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary packages to reduce size
        'matplotlib',
        'scipy',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'tkinter.test',
        'unittest',
        'test',
        'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],  # Don't bundle everything in one file - we need folder structure for Git
    exclude_binaries=True,  # Keep binaries separate for folder distribution
    name='RagilmalikGitCloner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Enable UPX compression
    upx_exclude=[],
    console=False,  # No console window (GUI only)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',  # Application icon
)

# COLLECT: Create folder distribution (required for bundled Git)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RagilmalikGitCloner',
)

# Note: Output will be dist/RagilmalikGitCloner/ folder containing:
# - RagilmalikGitCloner.exe (~80MB)
# - git_portable/ folder (~50MB with MinGit)
# - Other necessary DLLs and files
#
# Total distribution size: ~130-150MB
# This entire folder is portable - copy to any Windows 10+ PC and run!
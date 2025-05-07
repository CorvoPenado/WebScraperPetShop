# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

# Collect all selenium and requests submodules
selenium_modules = collect_submodules('selenium')
requests_modules = collect_submodules('requests')

datas = [
    ('bot/*.pyd', 'bot'),  # Cython-compiled files
    ('bot/*.py', 'bot'),   # Python files
    ('app/static/*', 'app/static'),
]

# Add required data files
datas += collect_data_files('selenium')
datas += collect_data_files('beautifulsoup4')
datas += collect_data_files('openpyxl')
datas += collect_data_files('requests')

hiddenimports = [
    'selenium',
    'selenium.webdriver',
    'selenium.webdriver.common.keys',
    'selenium.webdriver.common.by',
    'selenium.webdriver.support.ui',
    'selenium.webdriver.support.expected_conditions',
    'selenium.webdriver.remote.webdriver',
    'selenium.webdriver.remote.remote_connection',
    'selenium.webdriver.chrome.service',
    'selenium.webdriver.chrome.webdriver',
    'requests',
    'urllib3',
    'chardet',
    'idna',
    'certifi',
    'bs4',
    'openpyxl',
    'concurrent.futures',
    'threading',
    'bot',
    'bot.booking',
    'bot.constants',
    'bot.filtration',
    'bot.peixe',
    'PIL',
    'tkinter',
    'queue',
    'threading',
    'concurrent.futures._base',
    'concurrent.futures.thread',
    'concurrent.futures.process'
] + selenium_modules + requests_modules

a = Analysis(
    ['launcher.py'],
    pathex=[os.path.abspath('.')],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DataMiner Pet BETA',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app/static/icon.ico'
)
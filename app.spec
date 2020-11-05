# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=['/home/abraham/Pupil detection/pupila'],
             binaries=[],
             datas=[('view.qml', '.'),
                    ('icons/icons8-checkmark.svg', 'icons'),
                    ('icons/icons8-delete.svg', 'icons'),
                    ('icons/icons8-next-page-64.png', 'icons'),
                    ('i18n/qml_en.qm', 'i18n'),
                    ('i18n/qml_es.qm', 'i18n'),
                    ('i18n/qml_fr.qm', 'i18n'),
                    ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['matplotlib'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='app')

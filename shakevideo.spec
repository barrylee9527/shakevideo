# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['shakevideo.py'],
             pathex=['D:\\pythonitems\\first\\PYQT5\\shakegirl'],
             binaries=[],
             datas=[('./static/index.html', './static'), ('./static/js/*', './static/js'), ('./static/css/*', './static/css'), ('./static/css/fonts/*', './static/css/fonts'), ('./1.mp4', './'), ('./1.png', './')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='shakevideo',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='favicon.ico')

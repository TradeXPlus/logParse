# -*- mode: python -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=['C:\\Python27\\application\\LogParse'],
             binaries=None,
             datas=None,
             hiddenimports=['win32timezone'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          Tree('./resource', prefix='resource'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='LogParse',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='icon.ico')

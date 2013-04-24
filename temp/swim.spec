# -*- mode: python -*-
a = Analysis(['../SWIM-Executables/Unix/pyinstaller-2.0/swim2/swim.py'],
             pathex=['/Users/morrishopkins/Dropbox/Spring2013/PLT/PLT-SLAMM/swim'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'swim'),
          debug=False,
          strip=None,
          upx=True,
          console=True )

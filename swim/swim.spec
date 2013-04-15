# -*- mode: python -*-
a = Analysis(['swim.py'],
             pathex=['/home/swim/Documents/PLT-SLAMM/swim'],
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

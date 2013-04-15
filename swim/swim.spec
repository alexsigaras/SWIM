# -*- mode: python -*-
a = Analysis(['../pyinstaller-2.0/swim2/swim.py'],
             pathex=['/Users/SeungWoo_0914/MyFuture/Columbia/PLT/PLT-SLAMM/PLT-SLAMM/swim'],
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

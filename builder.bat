set PY_VER=3.7

rem 32bit build
py -%PY_VER%-32 -m pip install PyInstaller netifaces
py -%PY_VER%-32 -OO -m PyInstaller hachi.py ^
  --distpath . ^
  --clean ^
  --onefile ^
  --add-data hachi.ico;. ^
  --add-data version;. ^
  --icon hachi.ico ^
  --name hachi_x86.exe

rem 64bit build
py -%PY_VER% -m pip install PyInstaller netifaces
py -%PY_VER% -OO -m PyInstaller hachi.py ^
  --distpath . ^
  --clean ^
  --onefile ^
  --noconsole ^
  --add-data hachi.ico;. ^
  --add-data version;. ^
  --icon hachi.ico ^
  --name hachi_x64.exe

rem crean up
rmdir /s /q build
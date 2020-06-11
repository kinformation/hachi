python -OO -m PyInstaller hachi.py ^
  --distpath . ^
  --clean ^
  --onefile ^
  --noconsole ^
  --add-data hachi.ico;. ^
  --add-data version;. ^
  --icon hachi.ico

rmdir /s /q build
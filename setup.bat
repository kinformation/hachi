python -OO -m PyInstaller hachi.py ^
  --distpath . ^
  --clean ^
  --onefile ^
  --noconsole ^
  --add-data hachi.ico;. ^
  --icon hachi.ico

rmdir /s /q build
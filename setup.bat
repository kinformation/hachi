python -OO -m PyInstaller hachi.py ^
  --distpath . ^
  --clean ^
  --onefile ^
  --noconsole ^
  --icon hachi.ico

rmdir /s /q build
rmdir /s /q dist
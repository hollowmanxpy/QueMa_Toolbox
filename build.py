import PyInstaller.__main__
import os

addition_data = f"assets{os.pathsep}assets"

PyInstaller.__main__.run([
    'src/main.py',
    '--onefile',
    '--windowed',
    '--name=QueMa_Office',
    f'--add-data={addition_data}',
    '--icon=assets/icons/app_icon.ico',
    '--clean',
    '-y',
])
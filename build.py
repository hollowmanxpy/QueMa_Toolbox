import PyInstaller.__main__
import os

# 定义资源路径，兼容 Windows 的分号
addition_data = f"assets{os.pathsep}assets"

PyInstaller.__main__.run([
    'src/main.py',
    '--onefile',
    '--windowed',
    '--name=雀码工具箱',
    f'--add-data={addition_data}',
    '--icon=assets/icons/app_icon.ico',
    '--clean',
    '-y',
])
import os
import sys
from pathlib import Path

def get_resource_path(relative_path: str) -> str:
    """
    获取静态资源的绝对路径。
    兼容开发环境与 PyInstaller 打包后的运行环境。
    """
    # noinspection SpellCheckingInspection
    if hasattr(sys, '_MEIPASS'):
        # noinspection PyProtectedMember
        return os.path.join(str(sys._MEIPASS), relative_path)

    # 使用 pathlib 优雅获取项目根目录
    base_path = str(Path(__file__).resolve().parent.parent.parent)
    return os.path.join(base_path, relative_path)
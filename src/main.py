import tkinter as tk
from src.gui.app import QueMaToolboxApp

def main():
    root = tk.Tk()
    # 明确声明变量，消除“未使用”警告
    _app = QueMaToolboxApp(root)
    root.mainloop()

# 【终极屏蔽】告诉 PyCharm：接下来的代码块里如果有你不认识的单词，统统闭嘴！
# noinspection SpellCheckingInspection
if __name__ == '__main__':
    # 【终极适配】解决高分屏模糊，消除动态 DLL 引用的类型警告
    try:
        from ctypes import windll
        # 安全获取 shcore 模块
        shcore = getattr(windll, 'shcore', None)
        if shcore is not None:
            # 安全获取并调用方法，彻底阻断 IDE 推断警告
            set_dpi_func = getattr(shcore, 'SetProcessDpiAwareness', None)
            if set_dpi_func:
                set_dpi_func(1)
    except (ImportError, AttributeError, OSError):
        pass

    main()
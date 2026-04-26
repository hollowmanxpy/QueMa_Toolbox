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
    # ==========================================
    # Windows 底层 API 调用区 (保证健壮性，绝不崩溃)
    # ==========================================
    try:
        from ctypes import windll

        # 1. 【修复任务栏图标】强制声明独立的 AppUserModelID
        # 这样 Windows 就不会把我们的程序和 Python 默认的羽毛图标混为一谈
        shell32 = getattr(windll, 'shell32', None)
        if shell32 is not None:
            set_appid_func = getattr(shell32, 'SetCurrentProcessExplicitAppUserModelID', None)
            if set_appid_func:
                my_app_id = 'quema.office.toolbox.v1.2.0'  # 任意独立的字符串即可
                set_appid_func(my_app_id)

        # 2. 【解决高分屏模糊】消除动态 DLL 引用的类型警告
        shcore = getattr(windll, 'shcore', None)
        if shcore is not None:
            set_dpi_func = getattr(shcore, 'SetProcessDpiAwareness', None)
            if set_dpi_func:
                set_dpi_func(1)

    except (ImportError, AttributeError, OSError):
        # 兼容非 Windows 系统或缺失相关 DLL 的残缺系统
        pass

    # 启动主程序
    main()
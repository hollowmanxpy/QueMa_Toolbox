import tkinter as tk


class BaseTab:
    """
    所有功能选项卡的抽象基类。
    规范了 UI 初始化接口和主题动态切换接口。
    """

    def __init__(self, parent, update_status_cb):
        self.parent = parent
        self.update_status = update_status_cb  # 用于向主窗口状态栏发送消息的回调函数
        self.dynamic_widgets = []  # 存储需要跟随主题变色的 UI 组件

        # 子类在继承时，必须在 __init__ 最后调用 self.setup_ui()

    def setup_ui(self):
        """具体 UI 的构建逻辑，由子类实现"""
        raise NotImplementedError("子类必须实现 setup_ui 方法！")

    def apply_theme(self, colors):
        """统一的主题切换接口，一键让选项卡内的组件变色"""
        for widget, attr, color_key in self.dynamic_widgets:
            try:
                widget.configure(**{attr: colors[color_key]})
            except Exception:
                pass
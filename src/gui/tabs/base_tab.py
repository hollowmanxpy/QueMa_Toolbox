import tkinter as tk


class BaseTab:
    """
    所有功能选项卡的抽象基类。
    规范了 UI 初始化接口、主题动态切换接口，以及完美的 UI 组件生成范式。
    """

    def __init__(self, parent, update_status_cb):
        self.parent = parent
        self.update_status = update_status_cb
        self.dynamic_widgets = []

        # [彻底消除灰边]：强制让 Notebook 分配给这个 Tab 的底层框架也变成纯白色！
        self.dynamic_widgets.append((self.parent, "bg", "panel"))

    def _create_perfect_entry(self, parent, str_var, width=10):
        """生成带 1px 边框的完美输入框"""
        bf = tk.Frame(parent, padx=1, pady=1)
        self.dynamic_widgets.append((bf, "bg", "border"))
        e = tk.Entry(bf, textvariable=str_var, font=("Microsoft YaHei", 10), relief="flat", bd=0, width=width)
        e.pack(fill="both", expand=True, ipady=4, ipadx=6)
        self.dynamic_widgets.append((e, "bg", "panel"))
        self.dynamic_widgets.append((e, "fg", "text"))
        e.config(insertbackground="#000000")  # 光标颜色会在主题切换时动态修正
        return bf, e

    def _create_perfect_button(self, parent, text, cmd):
        """生成带 1px 边框的完美按钮"""
        bf = tk.Frame(parent, padx=1, pady=1)
        self.dynamic_widgets.append((bf, "bg", "border"))
        btn = tk.Button(bf, text=text, font=("Microsoft YaHei", 9), relief="flat", cursor="hand2", command=cmd)
        btn.pack(fill="both", expand=True, ipadx=10, ipady=2)
        self.dynamic_widgets.append((btn, "bg", "bg"))
        self.dynamic_widgets.append((btn, "fg", "text"))
        return bf

    def _register_widgets_recursive(self, container):
        """递归洗地机制，消除所有未注册容器的灰底"""
        registered = [item[0] for item in self.dynamic_widgets]
        for child in container.winfo_children():
            if child not in registered:
                if isinstance(child, (tk.Label, tk.Frame, tk.Checkbutton)):
                    self.dynamic_widgets.append((child, "bg", "panel"))
                    if isinstance(child, tk.Checkbutton):
                        # noinspection SpellCheckingInspection
                        self.dynamic_widgets.append((child, "activebackground", "panel"))
                        # noinspection SpellCheckingInspection
                        self.dynamic_widgets.append((child, "selectcolor", "panel"))
                    if isinstance(child, tk.Label) and child.cget("fg") != "gray":
                        self.dynamic_widgets.append((child, "fg", "text"))
            if child.winfo_children():
                self._register_widgets_recursive(child)

    def setup_ui(self):
        raise NotImplementedError("子类必须实现 setup_ui 方法！")

    def apply_theme(self, colors):
        """统一主题切换，自动修正输入框光标颜色"""
        for widget, attr, color_key in self.dynamic_widgets:
            # 精确捕获 Tkinter 渲染错误与字典键值错误
            try:
                widget.configure(**{attr: colors[color_key]})
                if isinstance(widget, tk.Entry):
                    widget.config(insertbackground=colors["text"])
            except (tk.TclError, KeyError):
                pass
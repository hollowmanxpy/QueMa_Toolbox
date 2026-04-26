import tkinter as tk
import os
import webbrowser
from tkinter import ttk

from src.gui.tabs.tab_source import SourceExtractorTab
from src.gui.tabs.tab_tree import TreeGeneratorTab
from src.core.updater import check_for_updates
from src.utils.theme_utils import QUEMA_THEMES
from src.utils.path_utils import get_resource_path
from src.gui.tabs.tab_rename import BatchRenameTab


class QueMaToolboxApp:
    def __init__(self, root):
        self.root = root
        # 统一名称规范
        self.root.title("QueMa_Office - 办公代码工具")
        self.root.geometry("1000x750")
        self.root.resizable(False, False)

        icon_path = get_resource_path("assets/icons/app_icon.ico")
        if os.path.exists(icon_path):
            # 核心修复：必须加上 default=，强制将窗口和任务栏的默认图标全部替换
            self.root.iconbitmap(default=icon_path)

        self.status_var = tk.StringVar(value="准备就绪")
        self.theme_var = tk.StringVar(value="极简白")

        self.dynamic_widgets = []
        self.tabs = []

        self.progress = None
        self.notebook = None
        self.latest_url = ""

        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')

        self.setup_ui()
        self.apply_theme()

        # 启动更新检测
        self.root.after(2000, lambda: check_for_updates(self._on_update_checked))

    def _on_update_checked(self, has_update, version, url):
        if has_update:
            self.status_var.set(f"🚀 发现新版本 v{version}，点击右上角【💡问题与反馈】获取下载链接")
            self.latest_url = url

    def setup_ui(self):
        top_bar = tk.Frame(self.root)
        top_bar.pack(side="top", fill="x", padx=30, pady=15)
        self.dynamic_widgets.append((top_bar, "bg", "bg"))

        # 统一名称规范
        lbl_title = tk.Label(top_bar, text="QueMa_Office - 办公代码工具", font=("Microsoft YaHei", 15, "bold"))
        lbl_title.pack(side="left")
        self.dynamic_widgets.append((lbl_title, "bg", "bg"))
        self.dynamic_widgets.append((lbl_title, "fg", "text"))

        theme_frame = tk.Frame(top_bar)
        theme_frame.pack(side="right")
        self.dynamic_widgets.append((theme_frame, "bg", "bg"))

        btn_about = tk.Button(theme_frame, text="💡问题与反馈 / 更新", font=("Microsoft YaHei", 9), relief="flat",
                              cursor="hand2", command=self.show_about_dialog)
        btn_about.pack(side="left", padx=(0, 20))
        self.dynamic_widgets.append((btn_about, "bg", "bg"))
        self.dynamic_widgets.append((btn_about, "fg", "accent"))

        lbl_tm = tk.Label(theme_frame, text="界面主题:", font=("Microsoft YaHei", 10))
        lbl_tm.pack(side="left", padx=5)
        self.dynamic_widgets.append((lbl_tm, "bg", "bg"))
        self.dynamic_widgets.append((lbl_tm, "fg", "sub"))

        cb_theme = ttk.Combobox(theme_frame, textvariable=self.theme_var, values=list(QUEMA_THEMES.keys()),
                                state="readonly", width=8)
        cb_theme.pack(side="left")
        cb_theme.bind("<<ComboboxSelected>>", lambda e: self.apply_theme())

        status_bar = tk.Frame(self.root, padx=25, pady=10)
        status_bar.pack(side="bottom", fill="x")
        self.dynamic_widgets.append((status_bar, "bg", "panel"))

        lbl_status = tk.Label(status_bar, textvariable=self.status_var, font=("Microsoft YaHei", 9), width=50,
                              anchor="w")
        lbl_status.pack(side="left")
        self.dynamic_widgets.append((lbl_status, "bg", "panel"))
        self.dynamic_widgets.append((lbl_status, "fg", "text"))

        self.progress = ttk.Progressbar(status_bar, orient="horizontal", mode="determinate")
        self.progress.pack(side="right", fill="x", expand=True, padx=(10, 0))

        # Notebook 选项卡容器
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side="top", fill="both", expand=True, padx=25, pady=(0, 5))

        # 选项卡 1：源码提取
        tab1_frame = tk.Frame(self.notebook)
        self.notebook.add(tab1_frame, text=" 💻 源码提取 ")
        self.tabs.append(SourceExtractorTab(tab1_frame, self.update_status))

        # 选项卡 2：目录树生成
        tab2_frame = tk.Frame(self.notebook)
        self.notebook.add(tab2_frame, text=" 🌲 目录结构树 ")
        self.tabs.append(TreeGeneratorTab(tab2_frame, self.update_status))

        # 选项卡 3：批量重命名 (v2.0 医疗前置)
        tab3_frame = tk.Frame(self.notebook)
        self.notebook.add(tab3_frame, text=" 🏷️ 批量重命名 ")
        self.tabs.append(BatchRenameTab(tab3_frame, self.update_status))

    def show_about_dialog(self):
        colors = QUEMA_THEMES.get(self.theme_var.get(), QUEMA_THEMES["极简白"])

        dlg = tk.Toplevel(self.root)
        # 修改左上角标题，使其与按钮文案一致
        dlg.title("问题与反馈 / 更新")
        dlg.geometry("520x360")
        dlg.resizable(False, False)
        dlg.configure(bg=colors["panel"])
        dlg.transient(self.root)
        dlg.grab_set()

        dlg.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 520) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 360) // 2
        dlg.geometry(f"+{x}+{y}")

        # 统一名称规范
        lbl_title = tk.Label(dlg, text="QueMa_Office - 办公代码工具",
                             font=("Microsoft YaHei", 14, "bold"), bg=colors["panel"], fg=colors["accent"])
        lbl_title.pack(pady=(35, 5))

        lbl_version = tk.Label(dlg, text="当前版本: v1.1.0", font=("Consolas", 10), bg=colors["panel"], fg=colors["sub"])
        lbl_version.pack(pady=(0, 15))

        # 优化文案，更加精简；直接打包(pack)进顶级容器，彻底去除限制宽度的Frame，防止文字被边缘裁剪
        about_text = (
            "极简、高效的桌面端代码提取与结构梳理方案。\n"
            "底层解耦架构，轻松应对万级文件的大型工程。\n\n"
            "如有界面建议或新功能想法，欢迎随时反馈！"
        )
        tk.Label(dlg, text=about_text, font=("Microsoft YaHei", 10), bg=colors["panel"],
                 fg=colors["text"], justify="center").pack(pady=5)

        # 链接矩阵（增加适当间距保持呼吸感）
        link_frame = tk.Frame(dlg, bg=colors["panel"])
        link_frame.pack(pady=15)

        tk.Label(link_frame, text="开发者邮箱：", font=("Microsoft YaHei", 10), bg=colors["panel"], fg=colors["text"]).grid(row=0, column=0, sticky="e")
        tk.Label(link_frame, text="227598042@qq.com", font=("Consolas", 10), bg=colors["panel"], fg=colors["accent"]).grid(row=0, column=1, sticky="w")

        tk.Label(link_frame, text="开源主页：", font=("Microsoft YaHei", 10), bg=colors["panel"], fg=colors["text"]).grid(row=1, column=0, sticky="e", pady=8)
        link_gh = tk.Label(link_frame, text="GitHub/QueMa_Toolbox", font=("Consolas", 10, "underline"), bg=colors["panel"], fg=colors["accent"], cursor="hand2")
        link_gh.grid(row=1, column=1, sticky="w", pady=8)
        link_gh.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/hollowmanxpy/QueMa_Toolbox"))

        # 动态更新按钮
        if self.latest_url:
            def open_url():
                webbrowser.open(self.latest_url)
                dlg.destroy()

            tk.Button(dlg, text="✨ 发现新版本，点击前往下载 ✨", font=("Microsoft YaHei", 10, "bold"),
                      bg=colors["accent"], fg="white", relief="flat", cursor="hand2",
                      command=open_url).pack(pady=(5, 0), ipadx=20, ipady=6)

    def update_status(self, msg, percent=None):
        self.status_var.set(msg)
        if percent is not None:
            self.progress["value"] = percent
        self.root.update_idletasks()

    def apply_theme(self):
        theme_name = self.theme_var.get()
        colors = QUEMA_THEMES.get(theme_name, QUEMA_THEMES["极简白"])
        self.root.configure(bg=colors["bg"])

        style = ttk.Style()
        style.configure('TNotebook', background=colors["bg"], borderwidth=0)
        style.configure('TNotebook.Tab', background=colors["border"], foreground=colors["text"],
                        padding=[15, 4], font=("Microsoft YaHei", 10))
        style.map('TNotebook.Tab', background=[('selected', colors["panel"])],
                  foreground=[('selected', colors["accent"])])

        style.configure('TCombobox', fieldbackground=colors["panel"], background=colors["border"],
                        foreground=colors["text"], arrowcolor=colors["text"])
        style.map('TCombobox', fieldbackground=[('readonly', colors["panel"])],
                  selectbackground=[('readonly', colors["accent"])], selectforeground=[('readonly', '#FFFFFF')])

        style.configure('TSpinbox', fieldbackground=colors["panel"], background=colors["border"],
                        foreground=colors["text"], arrowcolor=colors["text"])
        style.map('TSpinbox', fieldbackground=[('readonly', colors["panel"])],
                  selectbackground=[('readonly', colors["accent"])], selectforeground=[('readonly', '#FFFFFF')])

        style.configure('Horizontal.TProgressbar', background=colors["accent"], troughcolor=colors["border"],
                        borderwidth=0, thickness=12)

        for widget, attr, color_key in self.dynamic_widgets:
            try:
                widget.configure(**{attr: colors[color_key]})
            except (tk.TclError, KeyError):
                continue

        # 批量通知所有选项卡更新主题
        for tab in self.tabs:
            tab.apply_theme(colors)
import tkinter as tk
import os  # 👈 修复了未解析的引用
from tkinter import ttk
from src.gui.tabs.tab_source import SourceExtractorTab
from src.utils.theme_utils import QUEMA_THEMES
from src.utils.path_utils import get_resource_path

class QueMaToolboxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("雀码 (QueMa) - 个人开发工具箱")
        # 1000x750 黄金比例宽屏
        self.root.geometry("1000x750")
        self.root.resizable(False, False)

        icon_path = get_resource_path("assets/icons/app_icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

        self.status_var = tk.StringVar(value="准备就绪")
        self.theme_var = tk.StringVar(value="极简白")
        self.progress = None
        self.notebook = None
        self.tab_source_frame = None
        self.tab_source = None
        self.dynamic_widgets = []

        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')

        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        top_bar = tk.Frame(self.root)
        top_bar.pack(side="top", fill="x", padx=30, pady=15)
        self.dynamic_widgets.append((top_bar, "bg", "bg"))

        lbl_title = tk.Label(top_bar, text="雀码 - 多功能开发工具箱", font=("Microsoft YaHei", 15, "bold"))
        lbl_title.pack(side="left")
        self.dynamic_widgets.append((lbl_title, "bg", "bg"))
        self.dynamic_widgets.append((lbl_title, "fg", "text"))

        theme_frame = tk.Frame(top_bar)
        theme_frame.pack(side="right")
        self.dynamic_widgets.append((theme_frame, "bg", "bg"))

        btn_about = tk.Button(theme_frame, text="💡问题与反馈", font=("Microsoft YaHei", 9), relief="flat",
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

        lbl_status = tk.Label(status_bar, textvariable=self.status_var, font=("Microsoft YaHei", 9), width=35,
                              anchor="w")
        lbl_status.pack(side="left")
        self.dynamic_widgets.append((lbl_status, "bg", "panel"))
        self.dynamic_widgets.append((lbl_status, "fg", "text"))

        self.progress = ttk.Progressbar(status_bar, orient="horizontal", mode="determinate")
        self.progress.pack(side="right", fill="x", expand=True, padx=(10, 0))

        # noqa: SpellCheckingInspection
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side="top", fill="both", expand=True, padx=25, pady=(0, 5))

        self.tab_source_frame = tk.Frame(self.notebook)
        self.notebook.add(self.tab_source_frame, text=" 💻 代码整理与提取 ")
        self.tab_source = SourceExtractorTab(self.tab_source_frame, self.update_status)

    def show_about_dialog(self):
        colors = QUEMA_THEMES.get(self.theme_var.get(), QUEMA_THEMES["极简白"])

        dlg = tk.Toplevel(self.root)
        dlg.title("问题与反馈")
        dlg.geometry("480x280")
        dlg.resizable(False, False)
        dlg.configure(bg=colors["panel"])
        dlg.transient(self.root)
        dlg.grab_set()

        dlg.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 480) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 280) // 2
        dlg.geometry(f"+{x}+{y}")

        lbl_title = tk.Label(dlg, text="【 雀码 (QueMa) - 个人开发工具箱 】",
                             font=("Microsoft YaHei", 12, "bold"), bg=colors["panel"], fg=colors["accent"])
        lbl_title.pack(pady=(35, 10))

        about_text = (
            "如果您在使用中遇到了 Bug，或者有界面建议、新功能想法，\n"
            "欢迎随时与我们取得联系。您的建议是雀码进步的唯一动力。\n\n"
            "祝您代码无 Bug，一路绿灯！"
        )
        tk.Label(dlg, text=about_text, font=("Microsoft YaHei", 10), bg=colors["panel"],
                 fg=colors["text"], justify="center").pack(pady=5)

        btn_ok = tk.Button(dlg, text="确 定", font=("Microsoft YaHei", 10, "bold"),
                           fg="white", bg=colors["accent"], width=12, cursor="hand2", relief="flat",
                           command=dlg.destroy)
        btn_ok.pack(pady=25)

    def update_status(self, msg, percent=None):
        self.status_var.set(msg)
        if percent is not None:
            self.progress["value"] = percent
        self.root.update_idletasks()

    def apply_theme(self):
        theme_name = self.theme_var.get()
        colors = QUEMA_THEMES.get(theme_name, QUEMA_THEMES["极简白"])

        self.root.configure(bg=colors["bg"])

        # noqa: SpellCheckingInspection
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

        if hasattr(self, 'tab_source') and self.tab_source:
            self.tab_source.apply_theme(colors)
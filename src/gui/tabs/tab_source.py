import os
import re
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Tuple, Dict, Any, Literal

from src.gui.tabs.base_tab import BaseTab
from src.core.reader import scan_and_read
from src.core.writer import save_output


class SourceExtractorTab(BaseTab):
    def __init__(self, parent, update_status_cb):
        super().__init__(parent, update_status_cb)

        self.btn_run = None
        self.btn_exit = None
        self.chk_hf = None
        self.preview = None
        self.current_theme_colors = None

        self.dir_var = tk.StringVar()
        self.out_dir_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Desktop"))
        self.ext_var = tk.StringVar(value="py, java, js, html, css, cpp, h, vue")
        self.filename_var = tk.StringVar(value="QueMa_Export")
        self.format_var = tk.StringVar(value="Word")
        self.enable_hf_var = tk.BooleanVar(value=True)

        self.t_font = tk.StringVar(value="黑体")
        self.t_size = tk.StringVar(value="14")
        self.t_color = tk.StringVar(value="科技蓝")

        self.b_font = tk.StringVar(value="Consolas")
        self.b_size = tk.StringVar(value="10")
        self.b_color = tk.StringVar(value="警示红")

        self.color_map: Dict[str, Dict[str, Any]] = {
            "标准黑": {"rgb": (0, 0, 0), "hex": "#000000"},
            "科技蓝": {"rgb": (31, 73, 125), "hex": "#1F497D"},
            "警示红": {"rgb": (192, 0, 0), "hex": "#C00000"},
            "护眼绿": {"rgb": (56, 118, 29), "hex": "#38761D"}
        }

        self.word_only_widgets = []
        self.style_labels = []

        self.setup_ui()

        self.format_var.trace_add("write", lambda *_: self.on_format_change())
        for v in (self.t_font, self.t_size, self.t_color, self.b_font, self.b_size, self.b_color):
            v.trace_add("write", lambda *_: self.update_preview())

        self.update_preview()

    def apply_theme(self, colors):
        super().apply_theme(colors)
        self.current_theme_colors = colors
        self.on_format_change()

    def _create_perfect_entry(self, parent, str_var, width=10):
        # 外层 Frame：负责充当 1px 的框线，明确绑定为 border 颜色
        bf = tk.Frame(parent, padx=1, pady=1)
        self.dynamic_widgets.append((bf, "bg", "border"))

        # 内层 Entry：绑定为 panel 颜色
        e = tk.Entry(bf, textvariable=str_var, font=("Microsoft YaHei", 10), relief="flat", bd=0, width=width)
        e.pack(fill="both", expand=True, ipady=4, ipadx=6)
        self.dynamic_widgets.append((e, "bg", "panel"))
        self.dynamic_widgets.append((e, "fg", "text"))

        # noinspection PyTypeChecker
        e.config(insertbackground=str(self.color_map["标准黑"]["hex"]))
        return bf, e

    def _create_perfect_button(self, parent, text, cmd):
        # 同样，明确绑定为 border 颜色
        bf = tk.Frame(parent, padx=1, pady=1)
        self.dynamic_widgets.append((bf, "bg", "border"))
        btn = tk.Button(bf, text=text, font=("Microsoft YaHei", 9), relief="flat", cursor="hand2", command=cmd)
        btn.pack(fill="both", expand=True, ipadx=10, ipady=2)
        self.dynamic_widgets.append((btn, "bg", "bg"))
        self.dynamic_widgets.append((btn, "fg", "text"))
        return bf

    @staticmethod
    def _select_dir(var):
        p = filedialog.askdirectory()
        if p:
            var.set(p)

    def _register_widgets_recursive(self, container):
        """【终极修复】提取已注册组件列表。只给漏网的组件刷色，绝不破坏原有的边框色！"""
        registered = [item[0] for item in self.dynamic_widgets]

        for child in container.winfo_children():
            # 只有没有被手动注册过的组件，才会被系统强制刷成 panel 白底
            if child not in registered:
                # 把 tk.Frame 加回来！这样大面积的灰底容器就能变白了！
                if isinstance(child, (tk.Label, tk.Frame, tk.Checkbutton)):
                    self.dynamic_widgets.append((child, "bg", "panel"))

                    if isinstance(child, tk.Checkbutton):
                        # noinspection SpellCheckingInspection
                        self.dynamic_widgets.append((child, "activebackground", "panel"))
                        # noinspection SpellCheckingInspection
                        self.dynamic_widgets.append((child, "selectcolor", "panel"))

                    if isinstance(child, tk.Label) and child.cget("fg") != "gray":
                        self.dynamic_widgets.append((child, "fg", "text"))

            # 继续向下挖掘
            if child.winfo_children():
                self._register_widgets_recursive(child)

    def setup_ui(self):
        main_f = tk.Frame(self.parent)
        main_f.pack(fill="both", expand=True)
        self.dynamic_widgets.append((main_f, "bg", "panel"))

        inner_f = tk.Frame(main_f)
        inner_f.pack(fill="both", expand=True, padx=45, pady=(20, 15))
        self.dynamic_widgets.append((inner_f, "bg", "panel"))

        bot_area = tk.Frame(inner_f)
        bot_area.pack(side="bottom", fill="x", pady=(10, 0))

        lbl_hint = tk.Label(bot_area, text="💡 提示：建议单次提取不超过500份文件以防卡顿。正式用途请更新摘要。",
                            font=("Microsoft YaHei", 9))
        lbl_hint.pack(side="top", fill="x", pady=(0, 15))

        btn_c = tk.Frame(bot_area)
        btn_c.pack(side="top")

        self.btn_run = tk.Button(btn_c, text="提 取", font=("Microsoft YaHei", 12, "bold"), fg="white", cursor="hand2",
                                 relief="flat", command=self.run_extraction)
        self.btn_run.pack(side="left", ipadx=40, ipady=5, padx=25)
        self.dynamic_widgets.append((self.btn_run, "bg", "accent"))

        self.btn_exit = tk.Button(btn_c, text="退 出", font=("Microsoft YaHei", 12, "bold"), fg="white", bg="#F56C6C",
                                  cursor="hand2", relief="flat", command=self.parent.winfo_toplevel().destroy)
        self.btn_exit.pack(side="left", ipadx=40, ipady=5, padx=25)

        top_area = tk.Frame(inner_f)
        top_area.pack(side="top", fill="x")

        lbl_g1 = tk.Label(top_area, text="一、 目录选择与导出设置", font=("Microsoft YaHei", 11, "bold"))
        lbl_g1.pack(side="top", anchor="w", padx=5, pady=(0, 5))

        for label_text, str_var, show_btn in [
            ("代码文件夹:", self.dir_var, True),
            ("保存位置:", self.out_dir_var, True),
            ("文件后缀:", self.ext_var, False)
        ]:
            row = tk.Frame(top_area)
            row.pack(fill="x", padx=5, pady=3)
            tk.Label(row, text=label_text, width=10, anchor="e").pack(side="left", padx=(0, 5))
            bf, _ = self._create_perfect_entry(row, str_var)
            bf.pack(side="left", fill="x", expand=True, padx=5)
            if show_btn:
                self._create_perfect_button(row, "浏览...", lambda v=str_var: self._select_dir(v)).pack(side="left",
                                                                                                        padx=(5, 0))

        row4 = tk.Frame(top_area)
        row4.pack(fill="x", padx=5, pady=(2, 10))
        tk.Label(row4, text="文件名:", width=10, anchor="e").pack(side="left", padx=(0, 5))
        bfn, _ = self._create_perfect_entry(row4, self.filename_var, width=18)
        bfn.pack(side="left", padx=5)
        tk.Label(row4, text="导出格式:").pack(side="left", padx=(25, 5))
        cb_fmt = ttk.Combobox(row4, textvariable=self.format_var, values=["Word", "TXT"], state="readonly", width=8)
        cb_fmt.pack(side="left", ipady=1)

        mid_area = tk.Frame(inner_f)
        mid_area.pack(side="top", fill="both", expand=True, pady=(10, 0))
        mid_area.columnconfigure(0, weight=18, minsize=580, uniform="gold")
        mid_area.columnconfigure(1, weight=10, uniform="gold")
        mid_area.rowconfigure(0, weight=1)

        left_p = tk.Frame(mid_area)
        left_p.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        lbl_g2 = tk.Label(left_p, text="二、 排版样式", font=("Microsoft YaHei", 11, "bold"))
        lbl_g2.pack(side="top", anchor="w", padx=5, pady=(0, 10))

        style_f = tk.Frame(left_p)
        style_f.pack(side="top", fill="x", padx=5)
        style_f.columnconfigure((1, 3, 5), weight=1)

        l_tf = tk.Label(style_f, text="标题字体:")
        l_tf.grid(row=0, column=0, padx=2, pady=6, sticky="e")
        cb_tf = ttk.Combobox(style_f, textvariable=self.t_font, values=["黑体", "微软雅黑", "宋体"], state="readonly",
                             width=12)
        cb_tf.grid(row=0, column=1, sticky="w")

        l_ts = tk.Label(style_f, text="字号:")
        l_ts.grid(row=0, column=2, padx=(10, 2), sticky="e")
        sp_ts = ttk.Spinbox(style_f, from_=10, to=30, textvariable=self.t_size, width=5)
        sp_ts.grid(row=0, column=3, sticky="w")

        l_tc = tk.Label(style_f, text="颜色:")
        l_tc.grid(row=0, column=4, padx=(10, 2), sticky="e")
        cb_tc = ttk.Combobox(style_f, textvariable=self.t_color, values=list(self.color_map.keys()), state="readonly",
                             width=10)
        cb_tc.grid(row=0, column=5, sticky="w")

        l_bf = tk.Label(style_f, text="代码字体:")
        l_bf.grid(row=1, column=0, padx=2, pady=6, sticky="e")
        cb_bf = ttk.Combobox(style_f, textvariable=self.b_font, values=["Consolas", "Courier New", "宋体"],
                             state="readonly", width=12)
        cb_bf.grid(row=1, column=1, sticky="w")

        l_bs = tk.Label(style_f, text="字号:")
        l_bs.grid(row=1, column=2, padx=(10, 2), sticky="e")
        sp_bs = ttk.Spinbox(style_f, from_=8, to=24, textvariable=self.b_size, width=5)
        sp_bs.grid(row=1, column=3, sticky="w")

        l_bc = tk.Label(style_f, text="颜色:")
        l_bc.grid(row=1, column=4, padx=(10, 2), sticky="e")
        cb_bc = ttk.Combobox(style_f, textvariable=self.b_color, values=list(self.color_map.keys()), state="readonly",
                             width=10)
        cb_bc.grid(row=1, column=5, sticky="w")

        self.chk_hf = tk.Checkbutton(left_p, text="添加 Word 页眉(文件名)与页脚(第X页 / 共X页)",
                                     variable=self.enable_hf_var)
        self.chk_hf.pack(side="top", anchor="w", padx=5, pady=(15, 0))

        right_p = tk.Frame(mid_area)
        right_p.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        pv_lbl = tk.Label(right_p, text="排版效果预览:", fg="gray", font=("Microsoft YaHei", 9))
        pv_lbl.pack(side="top", anchor="w", pady=(0, 5))

        txt_b = tk.Frame(right_p, padx=1, pady=1)
        txt_b.pack(side="top", fill="both", expand=True)
        self.dynamic_widgets.append((txt_b, "bg", "border"))

        txt_bg = tk.Frame(txt_b)
        txt_bg.pack(fill="both", expand=True)
        self.dynamic_widgets.append((txt_bg, "bg", "panel"))

        self.preview = tk.Text(txt_bg, width=1, height=1, wrap="word", relief="flat", bd=0, padx=15, pady=10)
        self.preview.pack(fill="both", expand=True)

        self.word_only_widgets = [cb_tf, sp_ts, cb_tc, cb_bf, sp_bs, cb_bc, self.chk_hf]
        self.style_labels = [l_tf, l_ts, l_tc, l_bf, l_bs, l_bc, self.chk_hf]

        # 启动终极递归洗地！
        self._register_widgets_recursive(inner_f)

    def update_preview(self):
        if self.format_var.get() == "TXT":
            return
        try:
            t_f, t_s = self.t_font.get(), int(self.t_size.get())
            b_f, b_s = self.b_font.get(), int(self.b_size.get())
            t_hex = str(self.color_map.get(self.t_color.get(), {}).get("hex", "#000000"))
            b_hex = str(self.color_map.get(self.b_color.get(), {}).get("hex", "#000000"))

            if self.current_theme_colors and self.current_theme_colors.get("bg") in ["#1E1E1E", "#120324"]:
                if t_hex == "#000000":
                    t_hex = self.current_theme_colors["text"]
                if b_hex == "#000000":
                    b_hex = self.current_theme_colors["text"]

            self.preview.config(state="normal")
            self.preview.delete("1.0", "end")
            self.preview.insert("end", "文件: main.py\n", "title")
            self.preview.tag_configure("title", font=(t_f, t_s, "bold"), foreground=t_hex)
            self.preview.insert("end", "print('排版预览已同步')", "body")
            self.preview.tag_configure("body", font=(b_f, b_s), foreground=b_hex)
            self.preview.config(state="disabled")
        except (ValueError, tk.TclError):
            pass

    def on_format_change(self):
        fmt = self.format_var.get()
        is_txt = (fmt == "TXT")

        state_val: Literal["normal", "disabled", "readonly"] = "disabled" if is_txt else "readonly"
        chk_state: Literal["normal", "disabled"] = "disabled" if is_txt else "normal"

        for w in self.word_only_widgets:
            try:
                if isinstance(w, tk.Checkbutton):
                    w.config(state=chk_state)
                else:
                    w.config(state=state_val)
            except (tk.TclError, AttributeError):
                pass

        txt_c = self.current_theme_colors["text"] if self.current_theme_colors else "#000000"
        dim_c = "#909399" if getattr(self, 'current_theme_colors', {}).get('bg') == "#F5F7FA" else "#5C5C5C"

        for lbl in self.style_labels:
            try:
                lbl.config(fg=dim_c if is_txt else txt_c)
            except (tk.TclError, AttributeError):
                pass

        self.preview.config(state="normal")
        self.preview.delete("1.0", "end")
        if is_txt:
            self.preview.config(bg=dim_c, fg="#FFFFFF")
            self.preview.insert("end", "【纯文本模式】\n\n剔除排版格式，提取代码序列。\n适合归档或分析。")
        else:
            if self.current_theme_colors:
                self.preview.config(bg=self.current_theme_colors["panel"], fg=self.current_theme_colors["text"])
            self.update_preview()
        self.preview.config(state="disabled")

    def run_extraction(self):
        in_d, out_d, fn = self.dir_var.get().strip(), self.out_dir_var.get().strip(), self.filename_var.get().strip()
        if not os.path.isdir(in_d) or not fn:
            messagebox.showwarning("提示", "请选择文件夹并输入文件名。")
            return

        fmt = self.format_var.get()
        ext = 'docx' if fmt == 'Word' else 'txt'
        if os.path.exists(os.path.join(out_d, f"{fn}.{ext}")):
            if not messagebox.askyesno("覆盖确认", "文件已存在，是否覆盖？"):
                return

        raw_ext = self.ext_var.get().strip()
        exs = tuple(e.strip().lower() if e.strip().startswith('.') else f".{e.strip().lower()}"
                    for e in re.split(r'[,，]', raw_ext) if e.strip()) if raw_ext else None

        self.btn_run.config(state="disabled", text="正在提取...")
        threading.Thread(target=self._worker, args=(in_d, out_d, fn, exs, fmt), daemon=True).start()

    def _worker(self, in_d, out_d, fn, exs, fmt):
        try:
            data = scan_and_read(in_d, allowed_extensions=exs)
            if not data:
                self.parent.after(0, lambda: messagebox.showwarning("提示", "未找到文件。"))
                return

            t_map = self.color_map.get(self.t_color.get(), self.color_map["标准黑"])
            b_map = self.color_map.get(self.b_color.get(), self.color_map["标准黑"])
            t_rgb: Tuple[int, int, int] = t_map["rgb"]
            b_rgb: Tuple[int, int, int] = b_map["rgb"]

            p_cb = lambda p: self.parent.after(0, lambda: self.update_status("正在保存...", p))

            final_p = save_output(
                data, out_d, fn, fmt,
                self.t_font.get(), int(self.t_size.get()),
                self.b_font.get(), int(self.b_size.get()),
                t_rgb, b_rgb, self.enable_hf_var.get(), p_cb
            )

            self.parent.after(0, lambda: messagebox.showinfo("成功", f"文件已保存至：\n{final_p}"))
        except (OSError, ValueError, tk.TclError) as e:
            self.parent.after(0, lambda: messagebox.showerror("错误", f"处理失败: {e}"))
        finally:
            self.parent.after(0, lambda: [self.btn_run.config(state="normal", text="提 取"),
                                          self.update_status("准备就绪", 0)])
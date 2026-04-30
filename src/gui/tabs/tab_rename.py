import os
import re
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Dict

from src.gui.tabs.base_tab import BaseTab


class BatchRenameTab(BaseTab):
    def __init__(self, parent, update_status_cb):
        super().__init__(parent, update_status_cb)

        self.dir_var = tk.StringVar()
        self.rule_type_var = tk.StringVar(value="添加前缀")
        self.input1_var = tk.StringVar()
        self.input2_var = tk.StringVar()

        # 新增：数量限制与序列号高级配置
        self.limit_var = tk.StringVar(value="0")
        self.seq_enable_var = tk.BooleanVar(value=False)
        self.seq_mode_var = tk.StringVar(value="递增")
        self.seq_start_var = tk.StringVar(value="001")  # 默认给个高级用法的示范
        self.seq_step_var = tk.StringVar(value="1")  # 新增步长变量

        self.btn_execute = None
        self.tree = None

        # 动态组件引用
        self.lbl_input1 = None
        self.lbl_input2 = None
        self.frame_input2 = None

        self.frame_dyn = None
        self.lbl_regex_hint = None
        self.frame_seq = None

        self._preview_data: List[Dict[str, str]] = []
        self._preview_timer = None
        self._max_preview_limit = 300

        self.setup_ui()

        # 监听所有变量，无感防抖刷新
        for v in (self.dir_var, self.rule_type_var, self.input1_var, self.input2_var,
                  self.limit_var, self.seq_enable_var, self.seq_mode_var, self.seq_start_var, self.seq_step_var):
            v.trace_add("write", lambda *_: self._schedule_preview())

    @staticmethod
    def _select_dir(var: tk.StringVar) -> None:
        p = filedialog.askdirectory()
        if p:
            var.set(p)

    def setup_ui(self):
        main_f = tk.Frame(self.parent)
        main_f.pack(fill="both", expand=True)
        self.dynamic_widgets.append((main_f, "bg", "panel"))

        # --- 底部：执行区 ---
        bot_area = tk.Frame(main_f)
        bot_area.pack(side="bottom", fill="x", pady=(10, 20))

        btn_container = tk.Frame(bot_area)
        btn_container.pack(anchor="center")
        self.dynamic_widgets.append((btn_container, "bg", "panel"))

        self.btn_execute = tk.Button(btn_container, text="🚀 确认执行重命名", font=("Microsoft YaHei", 12, "bold"),
                                     fg="white", disabledforeground="white", cursor="hand2", relief="flat",
                                     command=self.run_execute,
                                     state="disabled")
        self.btn_execute.pack(ipadx=60, ipady=6)
        self.dynamic_widgets.append((self.btn_execute, "bg", "accent"))

        # --- 顶部：规则配置区 ---
        top_area = tk.Frame(main_f)
        top_area.pack(side="top", fill="x", padx=45, pady=(20, 0))

        # [优化] 将处理限制参数，优雅地融合在标题行的右侧
        h1_f = tk.Frame(top_area)
        h1_f.pack(fill="x", pady=(0, 5))
        self.dynamic_widgets.append((h1_f, "bg", "panel"))

        tk.Label(h1_f, text="一、 目标文件夹与范围", font=("Microsoft YaHei", 11, "bold")).pack(side="left")

        tk.Label(h1_f, text="处理限制(0为全部):").pack(side="left", padx=(30, 5))
        e_limit_f, _ = self._create_perfect_entry(h1_f, self.limit_var, width=6)
        e_limit_f.pack(side="left")

        # [优化] 释放全部横向空间给目录输入框
        r1 = tk.Frame(top_area)
        r1.pack(fill="x", pady=5)
        e1_f, _ = self._create_perfect_entry(r1, self.dir_var)
        e1_f.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self._create_perfect_button(r1, "浏览目录...", lambda: self._select_dir(self.dir_var)).pack(side="left")

        tk.Label(top_area, text="二、 重命名规则", font=("Microsoft YaHei", 11, "bold")).pack(anchor="w", pady=(15, 5))

        r2 = tk.Frame(top_area)
        r2.pack(fill="x", pady=5)

        cb_rule = ttk.Combobox(r2, textvariable=self.rule_type_var, state="readonly", width=12,
                               values=["文本替换", "正则替换", "添加前缀", "添加后缀", "修改扩展名"])
        cb_rule.pack(side="left", ipady=2)
        cb_rule.bind("<<ComboboxSelected>>", self._on_rule_change)

        self.lbl_input1 = tk.Label(r2, text="查找内容:")
        self.lbl_input1.pack(side="left", padx=(15, 5))
        e_s_f, _ = self._create_perfect_entry(r2, self.input1_var)
        e_s_f.pack(side="left", fill="x", expand=True)

        self.frame_input2 = tk.Frame(r2)
        self.frame_input2.pack(side="left", fill="x", expand=True, padx=(15, 0))

        self.lbl_input2 = tk.Label(self.frame_input2, text="替换为:")
        self.lbl_input2.pack(side="left", padx=(0, 5))
        e_r_f, _ = self._create_perfect_entry(self.frame_input2, self.input2_var)
        e_r_f.pack(side="left", fill="x", expand=True)

        # --- 动态提示与序列面板区 ---
        self.frame_dyn = tk.Frame(top_area)
        self.frame_dyn.pack(fill="x", pady=(2, 0))
        self.dynamic_widgets.append((self.frame_dyn, "bg", "panel"))

        # 1. 正则提示标签
        self.lbl_regex_hint = tk.Label(self.frame_dyn,
                                       text="💡 正则白话指南：用 (.*) 抓取原名，用 \\1 填入新名。例：提取日期 '图_2026.png'，查 '图_(\\d+)\\.png'，替换 '\\1.png'",
                                       font=("Microsoft YaHei", 9))
        self.dynamic_widgets.append((self.lbl_regex_hint, "fg", "sub"))

        # 2. 序列配置面板 (全新高级配置)
        self.frame_seq = tk.Frame(self.frame_dyn)
        self.dynamic_widgets.append((self.frame_seq, "bg", "panel"))

        chk_seq = tk.Checkbutton(self.frame_seq, text="附加数字序列", variable=self.seq_enable_var)
        chk_seq.pack(side="left", padx=(0, 15))

        cb_mode = ttk.Combobox(self.frame_seq, textvariable=self.seq_mode_var, state="readonly", width=6,
                               values=["递增", "递减"])
        cb_mode.pack(side="left", padx=(0, 15))

        tk.Label(self.frame_seq, text="起始值(如001):").pack(side="left")
        e_start_f, _ = self._create_perfect_entry(self.frame_seq, self.seq_start_var, width=5)
        e_start_f.pack(side="left", padx=(5, 15))

        tk.Label(self.frame_seq, text="步长:").pack(side="left")
        e_step_f, _ = self._create_perfect_entry(self.frame_seq, self.seq_step_var, width=4)
        e_step_f.pack(side="left", padx=(5, 0))

        # --- 中部：数据表格预览区 ---
        mid_area = tk.Frame(main_f)
        mid_area.pack(side="top", fill="both", expand=True, padx=45, pady=(15, 10))

        header_f = tk.Frame(mid_area)
        header_f.pack(fill="x", pady=(0, 5))
        self.dynamic_widgets.append((header_f, "bg", "panel"))
        tk.Label(header_f, text="三、 实时预览 (按名称顺序排队处理):", font=("Microsoft YaHei", 11, "bold")).pack(
            side="left")

        tree_f = tk.Frame(mid_area, padx=1, pady=1)
        tree_f.pack(fill="both", expand=True)
        self.dynamic_widgets.append((tree_f, "bg", "border"))

        cols = ("status", "old", "new")
        self.tree = ttk.Treeview(tree_f, columns=cols, show="headings", selectmode="none")
        self.tree.heading("status", text="状态")
        self.tree.heading("old", text="原文件名")
        self.tree.heading("new", text="新文件名")

        self.tree.column("status", width=80, anchor="center")
        self.tree.column("old", width=300, anchor="w")
        self.tree.column("new", width=300, anchor="w")

        scroll_y = ttk.Scrollbar(tree_f, orient="vertical", command=self.tree.yview)
        scroll_y.pack(side="right", fill="y")
        self.tree.config(yscrollcommand=scroll_y.set)
        self.tree.pack(side="left", fill="both", expand=True)

        self._register_widgets_recursive(main_f)
        self._on_rule_change()

    def apply_theme(self, colors: dict) -> None:
        super().apply_theme(colors)
        try:
            style = ttk.Style()
            style.configure("Treeview", background=colors["panel"], foreground=colors["text"],
                            fieldbackground=colors["panel"], borderwidth=0, rowheight=25)
            style.configure("Treeview.Heading", background=colors["bg"], foreground=colors["text"],
                            font=("Microsoft YaHei", 9, "bold"))
            style.map("Treeview", background=[("selected", colors["accent"])])
        except tk.TclError:
            pass

    def _on_rule_change(self, *_) -> None:
        """根据当前规则，动态调整输入框与辅助面板的显示"""
        rule = self.rule_type_var.get()

        self.lbl_regex_hint.pack_forget()
        self.frame_seq.pack_forget()

        if rule in ["文本替换", "正则替换"]:
            self.lbl_input1.config(text="查找内容:" if rule == "文本替换" else "正则匹配:")
            self.frame_input2.pack(side="left", fill="x", expand=True, padx=(15, 0))
            if rule == "正则替换":
                self.lbl_regex_hint.pack(anchor="w", padx=15, pady=5)
        else:
            self.frame_input2.pack_forget()
            if rule == "添加前缀":
                self.lbl_input1.config(text="输入前缀:")
                self.frame_seq.pack(anchor="w", padx=15, pady=5)
            elif rule == "添加后缀":
                self.lbl_input1.config(text="输入后缀:")
                self.frame_seq.pack(anchor="w", padx=15, pady=5)
            elif rule == "修改扩展名":
                self.lbl_input1.config(text="新扩展名 (如 .txt):")

        self._schedule_preview()

    def _schedule_preview(self) -> None:
        if self._preview_timer is not None:
            self.parent.after_cancel(self._preview_timer)

        for item in self.tree.get_children():
            self.tree.delete(item)
        self.btn_execute.config(state="disabled", text="等候输入...")

        self._preview_timer = self.parent.after(500, self._start_preview_thread)

    def _start_preview_thread(self) -> None:
        in_d = self.dir_var.get().strip()
        if not os.path.isdir(in_d):
            self.update_status("准备就绪", 0)
            return

        self.update_status("正在生成预览...", 30)
        self.btn_execute.config(text="正在分析变更...")
        threading.Thread(target=self._preview_worker, args=(in_d, self.rule_type_var.get(),
                                                            self.input1_var.get(), self.input2_var.get()),
                         daemon=True).start()

    def _preview_worker(self, in_d: str, rule: str, val1: str, val2: str) -> None:
        self._preview_data.clear()
        try:
            # 1. 健壮的参数解析机制
            limit_val = int(self.limit_var.get()) if self.limit_var.get().isdigit() else 0
            enable_seq = self.seq_enable_var.get()
            is_increment = self.seq_mode_var.get() == "递增"

            start_str = self.seq_start_var.get().strip()
            step_str = self.seq_step_var.get().strip()

            # 智能补零探测：如果输入 '001'，长度为3，那么 2 会被补零成 '002'
            pad_len = len(start_str) if start_str.startswith('0') else 0

            # 极强防呆：用户随便输入字母也能优雅降级为 1
            try:
                current_seq = int(start_str) if start_str else 1
            except ValueError:
                current_seq = 1
                pad_len = 0

            try:
                step_val = abs(int(step_str)) if step_str else 1
            except ValueError:
                step_val = 1

            # 2. 扫描并强制排序
            all_files = sorted([e.name for e in os.scandir(in_d) if e.is_file()], key=lambda x: x.lower())

            if limit_val > 0:
                all_files = all_files[:limit_val]

            new_names_set = set()

            for old_name in all_files:
                new_name = old_name
                status = "✅ 正常"

                if val1 or (enable_seq and rule in ["添加前缀", "添加后缀"]):
                    try:
                        name_part, ext_part = os.path.splitext(old_name)

                        # 生成序列字符串 (处理智能补零)
                        if enable_seq:
                            seq_str = str(current_seq).zfill(pad_len) if pad_len > 0 else str(current_seq)
                        else:
                            seq_str = ""

                        if rule == "文本替换" and val1:
                            new_name = old_name.replace(val1, val2)
                        elif rule == "正则替换" and val1:
                            new_name = re.sub(val1, val2, old_name)
                        elif rule == "添加前缀":
                            new_name = f"{val1}{seq_str}{old_name}"
                        elif rule == "添加后缀":
                            new_name = f"{name_part}{val1}{seq_str}{ext_part}"
                        elif rule == "修改扩展名" and val1:
                            ext = val1 if val1.startswith(".") else f".{val1}"
                            new_name = f"{name_part}{ext}"

                        # 步长运算
                        if enable_seq and rule in ["添加前缀", "添加后缀"]:
                            if is_increment:
                                current_seq += step_val
                            else:
                                current_seq -= step_val
                    except re.error:
                        status = "❌ 正则错误"

                # 冲突检测
                if new_name != old_name:
                    target_full = os.path.join(in_d, new_name)
                    if new_name in new_names_set or (
                            os.path.exists(target_full) and new_name.lower() != old_name.lower()):
                        status = "⚠️ 命名冲突"
                    new_names_set.add(new_name)

                # 缓存记录
                if new_name != old_name or status != "✅ 正常":
                    self._preview_data.append({
                        "old_path": os.path.join(in_d, old_name),
                        "new_path": os.path.join(in_d, new_name),
                        "old_name": old_name,
                        "new_name": new_name,
                        "status": status
                    })

            self.parent.after(0, self._render_preview)
        except (OSError, re.error) as e:
            self.parent.after(0, lambda err=e: self.btn_execute.config(text=f"预览失败: {err}"))
            self.parent.after(0, lambda: self.update_status("预览错误", 0))

    def _render_preview(self) -> None:
        self.update_status("预览完成", 100)

        display_count = min(len(self._preview_data), self._max_preview_limit)

        for i in range(display_count):
            data = self._preview_data[i]
            self.tree.insert("", "end", values=(data["status"], data["old_name"], data["new_name"]))

        if len(self._preview_data) > self._max_preview_limit:
            self.tree.insert("", "end", values=("...", "...",
                                                f"(省略展示后续 {len(self._preview_data) - self._max_preview_limit} 条变更)"))

        valid_count = sum(1 for d in self._preview_data if d["status"] == "✅ 正常")
        if valid_count > 0:
            self.btn_execute.config(state="normal", text=f"🚀 确认执行 ({valid_count}个文件)")
        else:
            self.btn_execute.config(state="disabled", text="未检测到有效变更")

    def run_execute(self) -> None:
        valid_tasks = [d for d in self._preview_data if d["status"] == "✅ 正常"]
        if not valid_tasks:
            return

        if not messagebox.askyesno("二次确认",
                                   f"即将重命名 {len(valid_tasks)} 个文件。\n此操作可能影响工程运行且不可撤销，是否继续？"):
            return

        self.btn_execute.config(state="disabled", text="正在飞速重命名...")
        threading.Thread(target=self._rename_worker, args=(valid_tasks,), daemon=True).start()

    def _rename_worker(self, tasks: List[Dict[str, str]]) -> None:
        success_count = 0
        try:
            total = len(tasks)
            for i, task in enumerate(tasks):
                os.rename(str(task["old_path"]), str(task["new_path"]))
                success_count += 1
                self.parent.after(0,
                                  lambda p=int((i / total) * 100): self.update_status(f"处理中: {task['new_name']}", p))

            self.parent.after(0, lambda: messagebox.showinfo("圆满完成", f"成功重命名 {success_count} 个文件！"))
        except OSError as e:
            self.parent.after(0, lambda err=e: messagebox.showerror("权限受限", f"部分文件被占用或拒绝访问:\n{err}"))
        finally:
            def _cleanup():
                self.update_status("准备就绪", 0)
                current_rule = self.rule_type_var.get()
                self.rule_type_var.set(current_rule)

            self.parent.after(0, _cleanup)
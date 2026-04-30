import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from src.gui.tabs.base_tab import BaseTab
from src.core.reader import generate_ascii_tree
from src.core.writer import save_tree_output


class TreeGeneratorTab(BaseTab):
    def __init__(self, parent, update_status_cb):
        super().__init__(parent, update_status_cb)
        self.dir_var = tk.StringVar()
        self.out_dir_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Desktop"))
        self.filename_var = tk.StringVar(value="Project_Tree")
        self.format_var = tk.StringVar(value="TXT")
        self.depth_var = tk.StringVar(value="0")  # [新增] 控制展开深度

        self.btn_run = None
        self.preview = None
        self._current_full_tree = ""

        self.setup_ui()

        # 深度改变也会触发自动预览
        for v in (self.dir_var, self.depth_var):
            v.trace_add("write", lambda *_: self.update_preview())

    @staticmethod
    def _select_dir(var):
        p = filedialog.askdirectory()
        if p:
            var.set(p)

    def copy_to_clipboard(self):
        if not self._current_full_tree:
            messagebox.showwarning("提示", "当前没有可复制的目录树内容，请先选择有效路径。")
            return

        self.parent.clipboard_clear()
        self.parent.clipboard_append(self._current_full_tree)
        messagebox.showinfo("成功", "✅ 完整目录结构已复制到剪贴板！可以直接去粘贴了。")

    def setup_ui(self):
        main_f = tk.Frame(self.parent)
        main_f.pack(fill="both", expand=True)
        self.dynamic_widgets.append((main_f, "bg", "panel"))

        bot_area = tk.Frame(main_f)
        bot_area.pack(side="bottom", fill="x", pady=(10, 30))

        btn_container = tk.Frame(bot_area)
        btn_container.pack(anchor="center")
        self.dynamic_widgets.append((btn_container, "bg", "panel"))

        self.btn_run = tk.Button(btn_container, text="生成目录结构树", font=("Microsoft YaHei", 12, "bold"), fg="white",
                                 cursor="hand2", relief="flat", command=self.run_generation)
        self.btn_run.pack(ipadx=40, ipady=5)
        self.dynamic_widgets.append((self.btn_run, "bg", "accent"))

        top_area = tk.Frame(main_f)
        top_area.pack(side="top", fill="x", padx=45, pady=(25, 0))

        # === 替换开始 ===
        tk.Label(top_area, text="一、 目录选择与导出设置", font=("Microsoft YaHei", 11, "bold")).pack(anchor="w",
                                                                                                     pady=(0, 10))

        # [优化] 第一行：完全释放空间给项目文件夹
        r1 = tk.Frame(top_area)
        r1.pack(fill="x", pady=5)
        tk.Label(r1, text="项目文件夹:", width=10).pack(side="left")
        e1_f, _ = self._create_perfect_entry(r1, self.dir_var)
        e1_f.pack(side="left", fill="x", expand=True, padx=5)
        self._create_perfect_button(r1, "浏览...", lambda: self._select_dir(self.dir_var)).pack(side="left")

        r2 = tk.Frame(top_area)
        r2.pack(fill="x", pady=5)
        tk.Label(r2, text="保存至:", width=10).pack(side="left")
        e2_f, _ = self._create_perfect_entry(r2, self.out_dir_var)
        e2_f.pack(side="left", fill="x", expand=True, padx=5)
        self._create_perfect_button(r2, "浏览...", lambda: self._select_dir(self.out_dir_var)).pack(side="left")

        # [优化] 第三行：将“展开层级”完美融入这行的留白处
        r3 = tk.Frame(top_area)
        r3.pack(fill="x", pady=5)
        tk.Label(r3, text="文件名:", width=10).pack(side="left")
        e3_f, _ = self._create_perfect_entry(r3, self.filename_var, width=20)
        e3_f.pack(side="left", padx=5)

        tk.Label(r3, text="格式:").pack(side="left", padx=(15, 5))
        ttk.Combobox(r3, textvariable=self.format_var, values=["TXT", "Word"], state="readonly", width=8).pack(
            side="left", ipady=2)

        # 移动到此处的层级控制
        tk.Label(r3, text="展开层级(0不限):").pack(side="left", padx=(25, 5))
        e_depth_f, _ = self._create_perfect_entry(r3, self.depth_var, width=6)
        e_depth_f.pack(side="left")
        # === 替换结束 ===

        mid_area = tk.Frame(main_f)
        mid_area.pack(side="top", fill="both", expand=True, padx=45, pady=(20, 10))

        header_f = tk.Frame(mid_area)
        header_f.pack(fill="x", pady=(0, 5))
        self.dynamic_widgets.append((header_f, "bg", "panel"))

        tk.Label(header_f, text="二、 结构预览 (仅展示前 50 行):", font=("Microsoft YaHei", 11, "bold")).pack(
            side="left")

        btn_copy_f = self._create_perfect_button(header_f, "📋 复制完整结构", self.copy_to_clipboard)
        btn_copy_f.pack(side="right")

        txt_b = tk.Frame(mid_area, padx=1, pady=1)
        txt_b.pack(fill="both", expand=True)
        self.dynamic_widgets.append((txt_b, "bg", "border"))

        txt_bg = tk.Frame(txt_b)
        txt_bg.pack(fill="both", expand=True)
        self.dynamic_widgets.append((txt_bg, "bg", "panel"))

        scroll = ttk.Scrollbar(txt_bg)
        scroll.pack(side="right", fill="y")

        self.preview = tk.Text(txt_bg, wrap="none", relief="flat", bd=0, padx=15, pady=10,
                               font=("Consolas", 10), yscrollcommand=scroll.set)
        self.preview.pack(side="left", fill="both", expand=True)
        scroll.config(command=self.preview.yview)

        self.dynamic_widgets.append((self.preview, "bg", "panel"))
        self.dynamic_widgets.append((self.preview, "fg", "text"))

        self._register_widgets_recursive(main_f)
        self.update_preview()

    def update_preview(self):
        in_d = self.dir_var.get().strip()
        self.preview.config(state="normal")
        self.preview.delete("1.0", "end")
        self._current_full_tree = ""

        if not os.path.isdir(in_d):
            self.preview.insert("end", "【请在上方选择有效的项目文件夹以生成预览】")
            self.preview.config(state="disabled")
            return

        self.preview.insert("end", "正在扫描目录，生成预览中...")
        self.preview.config(state="disabled")

        threading.Thread(target=self._preview_worker, args=(in_d,), daemon=True).start()

    def _preview_worker(self, in_d):
        try:
            depth = int(self.depth_var.get()) if self.depth_var.get().isdigit() else 0
            tree_str = generate_ascii_tree(in_d, max_depth=depth)
            self._current_full_tree = tree_str

            lines = tree_str.split('\n')
            display_str = '\n'.join(lines[:50])
            if len(lines) > 50:
                display_str += f"\n\n... (此处省略其余 {len(lines) - 50} 行内容，点击右上角可【复制完整结构】)"

            self.parent.after(0, lambda: self._render_preview(display_str))
        except (OSError, tk.TclError):
            pass

    def _render_preview(self, content):
        self.preview.config(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("end", content)
        self.preview.config(state="disabled")

    def run_generation(self):
        in_d, out_d, fn = self.dir_var.get().strip(), self.out_dir_var.get().strip(), self.filename_var.get().strip()

        if not os.path.isdir(in_d) or not fn:
            messagebox.showwarning("提示", "请正确选择文件夹并输入文件名。")
            return

        fmt = self.format_var.get()
        ext = 'docx' if fmt == 'Word' else 'txt'
        target_file_path = os.path.join(out_d, f"{fn}.{ext}")

        if os.path.exists(target_file_path):
            if not messagebox.askyesno("覆盖确认", f"目标文件 [{fn}.{ext}] 已存在，是否继续并覆盖？"):
                return

        self.btn_run.config(state="disabled", text="正在生成...")
        threading.Thread(target=self._worker, args=(in_d, out_d, fn, fmt), daemon=True).start()

    def _worker(self, in_d, out_d, fn, fmt):
        try:
            self.update_status("正在扫描目录结构...", 30)
            depth = int(self.depth_var.get()) if self.depth_var.get().isdigit() else 0
            tree_str = generate_ascii_tree(in_d, max_depth=depth)
            self.update_status("正在保存...", 80)
            final_p = save_tree_output(tree_str, out_d, fn, fmt)
            self.parent.after(0, lambda: messagebox.showinfo("成功", f"目录树已生成至：\n{final_p}"))

        except PermissionError:
            err_msg = "生成失败！\n\n目标文件正被其他程序（如 Word 或文本编辑器）占用。\n请先关闭该文件后，再尝试重新生成。"
            self.parent.after(0, lambda: messagebox.showerror("文件被占用", err_msg))

        except (OSError, ValueError, tk.TclError) as e:
            self.parent.after(0, lambda: messagebox.showerror("错误", f"处理失败: {e}"))
        finally:
            self.parent.after(0, lambda: [self.btn_run.config(state="normal", text="生成目录结构树"),
                                          self.update_status("准备就绪", 0)])
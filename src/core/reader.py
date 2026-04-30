import os
from typing import List, Dict, Optional, Tuple, Set


def scan_and_read(target_dir: str, allowed_extensions: Optional[Tuple[str, ...]] = None) -> List[Dict[str, str]]:
    """
    扫描指定目录，读取所有符合后缀条件的文件内容。
    :param target_dir: 要扫描的目标文件夹绝对路径
    :param allowed_extensions: 允许的后缀元组，例如 ('.py', '.java')
    :return: 包含文件信息的列表 [{'filename': '相对路径', 'content': '代码内容'}]
    """
    if allowed_extensions is None:
        allowed_extensions = (
            '.py', '.java', '.c', '.cpp', '.h', '.cs', '.js', '.ts',
            '.html', '.css', '.json', '.xml', '.yaml', '.yml', '.md', '.txt'
        )

    ignore_dirs = {'.git', '.svn', '.idea', '__pycache__', 'venv', '.venv', 'node_modules', 'dist', 'build'}
    extracted_data = []

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if file.endswith(allowed_extensions):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, target_dir)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    try:
                        with open(file_path, 'r', encoding='gbk') as f:
                            content = f.read()
                    except Exception as e:
                        content = f"[无法读取文件内容: {e}]"

                extracted_data.append({'filename': rel_path, 'content': content})

    return extracted_data


def generate_ascii_tree(target_dir: str, ignore_dirs: Optional[Set[str]] = None, max_depth: int = 0) -> str:
    """
    高性能生成 ASCII 目录树。
    :param target_dir: 目标文件夹路径
    :param ignore_dirs: 需要忽略的文件夹集合
    :param max_depth: 最大下探层级，0 表示不限制深度
    :return: 格式化后的 ASCII 目录树字符串
    """
    if ignore_dirs is None:
        ignore_dirs = {'.git', '.svn', '.idea', '__pycache__', 'venv', '.venv', 'node_modules', 'dist', 'build'}

    tree_lines = [f"📁 {os.path.basename(os.path.abspath(target_dir))}"]

    # 递归深度的阻断逻辑
    def _build_tree(current_dir: str, prefix: str = "", current_depth: int = 1) -> None:
        # [修复] 简化链式比较：current_depth > max_depth 且 max_depth > 0
        if current_depth > max_depth > 0:
            return

        try:
            with os.scandir(current_dir) as it:
                entries = [entry for entry in it if entry.name not in ignore_dirs]
                entries.sort(key=lambda e: (not e.is_dir(), e.name.lower()))

                count = len(entries)
                for i, entry in enumerate(entries):
                    is_last = (i == count - 1)
                    connector = "└── " if is_last else "├── "

                    # [修复] 简化链式比较：避免在最后被阻断的一层显示为文件夹连接符却无内容
                    if entry.is_dir() and current_depth == max_depth > 0:
                        tree_lines.append(f"{prefix}{connector}{entry.name}/")
                    else:
                        tree_lines.append(f"{prefix}{connector}{entry.name}")

                    if entry.is_dir():
                        extension = "    " if is_last else "│   "
                        _build_tree(entry.path, prefix + extension, current_depth + 1)
        except PermissionError:
            tree_lines.append(f"{prefix}└── [拒绝访问]")

    _build_tree(target_dir)
    return "\n".join(tree_lines)
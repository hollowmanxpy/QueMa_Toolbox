import os

def scan_and_read(target_dir: str, allowed_extensions: tuple = None) -> list:
    """
    扫描指定目录，读取所有符合后缀条件的文件内容。
    :param target_dir: 要扫描的目标文件夹绝对路径
    :param allowed_extensions: 允许的后缀元组，例如 ('.py', '.java')
    :return: 包含文件信息的列表 [{'filename': '相对路径', 'content': '代码内容'}]
    """
    # 默认支持提取的常见代码后缀
    if allowed_extensions is None:
        allowed_extensions = (
            '.py', '.java', '.c', '.cpp', '.h', '.cs', '.js', '.ts',
            '.html', '.css', '.json', '.xml', '.yaml', '.yml', '.md', '.txt'
        )

    # 遇到这些文件夹直接跳过，防止提取到毫无意义的依赖文件和打包产物
    ignore_dirs = {'.git', '.svn', '.idea', '__pycache__', 'venv', '.venv', 'node_modules', 'dist', 'build'}
    extracted_data = []

    # os.walk 会递归遍历文件夹
    for root, dirs, files in os.walk(target_dir):
        # 原地修改 dirs 列表，剔除需要忽略的文件夹
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            if file.endswith(allowed_extensions):
                file_path = os.path.join(root, file)
                # 获取相对路径，让生成的 Word 里标题好看些
                rel_path = os.path.relpath(file_path, target_dir)

                # 读取文件内容（先尝试 utf-8，如果报错再尝试 gbk）
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    try:
                        with open(file_path, 'r', encoding='gbk') as f:
                            content = f.read()
                    except Exception as e:
                        content = f"[无法读取文件内容: {e}]"

                extracted_data.append({
                    'filename': rel_path,
                    'content': content
                })

    return extracted_data


def generate_ascii_tree(target_dir: str, ignore_dirs: set = None) -> str:
    """
    高性能生成 ASCII 目录树。
    使用 os.scandir 代替 os.listdir 以提升 IO 性能。
    """
    if ignore_dirs is None:
        ignore_dirs = {'.git', '.svn', '.idea', '__pycache__', 'venv', '.venv', 'node_modules', 'dist', 'build'}

    # 根节点名称
    tree_lines = [f"📁 {os.path.basename(os.path.abspath(target_dir))}"]

    def _build_tree(current_dir, prefix=""):
        try:
            with os.scandir(current_dir) as it:
                # 过滤黑名单，并将文件夹排在文件前面
                entries = [entry for entry in it if entry.name not in ignore_dirs]
                entries.sort(key=lambda e: (not e.is_dir(), e.name.lower()))

                count = len(entries)
                for i, entry in enumerate(entries):
                    is_last = (i == count - 1)
                    connector = "└── " if is_last else "├── "
                    tree_lines.append(f"{prefix}{connector}{entry.name}")

                    if entry.is_dir():
                        extension = "    " if is_last else "│   "
                        _build_tree(entry.path, prefix + extension)
        except PermissionError:
            tree_lines.append(f"{prefix}└── [拒绝访问]")

    _build_tree(target_dir)
    return "\n".join(tree_lines)
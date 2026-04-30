import PyInstaller.__main__
import os
import zipfile

addition_data = f"assets{os.pathsep}assets"

print("🚀 开始编译 QueMa_Office.exe...")
PyInstaller.__main__.run([
    'src/main.py',
    '--onefile',
    '--windowed',
    '--name=QueMa_Office',
    f'--add-data={addition_data}',
    '--icon=assets/icons/app_icon.ico',
    '--clean',
    '-y',
])

print("\n📦 开始生成发布压缩包与使用说明...")
dist_dir = "dist"
exe_path = os.path.join(dist_dir, "QueMa_Office.exe")
readme_path = os.path.join(dist_dir, "使用说明_必看.txt")
zip_path = os.path.join(dist_dir, "QueMa_Office_v1.2.0.zip")

readme_content = """【QueMa_Office - 办公代码提取与整理工具】
版本：v1.2.0

【⚠️ 常见安全提示说明】
由于本软件为个人开源免费编译，未购买微软高昂的开发者证书。浏览器（如 Edge）或杀毒软件（如 360）可能会出现“未知发布者”的安全拦截。
请放心，本软件底层源码已在 GitHub 完全公开，绝无任何联网上传文件的后门。
若遇到拦截，请点击“保留” -> “显示详细信息” -> “仍要保留/仍要运行”即可。

【核心功能】
1. 源码提取：一键将工程代码导出为 Word/TXT，防卡死，适用于软著申请与代码归档。
2. 目录树生成：一键生成并复制项目目录结构，支持层级深度限制。
3. 批量重命名：支持打字即预览、正则替换、智能数字序列与后缀修改。

【项目开源地址】
https://github.com/hollowmanxpy/QueMa_Toolbox
（欢迎前往点亮 Star ⭐ 或提交反馈）
"""

if os.path.exists(exe_path):
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(exe_path, "QueMa_Office.exe")
        zf.write(readme_path, "使用说明_必看.txt")
    print(f"✅ 打包圆满完成！请将压缩包上传至 GitHub: {zip_path}")
else:
    print("❌ 未找到生成的 exe 文件，打包可能出现异常。")
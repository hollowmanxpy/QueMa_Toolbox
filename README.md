# 🪶 QueMa_Office - 办公代码工具

<div align="center">
  <img src="assets/QueMa_1.jpg" alt="QueMa Logo" width="300">
</div>

<div align="center">
  <a href="https://github.com/hollowmanxpy/QueMa_Toolbox/releases">
    <img alt="Version" src="https://img.shields.io/badge/Version-v1.1.0-blue.svg">
  </a>
  <a href="https://github.com/hollowmanxpy/QueMa_Toolbox/blob/main/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg">
  </a>
  <a href="https://www.python.org/">
    <img alt="Python Version" src="https://img.shields.io/badge/Python-3.10+-brightgreen.svg">
  </a>
  <a href="https://github.com/hollowmanxpy/QueMa_Toolbox/releases">
    <img alt="Platform" src="https://img.shields.io/badge/Platform-Windows-lightgrey.svg">
  </a>
</div>

QueMa_Office 是一款专为开发者与办公人员打造的轻量级桌面端代码提取与结构梳理工具。基于 Python + Tkinter 构建，底层实现了逻辑与视图的彻底解耦，轻松应对万级文件的大型工程，便于代码归档、作业提交或软件著作权申请。

## ✨ 核心功能

* **💻 源码智能提取**
    * 支持一键扫描并提取工程源码，导出为 **Word** 或 **纯文本 (TXT)**。
    * 自带排版引擎：支持自定义标题/代码字体、字号与颜色，自动处理深色模式反转适配。
    * 可选择性添加包含文件名的页眉和动态页脚（第 X 页 / 共 Y 页）。
    * 多语言支持：完美识别 `.py, .java, .js, .vue, .cpp, .v` 等数十种常见代码文件。
* **🌲 目录结构树生成 (v1.1.0 新增)**
    * 毫秒级扫描：自动过滤 `.git`, `node_modules` 等无关目录。
    * 实时预览：内存级处理，支持界面即时预览前 50 行，并提供**一键复制完整结构**功能。
* **🎨 全天候动态主题与高分屏优化**
    * 内置极简白、暗夜黑、护眼绿、赛博紫、樱花粉五套配色，支持无缝切换。
    * 全局 1px 极简无边框 UI 设计；底层进行 DPI 感知适配，确保高分屏下文字清晰、界面不变形。
* **🛡️ 极致健壮性**
    * 文件防占用拦截与编码降级策略，异步多线程处理，大型工程解析不卡死、不崩溃。

## 🚀 快速开始

### 直接运行 (Windows)
1. 前往 [Releases](https://github.com/hollowmanxpy/QueMa_Toolbox/releases) 页面下载最新的 `QueMa_Office.exe`。
2. 双击运行即可，无需配置 Python 环境。

### 源码运行
1. 克隆项目：
   ```bash
   git clone [https://github.com/hollowmanxpy/QueMa_Toolbox.git](https://github.com/hollowmanxpy/QueMa_Toolbox.git)
   cd QueMa_Toolbox
安装依赖：

Bash
pip install -r requirements.txt
启动程序：

Bash
python src/main.py
📦 打包指南
执行项目根目录下的打包脚本，即可生成单文件可执行程序：

Bash
python build.py
🤝 反馈与联系
如果您发现 Bug 或有改进建议，可以通过以下方式反馈：

提交 Issue：GitHub Issues

开发者邮箱：227598042@qq.com

祝您代码一路绿灯！
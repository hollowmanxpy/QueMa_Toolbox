# 🪶 雀码 (QueMa_Office) - 办公代码提取专家

![Version](https://img.shields.io/badge/version-v1.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

QueMa_Office 是一款专为开发者与办公人员打造的轻量级桌面端代码提取与结构梳理工具。基于 Python + Tkinter 构建，底层实现了逻辑与视图的彻底解耦，轻松应对万级文件的大型工程。

## ✨ 核心功能

* **💻 源码智能提取**
    * 支持一键扫描并提取工程源码，导出为 **Word** 或 **纯文本 (TXT)**。
    * 自带排版引擎：支持自定义标题/代码字体、字号与颜色，可自动生成带文件名的页眉与动态页码。
    * 多语言支持：完美识别 `.py, .java, .js, .vue, .cpp, .v` 等数十种常见代码文件。
* **🌲 目录结构树生成**
    * 毫秒级扫描：自动过滤 `.git`, `node_modules` 等无关目录。
    * 实时预览：内存级处理，支持界面即时预览前 50 行，并提供**一键复制完整结构**功能。
* **🎨 全天候动态主题**
    * 内置「极简白」、「暗夜黑」、「护眼绿」等多种主题。
    * 全局 1px 极简无边框 UI 设计，抛弃传统粗糙的 3D 边框，支持 Windows 高分屏完美适配。
* **🛡️ 极致健壮性**
    * 文件防占用拦截与编码降级策略，大型工程解析不卡死、不崩溃。

## 🚀 快速开始

### 直接运行 (Windows 用户)
1. 前往 `Releases` 页面下载最新版的 `QueMa_Office.exe`。
2. 双击运行即可，无需配置 Python 环境。

### 源码运行与构建
1. 克隆本项目：
   ```bash
   git clone [https://github.com/hollowmanxpy/QueMa_Toolbox.git](https://github.com/hollowmanxpy/QueMa_Toolbox.git)
   cd QueMa_Toolbox
激活虚拟环境并安装依赖：

Bash
pip install -r requirements.txt
运行程序：

Bash
python src/main.py
一键打包为 .exe（自动处理资源路径依赖）：

Bash
python build.py
📧 反馈与建议
如果您在使用中遇到 Bug，或者有新功能想法，欢迎随时提交 Issue 或与我们联系！

开发者邮箱：227598042@qq.com
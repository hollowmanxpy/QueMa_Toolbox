# 🪶 雀码 (QueMa) - 多功能开发工具箱

<div align="center">
  <img src="assets/QueMa_1.jpg" alt="QueMa Logo">
</div>

<div align="center">
  <a href="https://github.com/hollowmanxpy/QueMa_Toolbox/blob/main/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg">
  </a>
  <a href="https://www.python.org/">
    <img alt="Python Version" src="https://img.shields.io/badge/Python-3.10+-green.svg">
  </a>
  <a href="https://github.com/hollowmanxpy/QueMa_Toolbox/releases">
    <img alt="Platform" src="https://img.shields.io/badge/Platform-Windows-lightgrey.svg">
  </a>
</div>

**雀码 (QueMa)** 是一款极简、优雅且高效的桌面端源码提取与排版工具。专为开发者、学生及科研人员设计，能够一键将杂乱的代码工程目录，转换为格式统一、排版精美的 Word 文档或纯文本归档。

## ✨ 核心特性

- 🎨 **多主题沉浸美学**：内置「极简白」、「暗夜黑」、「护眼绿」、「赛博紫」、「樱花粉」五大主题，一键无缝切换。
- 📐 **黄金分割布局**：采用严苛的 `16:10` 界面分栏与像素级对齐，底层强制锁定控件比例，告别界面形变。
- 📄 **工业级排版导出**：
  - 自动套用定制 `.docx` 底包模板。
  - 支持自定义标题与代码字体、字号、颜色（深色模式智能反色适配）。
  - 智能附加带文件名的 Word 页眉与动态页脚（第 X 页 / 共 Y 页）。
- 🛡️ **极客级健壮性**：全代码零警告。针对大型工程及“文件被占用”等极限场景，进行了严格的后台线程剥离与中文异常拦截。

## 🚀 快速开始

### 方式一：直接运行 (推荐普通用户)
直接前往 [Releases](https://github.com/hollowmanxpy/QueMa_Toolbox/releases) 页面下载最新版的 `雀码工具箱.exe`。将其放置在电脑任意位置，双击即可使用，**无需安装任何 Python 环境**。

### 方式二：源码运行 (推荐开发者)
1. 克隆本项目：
   ```bash
   git clone [https://github.com/hollowmanxpy/QueMa_Toolbox.git](https://github.com/hollowmanxpy/QueMa_Toolbox.git)
   cd QueMa_Toolbox
安装依赖：

Bash
pip install -r requirements.txt
启动程序：

Bash
python src/main.py
🛠️ 构建可执行文件
本项目内置一键打包脚本，执行以下命令即可在 dist 目录下生成独立的单文件程序：

Bash
python build.py
## 🤝 贡献与反馈
如果您在使用中遇到了 Bug，或有新的功能想法，欢迎随时通过以下方式联系我：
- **提交 Issue**：[点击这里提交 Bug 或建议](https://github.com/hollowmanxpy/QueMa_Toolbox/issues)
- **开发者邮箱**：227598042@qq.com

祝您代码无 Bug，一路绿灯！
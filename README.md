# 🪶 雀码 (QueMa) - 源码提取工具

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

雀码 (QueMa) 是一款面向开发者的桌面端辅助工具，主要用于将代码工程目录一键提取并整理为格式统一的 Word 文档或纯文本文件，便于代码归档、作业提交或软件著作权申请。

## 🛠️ 主要功能

- **多主题支持**：内置极简白、暗夜黑、护眼绿、赛博紫、樱花粉五套配色，支持无缝切换。
- **高分屏优化**：底层进行 DPI 感知适配，确保在不同分辨率的显示器下文字清晰且界面不变形。
- **自定义排版**：
  - 支持设置标题与正文的代码字体、字号及颜色。
  - 自动处理深色模式下的颜色反转适配。
  - 可选择性添加包含文件名的页眉和动态页脚（第 X 页 / 共 Y 页）。
- **异步处理**：提取过程在后台线程执行，确保在处理大型工程时界面不卡顿。

## 🚀 快速开始

### 直接运行 (Windows)
1. 前往 [Releases](https://github.com/hollowmanxpy/QueMa_Toolbox/releases) 页面下载 `QueMa_Toolbox_v1.0.0.exe`。
2. 双击运行即可，无需配置 Python 环境。

### 源码运行
1. 克隆项目：
   ```bash
   git clone [https://github.com/hollowmanxpy/QueMa_Toolbox.git](https://github.com/hollowmanxpy/QueMa_Toolbox.git)
   cd QueMa_Toolbox
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 启动程序：
   ```bash
   python src/main.py
   ```

## 📦 打包指南
执行项目根目录下的打包脚本，即可生成单文件可执行程序：
```bash
python build.py
```

## 🤝 反馈与联系
如果您发现 Bug 或有改进建议，可以通过以下方式反馈：
- **提交 Issue**：[GitHub Issues](https://github.com/hollowmanxpy/QueMa_Toolbox/issues)
- **开发者邮箱**：227598042@qq.com

祝您代码一路绿灯！
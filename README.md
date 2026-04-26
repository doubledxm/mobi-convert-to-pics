# Mobi 漫画提取图片工具 / Mobi to Image Extractor

[中文](#中文) | [English](#english)

---

<h2 id="中文">🇨🇳 中文</h2>

一个简单轻量的 Windows 桌面工具，用于从 `.mobi` 格式的电子书（尤其是漫画）中无损批量提取出原始分辨率的图片。

### ✨ 核心特性

- 📦 **无损提取**：不对图片进行任何二次编码或压缩，原封不动提取电子书中打包的原始图片。
- 🚀 **批量处理**：支持一次性导入多个 `.mobi` 文件自动排队处理。
- 📂 **智能分类**：每个电子书会自动建立一个同名文件夹存放图片，绝不会把不同漫画混在一起。
- 🎯 **支持源路径输出**：一键勾选，直接在原始电子书所在的目录下生成图片文件夹，免去寻找输出目录的烦恼。
- 🖥️ **绿色独立运行**：提供了打包好的单文件 `.exe` 可执行程序，无需配置繁琐的 Python 环境变量。

### 📥 如何使用

#### 方法一：直接运行可执行文件（推荐普通用户）
1. 前往右侧的 [Releases](#) 下载最新的 `extract.exe` 文件。
2. 将其放在电脑的任意位置，双击直接运行即可。
3. 点击“添加文件”选择你的电子书，设置好输出路径，点击“开始提取”。

#### 方法二：通过 Python 源码运行（推荐开发者）
1. 确保你的电脑安装了 Python 3 环境。
2. 克隆本仓库：
   ```bash
   git clone https://github.com/doubledxm/mobi-convert-to-pics.git
   cd mobi-convert-to-pics
   ```
3. 安装依赖：
   ```bash
   pip install mobi
   ```
4. 运行程序：
   ```bash
   python extract.py
   ```

### 🛠️ 技术栈
- **Python 3**
- **Tkinter**: 构建原生 GUI 界面。
- **mobi (KindleUnpack)**: 用于解包解析 `.mobi` 容器格式。

---

<h2 id="english">🇬🇧 English</h2>

A simple and lightweight Windows desktop tool to losslessly batch extract original resolution images from `.mobi` format ebooks (especially comics).

### ✨ Core Features

- 📦 **Lossless Extraction**: No re-encoding or compression. Extracts the original images exactly as they were packed in the ebook.
- 🚀 **Batch Processing**: Import multiple `.mobi` files at once for automatic queued processing.
- 📂 **Smart Organization**: Automatically creates a subfolder named after each ebook to store its extracted images, preventing different comics from mixing.
- 🎯 **Source Directory Output**: One-click toggle to generate image folders directly in the original directory of the ebook, saving you the hassle of manual path selection.
- 🖥️ **Standalone Executable**: Provides a pre-packaged single `.exe` file. No need to install Python or configure complex environment variables.

### 📥 How to Use

#### Method 1: Run Executable (Recommended for regular users)
1. Go to the [Releases](#) section on the right to download the latest `extract.exe` file.
2. Place it anywhere on your PC and double-click to run.
3. Click "添加文件" (Add Files) to select your ebooks, set the output path, and click "开始提取" (Start Extraction).

#### Method 2: Run from Python Source (Recommended for developers)
1. Ensure you have Python 3 installed.
2. Clone this repository:
   ```bash
   git clone https://github.com/doubledxm/mobi-convert-to-pics.git
   cd mobi-convert-to-pics
   ```
3. Install dependencies:
   ```bash
   pip install mobi
   ```
4. Run the program:
   ```bash
   python extract.py
   ```

### 🛠️ Tech Stack
- **Python 3**
- **Tkinter**: For building the native GUI.
- **mobi (KindleUnpack)**: For unpacking and parsing the `.mobi` container format.

---

## 📝 License / 许可证
MIT License

# Powerful TXT 解码器

> 一个小型 Python 命令行工具，用于自动检测网上下载的乱码 TXT 小说等文件的编码，并修复常见的乱码（mojibake）问题。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![GitHub](https://img.shields.io/badge/GitHub-PowerfulDecoderForTxt-181717.svg?logo=github)](https://github.com/zyphraxns/PowerfulDecoderForTxt)

[English](README.md) | **中文说明**

## 简介

你是否遇到过这种情况：从网上下载的 TXT 小说打开后全是乱码（`锟斤拷`、`����`、`Ã©`…）？这通常是因为文件的编码被错误识别，或者文件本身被双重编码所致。

Powerful TXT 解码器可以解决这个问题：它读取原始字节，利用 `charset-normalizer`（回退到 `chardet`）检测最可能的编码；当单次解码效果不佳时，会尝试常见的双重解码修复（如 Latin-1 → UTF-8）来还原原始文本。输出结果始终为干净的 UTF-8 文件，在任何现代编辑器中都能正常打开。

## 功能特性

- **自动检测编码** — 优先使用 `charset-normalizer`，回退到 `chardet`
- **BOM 检测** — 自动处理 UTF-8 / UTF-16 / UTF-32 的 BOM 标记
- **乱码修复** — 单次解码效果不佳时，尝试常见双重解码模式（如 Latin-1 → UTF-8）
- **智能评分** — 综合 CJK 字符占比、可打印字符占比、中文标点和替换字符惩罚，选出最佳结果
- **广泛编码支持** — 支持 UTF-8、GB18030/GBK/GB2312、Big5、Shift-JIS、EUC-KR、Latin-1、CP1252 等
- **UTF-8 输出** — 所有写入的文件均为 UTF-8 编码

## 安装

### 环境要求

- Python 3.8 及以上

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/zyphraxns/PowerfulDecoderForTxt.git
cd PowerfulDecoderForTxt

# 安装依赖
pip install -r requirements.txt
```

## 快速开始

```bash
# 解码文件（默认输出文件名追加 _decoded.txt）
python3 txt_decoder.py book.txt

# 指定输出路径，并在已存在时覆盖
python3 txt_decoder.py book.txt -o fixed_book.txt --overwrite

# 仅打印检测到的编码和评分（不写入文件）
python3 txt_decoder.py book.txt --show-encoding
```

示例输出：

```
$ python3 txt_decoder.py book.txt --show-encoding
detected_encoding: gb18030, score: 0.9765

$ python3 txt_decoder.py book.txt
Written: book_decoded.txt  (detected encoding: gb18030, score: 0.9765)
```

## 命令行参数

| 参数 | 说明 |
|------|------|
| `input` | 待解码的 TXT 文件路径（必填） |
| `-o, --output` | 输出文件路径。默认为 `<input>_decoded.txt` |
| `--overwrite` | 若输出文件已存在则覆盖 |
| `--show-encoding` | 仅打印检测到的编码和评分，不写入文件 |

退出码：

- `0` — 成功
- `2` — 输入文件不存在
- `3` — 输出文件已存在（需使用 `--overwrite` 覆盖）

## 工作原理

1. 检查 BOM（UTF-8 / UTF-16 / UTF-32），若存在则直接解码。
2. 使用 `charset-normalizer`（回退 `chardet`）检测编码。
3. 用候选编码逐一尝试解码，并对结果进行评分。
4. 若单次解码效果不佳，尝试双重解码修复（如 Latin-1 → UTF-8 → GB18030），保留评分最高的文本。
5. 将最终文本以 UTF-8 编码写入文件。

## 文档

- [English README](README.md) — English version
- [贡献指南](CONTRIBUTING.md) — 如何提交 Issue 和代码
- [更新日志](CHANGELOG.md) — 版本发布记录

## 贡献

欢迎任何形式的贡献！在提交 Issue 或 Pull Request 前，请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

本项目基于 [MIT License](LICENSE) 开源。

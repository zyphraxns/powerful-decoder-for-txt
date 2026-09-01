# Powerful TXT Decoder

> A small Python CLI tool that automatically detects the encoding of garbled TXT files (e.g. novels downloaded from the Internet) and repairs common mojibake.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![GitHub](https://img.shields.io/badge/GitHub-PowerfulDecoderForTxt-181717.svg?logo=github)](https://github.com/zyphraxns/PowerfulDecoderForTxt)

**English** | [中文说明](README_zh.md)

## Introduction

Have you ever downloaded a TXT novel from the Internet only to find it full of garbled characters (`锟斤拷`、`����`、`Ã©`…)? That is usually caused by a wrong encoding interpretation or by a file that was double-encoded.

Powerful TXT Decoder fixes this: it reads the raw bytes, detects the most likely encoding (using `charset-normalizer`, falling back to `chardet`), and when a single decoding pass looks poor, it attempts common double-decode repairs (such as Latin-1 → UTF-8) to recover the original text. The result is always written as a clean UTF-8 file that opens correctly in any modern editor.

## Features

- **Automatic encoding detection** — prefers `charset-normalizer`, falls back to `chardet`
- **BOM detection** — handles UTF-8 / UTF-16 / UTF-32 BOM markers automatically
- **Mojibake repair** — tries common double-decode patterns (e.g. Latin-1 → UTF-8) when a single decode looks bad
- **Smart scoring** — picks the best result using CJK character ratio, printable-character ratio, Chinese punctuation, and replacement-character penalty
- **Wide encoding coverage** — supports UTF-8, GB18030/GBK/GB2312, Big5, Shift-JIS, EUC-KR, Latin-1, CP1252 and more
- **UTF-8 output** — every written file is UTF-8 encoded

## Installation

### Prerequisites

- Python 3.8 or newer

### Steps

```bash
# Clone the repository
git clone https://github.com/zyphraxns/PowerfulDecoderForTxt.git
cd PowerfulDecoderForTxt

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```bash
# Decode a file (default output appends _decoded.txt)
python3 txt_decoder.py book.txt

# Specify output path and overwrite if it exists
python3 txt_decoder.py book.txt -o fixed_book.txt --overwrite

# Only print the detected encoding and score (no file is written)
python3 txt_decoder.py book.txt --show-encoding
```

Example output:

```
$ python3 txt_decoder.py book.txt --show-encoding
detected_encoding: gb18030, score: 0.9765

$ python3 txt_decoder.py book.txt
Written: book_decoded.txt  (detected encoding: gb18030, score: 0.9765)
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `input` | Path to the TXT file to decode (required) |
| `-o, --output` | Output file path. Defaults to `<input>_decoded.txt` |
| `--overwrite` | Overwrite the output file if it already exists |
| `--show-encoding` | Only print the detected encoding and score, without writing a file |

Exit codes:

- `0` — success
- `2` — input file not found
- `3` — output file already exists (use `--overwrite` to replace it)

## How It Works

1. Check for a BOM (UTF-8 / UTF-16 / UTF-32) and decode directly if found.
2. Detect the encoding with `charset-normalizer` (or `chardet` as fallback).
3. Try decoding the bytes with each candidate encoding and score the result.
4. If a single pass yields poor results, try double-decode repairs (e.g. Latin-1 → UTF-8 → GB18030) and keep the best-scoring text.
5. Write the winning text as a UTF-8 file.

## Documentation

- [中文说明](README_zh.md) — 中文版说明
- [Contributing Guide](CONTRIBUTING.md) — how to report issues and submit code
- [Changelog](CHANGELOG.md) — release history

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request.

## License

This project is licensed under the [MIT License](LICENSE).

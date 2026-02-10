# Powerful TXT decoder

This is a small tool for repairing and decoding potentially garbled TXT novel files downloaded from the Internet.

Features:
- Automatically detect file encoding (using `charset-normalizer` or `chardet`)
- Try to fix common mojibake (garbled characters caused by double encoding)
- Output as UTF-8 encoded text file

Usage example:

```bash
# Install dependencies
pip install -r requirements.txt

# Decode and write a new file (default appends _decoded.txt)
python3 txt_decoder.py book.txt

# Specify output and overwrite if exists
python3 txt_decoder.py book.txt -o book_fixed.txt --overwrite

# Only show detected encoding and score
python3 txt_decoder.py book.txt --show-encoding
```

Implementation (brief):
- First check BOM (UTF-8/16/32)
- Use `charset-normalizer` (preferred) or `chardet` to detect encoding
- Try decoding among candidate encodings and pick the best one based on a simple scoring function (CJK ratio, printable character ratio, number of replacement characters)
- When single decoding yields poor results, try common double-decode repairs (like Latin1 -> UTF-8) to recover text

If you want this packaged as an installable CLI, batch directory processing, or a GUI, tell me which option you prefer.

**Quick Start**

- **Prerequisite**: Install Python 3 (3.8+ recommended) and dependencies:

  ```bash
  pip install -r requirements.txt
  ```

- **Single file decoding (default output UTF-8, new file name adds `_decoded.txt`)**:

  ```bash
  python3 txt_decoder.py book.txt
  ```

- **Specify output and overwrite existing files**:

  ```bash
  python3 txt_decoder.py book.txt -o fixed_book.txt --overwrite
  ```

- **Only display detected encoding and score (do not write file)**:

  ```bash
  python3 txt_decoder.py book.txt --show-encoding
  ```

- **Batch process all `.txt` in a directory (example: output to `decoded/`)**:

  ```bash
  mkdir -p decoded
  for f in *.txt; do
    python3 txt_decoder.py "$f" -o "decoded/${f%.txt}_decoded.txt" --overwrite
  done
  ```

- **Output**: All written files are UTF-8 encoded for easy opening in modern editors.

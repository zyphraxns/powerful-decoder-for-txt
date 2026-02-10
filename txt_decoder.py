#!/usr/bin/env python3
"""
Powerful TXT decoder — auto-detects encoding and attempts to repair common mojibake

Usage example:
  python3 txt_decoder.py input.txt -o output.txt --overwrite

Dependencies: charset-normalizer, chardet (prefer charset-normalizer, fallback to chardet)
"""
from __future__ import annotations
import argparse
import sys
from typing import Optional, Tuple, List

COMMON_ENCODINGS = [
    "utf-8",
    "utf-8-sig",
    "gb18030",
    "gbk",
    "gb2312",
    "big5",
    "cp950",
    "cp936",
    "euc-jp",
    "shift_jis",
    "euc-kr",
    "iso-8859-1",
    "cp1252",
    "latin1",
]


def is_cjk(ch: str) -> bool:
    o = ord(ch)
    # Common CJK ranges
    return (0x4E00 <= o <= 0x9FFF) or (0x3400 <= o <= 0x4DBF) or (0xF900 <= o <= 0xFAFF)


def cjk_ratio(text: str) -> float:
    if not text:
        return 0.0
    cjk = sum(1 for ch in text if is_cjk(ch))
    return cjk / max(1, len(text))


def printable_ratio(text: str) -> float:
    printable = sum(1 for ch in text if ch.isprintable())
    return printable / max(1, len(text))


def detect_with_charset_normalizer(data: bytes) -> Optional[Tuple[str, float]]:
    try:
        from charset_normalizer import from_bytes

        result = from_bytes(data)
        best = result.best()
        if best:
            return best.encoding, getattr(best, "confidence", 0.0)
    except Exception:
        return None
    return None


def detect_with_chardet(data: bytes) -> Optional[Tuple[str, float]]:
    try:
        import chardet

        r = chardet.detect(data)
        if r and r.get("encoding"):
            return r["encoding"], float(r.get("confidence", 0.0))
    except Exception:
        return None
    return None


def score_text(s: str) -> float:
    # Scoring: prefer Chinese text (higher CJK ratio) and printable characters,
    # penalize replacement characters. Boost for Chinese punctuation common in novels.
    if not s:
        return -999.0
    replace_count = s.count("�")
    score = cjk_ratio(s) * 2.0 + printable_ratio(s)
    punct = '，。！？、：；“”'
    punct_boost = sum(s.count(p) for p in punct) * 0.5
    score += punct_boost
    score -= replace_count * 1.5
    return score


def try_candidates(data: bytes, candidates: List[str]) -> Tuple[Optional[str], Optional[str], float]:
    best_text = None
    best_enc = None
    best_score = -1e9
    tried = set()
    for enc in candidates:
        if not enc:
            continue
        e = enc.lower()
        if e in tried:
            continue
        tried.add(e)
        try:
            s = data.decode(e, errors="strict")
        except Exception:
            try:
                s = data.decode(e, errors="replace")
            except Exception:
                continue
        sc = score_text(s)
        if sc > best_score:
            best_score = sc
            best_text = s
            best_enc = e
    return best_text, best_enc, best_score


def try_double_decode(data: bytes) -> Tuple[Optional[str], Optional[str], float]:
    # Improved double-decode attempt to handle common mojibake patterns such as
    # latin1 -> utf-8 or utf-8 interpreted as latin1, etc.
    decode_candidates = ["utf-8", "latin1", "cp1252", "gbk", "gb18030", "big5"]
    back_encode_candidates = ["latin1", "cp1252", "utf-8"]
    final_decode_candidates = ["gb18030", "gbk", "big5", "utf-8", "cp1252", "latin1"]

    best_text = None
    best_desc = None
    best_score = -1e9

    for dec in decode_candidates:
        try:
            s0 = data.decode(dec, errors="replace")
        except Exception:
            continue
        for back in back_encode_candidates:
            try:
                # Re-encode the intermediate string to recover candidate original bytes
                b = s0.encode(back, errors="replace")
            except Exception:
                continue
            for final in final_decode_candidates:
                try:
                    s = b.decode(final, errors="strict")
                except Exception:
                    continue
                sc = score_text(s)
                if sc > best_score:
                    best_score = sc
                    best_text = s
                    best_desc = f"{dec} -> encode({back}) -> decode({final})"

    return best_text, best_desc, best_score


def decode_bytes_to_text(data: bytes) -> Tuple[str, str, float]:
    # 1) Check BOMs: UTF-16/32/8
    if data.startswith(b"\xff\xfe") or data.startswith(b"\xfe\xff"):
        try:
            return data.decode("utf-16"), "utf-16", 1.0
        except Exception:
            pass
    if data.startswith(b"\xff\xfe\x00\x00") or data.startswith(b"\x00\x00\xfe\xff"):
        try:
            return data.decode("utf-32"), "utf-32", 1.0
        except Exception:
            pass
    if data.startswith(b"\xef\xbb\xbf"):
        try:
            return data.decode("utf-8-sig"), "utf-8-sig", 1.0
        except Exception:
            pass

    # 2) Use charset-normalizer or chardet
    detected = detect_with_charset_normalizer(data) or detect_with_chardet(data)
    candidates = []
    if detected:
        candidates.append(detected[0])
    candidates.extend(COMMON_ENCODINGS)

    # 3) Single-pass candidates
    text, enc, score = try_candidates(data, candidates)

    # 4) Also try double-decode repairs and pick the higher-scoring result
    dd_text, dd_desc, dd_score = try_double_decode(data)
    if dd_text and dd_score > score:
        return dd_text, dd_desc or "double", dd_score

    return text or data.decode("latin1", errors="replace"), enc or "unknown", score


def process_file(path: str) -> Tuple[str, str, float]:
    with open(path, "rb") as f:
        data = f.read()
    text, enc, score = decode_bytes_to_text(data)
    return text, enc, score


def main(argv=None):
    p = argparse.ArgumentParser(description="Powerful TXT decoder — auto-detect and repair mojibake")
    p.add_argument("input", help="Path to the txt file to decode")
    p.add_argument("-o", "--output", help="Output file path (default: add _decoded.txt)")
    p.add_argument("--overwrite", action="store_true", help="Overwrite output file if it exists")
    p.add_argument("--show-encoding", action="store_true", help="Only show detected encoding and score, do not write file")
    args = p.parse_args(argv)

    try:
        text, enc, score = process_file(args.input)
    except FileNotFoundError:
        print("Input file not found:", args.input, file=sys.stderr)
        sys.exit(2)

    if args.show_encoding:
        print(f"detected_encoding: {enc}, score: {score:.4f}")
        return

    outpath = args.output
    if not outpath:
        if args.input.lower().endswith(".txt"):
            outpath = args.input[:-4] + "_decoded.txt"
        else:
            outpath = args.input + "_decoded.txt"

    if not args.overwrite:
        try:
            import os

            if os.path.exists(outpath):
                print("Output file exists (use --overwrite to replace):", outpath, file=sys.stderr)
                sys.exit(3)
        except Exception:
            pass

    with open(outpath, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    print(f"Written: {outpath}  (detected encoding: {enc}, score: {score:.4f})")


if __name__ == "__main__":
    main()

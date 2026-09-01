# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial release
- Automatic encoding detection via `charset-normalizer` (preferred) with `chardet` fallback
- BOM detection for UTF-8 / UTF-16 / UTF-32 files
- Mojibake repair using common double-decode patterns (e.g. Latin-1 → UTF-8)
- Candidate-decoding with a scoring function (CJK ratio, printable ratio, punctuation boost, replacement-character penalty)
- CLI options: `-o/--output`, `--overwrite`, `--show-encoding`
- Always writes output as UTF-8 text

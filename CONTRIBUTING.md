# Contributing Guide

Thank you for your interest in contributing to **Powerful TXT Decoder**! Your help — whether reporting a bug, suggesting a feature, or submitting code — is greatly appreciated.

## How to Contribute

### Reporting a Bug

1. Search the existing [Issues](https://github.com/zyphraxns/PowerfulDecoderForTxt/issues) to make sure the bug hasn't been reported already.
2. Open a new issue and include:
   - Your operating system and Python version
   - The command you ran
   - The exact error output or screenshot
   - (If possible) a small sample of the garbled input file

### Suggesting a Feature

1. Search the existing Issues first.
2. Open a new issue describing:
   - What you want to add
   - Why you need it (use case)
   - How you expect it to work

### Submitting Code

#### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/<your-username>/PowerfulDecoderForTxt.git
cd PowerfulDecoderForTxt

# Install dependencies
pip install -r requirements.txt
```

#### Development Workflow

1. Create a branch from `main`:

   ```bash
   git checkout -b feat/your-feature-name
   ```

2. Make your changes, keeping them focused and consistent with the existing code style (PEP 8, 4-space indentation, semantic naming, comments for non-obvious logic).

3. Test your changes against a real garbled TXT file:

   ```bash
   python3 txt_decoder.py your_sample.txt --show-encoding
   python3 txt_decoder.py your_sample.txt -o output.txt --overwrite
   ```

4. Commit with a clear message following [Conventional Commits](https://www.conventionalcommits.org/):

   ```
   feat: add support for batch directory processing
   fix: handle empty input files gracefully
   docs: update README installation section
   ```

5. Push your branch and open a Pull Request.

#### Pull Request Requirements

- PR title follows Conventional Commits conventions
- Describe the change and the motivation behind it
- Reference related issues (e.g. `Closes #123`)
- Make sure the change is tested against sample files
- Update the README / CHANGELOG if the change affects users

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) with 4-space indentation
- Use semantic, descriptive names for functions and variables
- Add comments for complex logic (the existing scoring/double-decode functions are good examples)
- Keep the tool a single, dependency-light script unless a strong reason exists otherwise

## Project Structure

```
PowerfulDecoderForTxt/
├── txt_decoder.py      # The tool itself (single-file CLI)
├── requirements.txt    # Runtime dependencies
├── README.md           # English documentation
├── README_zh.md        # Chinese documentation
└── CHANGELOG.md        # Release history
```

## Questions

If you have any questions, feel free to open an issue on GitHub.

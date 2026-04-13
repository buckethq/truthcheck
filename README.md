# truthcheck
 PyPI package structure focused on modern Python packaging standards
[![PyPI](https://img.shields.io/pypi/v/truthcheck2)](https://pypi.org/project/truthcheck2/)
---

## 🗂️ 1. Project Structure (Standard `src/` Layout)
```
your-package/
├── .github/workflows/ci.yml      # GitHub Actions CI
├── src/
│   └── your_package/             # Package code (use underscores)
│       ├── __init__.py           # Public API exports
│       ├── core.py               # Main functionality
│       └── tokenizer.py          # Optional utilities
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_tokenizer.py
├── .gitignore
├── LICENSE
├── pyproject.toml                # Single-source config (PEP 621)
├── README.md
└── CHANGELOG.md                  # Optional but recommended
```

---

## ⚙️ 2. `pyproject.toml` Template
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "your-package-name"         # Must be unique on PyPI
version = "0.1.0"
description = "Short, clear description"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
authors = [{name = "Your Name", email = "you@example.com"}]
dependencies = ["tiktoken>=0.7.0"]  # Runtime deps only

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "ruff>=0.5.0",
    "mypy>=1.10",
    "build>=1.2",
    "twine>=5.0",
]

[tool.ruff]
target-version = "py310"
line-length = 100
lint.select = ["E", "F", "I", "N", "UP", "B", "SIM", "TCH"]

[tool.mypy]
python_version = "3.10"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src/your_package --cov-report=term-missing"
```

---

## 🧱 3. Source Code Best Practices

### `src/your_package/__init__.py`
```python
"""Your package: One-line description."""

__version__ = "0.1.0"

from .core import is_truthy
from .tokenizer import count_tokens, print_token_count

__all__ = ["is_truthy", "count_tokens", "print_token_count"]
```

### `src/your_package/core.py`
```python
from typing import Any

def is_truthy(value: Any) -> bool:
    """Evaluate truthiness of any Python object.
    
    Args:
        value: Any Python object.
        
    Returns:
        bool: True if truthy, False otherwise.
    """
    return bool(value)
```

### `src/your_package/tokenizer.py`
```python
from typing import Any

import tiktoken

def count_tokens(value: Any, model: str = "cl100k_base") -> int:
    """Count tokens in string representation of any object."""
    try:
        encoding = tiktoken.get_encoding(model)
    except Exception as e:
        raise ValueError(f"Failed to load model '{model}': {e}") from e
    
    try:
        text = str(value)
    except Exception as e:
        raise TypeError(
            f"Cannot convert {type(value).__name__} to string: {e}"
        ) from e
    
    return len(encoding.encode(text))

def print_token_count(value: Any, model: str = "cl100k_base") -> int:
    """Print and return token count."""
    count = count_tokens(value, model)
    print(f"🔢 Token count ({model}): {count}")
    return count
```

> 💡 **Key Rules**:
> - Separate import blocks: stdlib → third-party → local (ruff `I001`)
> - Keep lines ≤100 chars (ruff `E501`)
> - Always add type hints + docstrings
> - Use `__all__` to define public API

---

## 🧪 4. Testing Template (`tests/test_core.py`)
```python
import pytest

from your_package.core import is_truthy

@pytest.mark.parametrize("value,expected", [
    (0, False), (1, True), ("", False), ("hello", True),
    ([], False), ([1], True), ({}, False), ({"a": 1}, True),
    (None, False), (False, False), (True, True),
])
def test_is_truthy(value: object, expected: bool) -> None:
    assert is_truthy(value) is expected
```

> ✅ Run tests: `pytest`  
> ✅ With coverage: `pytest --cov=src/your_package`

---

## 🤖 5. GitHub Actions CI (`.github/workflows/ci.yml`)
```yaml
name: CI

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false  # Don't cancel other versions on failure
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      
      - name: Install deps
        run: |
          python -m pip install --upgrade pip setuptools wheel
          pip install -e ".[dev]"
      
      - name: Format check
        run: ruff format --check .
      
      - name: Lint
        run: ruff check .
      
      - name: Type check
        run: mypy src/your_package
      
      - name: Test
        run: pytest
      
      - name: Build
        run: python -m build
```

---

## 🛠️ 6. Local Development Workflow

```bash
# 1. Create & activate venv
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows PowerShell

# 2. Install in editable + dev mode
pip install -e ".[dev]"

# 3. Auto-fix linting issues
ruff check . --fix
ruff format .

# 4. Run quality checks
ruff check . && ruff format --check .
mypy src/your_package
pytest

# 5. Build distribution
python -m build
# Output: dist/your_package-0.1.0-py3-none-any.whl

# 6. Validate before upload
twine check dist/*
```

---

## 🚀 7. Publishing to PyPI

### 🔐 Step 1: Create API Token
1. Go to https://pypi.org/manage/account/token/
2. Create new token with scope: **"Entire account"** (or scoped to package)
3. Copy token (starts with `pypi-AgEIcHlwaS5vcmc...`)

### 🔑 Step 2: Authenticate (Choose One)

**Option A: Environment Variables (Recommended for scripts)**
```powershell
# PowerShell
$env:TWINE_USERNAME="__token__"
$env:TWINE_PASSWORD="pypi-AgEIcHlwaS5vcmc..."
twine upload dist/*

# Bash
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="pypi-AgEIcHlwaS5vcmc..."
twine upload dist/*
```

**Option B: `.pypirc` Config File** (`~/.pypirc`)
```ini
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS5vcmc...
```
Then run:
```bash
twine upload dist/*                    # Production PyPI
twine upload --repository testpypi dist/*  # TestPyPI (recommended first)
```

### ⚠️ Critical Upload Notes
| Issue | Solution |
|-------|----------|
| `403 Forbidden` | Use username `__token__` (literal), not your token as username |
| Package name taken | Check https://pypi.org/project/NAME/ → pick unique name |
| Token not working | Revoke & create new token; ensure "Entire account" scope |
| Uploading to wrong repo | Use `--repository testpypi` for testing |

---

## 🐛 8. Troubleshooting Cheat Sheet

### Ruff Errors (`I001`, `E501`)
```bash
# Auto-fix all fixable issues
ruff check . --fix
ruff format .

# Prevent in CI: always run format before check
ruff format --check . && ruff check .
```

### GitHub Actions Matrix Cancellation
```yaml
# Add to strategy to prevent fail-fast cancellation
strategy:
  fail-fast: false
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
```

### TikTok/Rust Dependency Issues (Python 3.12)
```bash
# Force binary wheels to avoid Rust compilation
pip install tiktoken --only-binary :all:

# Or add build tools in CI
- name: Install build tools (Linux)
  run: sudo apt-get install -y build-essential
```

### mypy Strict Mode Complaints
```toml
# In pyproject.toml, relax for third-party libs
[tool.mypy]
strict = true
ignore_missing_imports = true  # For libs without type stubs
```

### Package Already Exists on PyPI
1. Search: https://pypi.org/search/?q=yourname
2. If taken, rename:
   ```toml
   # pyproject.toml
   name = "yourname-utils"  # or "py-yourname", "yourname-dev"
   ```
3. Update folder: `src/your_package/` → `src/yourname_utils/`
4. Update all imports and rebuild

---

## 🔄 9. Versioning & Releases (SemVer)

```toml
# pyproject.toml
version = "0.1.0"  # Format: MAJOR.MINOR.PATCH
```

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking API change | MAJOR +1 | 1.0.0 → 2.0.0 |
| New feature (backward compat) | MINOR +1 | 0.1.0 → 0.2.0 |
| Bug fix | PATCH +1 | 0.1.0 → 0.1.1 |

**Release Checklist**:
1. Update `__version__` in `__init__.py`
2. Update `version` in `pyproject.toml`
3. Add entry to `CHANGELOG.md`
4. Git tag: `git tag v0.1.0 && git push origin v0.1.0`
5. Rebuild & upload: `python -m build && twine upload dist/*`

---

## 📋 Quick Reference Commands

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Quality
ruff check . --fix && ruff format .
mypy src/your_package
pytest --cov=src/your_package

# Build & Publish
python -m build
twine check dist/*
twine upload dist/*  # or --repository testpypi

# Debug Upload
$env:TWINE_USERNAME="__token__"; $env:TWINE_PASSWORD="..."
twine upload dist/* --verbose
```

---

## 🔐 Security Best Practices
- ❌ Never commit API tokens to Git
- ✅ Use environment variables or `.pypirc` (gitignored)
- ✅ Revoke exposed tokens immediately at https://pypi.org/manage/account/token/
- ✅ Use scoped tokens when possible (limit to specific package)
- ✅ Rotate tokens periodically

---

> 💡 **Pro Tip**: Always test on **TestPyPI** first!  
> ```bash
> twine upload --repository testpypi dist/*
> pip install --index-url https://test.pypi.org/simple/ your-package
> ```

Save this guide, and you'll have a repeatable, professional workflow for every Python package you build. 🎯

*Last updated: April 2026 | Compatible with Python 3.10+*


```bash
#🛠️ Setup & Local Development Commands

# 1. Create & activate virtual environment
python -m venv .venv && source .venv/bin/activate

# 2. Install package in editable + dev mode
pip install -e ".[dev]"

# 3. Run quality checks
python -m ruff check . 
python -m ruff format .
python -m mypy src/truthcheck2

# 4. Run tests with coverage
python -m pytest

# 5. Build distribution
python -m build

# 6. Check package before upload
python -m twine check dist/*

# PowerShell
$env:TWINE_USERNAME="__token__"
$env:TWINE_PASSWORD="pypi-AgEIcHlwaS5vcmc..."  

python -m  twine upload --repository testpypi dist/*
python -m twine upload dist/*
```


```
```


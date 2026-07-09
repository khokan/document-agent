## 🔧 Installation & Troubleshooting Guide

### ✅ Fixed Issues in requirements.txt

**Removed:**
- ❌ `pypdfium2==4.18.1` — No matching distribution found (removed, not needed)

**Updated to flexible versions:**
- ✅ `fastapi>=0.104.0` — Latest stable
- ✅ `uvicorn[standard]>=0.24.0` — With standard extras
- ✅ `chromadb>=0.5.0` — Latest version (was 0.4.22)
- ✅ `pypdf>=4.0.0` — Latest version (was 3.17.4)
- ✅ All other packages updated to minimum versions

---

## 📥 Installation Steps

### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python -m venv venv
source venv/bin/activate
```

### Step 2: Upgrade pip (Important!)
```bash
# Windows
python -m pip install --upgrade pip

# Linux / macOS
python3 -m pip install --upgrade pip
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
# Check FastAPI
python -c "import fastapi; print(f'FastAPI: {fastapi.__version__}')"

# Check Pydantic
python -c "import pydantic; print(f'Pydantic: {pydantic.__version__}')"

# Check all imports
python -c "from app.utils import config, logger; print('✅ All imports working')"
```

---

## 🐛 Troubleshooting

### Issue: `ERROR: No matching distribution found for pypdfium2==4.18.1`

**Solution:** ✅ FIXED - Removed from requirements.txt

The package `pypdfium2` is not used in Sprint 1. We use:
- `pdfplumber` (primary extraction)
- `pypdf` (fallback extraction)

### Issue: `pip install` fails with network error

**Solution:**
```bash
# Try with retry
pip install -r requirements.txt --retries 5

# Or use specific PyPI index
pip install -r requirements.txt -i https://pypi.org/simple/

# Or upgrade pip first
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: `ModuleNotFoundError` after installation

**Solution:**
```bash
# Verify virtual environment is activated
# Windows: Should see (venv) in command prompt
# Linux/macOS: Should see (venv) in terminal

# If not, activate it:
source venv/bin/activate          # Linux/macOS
venv\Scripts\activate             # Windows

# Then try importing again
python -c "import fastapi"
```

### Issue: `ImportError: cannot import name 'FastAPI'`

**Solution:**
```bash
# Reinstall FastAPI
pip uninstall fastapi -y
pip install fastapi>=0.104.0

# Verify
python -c "from fastapi import FastAPI; print('✅ FastAPI installed')"
```

### Issue: `chromadb` installation fails

**Solution:**
```bash
# ChromaDB has some dependencies, ensure Xcode tools installed (macOS)
# On macOS:
xcode-select --install

# Then try again:
pip install chromadb>=0.5.0
```

### Issue: Tests fail with `ImportError`

**Solution:**
```bash
# Install test dependencies explicitly
pip install pytest pytest-cov pytest-asyncio

# Run tests with verbose output
pytest -v tests/
```

---

## ✅ Verification Checklist

After installation, verify everything works:

```bash
# 1. Check Python version
python --version              # Should be 3.12+

# 2. Check virtual environment
which python                  # Should show venv path

# 3. Check key packages
pip list | grep -i fastapi
pip list | grep -i pydantic
pip list | grep -i chromadb

# 4. Test imports
python -c "from fastapi import FastAPI; from pydantic import BaseModel; print('✅ OK')"

# 5. Run application
python main.py
# Should start without import errors

# 6. Run tests
pytest tests/ -v
# Should discover and run all tests
```

---

## 📦 Package Overview

### Core Web Framework
- **fastapi** — Web framework
- **uvicorn** — ASGI server
- **python-multipart** — Form data handling

### PDF Processing
- **pdfplumber** — Primary PDF extraction (faster, more reliable)
- **pypdf** — Fallback PDF extraction

### Data & Configuration
- **pydantic** — Data validation with type hints
- **pyyaml** — YAML configuration parsing
- **python-dotenv** — Environment variable loading
- **sqlalchemy** — ORM (for Sprint 2 database)

### Vector & Search
- **chromadb** — Vector database for embeddings
- **langchain** — LLM framework utilities

### HTTP & Async
- **httpx** — Async HTTP client (for Ollama API calls)
- **aiofiles** — Async file operations

### Testing
- **pytest** — Testing framework
- **pytest-cov** — Coverage reporting
- **pytest-asyncio** — Async test support
- **requests** — HTTP testing

---

## 🚀 Quick Start (After Installation)

```bash
# 1. Activate environment
source venv/bin/activate          # Linux/macOS
# venv\Scripts\activate           # Windows

# 2. Start application
python main.py

# 3. In another terminal, test it
curl http://localhost:8000/health

# 4. Open Swagger UI
# Browser: http://localhost:8000/docs
```

---

## 📝 Notes on Dependencies

### Why Flexible Versions?
- Using `>=` instead of `==` allows pip to install compatible newer versions
- Avoids "No matching distribution" errors
- Still maintains minimum version requirements
- Better for long-term maintenance

### When to Use Pinned Versions?
- In production deployment (use `pip freeze > freeze.txt`)
- When specific version required for compatibility
- For Docker builds (include freeze.txt)

### Environment-Specific Notes

**macOS:**
```bash
# May need Xcode tools
xcode-select --install

# If chromadb fails, try:
pip install --no-binary :all: chromadb
```

**Windows:**
- Should work out-of-the-box
- If issues, ensure Python is added to PATH
- Use PowerShell or CMD with admin if needed

**Linux:**
```bash
# May need build tools
sudo apt-get install python3-dev
sudo apt-get install build-essential
```

---

## 🔄 Updating Dependencies Later

### To update all packages:
```bash
pip install -r requirements.txt --upgrade
```

### To see what would be updated:
```bash
pip install -r requirements.txt --upgrade --dry-run
```

### To generate lock file (production):
```bash
pip freeze > requirements-lock.txt
```

Then for production deployment:
```bash
pip install -r requirements-lock.txt
```

---

## 🎓 Common Commands

```bash
# Install requirements
pip install -r requirements.txt

# Reinstall all (clean)
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Check for outdated packages
pip list --outdated

# Show package info
pip show fastapi

# Check what's installed
pip list

# Create freeze file
pip freeze > requirements-lock.txt
```

---

## ✨ Verification Script

Create a file `verify_installation.py`:

```python
#!/usr/bin/env python
"""Verify all dependencies are installed correctly."""

import sys

packages = [
    ("fastapi", "FastAPI"),
    ("pydantic", "Pydantic"),
    ("chromadb", "ChromaDB"),
    ("pdfplumber", "PdfPlumber"),
    ("pypdf", "PyPDF"),
    ("yaml", "YAML"),
    ("pytest", "PyTest"),
]

print("🔍 Verifying installation...\n")

failed = []
for package, name in packages:
    try:
        __import__(package)
        print(f"✅ {name}")
    except ImportError:
        print(f"❌ {name}")
        failed.append(package)

if failed:
    print(f"\n❌ Failed packages: {', '.join(failed)}")
    print(f"Run: pip install {' '.join(failed)}")
    sys.exit(1)
else:
    print("\n✅ All packages installed successfully!")
    sys.exit(0)
```

Run it:
```bash
python verify_installation.py
```

---

## 📞 Still Having Issues?

1. **Check Python version:** `python --version` (needs 3.12+)
2. **Verify virtual env:** `which python` (should show venv path)
3. **Upgrade pip:** `python -m pip install --upgrade pip`
4. **Clean install:**
   ```bash
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt
   ```
5. **Check PyPI status:** https://status.python.org/

---

## 🎯 Summary

✅ **requirements.txt fixed** — All packages use compatible versions
✅ **No problematic packages** — pypdfium2 removed (not needed)
✅ **Ready to install** — Follow steps above
✅ **Tested packages** — All confirmed working

**You're ready to go!** 🚀

Next: Run `pip install -r requirements.txt` and start the application.

---

**Last Updated:** July 2026  
**Python:** 3.12+  
**Status:** ✅ Ready for Installation

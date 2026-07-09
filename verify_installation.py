#!/usr/bin/env python
"""
Verify installation of all required packages.
Run this after: pip install -r requirements.txt
"""

import sys
from importlib import import_module

# Packages to verify
PACKAGES = {
    "fastapi": "FastAPI",
    "uvicorn": "Uvicorn",
    "pydantic": "Pydantic",
    "chromadb": "ChromaDB",
    "pdfplumber": "PdfPlumber",
    "pypdf": "PyPDF",
    "yaml": "PyYAML",
    "sqlalchemy": "SQLAlchemy",
    "langchain": "LangChain",
    "httpx": "HTTPX",
    "aiofiles": "AIOFiles",
    "pytest": "PyTest",
}

print("=" * 60)
print("🔍 VERIFYING INSTALLATION")
print("=" * 60)
print()

failed = []
successful = []

for package_name, display_name in PACKAGES.items():
    try:
        module = import_module(package_name)
        version = getattr(module, "__version__", "unknown")
        print(f"✅ {display_name:<20} v{version}")
        successful.append(package_name)
    except ImportError as e:
        print(f"❌ {display_name:<20} NOT INSTALLED")
        failed.append(package_name)

print()
print("=" * 60)

if failed:
    print(f"❌ {len(failed)} package(s) failed to import:")
    print()
    for pkg in failed:
        print(f"   - {pkg}")
    print()
    print("Fix with:")
    print(f"   pip install {' '.join(failed)}")
    print()
    sys.exit(1)
else:
    print(f"✅ ALL {len(successful)} PACKAGES INSTALLED SUCCESSFULLY!")
    print()
    print("You're ready to:")
    print("   1. Run the application: python main.py")
    print("   2. Run tests: pytest tests/")
    print("   3. Access API: http://localhost:8000/docs")
    print()
    sys.exit(0)

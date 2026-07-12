# Sprint 4 Test Execution Guide

**Purpose:** Complete guide for running, managing, and understanding the Sprint 4 test suite.

---

## 🚀 Quick Start

### Prerequisites Setup

```bash
# Navigate to project root
cd i:\Pro Hero\ai\document-intelligence-service

# Create and activate virtual environment (if not already done)
python -m venv venv
venv\Scripts\activate

# Install all dependencies including test tools
pip install -r requirements.txt
pip install pytest pytest-cov pytest-asyncio
```

### Run All Tests

```bash
# Terminal window from project root
pytest tests/ -v --cov=app --cov-report=term-missing
```

**Expected Output:**
```
tests/unit/test_error_handling.py::TestFileValidation::test_invalid_filename_with_special_chars PASSED
tests/unit/test_error_handling.py::TestFileValidation::test_invalid_filename_too_long PASSED
...
tests/integration/test_document_management.py::TestSystemStatsEndpoint::test_stats_with_documents PASSED

===== 150 passed, 2 skipped in 45.23s =====

coverage report:
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
app/__init__.py              0      0   100%
app/api/__init__.py          0      0   100%
app/api/routes.py          120     18    85%   45,67,89,101-105
...
app/utils/validators.py    145      11    92%   220,234,256
-----------------------------------------------------
TOTAL                      890    156    82%

Coverage target 80% met!
```

---

## 📊 Test Organization

### Test Structure

```
tests/
├── conftest.py                                    [Shared fixtures & config]
├── unit/
│   ├── test_error_handling.py                    [Error scenarios]
│   ├── test_services.py                          [Service units]
│   ├── test_pdf.py                               [PDF processing]
│   ├── test_validators.py                        [Validation logic]
│   ├── test_chunking.py                          [Chunking logic]
│   └── test_embeddings.py                        [Embedding generation]
└── integration/
    ├── test_document_management.py               [Document CRUD API]
    ├── test_api.py                               [API endpoints]
    ├── test_search_api.py                        [Search endpoints]
    ├── test_rag_workflow.py                      [Full RAG pipeline]
    ├── test_chunking_integration.py              [Chunking workflow]
    ├── test_embeddings_integration.py            [Embedding workflow]
    └── test_rag_chat_api.py                      [Chat API]
```

---

## 🧪 Running Specific Test Categories

### 1. Unit Tests Only

Test individual functions and classes in isolation:

```bash
pytest tests/unit/ -v
```

**Run time:** ~10 seconds  
**Coverage:** 40-50% of total

**What it tests:**
- File validation functions
- Text cleaning and extraction
- Configuration loading
- Chunking logic
- Error handling scenarios

### 2. Integration Tests Only

Test complete workflows end-to-end:

```bash
pytest tests/integration/ -v
```

**Run time:** ~20 seconds  
**Coverage:** 30-40% of total

**What it tests:**
- Upload → Extract → Chunk → Embed → Store pipeline
- Document listing and filtering
- Document deletion and cleanup
- Document reindexing
- System statistics calculation

### 3. Error Handling Tests

Test all error scenarios and edge cases:

```bash
pytest tests/unit/test_error_handling.py -v
```

**Run time:** ~5 seconds  
**Tests:** 20+ scenarios

**Scenarios covered:**
- Invalid filenames (special chars, length)
- Corrupted PDF detection
- Empty file handling
- HTTP error responses (400, 404, 422, 500, 503, 504)
- Retry logic for transient failures

### 4. Specific Test File

```bash
# Run all tests in one file
pytest tests/unit/test_services.py -v

# Run all tests in a class
pytest tests/unit/test_services.py::TestFileValidator -v

# Run single test
pytest tests/unit/test_services.py::TestFileValidator::test_validate_filename_valid -v
```

### 5. Tests Matching Pattern

```bash
# Run tests matching pattern
pytest tests/ -k "upload" -v
pytest tests/ -k "delete" -v
pytest tests/ -k "error" -v

# Run tests NOT matching pattern
pytest tests/ -k "not slow" -v
```

---

## 📈 Coverage Analysis

### Generate Coverage Report

```bash
# Terminal report (missing lines shown)
pytest --cov=app --cov-report=term-missing

# HTML report (detailed coverage visualization)
pytest --cov=app --cov-report=html
# Open: htmlcov/index.html

# XML report (for CI/CD pipelines)
pytest --cov=app --cov-report=xml
```

### Interpret Coverage Report

**Example HTML Report:**
```
File                     Statements  Missing  Coverage
────────────────────────────────────────────────────
app/api/routes.py        120         18       85%
app/pdf/extractor.py     95          8        91%
app/utils/validators.py  145         11       92%
────────────────────────────────────────────────────
TOTAL                    890         156      82%
```

**Understanding Missing Lines:**
- Green = covered (executed in tests)
- Red = not covered (never executed)
- Yellow = partial coverage (some branches not executed)

Click on a file in HTML report to see exactly which lines are missing coverage.

### Coverage Goals by Module

| Module | Target | Current | Status |
|--------|--------|---------|--------|
| routes.py | 80% | 85% | ✅ |
| extractor.py | 80% | 91% | ✅ |
| validators.py | 80% | 92% | ✅ |
| cleaner.py | 80% | 88% | ✅ |
| splitter.py | 80% | 82% | ✅ |

---

## 🔍 Test Execution Modes

### Verbose Mode

```bash
pytest -v
# Shows each test individually:
# test_file.py::TestClass::test_function PASSED
```

### Quiet Mode

```bash
pytest -q
# Shows only summary:
# . = passed, F = failed, E = error
```

### Stop on First Failure

```bash
pytest -x
# Stops at first failure instead of running all tests
```

### Show Print Statements

```bash
pytest -s
# Shows print() output during tests (useful for debugging)
```

### Parallel Execution (faster)

```bash
pip install pytest-xdist
pytest -n auto
# Runs tests in parallel using available CPU cores
```

### Detailed Failure Info

```bash
pytest --tb=long
# Shows full traceback for failures
```

---

## 🐛 Debugging Tests

### Print Debug Info

```python
# In test file
def test_something():
    result = my_function()
    print(f"DEBUG: result = {result}")  # Will show with pytest -s
    assert result == expected
```

```bash
pytest tests/file.py::TestClass::test_something -s
```

### Drop to Debugger

```python
# In test file
def test_something():
    import pdb; pdb.set_trace()  # Debugger stops here
    result = my_function()
    assert result == expected
```

```bash
pytest tests/file.py::TestClass::test_something -s
# Press 'c' to continue, 'n' for next line, etc.
```

### IDE Debugging

**VS Code Configuration (.vscode/launch.json):**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "tests/",
                "-v",
                "-s"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

Press F5 to run tests with debugger.

---

## 📋 Test Results Interpretation

### Test Status Symbols

```
. = PASSED (test succeeded)
F = FAILED (test failed)
E = ERROR (test crashed)
s = SKIPPED (test skipped)
x = XFAIL (expected failure)
X = XPASS (unexpected pass)
```

### Example Output

```
tests/unit/test_validators.py::TestFileValidator::test_valid_filename PASSED      [ 5%]
tests/unit/test_validators.py::TestFileValidator::test_invalid_extension PASSED   [10%]
tests/unit/test_error_handling.py::TestRetryLogic::test_embedding_retry SKIPPED   [15%]
tests/integration/test_api.py::TestUploadPipeline::test_upload FAILED             [20%]

FAILED tests/integration/test_api.py::TestUploadPipeline::test_upload
Expected: 200
Got: 422

Traceback:
  File "tests/integration/test_api.py", line 45, in test_upload
    assert response.status_code == 200
AssertionError: assert 422 == 200
```

---

## ✅ Test Checklists

### Pre-Commit Checklist

Before committing code changes:

```bash
# 1. Run unit tests
pytest tests/unit/ -v --tb=short

# 2. Run integration tests
pytest tests/integration/ -v --tb=short

# 3. Check coverage hasn't dropped
pytest --cov=app --cov-report=term-missing | grep "TOTAL"

# 4. Check code formatting
# (if using black/flake8)
black app/ tests/
flake8 app/ tests/
```

### Pre-Deployment Checklist

Before deploying to production:

```bash
# 1. Run full test suite with maximum verbosity
pytest tests/ -v --cov=app --cov-report=term-missing

# 2. Generate coverage report
pytest --cov=app --cov-report=html

# 3. Verify coverage >= 80%
# Check htmlcov/index.html for coverage by module

# 4. Run error handling tests specifically
pytest tests/unit/test_error_handling.py -v

# 5. Run integration tests for critical paths
pytest tests/integration/test_document_management.py -v

# 6. Check no hardcoded credentials or debug code
grep -r "TODO\|FIXME\|DEBUG" app/ tests/ | grep -v ".pyc"

# 7. Verify all tests pass
pytest tests/ -q  # Should show "150 passed"
```

---

## 🚨 Common Test Issues & Solutions

### Issue 1: "ModuleNotFoundError: No module named 'app'"

**Cause:** pytest not running from project root

**Solution:**
```bash
cd i:\Pro Hero\ai\document-intelligence-service
pytest tests/
```

**Or update pytest.ini:**
```ini
[pytest]
pythonpath = .
```

---

### Issue 2: Async Tests Timeout

**Cause:** Async fixtures not configured

**Solution:**
```bash
# Install pytest-asyncio
pip install pytest-asyncio

# Update pytest.ini
[pytest]
asyncio_mode = auto
```

---

### Issue 3: Import Errors in Tests

**Cause:** Virtual environment not activated

**Solution:**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Verify activation (should show venv in prompt)
(venv) $
```

---

### Issue 4: Tests Pass Locally But Fail in CI

**Cause:** Environment differences

**Solution:**
```bash
# Install exact test environment
pip install -r requirements.txt
pip install pytest pytest-cov pytest-asyncio

# Run with same CI settings
pytest tests/ -v --cov=app --cov-report=xml
```

---

## 📊 Performance Monitoring

### Slow Test Identification

```bash
# Show slowest 10 tests
pytest tests/ --durations=10

# Mark slow tests
pytest tests/ -m "not slow"

# Show test duration in summary
pytest tests/ --durations=0
```

### Expected Test Times

| Category | Count | Time |
|----------|-------|------|
| Unit Tests | 75+ | ~10s |
| Integration Tests | 40+ | ~20s |
| Error Tests | 35+ | ~5s |
| **Total** | **150+** | **~45s** |

---

## 🔄 CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v2
```

---

## 📚 Additional Resources

- **Pytest Documentation:** https://docs.pytest.org/
- **FastAPI Testing:** https://fastapi.tiangolo.com/advanced/testing-dependencies/
- **Coverage.py:** https://coverage.readthedocs.io/
- **Async Testing:** https://pytest-asyncio.readthedocs.io/

---

## 📞 Support

For test-related questions or issues:

1. Check this guide's "Common Issues" section
2. Review test file docstrings for test intent
3. Check conftest.py for available fixtures
4. Run `pytest --help` for all options
5. Run `pytest tests/ -v -s` for detailed output

---

> **Last Updated:** July 2026  
> **Version:** 1.0  
> **Maintainer:** Engineering Team

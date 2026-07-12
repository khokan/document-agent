# 📂 Directory Structure & Setup Guide

## Issue: npm ENOENT Error

**Error**: `Could not read package.json: ENOENT`

**Cause**: Running npm from the wrong directory

---

## Correct Directory Structure

```
document-agent/
├── frontend/
│   ├── document-agent-ui/          ← You need to be HERE
│   │   ├── src/
│   │   ├── package.json            ← npm looks for this here
│   │   ├── tsconfig.json
│   │   ├── vite.config.ts
│   │   └── ...
│   ├── README.md
│   └── docs/
└── ...
```

---

## Solution: Navigate to Correct Directory

### Windows (CMD)
```cmd
cd "I:\Pro Hero\ai\document-agent\frontend\document-agent-ui"
npm install
npm run dev
```

### Windows (PowerShell)
```powershell
Set-Location -Path "I:\Pro Hero\ai\document-agent\frontend\document-agent-ui"
npm install
npm run dev
```

### macOS/Linux
```bash
cd "/path/to/document-agent/frontend/document-agent-ui"
npm install
npm run dev
```

---

## Step-by-Step Setup

### 1. Open Terminal/Command Prompt

### 2. Navigate to Correct Folder
```bash
# From current location, navigate to the UI folder
cd frontend
cd document-agent-ui
```

Or use the full path:
```bash
# Windows
cd /d "I:\Pro Hero\ai\document-agent\frontend\document-agent-ui"

# macOS/Linux
cd "/path/to/document-agent/frontend/document-agent-ui"
```

### 3. Verify You're in the Right Place
```bash
# You should see these files:
ls
# or (Windows)
dir

# Look for:
# - package.json ✓
# - src/ folder ✓
# - vite.config.ts ✓
# - tsconfig.json ✓
```

### 4. Install Dependencies
```bash
npm install
```

Or use pnpm (faster):
```bash
pnpm install
```

### 5. Start Development Server
```bash
npm run dev
```

Expected output:
```
  VITE v5.x.x

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

---

## Using VS Code Terminal (Recommended)

1. Open VS Code
2. Open the folder: `File → Open Folder`
3. Navigate to: `I:\Pro Hero\ai\document-agent\frontend\document-agent-ui`
4. Press `` Ctrl+` `` to open integrated terminal
5. Terminal automatically opens in the right directory
6. Run: `npm install && npm run dev`

---

## Common Directory Mistakes

### ❌ Wrong - Running from parent folder
```bash
cd I:\Pro Hero\ai\document-agent\frontend
npm install  # ❌ Error: Can't find package.json
```

### ✅ Correct - Run from UI folder
```bash
cd I:\Pro Hero\ai\document-agent\frontend\document-agent-ui
npm install  # ✅ Works!
```

---

## Quick Setup Script

### For Windows (create `setup.bat`)
```batch
@echo off
cd /d "I:\Pro Hero\ai\document-agent\frontend\document-agent-ui"
echo Current directory: %cd%
echo Installing dependencies...
npm install
echo Setup complete!
pause
```

Run it:
```bash
setup.bat
```

### For macOS/Linux (create `setup.sh`)
```bash
#!/bin/bash
cd "/path/to/document-agent/frontend/document-agent-ui"
echo "Current directory: $(pwd)"
echo "Installing dependencies..."
npm install
echo "Setup complete!"
```

Make executable and run:
```bash
chmod +x setup.sh
./setup.sh
```

---

## Folder Structure Guide

### Frontend Root (`frontend/`)
- Contains README and docs
- **Does NOT have package.json**
- ❌ Don't run npm here

### Frontend UI (`frontend/document-agent-ui/`)
- Contains all source code (`src/`)
- **Has package.json** ✓
- ✅ Run npm commands here

---

## Verify Correct Directory

After navigating, verify with:

```bash
# Windows
echo %cd%

# macOS/Linux
pwd
```

**Should show**: `...frontend\document-agent-ui` (Windows) or `.../frontend/document-agent-ui` (Mac/Linux)

**Should contain**:
```
✓ package.json
✓ src/
✓ vite.config.ts
✓ tsconfig.json
✓ index.html
✓ tailwind.config.js
```

If you don't see these files, you're in the wrong directory!

---

## Complete First-Time Setup

```bash
# 1. Navigate to correct directory
cd I:\Pro Hero\ai\document-agent\frontend\document-agent-ui

# 2. Verify location
dir

# 3. Install dependencies
npm install

# 4. Setup environment
copy .env.example .env.local

# 5. Start dev server
npm run dev

# 6. Open browser
# Navigate to: http://localhost:5173
```

---

## If You Still Get ENOENT Error

### Try these steps:

1. **Clear npm cache**
   ```bash
   npm cache clean --force
   ```

2. **Delete node_modules and reinstall**
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **Check npm is installed**
   ```bash
   npm --version
   node --version
   ```

4. **Verify package.json exists**
   ```bash
   # Windows
   type package.json
   
   # macOS/Linux
   cat package.json
   ```

5. **Use full path**
   ```bash
   npm --prefix "I:\Pro Hero\ai\document-agent\frontend\document-agent-ui" install
   ```

---

## Using Different Package Managers

All these work from the correct directory:

```bash
# npm (default)
npm install
npm run dev

# pnpm (faster)
pnpm install
pnpm dev

# yarn
yarn install
yarn dev

# bun (experimental)
bun install
bun run dev
```

---

## IDE Setup Tips

### VS Code
1. Open folder: `File → Open Folder`
2. Select: `I:\Pro Hero\ai\document-agent\frontend\document-agent-ui`
3. Open Terminal: `` Ctrl+` ``
4. Type: `npm install && npm run dev`

### WebStorm/IntelliJ
1. Open Project
2. Select: `I:\Pro Hero\ai\document-agent\frontend\document-agent-ui`
3. IDE auto-detects package.json
4. Run npm scripts from IDE

### Sublime Text
1. Open folder
2. Select: `I:\Pro Hero\ai\document-agent\frontend\document-agent-ui`
3. Use terminal from within editor

---

## Troubleshooting Path Issues

### Issue: "No such file or directory"
**Solution**: Use absolute path without quotes, or with quotes but proper escaping

```bash
# ✓ Without spaces in path - no quotes needed
cd C:\projects\frontend\document-agent-ui

# ✓ With spaces - use quotes
cd "I:\Pro Hero\ai\document-agent\frontend\document-agent-ui"

# ✓ Alternative - use single quotes
cd 'I:\Pro Hero\ai\document-agent\frontend\document-agent-ui'
```

### Issue: "Command not found"
**Cause**: npm not in PATH or wrong directory
**Solution**: 
1. Reinstall Node.js
2. Verify with `npm --version`
3. Make sure you're in the right directory

---

## Environment Variables Setup

Once in correct directory:

```bash
# Copy example env file
cp .env.example .env.local

# Edit if needed (optional)
# Windows
notepad .env.local

# macOS/Linux
nano .env.local
```

Default values should work fine for local development.

---

## Verification Checklist

- ✅ Current directory shows `document-agent-ui` in path
- ✅ `package.json` exists in current directory
- ✅ `src/` folder exists
- ✅ npm is installed (`npm --version` works)
- ✅ Node.js is installed (`node --version` works)
- ✅ Backend API running on localhost:8000 (optional, for features)
- ✅ Can run `npm install` without errors

---

## Quick Reference

| Task | Command |
|------|---------|
| Check current directory | `pwd` (Mac/Linux) or `cd` (Windows) |
| List files | `ls` (Mac/Linux) or `dir` (Windows) |
| Navigate | `cd path/to/folder` |
| Install dependencies | `npm install` |
| Start dev server | `npm run dev` |
| Build for production | `npm run build` |
| Type check | `npm run type-check` |
| Lint code | `npm run lint` |

---

## Summary

**Remember:**
1. Always run npm from: `frontend/document-agent-ui/`
2. NOT from: `frontend/`
3. Verify with: `ls` or `dir` to see package.json
4. Then: `npm install && npm run dev`

---

> **Last Updated**: July 2026
> **Issue**: ✅ Resolved
> **Status**: Ready to proceed

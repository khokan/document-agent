@echo off
REM Frontend Development Setup Verification Script (Windows)
REM This script verifies that all development tools and dependencies are properly configured

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo Frontend Development Environment Checker
echo ==========================================
echo.

set /a CHECKS_PASSED=0
set /a CHECKS_FAILED=0

REM Function to check if a command exists
:check_command
set "command=%1"
set "display_name=%2"
where /q %command%
if %errorlevel% equ 0 (
    echo [OK] %display_name% is installed
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] %display_name% is NOT installed
    set /a CHECKS_FAILED+=1
)
exit /b

echo 1. Checking System Dependencies
echo --------------------------------
where /q node
if %errorlevel% equ 0 (
    echo [OK] Node.js is installed
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] Node.js is NOT installed
    set /a CHECKS_FAILED+=1
)

where /q npm
if %errorlevel% equ 0 (
    echo [OK] NPM is installed
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] NPM is NOT installed
    set /a CHECKS_FAILED+=1
)

where /q git
if %errorlevel% equ 0 (
    echo [OK] Git is installed
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] Git is NOT installed
    set /a CHECKS_FAILED+=1
)
echo.

echo 2. Checking Node Version
echo --------------------------------
for /f "tokens=*" %%i in ('node --version 2^>nul') do set NODE_VERSION=%%i
if defined NODE_VERSION (
    echo Node version: %NODE_VERSION%
) else (
    echo Could not determine Node version
)
echo.

echo 3. Checking NPM Version
echo --------------------------------
for /f "tokens=*" %%i in ('npm --version 2^>nul') do set NPM_VERSION=%%i
if defined NPM_VERSION (
    echo NPM version: %NPM_VERSION%
) else (
    echo Could not determine NPM version
)
echo.

echo 4. Checking Frontend Directory Structure
echo --------------------------------
if exist "src" (
    echo [OK] src directory exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] src directory NOT found
    set /a CHECKS_FAILED+=1
)

if exist "src\types" (
    echo [OK] src/types directory exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] src/types directory NOT found
    set /a CHECKS_FAILED+=1
)

if exist "src\components" (
    echo [OK] src/components directory exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] src/components directory NOT found
    set /a CHECKS_FAILED+=1
)

if exist "src\pages" (
    echo [OK] src/pages directory exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] src/pages directory NOT found
    set /a CHECKS_FAILED+=1
)

if exist "src\hooks" (
    echo [OK] src/hooks directory exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] src/hooks directory NOT found
    set /a CHECKS_FAILED+=1
)

if exist "src\stores" (
    echo [OK] src/stores directory exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] src/stores directory NOT found
    set /a CHECKS_FAILED+=1
)

if exist ".vscode" (
    echo [OK] .vscode directory exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] .vscode directory NOT found
    set /a CHECKS_FAILED+=1
)
echo.

echo 5. Checking Configuration Files
echo --------------------------------
if exist "package.json" (
    echo [OK] package.json exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] package.json NOT found
    set /a CHECKS_FAILED+=1
)

if exist "tsconfig.json" (
    echo [OK] tsconfig.json exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] tsconfig.json NOT found
    set /a CHECKS_FAILED+=1
)

if exist "vite.config.ts" (
    echo [OK] vite.config.ts exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] vite.config.ts NOT found
    set /a CHECKS_FAILED+=1
)

if exist "tailwind.config.js" (
    echo [OK] tailwind.config.js exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] tailwind.config.js NOT found
    set /a CHECKS_FAILED+=1
)

if exist ".eslintrc.json" (
    echo [OK] .eslintrc.json exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] .eslintrc.json NOT found
    set /a CHECKS_FAILED+=1
)
echo.

echo 6. Checking VS Code Configuration
echo --------------------------------
if exist ".vscode\launch.json" (
    echo [OK] .vscode/launch.json exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] .vscode/launch.json NOT found
    set /a CHECKS_FAILED+=1
)

if exist ".vscode\tasks.json" (
    echo [OK] .vscode/tasks.json exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] .vscode/tasks.json NOT found
    set /a CHECKS_FAILED+=1
)

if exist ".vscode\settings.json" (
    echo [OK] .vscode/settings.json exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] .vscode/settings.json NOT found
    set /a CHECKS_FAILED+=1
)
echo.

echo 7. Checking Essential Source Files
echo --------------------------------
if exist "src\main.tsx" (
    echo [OK] src/main.tsx exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] src/main.tsx NOT found
    set /a CHECKS_FAILED+=1
)

if exist "src\App.tsx" (
    echo [OK] src/App.tsx exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] src/App.tsx NOT found
    set /a CHECKS_FAILED+=1
)

if exist "index.html" (
    echo [OK] index.html exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] index.html NOT found
    set /a CHECKS_FAILED+=1
)
echo.

echo 8. Checking Node Modules
echo --------------------------------
if exist "node_modules" (
    echo [OK] node_modules directory exists
    set /a CHECKS_PASSED+=1
    
    if exist "node_modules\react" (
        echo [OK] React is installed
        set /a CHECKS_PASSED+=1
    ) else (
        echo [FAIL] React is NOT installed
        set /a CHECKS_FAILED+=1
    )
    
    if exist "node_modules\typescript" (
        echo [OK] TypeScript is installed
        set /a CHECKS_PASSED+=1
    ) else (
        echo [FAIL] TypeScript is NOT installed
        set /a CHECKS_FAILED+=1
    )
    
    if exist "node_modules\vite" (
        echo [OK] Vite is installed
        set /a CHECKS_PASSED+=1
    ) else (
        echo [FAIL] Vite is NOT installed
        set /a CHECKS_FAILED+=1
    )
) else (
    echo [FAIL] node_modules directory NOT found
    echo        Run 'npm install' to install dependencies
    set /a CHECKS_FAILED+=1
)
echo.

echo ==========================================
echo Summary
echo ==========================================
echo Checks Passed: %CHECKS_PASSED%
echo Checks Failed: %CHECKS_FAILED%
echo.

if %CHECKS_FAILED% equ 0 (
    echo [SUCCESS] All checks passed! Your environment is ready.
    echo.
    echo Next steps:
    echo   1. Run: npm run dev
    echo   2. Open: http://localhost:5173
    echo   3. Press F5 to start debugging
) else (
    echo [WARNING] Some checks failed. Please address the issues above.
    echo.
    echo Common fixes:
    echo   - If node_modules is missing: run 'npm install'
    echo   - If Node.js is not installed: download from https://nodejs.org/
    echo   - If TypeScript errors occur: run 'npm run type-check'
)

pause

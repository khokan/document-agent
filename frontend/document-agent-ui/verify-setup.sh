#!/bin/bash

# Frontend Development Setup Verification Script
# This script verifies that all development tools and dependencies are properly configured

echo "=========================================="
echo "Frontend Development Environment Checker"
echo "=========================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Initialize counters
CHECKS_PASSED=0
CHECKS_FAILED=0

# Function to check if a command exists
check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 is installed"
        CHECKS_PASSED=$((CHECKS_PASSED+1))
        return 0
    else
        echo -e "${RED}✗${NC} $1 is NOT installed"
        CHECKS_FAILED=$((CHECKS_FAILED+1))
        return 1
    fi
}

# Function to check if a file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        CHECKS_PASSED=$((CHECKS_PASSED+1))
        return 0
    else
        echo -e "${RED}✗${NC} $1 NOT found"
        CHECKS_FAILED=$((CHECKS_FAILED+1))
        return 1
    fi
}

# Function to check if a directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 directory exists"
        CHECKS_PASSED=$((CHECKS_PASSED+1))
        return 0
    else
        echo -e "${RED}✗${NC} $1 directory NOT found"
        CHECKS_FAILED=$((CHECKS_FAILED+1))
        return 1
    fi
}

echo "1. Checking System Dependencies"
echo "-------------------------------"
check_command "node"
check_command "npm"
check_command "git"
echo ""

echo "2. Checking Node Version"
echo "-------------------------------"
NODE_VERSION=$(node --version)
echo "Node version: $NODE_VERSION"
echo ""

echo "3. Checking NPM Version"
echo "-------------------------------"
NPM_VERSION=$(npm --version)
echo "NPM version: $NPM_VERSION"
echo ""

echo "4. Checking Frontend Directory Structure"
echo "-------------------------------"
check_dir "src"
check_dir "src/types"
check_dir "src/components"
check_dir "src/pages"
check_dir "src/hooks"
check_dir "src/stores"
check_dir "src/services"
check_dir "src/utils"
check_dir "public"
check_dir ".vscode"
echo ""

echo "5. Checking Configuration Files"
echo "-------------------------------"
check_file "package.json"
check_file "tsconfig.json"
check_file "vite.config.ts"
check_file "tailwind.config.js"
check_file "postcss.config.js"
check_file ".eslintrc.json"
check_file ".prettierrc"
check_file ".env.example"
echo ""

echo "6. Checking VS Code Configuration"
echo "-------------------------------"
check_file ".vscode/launch.json"
check_file ".vscode/tasks.json"
check_file ".vscode/settings.json"
check_file ".vscode/extensions.json"
echo ""

echo "7. Checking Essential Source Files"
echo "-------------------------------"
check_file "src/main.tsx"
check_file "src/App.tsx"
check_file "src/index.css"
check_file "index.html"
echo ""

echo "8. Checking Node Modules"
echo "-------------------------------"
if [ -d "node_modules" ]; then
    echo -e "${GREEN}✓${NC} node_modules directory exists"
    CHECKS_PASSED=$((CHECKS_PASSED+1))
    
    # Check for critical dependencies
    if [ -d "node_modules/react" ]; then
        echo -e "${GREEN}✓${NC} React is installed"
        CHECKS_PASSED=$((CHECKS_PASSED+1))
    else
        echo -e "${RED}✗${NC} React is NOT installed"
        CHECKS_FAILED=$((CHECKS_FAILED+1))
    fi
    
    if [ -d "node_modules/typescript" ]; then
        echo -e "${GREEN}✓${NC} TypeScript is installed"
        CHECKS_PASSED=$((CHECKS_PASSED+1))
    else
        echo -e "${RED}✗${NC} TypeScript is NOT installed"
        CHECKS_FAILED=$((CHECKS_FAILED+1))
    fi
    
    if [ -d "node_modules/vite" ]; then
        echo -e "${GREEN}✓${NC} Vite is installed"
        CHECKS_PASSED=$((CHECKS_PASSED+1))
    else
        echo -e "${RED}✗${NC} Vite is NOT installed"
        CHECKS_FAILED=$((CHECKS_FAILED+1))
    fi
else
    echo -e "${RED}✗${NC} node_modules directory NOT found"
    echo -e "${YELLOW}  Run 'npm install' to install dependencies${NC}"
    CHECKS_FAILED=$((CHECKS_FAILED+1))
fi
echo ""

echo "9. Checking NPM Scripts"
echo "-------------------------------"
if grep -q '"dev"' package.json; then
    echo -e "${GREEN}✓${NC} dev script is configured"
    CHECKS_PASSED=$((CHECKS_PASSED+1))
else
    echo -e "${RED}✗${NC} dev script NOT found"
    CHECKS_FAILED=$((CHECKS_FAILED+1))
fi

if grep -q '"build"' package.json; then
    echo -e "${GREEN}✓${NC} build script is configured"
    CHECKS_PASSED=$((CHECKS_PASSED+1))
else
    echo -e "${RED}✗${NC} build script NOT found"
    CHECKS_FAILED=$((CHECKS_FAILED+1))
fi

if grep -q '"type-check"' package.json; then
    echo -e "${GREEN}✓${NC} type-check script is configured"
    CHECKS_PASSED=$((CHECKS_PASSED+1))
else
    echo -e "${RED}✗${NC} type-check script NOT found"
    CHECKS_FAILED=$((CHECKS_FAILED+1))
fi

if grep -q '"lint"' package.json; then
    echo -e "${GREEN}✓${NC} lint script is configured"
    CHECKS_PASSED=$((CHECKS_PASSED+1))
else
    echo -e "${RED}✗${NC} lint script NOT found"
    CHECKS_FAILED=$((CHECKS_FAILED+1))
fi
echo ""

echo "=========================================="
echo "Summary"
echo "=========================================="
echo -e "Checks Passed: ${GREEN}$CHECKS_PASSED${NC}"
echo -e "Checks Failed: ${RED}$CHECKS_FAILED${NC}"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Your environment is ready.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Run: npm run dev"
    echo "  2. Open: http://localhost:5173"
    echo "  3. Press F5 to start debugging"
else
    echo -e "${YELLOW}⚠ Some checks failed. Please address the issues above.${NC}"
    echo ""
    echo "Common fixes:"
    echo "  • If node_modules is missing: run 'npm install'"
    echo "  • If Node.js is not installed: download from https://nodejs.org/"
    echo "  • If TypeScript errors occur: run 'npm run type-check'"
fi

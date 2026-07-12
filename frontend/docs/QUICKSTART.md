## 🚀 Frontend Quick Start & Developer Guide
### PDF Knowledge Assistant — React UI

> **Document Version:** 1.0 | **Last Updated:** July 2026

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
3. [Development Environment](#development-environment)
4. [Running the Application](#running-the-application)
5. [Available Commands](#available-commands)
6. [Project Structure Overview](#project-structure-overview)
7. [Development Guidelines](#development-guidelines)
8. [Common Tasks](#common-tasks)
9. [Troubleshooting](#troubleshooting)
10. [Next Steps](#next-steps)

---

## Prerequisites

### System Requirements
- **Node.js**: v18.16.0 or higher
- **npm**: v9.0.0 or higher (or use pnpm for faster package management)
- **Git**: v2.37.0 or higher
- **Operating System**: Windows, macOS, or Linux

### Verify Installation
```bash
node --version      # Should be >= v18.16.0
npm --version       # Should be >= v9.0.0
git --version       # Should be >= v2.37.0
```

### Backend Requirements
The frontend requires the backend API running at `http://localhost:8000`
See the main backend `README.md` for setup instructions.

---

## Project Setup

### 1️⃣ Clone Repository (if not already done)

```bash
git clone <repository-url>
cd document-intelligence-service/frontend
```

### 2️⃣ Install Dependencies

**Using pnpm (recommended for speed):**
```bash
npm install -g pnpm  # Install pnpm globally if not already installed
pnpm install         # Fast, efficient installation
```

**Or using npm:**
```bash
npm install
```

### 3️⃣ Setup Environment Variables

```bash
# Copy example file
cp .env.example .env.local

# Edit .env.local with your settings
# VITE_API_URL=http://localhost:8000
# VITE_LOG_LEVEL=debug
# VITE_ENABLE_SENTRY=false
```

### 4️⃣ Verify Installation

```bash
pnpm --version          # Should show pnpm version
pnpm list --depth=0     # List top-level dependencies
npm run build           # Test that build works
```

---

## Development Environment

### Recommended VSCode Extensions

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "dsznajder.es7-react-js-snippets",
    "ms-playwright.playwright",
    "vitest.explorer"
  ]
}
```

### VSCode Settings (`.vscode/settings.json`)

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ],
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

### Chrome DevTools Extensions

- **React Developer Tools**: Debug React components
- **Redux DevTools**: Monitor state changes (if using Redux)
- **Sentry**: Error tracking (when enabled)

---

## Running the Application

### Start Development Server

```bash
# Terminal 1: Start backend (from root directory)
cd .. && pnpm dev:backend

# Terminal 2: Start frontend dev server
pnpm dev
```

This will start:
- Frontend: `http://localhost:5173` (Vite dev server)
- Backend: `http://localhost:8000` (FastAPI)

### Open in Browser

1. Navigate to `http://localhost:5173`
2. If redirected to home page, you're connected!
3. Open DevTools (F12) → Console tab
4. Look for initialization logs like: `[14:30:22] [INFO] Application started`

### First Time Setup Checklist

- [ ] Frontend running on port 5173
- [ ] Backend running on port 8000
- [ ] No CORS errors in console
- [ ] API health check passing (`GET http://localhost:8000/health`)
- [ ] Dashboard loading and showing stats
- [ ] Can navigate between pages
- [ ] No TypeScript errors in editor

---

## Available Commands

### Development

```bash
# Start dev server (hot reload)
pnpm dev

# Dev server with frontend only (requires manual backend)
pnpm dev:frontend

# Start dev server with UI for debugging
pnpm dev:ui
```

### Building

```bash
# Build for production
pnpm build

# Preview production build locally
pnpm preview

# Analyze bundle size
pnpm build --analyze
```

### Testing

```bash
# Run all tests (unit + integration)
pnpm test

# Run tests in watch mode
pnpm test:watch

# Run tests with UI (visual test runner)
pnpm test:ui

# Generate coverage report
pnpm test:coverage

# Run E2E tests with Playwright
pnpm test:e2e

# E2E tests with UI
pnpm test:e2e:ui
```

### Code Quality

```bash
# Lint with ESLint
pnpm lint

# Fix linting errors automatically
pnpm lint:fix

# Format code with Prettier
pnpm format

# Format check without changes
pnpm format:check

# Full type checking
pnpm type-check

# All checks (lint, format, type-check)
pnpm check
```

### Documentation

```bash
# Start Storybook (component library)
pnpm storybook

# Build Storybook static site
pnpm storybook:build
```

### Utility

```bash
# Clean build artifacts
pnpm clean

# Reinstall dependencies
pnpm reinstall

# Update dependencies
pnpm update
```

---

## Project Structure Overview

### Root Level
```
frontend/
├── src/                      # Source code (✨ Edit here)
│   ├── components/           # React components
│   ├── pages/                # Page components
│   ├── hooks/                # Custom hooks
│   ├── stores/               # Zustand stores
│   ├── services/             # API services
│   ├── utils/                # Utilities
│   ├── types/                # TypeScript types
│   ├── App.tsx               # Root component
│   └── main.tsx              # Entry point
├── public/                   # Static files
├── tests/                    # Test files
├── .vscode/                  # VSCode settings
├── .env.example              # Environment template
├── vite.config.ts            # Vite configuration
├── tsconfig.json             # TypeScript config
├── eslintrc.json             # ESLint config
├── tailwind.config.js        # TailwindCSS config
├── package.json              # Dependencies
└── README.md                 # This file
```

### src/ Subdirectories

```
src/
├── components/
│   ├── ui/                   # Base UI components (from Shadcn)
│   ├── layout/               # Layout components
│   ├── documents/            # Document management
│   ├── search/               # Search interface
│   ├── dashboard/            # Dashboard widgets
│   └── common/               # Shared components
├── pages/
│   ├── Dashboard.tsx
│   ├── DocumentsPage.tsx
│   ├── SearchPage.tsx
│   └── NotFound.tsx
├── hooks/
│   ├── useDocuments.ts
│   ├── useSearch.ts
│   └── useApi.ts
├── stores/
│   ├── documentStore.ts
│   ├── searchStore.ts
│   └── uiStore.ts
├── services/
│   ├── api/
│   │   ├── client.ts         # Axios instance
│   │   ├── documents.ts      # Document API
│   │   ├── search.ts         # Search API
│   │   └── health.ts         # Health API
│   └── mock/
│       └── mockData.ts
├── types/
│   ├── api.ts
│   ├── documents.ts
│   ├── search.ts
│   └── common.ts
├── utils/
│   ├── logger.ts
│   ├── errorHandler.ts
│   ├── validators.ts
│   ├── formatters.ts
│   └── constants.ts
├── config/
│   └── api.config.ts
├── App.tsx
├── main.tsx
└── index.css                 # Global styles + Tailwind
```

---

## Development Guidelines

### Code Style

**File Naming:**
```
Components:     PascalCase.tsx       (e.g., DocumentCard.tsx)
Hooks:          useCamelCase.ts      (e.g., useDocuments.ts)
Services:       camelCase.ts         (e.g., documentsApi.ts)
Utilities:      camelCase.ts         (e.g., errorHandler.ts)
Types:          camelCase.ts         (e.g., api.ts)
Stores:         camelCaseStore.ts    (e.g., documentStore.ts)
Tests:          *.test.ts            (e.g., Button.test.ts)
```

### Component Template

```typescript
// src/components/MyComponent.tsx
import React from 'react'
import logger from '@/utils/logger'

interface MyComponentProps {
  title: string
  onClick?: () => void
}

/**
 * MyComponent - Description of what this component does
 * 
 * @param props - Component props
 * @returns JSX element
 */
const MyComponent: React.FC<MyComponentProps> = ({ title, onClick }) => {
  logger.debug('[MyComponent] Rendering')

  return (
    <div className="p-4">
      <h1>{title}</h1>
    </div>
  )
}

export default MyComponent
```

### Hook Template

```typescript
// src/hooks/useMyHook.ts
import { useEffect, useState } from 'react'
import logger from '@/utils/logger'

/**
 * useMyHook - Description
 * @returns Hook return value
 */
export const useMyHook = () => {
  const [state, setState] = useState(null)

  useEffect(() => {
    logger.debug('[useMyHook] Effect running')
    // Hook logic
  }, [])

  return { state }
}
```

### Error Handling Pattern

```typescript
const handleAction = async () => {
  try {
    // Action logic
    logger.info('[Component] Action started')
    const result = await api.call()
    logger.info('[Component] Action completed')
  } catch (error) {
    const appError = handleError(error)
    setError(appError.message)
    logger.error('[Component] Error:', appError)
    showToast.error(appError.message)
  }
}
```

---

## Common Tasks

### Adding a New Component

1. Create file: `src/components/MyComponent.tsx`
2. Create test: `src/components/MyComponent.test.tsx`
3. Export from `src/components/index.ts`
4. Use in pages or other components

```typescript
// src/components/MyComponent.tsx
const MyComponent: React.FC = () => {
  return <div>My Component</div>
}
export default MyComponent

// src/components/index.ts
export { default as MyComponent } from './MyComponent'

// Usage in Page
import { MyComponent } from '@/components'
```

### Adding a New API Endpoint

1. Create service: `src/services/api/newFeature.ts`
2. Add types: `src/types/newFeature.ts`
3. Create hook: `src/hooks/useNewFeature.ts`
4. Use in components

```typescript
// src/services/api/newFeature.ts
export const newFeatureApi = {
  async fetch() {
    const response = await apiClient.get('/new-endpoint')
    return response.data
  },
}

// src/types/newFeature.ts
export interface NewFeature {
  id: string
  name: string
}

// src/hooks/useNewFeature.ts
export const useNewFeature = () => {
  const [data, setData] = useState<NewFeature[]>([])

  const fetch = async () => {
    try {
      const result = await newFeatureApi.fetch()
      setData(result)
    } catch (error) {
      logger.error('[useNewFeature] Error:', error)
    }
  }

  return { data, fetch }
}
```

### Adding a New Page

1. Create page: `src/pages/MyPage.tsx`
2. Add route: Update `src/App.tsx`
3. Add navigation: Update `src/components/layout/Sidebar.tsx`

```typescript
// src/pages/MyPage.tsx
const MyPage: React.FC = () => {
  return <div>My Page</div>
}
export default MyPage

// src/App.tsx
import MyPage from '@/pages/MyPage'

<Route path="/my-page" element={<MyPage />} />

// src/components/layout/Sidebar.tsx
<Link to="/my-page">My Page</Link>
```

### Adding Tests

```typescript
// src/components/Button.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Button from './Button'

describe('Button', () => {
  it('renders with label', () => {
    render(<Button label="Click me" />)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick handler', async () => {
    const onClick = vi.fn()
    render(<Button label="Click" onClick={onClick} />)
    await userEvent.click(screen.getByText('Click'))
    expect(onClick).toHaveBeenCalled()
  })
})
```

### Debugging in VSCode

1. Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Launch Chrome",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/src",
      "sourceMaps": true
    }
  ]
}
```

2. Add breakpoints in code
3. Press F5 to start debugging

---

## Troubleshooting

### Issue: Port 5173 Already in Use

```bash
# Find process using port 5173
lsof -i :5173           # macOS/Linux
netstat -ano | grep 5173  # Windows

# Kill process (Windows)
taskkill /PID <PID> /F

# Or use different port
pnpm dev --port 5174
```

### Issue: CORS Error from Backend

```
Access to XMLHttpRequest at 'http://localhost:8000/...' 
from origin 'http://localhost:5173' has been blocked by CORS policy
```

**Solution:**
1. Ensure backend CORS is configured
2. Check `VITE_API_URL` in `.env.local`
3. Verify backend is running on correct port

```bash
# Check backend health
curl http://localhost:8000/health
```

### Issue: Module Not Found

```bash
# Clear node_modules and reinstall
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### Issue: TypeScript Errors

```bash
# Run type checker
pnpm type-check

# Reload VSCode (Cmd+Shift+P → "TypeScript: Reload Projects")
```

### Issue: Hot Reload Not Working

```bash
# Restart dev server
pnpm dev

# If persists, clear Vite cache
rm -rf .vite
pnpm dev
```

### Issue: Tests Failing

```bash
# Run with verbose output
pnpm test -- --reporter=verbose

# Run specific test
pnpm test Button.test.ts

# Run with debugging
node --inspect-brk ./node_modules/vitest/vitest.mjs
```

---

## Next Steps

### After Initial Setup

1. **Run Tests**: `pnpm test` - Ensure all tests pass
2. **Check Coverage**: `pnpm test:coverage` - Aim for >80%
3. **Lint Code**: `pnpm lint` - Fix any style issues
4. **Try Features**: Navigate to each page and test
5. **Read Documentation**: Review PRD.md and ARCHITECTURE.md

### Start Development

1. **Pick a Task**: Choose from IMPLEMENTATION_PLAN.md
2. **Create Branch**: `git checkout -b feature/task-name`
3. **Implement Feature**: Follow code guidelines
4. **Write Tests**: Ensure >80% coverage
5. **Create PR**: Push and request review

### Useful Resources

- **React Docs**: https://react.dev
- **TypeScript Handbook**: https://www.typescriptlang.org/docs
- **TailwindCSS**: https://tailwindcss.com/docs
- **Zustand**: https://github.com/pmndrs/zustand
- **Vitest**: https://vitest.dev
- **Playwright**: https://playwright.dev

### Getting Help

1. **Check Logs**: Open DevTools Console (F12)
2. **Review Errors**: Look at error messages carefully
3. **Search Documentation**: Check PRD.md, ARCHITECTURE.md
4. **Debug with VSCode**: Use debugger (F5) to step through code
5. **Check Git Log**: See what others have done

---

## 📞 Support

For issues or questions:
1. Check this guide's Troubleshooting section
2. Review project documentation
3. Check backend logs and health
4. Review recent git commits to understand changes
5. Ask team members or create an issue

---

## ✅ Quick Verification Checklist

- [ ] Node.js v18+ installed
- [ ] Project dependencies installed (`pnpm list --depth=0`)
- [ ] `.env.local` configured with API URL
- [ ] Backend running on `http://localhost:8000`
- [ ] Frontend running on `http://localhost:5173`
- [ ] Dashboard loads without errors
- [ ] API calls working (check Network tab)
- [ ] Tests passing (`pnpm test`)
- [ ] No linting errors (`pnpm lint`)
- [ ] TypeScript passing (`pnpm type-check`)

---

> **Document Version:** 1.0 | **Last Updated:** July 2026
> **For:** Frontend Developers & Contributors

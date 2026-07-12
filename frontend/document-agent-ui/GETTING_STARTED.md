# Frontend Development - Getting Started Guide

Welcome to the Document Agent Frontend development environment! This guide will help you set up and start developing.

## Table of Contents

1. [Quick Start (5 minutes)](#quick-start)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Development Workflow](#development-workflow)
5. [Debugging](#debugging)
6. [Common Tasks](#common-tasks)
7. [Troubleshooting](#troubleshooting)
8. [Additional Resources](#additional-resources)

## Quick Start

### For Experienced Developers

```bash
# 1. Navigate to the frontend directory
cd frontend/document-agent-ui

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev

# 4. Open in browser
# Visit http://localhost:5173

# 5. Open the debugger in VS Code
# Press F5 and select "Frontend - Chrome"
```

That's it! You're ready to start developing.

---

## System Requirements

### Minimum Requirements
- **Node.js** v18.0.0 or higher
- **npm** v9.0.0 or higher
- **Git** v2.30.0 or higher
- **Visual Studio Code** (recommended, but not required)

### Recommended
- **Node.js** v20 LTS (long-term support)
- **npm** v10+
- **VS Code** with the following extensions:
  - ESLint
  - Prettier
  - Debugger for Chrome
  - Tailwind CSS IntelliSense

### Optional but Recommended
- React DevTools browser extension
- Redux DevTools (if using Redux)

---

## Installation

### Step 1: Verify System Requirements

Check that Node.js and npm are installed:

```bash
node --version      # Should be v18+
npm --version       # Should be v9+
```

If not installed, download from [nodejs.org](https://nodejs.org/)

### Step 2: Navigate to Frontend Directory

```bash
cd frontend/document-agent-ui
```

### Step 3: Verify Environment (Windows)

Run the verification script to ensure everything is set up correctly:

```bash
# Windows
verify-setup.bat

# macOS/Linux
bash verify-setup.sh
```

This script checks:
- ✓ Node.js and npm installation
- ✓ Directory structure
- ✓ Configuration files
- ✓ Dependencies installation status

### Step 4: Install Dependencies

```bash
npm install
```

This installs all required packages:
- React and React DOM
- TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- ESLint and Prettier (code quality)
- And more...

### Step 5: Create Environment File

Copy the example environment file:

```bash
# Windows
copy .env.example .env.local

# macOS/Linux
cp .env.example .env.local
```

Edit `.env.local` to set your API endpoint:

```env
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
VITE_DEBUG=false
```

---

## Development Workflow

### Starting the Development Server

```bash
npm run dev
```

This starts the Vite development server at `http://localhost:5173` with:
- Hot Module Replacement (HMR) - instant code updates
- TypeScript compilation
- Source maps for debugging
- Fast build times

Output:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  press h to show help
```

Open the URL in your browser to see the app.

### Project Structure

```
src/
├── main.tsx              # Application entry point
├── App.tsx               # Main App component with routing
├── index.css             # Global styles
├── types/                # TypeScript type definitions
│   ├── api.ts           # API types
│   ├── documents.ts     # Document types
│   ├── search.ts        # Search types
│   └── common.ts        # Common types
├── components/          # Reusable React components
│   ├── ui/             # UI components (Button, Card, etc.)
│   └── layout/         # Layout components (Header, Sidebar, etc.)
├── pages/               # Page components
│   ├── Dashboard.tsx
│   ├── Documents.tsx
│   ├── Search.tsx
│   └── NotFound.tsx
├── hooks/               # Custom React hooks
│   ├── useDocuments.ts
│   ├── useSearch.ts
│   └── useNotification.ts
├── stores/              # State management (Zustand-like)
│   ├── documentStore.ts
│   ├── searchStore.ts
│   └── uiStore.ts
├── services/            # API services
│   └── api/
│       ├── client.ts
│       ├── documents.ts
│       ├── health.ts
│       └── index.ts
├── utils/               # Utility functions
│   ├── logger.ts
│   ├── errorHandler.ts
│   ├── validators.ts
│   └── formatters.ts
└── config/              # Configuration
    └── constants.ts
```

### Common Development Tasks

#### 1. Create a New Component

```bash
# Create component directory
mkdir src/components/MyComponent

# Create component file
cat > src/components/MyComponent/MyComponent.tsx << 'EOF'
import React from 'react';

export interface MyComponentProps {
  title: string;
}

export const MyComponent: React.FC<MyComponentProps> = ({ title }) => {
  return <div>{title}</div>;
};
EOF

# Create index for easier imports
cat > src/components/MyComponent/index.ts << 'EOF'
export { MyComponent } from './MyComponent';
EOF
```

Then import and use:
```typescript
import { MyComponent } from '@/components/MyComponent';

function App() {
  return <MyComponent title="Hello" />;
}
```

#### 2. Add a New Page

Create a new file in `src/pages/`:
```typescript
import React from 'react';

export const NewPage: React.FC = () => {
  return (
    <div>
      <h1>New Page</h1>
    </div>
  );
};
```

Add route in `src/App.tsx`:
```typescript
import { NewPage } from '@/pages/NewPage';

// In the routes array
{
  path: '/new-page',
  component: NewPage
}
```

#### 3. Use Styling with Tailwind CSS

```typescript
export const StyledComponent: React.FC = () => {
  return (
    <div className="bg-blue-500 text-white p-4 rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold mb-2">Title</h1>
      <p className="text-sm">Description</p>
    </div>
  );
};
```

#### 4. Fetch Data from API

```typescript
import { useEffect, useState } from 'react';
import { apiClient } from '@/services/api';

export const DataComponent: React.FC = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await apiClient.get('/documents');
        setData(response.data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Unknown error'));
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return <div>{JSON.stringify(data)}</div>;
};
```

#### 5. Use Custom Hooks

```typescript
import { useDocuments } from '@/hooks/useDocuments';

export const DocumentsPage: React.FC = () => {
  const {
    documents,
    loading,
    error,
    fetchDocuments,
    uploadDocument,
    deleteDocument
  } = useDocuments();

  useEffect(() => {
    fetchDocuments();
  }, []);

  return (
    <div>
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error.message}</p>}
      {documents.map(doc => (
        <div key={doc.id}>{doc.name}</div>
      ))}
    </div>
  );
};
```

#### 6. Manage State with Stores

```typescript
import { useDocumentStore } from '@/stores/documentStore';

export const StateExample: React.FC = () => {
  const documents = useDocumentStore(state => state.documents);
  const setDocuments = useDocumentStore(state => state.setDocuments);

  return (
    <div>
      <h1>Documents: {documents.length}</h1>
      <button onClick={() => setDocuments([...documents, {}])}>
        Add Document
      </button>
    </div>
  );
};
```

---

## Debugging

### VS Code Debugging Setup

1. **Install Required Extensions** (if not already installed):
   - "Debugger for Chrome" by Microsoft
   - "ESLint" by Dirk Baeumer
   - "Prettier" by Esben Petersen

2. **Start Debugging**:
   - Press `Ctrl+Shift+D` to open the Debug view
   - Select "Frontend - Chrome" from the dropdown
   - Press `F5` to start debugging

3. **Set Breakpoints**:
   - Click on line numbers to place breakpoints
   - Red dots indicate active breakpoints

4. **Debug Controls**:
   - `F5` - Continue/Resume
   - `F10` - Step Over
   - `F11` - Step Into
   - `Shift+F11` - Step Out
   - `Ctrl+Shift+F5` - Restart

For detailed debugging information, see [DEBUGGING_GUIDE.md](./docs/DEBUGGING_GUIDE.md).

---

## Common Tasks

### Type Checking

Verify TypeScript types without building:

```bash
npm run type-check
```

### Linting

Check code quality:

```bash
npm run lint

# Fix fixable issues automatically
npm run lint:fix
```

### Formatting Code

Format code with Prettier:

```bash
npm run format
```

### Build for Production

Create an optimized production build:

```bash
npm run build
```

Output goes to `dist/` directory.

### Preview Production Build Locally

```bash
npm run preview
```

This serves the production build at `http://localhost:4173` for testing.

### Install New Packages

Add a new dependency:

```bash
npm install package-name

# Or for dev dependencies
npm install --save-dev package-name-dev
```

### Update Dependencies

Check for outdated packages:

```bash
npm outdated
```

Update all packages:

```bash
npm update
```

---

## Troubleshooting

### Issue: "Port 5173 is already in use"

**Solution:**
```bash
# Kill process on Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Kill process on macOS/Linux
lsof -i :5173
kill -9 <PID>

# Or use a different port
npm run dev -- --port 5174
```

### Issue: "Module not found" or "Cannot find module"

**Solution:**
1. Check the import path is correct
2. Verify the file exists in the location
3. Ensure file has proper extension (.ts, .tsx, .js, .jsx)
4. Try restarting the dev server: `npm run dev`

### Issue: TypeScript errors but code runs fine

**Solution:**
```bash
# Type check everything
npm run type-check

# Try clearing cache
rm -rf node_modules/.vite
npm run dev
```

### Issue: VSCode not recognizing path aliases like `@/`

**Solution:**
1. Check `tsconfig.json` has path mappings configured
2. Restart VS Code
3. Check `vite.config.ts` has corresponding alias configuration

### Issue: Hot Module Replacement (HMR) not working

**Solution:**
1. Check dev server is running: `npm run dev`
2. Verify port matches in browser (should be 5173)
3. Check for TypeScript compilation errors: `npm run type-check`
4. Restart dev server: stop and run `npm run dev` again

### Issue: Debugger not connecting

**Solution:**
1. Ensure dev server is running: `npm run dev`
2. Check port 5173 is accessible
3. Try the "Attach Chrome" configuration instead
4. Manually launch Chrome with: `chrome.exe --remote-debugging-port=9222`

### Issue: Dependencies installation failed

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and lock file
rm -rf node_modules
rm package-lock.json  # or package-lock.json on Windows

# Reinstall
npm install
```

### Issue: "ENOENT: no such file or directory"

**Solution:**
Make sure you're in the correct directory:
```bash
# Check current directory
pwd  # macOS/Linux
cd   # Windows

# Navigate to frontend directory
cd frontend/document-agent-ui

# Then run commands
npm run dev
```

---

## Additional Resources

### Documentation
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [ESLint Rules](https://eslint.org/docs/rules/)

### Project Documentation
- [Build & Deployment Guide](./docs/BUILD_DEPLOYMENT_GUIDE.md)
- [Debugging Guide](./docs/DEBUGGING_GUIDE.md)
- [Code Generation Summary](./docs/CODE_GENERATION_SUMMARY.md)
- [Directory Setup Guide](./docs/DIRECTORY_AND_SETUP.md)

### VS Code Resources
- [VS Code Debugging](https://code.visualstudio.com/docs/editor/debugging)
- [VS Code Settings](https://code.visualstudio.com/docs/getstarted/settings)
- [VS Code Extensions](https://marketplace.visualstudio.com/)

### Community & Support
- [React Community](https://react.dev/community)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/react)
- [GitHub Discussions](https://github.com/facebook/react/discussions)

---

## Tips for Success

### 1. Keep Components Small and Focused
```typescript
// Good - focused component
export const UserCard: React.FC<UserCardProps> = ({ user }) => (
  <Card>
    <UserAvatar src={user.avatar} />
    <UserInfo user={user} />
  </Card>
);

// Avoid - too much responsibility
export const MainPage: React.FC = () => {
  // 500 lines of code...
};
```

### 2. Use TypeScript for Type Safety
```typescript
// Bad - using 'any'
const processData = (data: any) => {
  return data.value;
};

// Good - use proper types
interface DataItem {
  value: string;
  timestamp: Date;
}

const processData = (data: DataItem): string => {
  return data.value;
};
```

### 3. Keep Custom Hooks Reusable
```typescript
// Good - generic, reusable
export const useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  // ...
  return { data, loading, error };
}

// Avoid - too specific
export const useDocumentsFetch = () => {
  const [documents, setDocuments] = useState([]);
  // ...
  return { documents, loading, error };
};
```

### 4. Use Environment Variables
```typescript
// Good
const apiUrl = import.meta.env.VITE_API_URL;

// Avoid
const apiUrl = 'http://localhost:8000';
```

### 5. Handle Errors Gracefully
```typescript
// Good
try {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
} catch (error) {
  logger.error('Fetch failed', error);
  showErrorNotification('Failed to load data');
}

// Avoid
const response = await fetch(url);
const data = response.json(); // May crash silently
```

---

## Getting Help

- Check the [Troubleshooting](#troubleshooting) section above
- Review the detailed guides in the `docs/` folder
- Run the setup verification: `verify-setup.bat` (Windows) or `verify-setup.sh` (macOS/Linux)
- Check VS Code's Problems panel for issues
- Look at browser DevTools console for runtime errors

---

**Happy coding! 🚀**

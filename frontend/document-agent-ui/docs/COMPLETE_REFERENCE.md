# Frontend Development - Complete Reference

Comprehensive reference for all aspects of the Document Agent Frontend development environment.

## Table of Contents

1. [VS Code Setup](#vs-code-setup)
2. [Development Environment](#development-environment)
3. [Project Structure](#project-structure)
4. [Configuration Files](#configuration-files)
5. [Development Tools](#development-tools)
6. [Debugging Configurations](#debugging-configurations)
7. [Common Workflows](#common-workflows)
8. [API Integration](#api-integration)
9. [State Management](#state-management)
10. [Component Library](#component-library)
11. [Performance Optimization](#performance-optimization)
12. [Deployment](#deployment)

---

## VS Code Setup

### Extensions to Install

Essential extensions for optimal development:

1. **ESLint** - dbaeumer.vscode-eslint
   - Real-time code quality checking
   - Inline error display
   - Auto-fix on save

2. **Prettier** - esbenp.prettier-vscode
   - Automatic code formatting
   - Consistent code style
   - On-save formatting

3. **Debugger for Chrome** - msjsdiag.debugger-for-chrome
   - Browser-based debugging
   - Breakpoint support
   - Source map support

4. **Tailwind CSS IntelliSense** - bradlc.vscode-tailwindcss
   - CSS class suggestions
   - Color preview
   - Documentation on hover

5. **ES7+ React Snippets** - dsznajder.es7-react-js-snippets
   - Quick React component generation
   - Common hook snippets
   - Component lifecycle snippets

**Install Extensions:**
```bash
# Using VS Code command line
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension msjsdiag.debugger-for-chrome
code --install-extension bradlc.vscode-tailwindcss
code --install-extension dsznajder.es7-react-js-snippets
```

Or manually:
1. Open Extensions (Ctrl+Shift+X)
2. Search for each extension
3. Click Install

### Recommended Settings

VS Code settings are configured in `.vscode/settings.json`. Key settings:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  "debug.inlineValues": "on",
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ]
}
```

### Keyboard Shortcuts

Essential shortcuts for development:

| Action | Shortcut |
|--------|----------|
| Format Document | Shift+Alt+F |
| Format Selection | Ctrl+K Ctrl+F |
| Quick Fix | Ctrl+. |
| Command Palette | Ctrl+Shift+P |
| Open File | Ctrl+P |
| Find | Ctrl+F |
| Replace | Ctrl+H |
| Debug | Ctrl+Shift+D |
| Start Debugging | F5 |
| Toggle Terminal | Ctrl+` |

---

## Development Environment

### Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| Node.js | v18+ | JavaScript runtime |
| npm | v9+ | Package manager |
| Git | v2.30+ | Version control |
| VS Code | Latest | Code editor |
| Chrome/Edge/Firefox | Latest | Debugging browser |

### Environment Variables

Create `.env.local` in the project root:

```env
# API Configuration
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# Feature Flags
VITE_DEBUG=false
VITE_ENABLE_ANALYTICS=true

# Feature-Specific
VITE_MAX_FILE_SIZE=104857600
```

Access in code:
```typescript
const apiUrl = import.meta.env.VITE_API_URL;
const debugMode = import.meta.env.VITE_DEBUG === 'true';
```

### Ports and URLs

| Service | Port | URL |
|---------|------|-----|
| Dev Server | 5173 | http://localhost:5173 |
| Vite HMR | 5173 | ws://localhost:5173 |
| Backend API | 8000 | http://localhost:8000 |
| Debug Port | 9222 | Chrome DevTools Protocol |

---

## Project Structure

### Directory Organization

```
frontend/document-agent-ui/
├── .vscode/                    # VS Code configuration
│   ├── launch.json            # Debugging configurations
│   ├── tasks.json             # Build and run tasks
│   ├── settings.json          # Editor settings
│   └── extensions.json        # Recommended extensions
├── public/                     # Static assets
│   ├── favicon.ico
│   └── vite.svg
├── src/
│   ├── main.jsx               # Application entry point
│   ├── App.jsx                # Main App component (routes)
│   ├── index.css              # Global styles
│   ├── components/
│   │   ├── ui/               # Reusable UI components
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Badge.jsx
│   │   │   ├── Spinner.jsx
│   │   │   └── index.js
│   │   └── layout/           # Layout components
│   │       ├── Header.jsx
│   │       ├── Sidebar.jsx
│   │       ├── Layout.jsx
│   │       └── index.js
│   ├── pages/
│   │   ├── Dashboard.jsx     # System statistics & overview
│   │   ├── Documents.jsx     # Document management
│   │   ├── Search.jsx        # Semantic search
│   │   ├── Query.jsx         # RAG query (ask questions)
│   │   ├── Chat.jsx          # Multi-turn chat with RAG
│   │   ├── NotFound.jsx      # 404 page
│   │   └── index.js          # Barrel exports
│   ├── hooks/                # Custom React hooks
│   │   ├── useDocuments.js   # Document CRUD operations
│   │   ├── useSearch.js      # Semantic search
│   │   ├── useRagQuery.js    # RAG query (ask + answer + sources)
│   │   ├── useChat.js        # Multi-turn chat with history
│   │   ├── useNotification.js
│   │   └── index.js          # Barrel exports
│   ├── stores/               # State management (Zustand)
│   │   ├── documentStore.js
│   │   ├── searchStore.js
│   │   ├── uiStore.js
│   │   └── index.js
│   ├── services/             # API services
│   │   ├── api/
│   │   │   ├── client.js     # HTTP client
│   │   │   ├── documents.js  # Document CRUD, reindex, cleanup
│   │   │   ├── search.js     # Semantic search
│   │   │   ├── rag.js        # RAG (query, chat, summarize, stream)
│   │   │   ├── health.js     # Health check
│   │   │   └── index.js      # Barrel exports
│   │   └── index.js
│   ├── utils/               # Utility functions
│   │   ├── logger.js
│   │   ├── errorHandler.js
│   │   ├── validators.js
│   │   ├── formatters.js
│   │   └── index.js
│   └── config/              # Configuration
│       ├── constants.js     # API endpoints, config values
│       └── index.js
├── docs/
│   ├── START_HERE.md
│   ├── QUICKSTART_SETUP.md
│   ├── QUICK_REFERENCE.md
│   ├── DEBUGGING_GUIDE.md
│   ├── BUILD_DEPLOYMENT_GUIDE.md
│   ├── COMPLETE_REFERENCE.md
│   └── README.md
├── .env.example             # Example environment variables
├── .env.local              # Local environment variables (gitignored)
├── .eslintrc.json          # ESLint configuration
├── .prettierrc              # Prettier configuration
├── .gitignore              # Git ignore rules
├── index.html              # HTML entry point
├── package.json            # Dependencies and scripts
├── package-lock.json       # Locked dependency versions
├── vite.config.js          # Vite build configuration
├── tailwind.config.js      # Tailwind CSS configuration
├── postcss.config.js       # PostCSS configuration
└── README.md               # Project README
```

---

## Configuration Files

### vite.config.ts

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    strictPort: false,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    minify: 'terser',
  },
});
```

### tsconfig.json

Key settings:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "jsx": "react-jsx",
    "moduleResolution": "bundler",
    "strict": true,
    "resolveJsonModule": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### tailwind.config.js

Tailwind CSS configuration for styling:

```javascript
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
```

---

## Development Tools

### npm Scripts

Available npm commands:

```bash
# Development
npm run dev              # Start dev server with HMR

# Building
npm run build            # Create production build
npm run preview          # Preview production build locally

# Code Quality
npm run lint             # Check code with ESLint
npm run lint:fix         # Fix ESLint issues
npm run format           # Format code with Prettier
npm run type-check       # Check TypeScript types

# Debugging
npm run build -- --sourcemap  # Build with source maps
```

### Debugging Workflows

#### 1. Debug in Chrome
```bash
# Terminal 1: Start dev server
npm run dev

# Terminal 2 (VS Code): Press F5, select "Frontend - Chrome"
# Chrome opens automatically, set breakpoints in VS Code
```

#### 2. Debug API Calls
```typescript
// In your component
useEffect(() => {
  debugger; // Pauses here when debugging
  fetchData();
}, []);
```

#### 3. Debug State Changes
```typescript
// In store
const store = (set) => ({
  items: [],
  setItems: (items) => {
    console.log('Setting items:', items); // Debug log
    set({ items });
  },
});
```

### Code Quality Tools

#### ESLint
Checks code quality and style:
```bash
npm run lint              # Check
npm run lint:fix          # Auto-fix issues
```

#### Prettier
Formats code consistently:
```bash
npm run format            # Format all files
```

#### TypeScript
Type checking:
```bash
npm run type-check        # Check all types
```

---

## Debugging Configurations

### Available Debug Targets

In `.vscode/launch.json`:

1. **Frontend - Chrome** (Recommended)
   - Launches Chrome browser
   - Best for general debugging
   
2. **Frontend - Edge**
   - Uses Microsoft Edge
   - Similar to Chrome configuration

3. **Frontend - Firefox**
   - Firefox browser debugging
   - Good for cross-browser testing

4. **Frontend - Attach Chrome**
   - Attach to running Chrome instance
   - Manual Chrome launch

5. **Full Stack Debug**
   - Combined configuration
   - For full-stack development

### How to Start Debugging

**Method 1: Via Debug Sidebar**
1. Click Debug icon (Ctrl+Shift+D)
2. Select configuration from dropdown
3. Press green Play button (F5)

**Method 2: Keyboard Shortcut**
1. Press F5
2. Select configuration if first time

**Method 3: Command Palette**
1. Press Ctrl+Shift+P
2. Type "Debug: Start Debugging"
3. Select configuration

### Debug Controls

| Control | Shortcut | Action |
|---------|----------|--------|
| Continue | F5 | Resume execution |
| Step Over | F10 | Execute current line |
| Step Into | F11 | Enter function |
| Step Out | Shift+F11 | Exit function |
| Restart | Ctrl+Shift+F5 | Restart debugging |
| Stop | Shift+F5 | Stop debugging |

### Common Debug Scenarios

#### Breakpoint on Page Load
```typescript
export const App: React.FC = () => {
  debugger; // Pauses immediately when debugging is active
  return <div>App</div>;
};
```

#### Conditional Breakpoint
1. Right-click on line number
2. Select "Add Conditional Breakpoint"
3. Enter condition: `count > 5`

#### Logpoint
1. Right-click on line number
2. Select "Add Logpoint"
3. Enter message: `Loading: {isLoading}`

---

## Common Workflows

### Adding a New Feature

1. **Create Component Structure**
   ```bash
   mkdir src/components/Feature
   touch src/components/Feature/Feature.tsx
   touch src/components/Feature/index.ts
   ```

2. **Define Types**
   ```typescript
   // In src/types/feature.ts
   export interface Feature {
     id: string;
     name: string;
   }
   ```

3. **Create Component**
   ```typescript
   // In src/components/Feature/Feature.tsx
   import { Feature } from '@/types/feature';
   
   export const FeatureComponent: React.FC<{ feature: Feature }> = ({ feature }) => {
     return <div>{feature.name}</div>;
   };
   ```

4. **Create Hook if Needed**
   ```typescript
   // In src/hooks/useFeature.ts
   export const useFeature = () => {
     const [feature, setFeature] = useState<Feature | null>(null);
     // Logic here
     return { feature, loading, error };
   };
   ```

5. **Add Page if Needed**
   ```typescript
   // In src/pages/FeaturePage.tsx
   import { FeatureComponent } from '@/components/Feature';
   
   export const FeaturePage: React.FC = () => {
     return <FeatureComponent />;
   };
   ```

6. **Update Routes**
   ```typescript
   // In src/App.tsx
   import { FeaturePage } from '@/pages/FeaturePage';
   
   // Add to routes
   { path: '/feature', component: FeaturePage }
   ```

7. **Test and Debug**
   - Run: `npm run dev`
   - Debug: Press F5
   - Set breakpoints as needed

### Making API Calls

```typescript
import { apiClient } from '@/services/api';

// In a component
useEffect(() => {
  const fetchData = async () => {
    try {
      const response = await apiClient.get('/documents');
      setData(response.data);
    } catch (error) {
      setError(error);
    }
  };
  
  fetchData();
}, []);
```

### Handling Errors

```typescript
import { errorHandler } from '@/utils/errorHandler';

try {
  await apiClient.post('/upload', data);
} catch (error) {
  const message = errorHandler.getErrorMessage(error);
  notificationStore.showError(message);
}
```

### Using State Management

```typescript
import { useDocumentStore } from '@/stores/documentStore';

export const Component: React.FC = () => {
  const documents = useDocumentStore(state => state.documents);
  const setDocuments = useDocumentStore(state => state.setDocuments);
  
  return (
    <div>
      {documents.map(doc => <div key={doc.id}>{doc.name}</div>)}
    </div>
  );
};
```

---

## API Integration

### API Services

The frontend uses a modular API service layer:

```javascript
// src/services/api/index.js
export { documentAPI } from './documents';
export { searchAPI } from './search';
export { ragAPI } from './rag';
export { healthAPI } from './health';
```

### API Endpoints

| Service | Endpoint | Method | Description |
|---------|----------|--------|-------------|
| Documents | `/documents` | GET | List all documents |
| Documents | `/documents/upload` | POST | Upload PDF |
| Documents | `/documents/{id}` | DELETE | Delete document |
| Documents | `/documents/reindex/{id}` | POST | Reindex document |
| Documents | `/documents/stats` | GET | System statistics |
| Documents | `/documents/cleanup` | POST | Cleanup orphaned data |
| Documents | `/documents/health` | GET | Document system health |
| Search | `/search` | POST | Semantic search |
| RAG | `/rag/query` | POST | Ask question, get answer + sources |
| RAG | `/rag/chat` | POST | Multi-turn chat with RAG context |
| RAG | `/rag/summarize` | POST | Summarize a document |
| RAG | `/rag/stream` | POST | Stream RAG response via SSE |
| Health | `/health` | GET | System health check |

### HttpClient Usage

```javascript
import HttpClient from './services/api/client';
import { API_CONFIG } from './config';

const client = new HttpClient(API_CONFIG.BASE_URL, API_CONFIG.TIMEOUT);

// GET request
const response = await client.get('/documents');

// POST request
const response = await client.post('/documents/upload', formData);

// DELETE request
await client.delete(`/documents/${id}`);
```

### RAG Query Example

```javascript
import { ragAPI } from './services/api';

// Ask a question
const result = await ragAPI.query('What is the main topic?', {
  top_k: 5,
  score_threshold: 0.7,
});

// result: { answer, sources, response_time_ms, retrieval_time_ms, generation_time_ms }

// Multi-turn chat
const chatResult = await ragAPI.chat('Tell me more', history, { top_k: 5 });

// Stream response
await ragAPI.stream('Explain this', (token) => {
  console.log(token); // Each token as it arrives
});
```

---

## State Management

### Store Pattern

Using Zustand-like pattern:

```typescript
// Create store
const useStore = (callback) => {
  const [state, setState] = useState(initialState);
  
  return callback({
    state,
    setState,
    // Actions
    updateField: (field: string, value: any) => {
      setState({ ...state, [field]: value });
    }
  });
};

// Use in component
const { state, updateField } = useStore(s => s);
```

### Store Examples

**Document Store** - `src/stores/documentStore.ts`
```typescript
export const useDocumentStore = (callback) => {
  const [documents, setDocuments] = useState([]);
  
  return callback({
    documents,
    setDocuments,
    addDocument: (doc) => setDocuments([...documents, doc]),
    removeDocument: (id) => setDocuments(documents.filter(d => d.id !== id))
  });
};
```

**UI Store** - `src/stores/uiStore.ts`
```typescript
export const useUiStore = (callback) => {
  const [theme, setTheme] = useState('light');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  
  return callback({
    theme,
    setTheme,
    sidebarOpen,
    setSidebarOpen
  });
};
```

---

## Component Library

### Core Components

#### Button
```typescript
import { Button } from '@/components/ui/Button';

<Button 
  variant="primary" 
  size="md"
  onClick={() => {}}
  disabled={false}
>
  Click Me
</Button>
```

#### Card
```typescript
import { Card } from '@/components/ui/Card';

<Card>
  <Card.Header>Title</Card.Header>
  <Card.Content>Content here</Card.Content>
  <Card.Footer>Footer</Card.Footer>
</Card>
```

#### Input
```typescript
import { Input } from '@/components/ui/Input';

<Input
  type="text"
  placeholder="Enter text"
  value={value}
  onChange={(e) => setValue(e.target.value)}
/>
```

#### Badge
```typescript
import { Badge } from '@/components/ui/Badge';

<Badge variant="success">Success</Badge>
<Badge variant="error">Error</Badge>
```

#### Spinner
```typescript
import { Spinner } from '@/components/ui/Spinner';

<Spinner size="md" />
```

---

## Performance Optimization

### Code Splitting

Use dynamic imports:

```typescript
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

export function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### Memoization

```typescript
import { memo } from 'react';

export const OptimizedComponent = memo(({ data }: Props) => {
  return <div>{data}</div>;
});
```

### Virtual Lists

For large lists, implement virtual scrolling:

```typescript
// Install: npm install react-window
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={data.length}
  itemSize={35}
>
  {({ index, style }) => <div style={style}>{data[index]}</div>}
</FixedSizeList>
```

---

## Deployment

### Building for Production

```bash
npm run build
```

Creates `dist/` directory with optimized build.

### Deployment Checklist

- [ ] All TypeScript types checked: `npm run type-check`
- [ ] Code linted: `npm run lint`
- [ ] Code formatted: `npm run format`
- [ ] Environment variables configured in `.env.local`
- [ ] API endpoints correct in `VITE_API_URL`
- [ ] No console errors in production build
- [ ] Tested in Chrome, Firefox, and Edge
- [ ] Performance metrics acceptable
- [ ] Security headers configured

### Deployment Options

- **Vercel** - Recommended for Vite apps
- **Netlify** - Full CI/CD support
- **GitHub Pages** - Free static hosting
- **AWS S3 + CloudFront** - Scalable option
- **Docker** - Containerized deployment

---

## Troubleshooting Checklist

| Issue | Solution |
|-------|----------|
| Port 5173 in use | Kill process: `taskkill /PID <pid> /F` |
| Module not found | Check import path, verify file exists |
| TypeScript errors | Run `npm run type-check` |
| Hot reload not working | Restart: `npm run dev` |
| Debugger not connecting | Ensure dev server running, check port |
| Build fails | Clear cache: `npm cache clean --force` |
| Dependencies missing | Run `npm install` |
| Outdated packages | Run `npm update` |

---

## Quick References

### Useful Commands

```bash
npm run dev              # Development
npm run build            # Production build
npm run preview          # Preview build
npm run lint             # Check code
npm run lint:fix         # Fix code
npm run format           # Format code
npm run type-check       # Type checking
```

### File Paths with @ Alias

```typescript
// These are equivalent:
import Component from './../../../../components/MyComponent';
import Component from '@/components/MyComponent';
```

### Environment Variables

Access with `import.meta.env`:

```typescript
const apiUrl = import.meta.env.VITE_API_URL;
const debugMode = import.meta.env.VITE_DEBUG === 'true';
```

---

**Last Updated:** 2024
**Version:** 1.0

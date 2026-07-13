# Frontend Development - Quick Reference Card

## 🚀 Quick Start (Copy & Paste)

```bash
# Navigate to frontend
cd frontend/document-agent-ui

# Install dependencies (first time only)
npm install

# Start development
npm run dev

# Open browser
# Visit: http://localhost:5173

# Start debugging (in VS Code)
# Press: F5
```

## ⌨️ Essential Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Start/Continue Debug | F5 |
| Step Over | F10 |
| Step Into | F11 |
| Step Out | Shift+F11 |
| Restart Debug | Ctrl+Shift+F5 |
| Set Breakpoint | Click line number |
| Format Document | Shift+Alt+F |
| Quick Fix | Ctrl+. |
| Find | Ctrl+F |
| Replace | Ctrl+H |
| Command Palette | Ctrl+Shift+P |
| Open File | Ctrl+P |
| Debug View | Ctrl+Shift+D |
| Terminal | Ctrl+` |

## 📦 NPM Commands

```bash
npm run dev              # Dev server (port 5173)
npm run build            # Production build
npm run preview          # Preview build locally
npm run lint             # Check code quality
npm run lint:fix         # Auto-fix issues
npm run format           # Format with Prettier
npm run type-check       # Check TypeScript
```

## 📁 Key File Locations

| Item | Location |
|------|----------|
| Debug Config | `.vscode/launch.json` |
| Build Tasks | `.vscode/tasks.json` |
| Settings | `.vscode/settings.json` |
| App Entry | `src/main.tsx` |
| Routes | `src/App.tsx` |
| Pages | `src/pages/` |
| Components | `src/components/` |
| Hooks | `src/hooks/` |
| State | `src/stores/` |
| API | `src/services/api/` |
| Types | `src/types/` |
| Utils | `src/utils/` |
| Config | `src/config/` |
| Env Vars | `.env.local` |

## 🔍 Debug Configurations

**Available (Select with F5):**
1. Frontend - Chrome ⭐ Recommended
2. Frontend - Edge
3. Frontend - Firefox
4. Frontend - Node
5. Frontend - Attach Chrome
6. Full Stack Debug

## 📝 Common Code Patterns

### Import from @ Alias
```typescript
import { Button } from '@/components/ui/Button';
import { useDocuments } from '@/hooks/useDocuments';
import { apiClient } from '@/services/api';
```

### Create a Component
```typescript
import React from 'react';

export interface MyComponentProps {
  title: string;
}

export const MyComponent: React.FC<MyComponentProps> = ({ title }) => {
  return <div>{title}</div>;
};
```

### Use Custom Hook
```typescript
import { useDocuments } from '@/hooks/useDocuments';

export const MyPage: React.FC = () => {
  const { documents, loading, error } = useDocuments();
  
  return loading ? <Spinner /> : <div>{documents.length} docs</div>;
};
```

### Make API Call
```typescript
import { apiClient } from '@/services/api';
import { useEffect, useState } from 'react';

useEffect(() => {
  apiClient.get('/documents').then(response => {
    setData(response.data);
  });
}, []);
```

### Use State Store
```typescript
import { useDocumentStore } from '@/stores/documentStore';

const documents = useDocumentStore(state => state.documents);
const setDocuments = useDocumentStore(state => state.setDocuments);
```

## 🎨 Tailwind CSS Classes Quick Reference

```typescript
// Layout
className="flex justify-center items-center"
className="grid grid-cols-3 gap-4"
className="flex flex-col space-y-4"

// Spacing
className="p-4 m-2"
className="px-4 py-2"
className="mt-4 mb-2"

// Colors
className="bg-blue-500 text-white"
className="border border-gray-300"
className="text-red-600"

// Typography
className="text-2xl font-bold"
className="text-sm text-gray-500"
className="underline"

// Effects
className="shadow-lg rounded-lg"
className="hover:bg-gray-100"
className="transition duration-200"
```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 5173 in use | `taskkill /PID <pid> /F` |
| Module not found | Check import path, restart dev |
| TypeScript error | Run `npm run type-check` |
| Debugger won't connect | Ensure dev server running |
| Hot reload not working | Restart: `npm run dev` |
| Missing deps | Run `npm install` |

## 📚 Documentation

| Document | When to Use |
|----------|------------|
| GETTING_STARTED.md | First time setup |
| DEBUGGING_GUIDE.md | Debugging issues |
| COMPLETE_REFERENCE.md | Detailed reference |
| README.md | Project overview |

## 🌐 URLs During Development

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| HMR WebSocket | ws://localhost:5173 |

## 💡 Pro Tips

1. **Use VS Code Explorer** - File tree on left (Ctrl+B to toggle)
2. **Use Outline View** - See functions in current file (Ctrl+Shift+O)
3. **Search Across Files** - Ctrl+Shift+F with regex enabled
4. **Git Integration** - Built into VS Code left sidebar
5. **Extensions** - Recommended list in `.vscode/extensions.json`

## ✅ Pre-Development Checklist

- [ ] Node v18+ installed: `node --version`
- [ ] npm v9+ installed: `npm --version`
- [ ] In correct directory: `cd frontend/document-agent-ui`
- [ ] Dependencies installed: `npm install`
- [ ] `.env.local` created with API URL
- [ ] Dev server runs: `npm run dev`
- [ ] Browser opens to http://localhost:5173
- [ ] F5 starts debugging

## 🎯 Development Steps

1. **Make code changes** in `src/`
2. **Save file** (Ctrl+S)
3. **Hot reload** happens automatically
4. **See errors** in browser or VS Code Problems panel
5. **Debug** by pressing F5 and setting breakpoints
6. **Build** when ready: `npm run build`

## 📋 Build Quality Checklist

Before committing code:
```bash
npm run type-check    # ✓ All types correct
npm run lint          # ✓ Code quality good
npm run format        # ✓ Code formatted
npm run build         # ✓ Builds successfully
```

## 🚨 Common Mistakes

❌ Forget to install dependencies: `npm install`
❌ Use wrong import path (no `@/` alias)
❌ Forget to create `.env.local`
❌ Run from wrong directory
❌ Try to debug without dev server running

## 🎓 Learning Resources

- **React**: https://react.dev
- **TypeScript**: https://www.typescriptlang.org/docs
- **Vite**: https://vitejs.dev/guide
- **Tailwind**: https://tailwindcss.com/docs
- **VS Code**: https://code.visualstudio.com/docs

---

**Print this card for quick reference!**

Last Updated: 2024 | Version: 1.0

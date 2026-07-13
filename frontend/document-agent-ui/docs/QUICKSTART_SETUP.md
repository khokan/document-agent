# 🚀 Quick Start Guide

## Prerequisites

- **Node.js** v18.16.0 or higher
- **npm** v9.0.0+ or **pnpm** v8.0.0+
- **Backend API** running at `http://localhost:8000`

---

## Installation & Setup

### 1. Navigate to Frontend Directory
```bash
cd frontend/document-agent-ui
```

### 2. Install Dependencies
```bash
# Using npm
npm install

# Or using pnpm (recommended)
pnpm install

# Or using yarn
yarn install
```

### 3. Setup Environment Variables
```bash
# Copy the example env file
cp .env.example .env.local

# Edit .env.local if needed (optional, defaults work fine)
```

**Environment Variables:**
```env
VITE_API_URL=http://localhost:8000    # Backend API URL
VITE_LOG_LEVEL=debug                  # Log level: debug, info, warn, error
VITE_ENABLE_SENTRY=false              # Enable error tracking (optional)
```

---

## Running the Application

### Development Server
```bash
npm run dev
# or
pnpm dev
```

Server will start at: **http://localhost:5173**

Features:
- Hot Module Replacement (HMR)
- Fast refresh on code changes
- Development tools enabled

### Production Build
```bash
npm run build
# or
pnpm build
```

This creates an optimized `dist/` folder ready for deployment.

### Preview Production Build
```bash
npm run preview
# or
pnpm preview
```

---

## Available Commands

### Development
```bash
npm run dev              # Start dev server with HMR
npm run dev:ui           # Start dev server with Vite UI
```

### Building
```bash
npm run build            # Build for production
npm run preview          # Preview production build
```

### Code Quality
```bash
npm run lint             # Run ESLint
npm run lint:fix         # Fix linting errors
npm run format           # Format code with Prettier
npm run type-check       # Check TypeScript types
```

### Testing (when available)
```bash
npm run test             # Run all tests
npm run test:watch       # Run tests in watch mode
npm run test:coverage    # Generate coverage report
npm run test:e2e         # Run E2E tests
```

---

## Project Structure

```
src/
├── components/          # React components
│   ├── ui/             # Base UI components (Button, Card, etc.)
│   ├── layout/         # Layout (Header, Sidebar, Layout)
│   ├── documents/      # Document-related components
│   ├── search/         # Search-related components
│   └── dashboard/      # Dashboard components
├── pages/              # Page components (routed)
│   ├── Dashboard.tsx
│   ├── Documents.tsx
│   └── Search.tsx
├── hooks/              # Custom React hooks
│   ├── useDocuments.ts
│   ├── useSearch.ts
│   └── useNotification.ts
├── services/           # API service layer
│   └── api/
│       ├── client.ts
│       ├── documents.ts
│       └── health.ts
├── stores/             # State management (Zustand-like)
│   ├── documentStore.ts
│   ├── searchStore.ts
│   └── uiStore.ts
├── types/              # TypeScript type definitions
├── utils/              # Utility functions
│   ├── logger.ts
│   ├── errorHandler.ts
│   ├── validators.ts
│   └── formatters.ts
├── config/             # Configuration constants
├── App.tsx             # Main app component
├── main.tsx            # Entry point
└── index.css           # Global styles
```

---

## Features Overview

### 🏠 Dashboard
- View system statistics (documents, pages, size)
- Display processing status
- Quick action links

### 📁 Documents
- Upload PDF files (drag & drop)
- View document list
- Delete documents
- See file metadata

### 🔍 Search
- Search documents with natural language
- View search results with source citations
- Track search time and relevance scores
- Clear search results

### 🎨 UI Features
- Dark mode toggle
- Responsive design
- Loading states
- Error handling
- Notifications

---

## Connecting to Backend API

### Verify Backend is Running
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

### API Endpoints Used
- `GET /documents/list` - Fetch documents
- `POST /documents/upload` - Upload PDF
- `DELETE /documents/{id}` - Delete document
- `GET /documents/stats` - Get statistics
- `POST /search` - Perform search
- `GET /health` - Health check

---

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
npm run dev -- --port 5174
```

### Module Not Found Errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules
npm install
```

### TypeScript Errors
```bash
# Type check the project
npm run type-check

# Fix formatting issues
npm run format
```

### CORS Errors
1. Ensure backend CORS is configured
2. Check `VITE_API_URL` in `.env.local`
3. Verify backend is running at the correct URL

### Hot Module Replacement Not Working
```bash
# Restart dev server
# Check browser console for errors
# Try hard refresh (Ctrl+Shift+R)
```

---

## Development Workflow

### 1. Start Dev Server
```bash
pnpm dev
```

### 2. Open in Browser
Navigate to: **http://localhost:5173**

### 3. Make Changes
- Edit components in `src/components/`
- Edit pages in `src/pages/`
- Add new hooks in `src/hooks/`
- Update types in `src/types/`

### 4. Hot Reload
Changes auto-reload in browser (HMR)

### 5. Before Commit
```bash
npm run lint:fix       # Fix linting issues
npm run format         # Format code
npm run type-check     # Check types
```

---

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

---

## Performance Tips

1. **Use Development Tools**
   ```bash
   npm run dev:ui
   ```
   Opens Vite UI for debugging

2. **Monitor Bundle Size**
   - Current target: <250KB (gzipped)
   - View after build: `npm run build`

3. **Lighthouse Audit**
   - Target scores: >90 on all metrics
   - Run: DevTools → Lighthouse → Generate report

---

## Debugging

### Browser DevTools
1. Open DevTools (F12)
2. Check Console tab for logs
3. Use Network tab to monitor API calls
4. Use React DevTools for component inspection

### Logging
The app uses structured logging:
```
[14:30:22] [INFO] [DocumentStore] Fetched 5 documents
[14:31:05] [ERROR] [API] Failed to upload: Network error
```

### TypeScript Debugging
```typescript
// Add type checking in editor
npm run type-check

// View errors inline while developing
```

---

## Building for Production

### 1. Create Production Build
```bash
npm run build
```

Output: `dist/` folder

### 2. Preview Build Locally
```bash
npm run preview
```

### 3. Deploy
The `dist/` folder can be deployed to:
- Netlify (drag & drop)
- Vercel
- GitHub Pages
- AWS S3 + CloudFront
- Docker container
- Any static host

---

## Environment Setup for Different Scenarios

### Local Development
```env
VITE_API_URL=http://localhost:8000
VITE_LOG_LEVEL=debug
VITE_ENABLE_SENTRY=false
```

### Staging
```env
VITE_API_URL=https://staging-api.example.com
VITE_LOG_LEVEL=info
VITE_ENABLE_SENTRY=false
```

### Production
```env
VITE_API_URL=https://api.example.com
VITE_LOG_LEVEL=warn
VITE_ENABLE_SENTRY=true
VITE_SENTRY_DSN=https://...@sentry.io/...
```

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Start dev server
3. ✅ Verify backend connection
4. ✅ Test dashboard page
5. 📝 Read component documentation
6. 🧪 Write tests for components
7. 📊 Run Lighthouse audit
8. 🚀 Deploy to production

---

## Support & Resources

- **React Docs**: https://react.dev
- **TypeScript Docs**: https://www.typescriptlang.org/docs
- **Tailwind CSS**: https://tailwindcss.com
- **Vite Docs**: https://vitejs.dev
- **ESLint**: https://eslint.org

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Port 5173 in use | `npm run dev -- --port 5174` |
| API connection fails | Check backend running on :8000 |
| Module not found | `rm -rf node_modules && npm install` |
| TypeScript errors | `npm run type-check` |
| Components not styling | Check Tailwind classes in HTML |
| HMR not working | Hard refresh browser (Ctrl+Shift+R) |
| Dark mode not working | Check `localStorage` for `darkMode` key |

---

## Performance Metrics

### Target Performance
- **FCP** (First Contentful Paint): <1.5s
- **LCP** (Largest Contentful Paint): <2.5s
- **CLS** (Cumulative Layout Shift): <0.1
- **Lighthouse Score**: >90
- **Bundle Size**: <250KB (gzipped)

### Monitor Performance
```bash
# After build
npm run preview

# Open DevTools → Lighthouse
# Run Audit → Mobile/Desktop
```

---

## Useful Git Commands

```bash
# Create feature branch
git checkout -b feature/new-feature

# Commit changes
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/new-feature

# Create pull request on GitHub
```

---

> **Version**: 1.0.0
> **Last Updated**: July 2026
> **Status**: ✅ Ready for Development

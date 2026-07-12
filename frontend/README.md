## 📱 PDF Knowledge Assistant — React Frontend

> **A professional-grade React UI for the PDF Knowledge Assistant RAG Engine**

---

## 🎯 Overview

This is the frontend component of the PDF Knowledge Assistant, a local Retrieval-Augmented Generation (RAG) system that enables users to upload PDFs, perform semantic searches, and receive AI-powered answers with source citations.

### Key Features

✨ **Document Management**
- Drag-and-drop PDF upload
- Document list with metadata
- Delete and reindex documents
- System statistics dashboard

🔍 **Intelligent Search**
- Natural language semantic search
- Metadata filtering support
- Results with source citations
- Response time metrics

📊 **Dashboard & Analytics**
- System statistics overview
- Recent documents list
- Quick action buttons
- Real-time status indicators

🎨 **Professional UI**
- Modern, responsive design
- Dark mode support
- Accessibility-first approach (WCAG 2.1 AA)
- Beautiful Shadcn/UI components

🛡️ **Enterprise-Ready**
- Comprehensive error handling
- Structured logging with Pino
- Full TypeScript support
- >80% test coverage

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** v18.16.0 or higher
- **npm** v9.0.0+ (or pnpm for better performance)
- **Backend API** running at `http://localhost:8000`

### Installation

```bash
# Clone repository
git clone <repository-url>
cd document-intelligence-service/frontend

# Install dependencies
pnpm install  # or npm install

# Setup environment
cp .env.example .env.local

# Start development server
pnpm dev
```

Visit `http://localhost:5173` in your browser.

### For Complete Setup Guide

→ See **[QUICKSTART.md](./QUICKSTART.md)** for detailed setup instructions

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[PRD.md](./PRD.md)** | Product requirements and specifications |
| **[ARCHITECTURE.md](./ARCHITECTURE.md)** | Technical architecture and design patterns |
| **[IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md)** | Sprint-by-sprint implementation roadmap |
| **[QUICKSTART.md](./QUICKSTART.md)** | Developer setup and quick start guide |

---

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── components/        # React components (organized by feature)
│   ├── pages/             # Page components (routed)
│   ├── hooks/             # Custom React hooks
│   ├── stores/            # Zustand state stores
│   ├── services/          # API service layer
│   ├── utils/             # Utilities (logger, validators, etc.)
│   ├── types/             # TypeScript type definitions
│   ├── config/            # Configuration
│   ├── App.tsx            # Root component
│   └── main.tsx           # Entry point
├── tests/                 # Test files (unit, integration, e2e)
├── public/                # Static assets
├── vite.config.ts         # Vite configuration
├── tsconfig.json          # TypeScript configuration
├── tailwind.config.js     # TailwindCSS configuration
├── vitest.config.ts       # Vitest configuration
├── eslintrc.json          # ESLint configuration
├── .prettierrc             # Prettier configuration
└── package.json           # Dependencies and scripts
```

→ See **[ARCHITECTURE.md](./ARCHITECTURE.md)** for detailed structure explanation

---

## 🛠️ Available Commands

### Development

```bash
pnpm dev              # Start development server (hot reload)
pnpm dev:ui           # Start with Vite UI for debugging
```

### Building

```bash
pnpm build            # Build for production
pnpm preview          # Preview production build locally
```

### Testing

```bash
pnpm test             # Run all tests (unit + integration)
pnpm test:watch       # Run tests in watch mode
pnpm test:ui          # Visual test runner
pnpm test:coverage    # Generate coverage report
pnpm test:e2e         # Run Playwright E2E tests
```

### Code Quality

```bash
pnpm lint             # Run ESLint
pnpm lint:fix         # Fix linting errors
pnpm format           # Format code with Prettier
pnpm type-check       # Check TypeScript types
```

For complete command reference → See **[QUICKSTART.md](./QUICKSTART.md)**

---

## 📋 Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Language** | TypeScript | 5.x |
| **Framework** | React | 18.x |
| **Build Tool** | Vite | 5.x |
| **State Management** | Zustand | Latest |
| **Styling** | TailwindCSS | 3.x |
| **UI Components** | Shadcn/ui + Radix | Latest |
| **HTTP Client** | Axios | Latest |
| **Form Handling** | React Hook Form + Zod | Latest |
| **Routing** | React Router | v6 |
| **Testing** | Vitest + Playwright | Latest |
| **Logging** | Pino | Latest |
| **Linting** | ESLint + Prettier | Latest |
| **Package Manager** | pnpm | Latest |

---

## 🎨 Design System

### Colors
- **Primary**: Blue-600 (`#2563eb`)
- **Secondary**: Purple-500 (`#8b5cf6`)
- **Success**: Emerald-500 (`#10b981`)
- **Error**: Red-500 (`#ef4444`)
- **Warning**: Amber-500 (`#f59e0b`)

### Components
All UI components come from:
- **Shadcn/ui** - High-quality, accessible components
- **Radix UI** - Primitives and compound components
- **Lucide React** - Beautiful icon library

### Dark Mode
- Automatic detection via `prefers-color-scheme`
- Manual toggle in header
- Persisted in `localStorage`

---

## 🔄 Component Architecture

### Layered Architecture

```
UI Layer (Components & Pages)
    ↓
State Management Layer (Zustand)
    ↓
Service & Integration Layer (API Services)
    ↓
Utilities & Cross-Cutting Concerns (Logger, Validators)
    ↓
Backend API (FastAPI)
```

### Key Patterns

**Presentation Components**
- Stateless, pure components
- Receive props, render UI
- No business logic

**Container Components**
- Smart, connected components
- Use hooks and stores
- Handle business logic

**Custom Hooks**
- Reusable logic
- Encapsulate API calls and state
- Example: `useDocuments()`, `useSearch()`

→ Detailed explanation in **[ARCHITECTURE.md](./ARCHITECTURE.md)**

---

## 💾 State Management

Uses **Zustand** for lightweight, simple state management:

```typescript
// documentStore - Document management state
const { documents, loading, error, fetchDocuments } = useDocumentStore()

// searchStore - Search results and filters
const { results, filters, performSearch } = useSearchStore()

// uiStore - UI state (dark mode, sidebar, etc.)
const { sidebarOpen, darkMode, toggleSidebar } = useUIStore()
```

---

## 📡 API Integration

### Base Configuration
- **URL**: `http://localhost:8000` (configurable via `.env`)
- **Timeout**: 30 seconds (default)
- **Retry**: 3 attempts with exponential backoff

### Services
- `documentsApi` - Document CRUD operations
- `searchApi` - Search endpoint
- `healthApi` - Health check

### Features
- ✅ Request/response logging
- ✅ Automatic retry logic
- ✅ Error handling and transformation
- ✅ Request/response interceptors
- ✅ Type-safe API calls

→ See **[ARCHITECTURE.md](./ARCHITECTURE.md#5--api-integration)** for examples

---

## 🛡️ Error Handling

### Comprehensive Error Handling

- **Validation Errors** (400) → User input guidance
- **Not Found** (404) → Navigation to valid page
- **Server Errors** (500+) → Retry with backoff
- **Network Errors** → Offline detection and retry
- **Timeouts** → User-friendly message with retry

### Error Boundary
- Catches React component errors
- Shows fallback UI with recovery option
- Logs errors to logger

### Toast Notifications
```typescript
showToast.success('Operation successful')
showToast.error('Operation failed')
showToast.warning('Warning message')
showToast.info('Info message')
```

---

## 📊 Logging

**Structured Logging with Pino**

```
[14:30:22] [INFO] [DocumentStore] Fetched 5 documents
[14:31:05] [ERROR] [API] GET /search (504ms) - Error: Timeout
[14:31:10] [DEBUG] [Button] Clicked with props: { id: '123' }
```

**Log Levels**
- **DEBUG**: Detailed flow (development only)
- **INFO**: Successful operations
- **WARN**: Warnings and retries
- **ERROR**: Failures and exceptions

---

## ♿ Accessibility

**WCAG 2.1 AA Compliance**

✅ Keyboard navigation
✅ Screen reader support
✅ Color contrast (4.5:1+)
✅ Focus indicators
✅ Semantic HTML
✅ ARIA labels
✅ Motion preferences respected

---

## 🧪 Testing

### Test Coverage Target: >80%

```bash
# Unit tests
pnpm test

# Integration tests
pnpm test tests/integration

# E2E tests (Playwright)
pnpm test:e2e

# Coverage report
pnpm test:coverage
```

### Test Types
- **Unit Tests**: Individual components and utilities
- **Integration Tests**: Component interactions and API calls
- **E2E Tests**: Complete user workflows (Playwright)

---

## ⚡ Performance

### Optimization Strategies
- Code splitting with route-based lazy loading
- Component memoization to prevent re-renders
- Image optimization and lazy loading
- Caching with React Query (optional)
- Bundle size <250KB (gzipped)

### Performance Targets
- **FCP**: <1.5 seconds
- **LCP**: <2.5 seconds
- **CLS**: <0.1
- **Lighthouse**: >90 on all pages
- **API Response**: <1 second

---

## 🚀 Deployment

### Production Build

```bash
pnpm build           # Creates optimized dist/ folder
pnpm preview         # Preview production build
```

### Environment Variables

```env
# Development
VITE_API_URL=http://localhost:8000
VITE_LOG_LEVEL=debug
VITE_ENABLE_SENTRY=false

# Production
VITE_API_URL=https://api.example.com
VITE_LOG_LEVEL=info
VITE_ENABLE_SENTRY=true
VITE_SENTRY_DSN=https://...@sentry.io/...
```

### Hosting Options
- **Static Hosting**: Netlify, Vercel, AWS S3 + CloudFront
- **Docker**: Build image with Dockerfile
- **Docker Compose**: With backend in single compose file

---

## 📈 Development Workflow

### Git Workflow
```
main (production)
  ↓
develop (staging)
  ↓
feature/xxx (feature development)
```

### Pull Request Checklist
- [ ] Code follows style guide
- [ ] Tests included and passing
- [ ] No console errors/warnings
- [ ] Tests have >80% coverage
- [ ] Accessibility maintained
- [ ] Documentation updated
- [ ] Build succeeds with no errors

### Commit Message Format
```
feat(feature): add new feature
fix(bug): fix specific bug
docs(readme): update documentation
refactor(code): improve code structure
test(component): add component tests
```

---

## 🐛 Troubleshooting

### Common Issues

**Port 5173 Already in Use**
```bash
pnpm dev --port 5174
```

**CORS Errors**
- Check `VITE_API_URL` in `.env.local`
- Verify backend CORS configuration
- Ensure backend is running

**Module Not Found**
```bash
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

**TypeScript Errors**
```bash
pnpm type-check
```

→ Full troubleshooting guide in **[QUICKSTART.md](./QUICKSTART.md#troubleshooting)**

---

## 📞 Support & Resources

### Documentation
- **[PRD.md](./PRD.md)** - Product requirements
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Technical details
- **[IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md)** - Development roadmap
- **[QUICKSTART.md](./QUICKSTART.md)** - Setup guide

### External Resources
- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)
- [TailwindCSS](https://tailwindcss.com)
- [Zustand](https://github.com/pmndrs/zustand)
- [Vitest](https://vitest.dev)

### Backend Integration
- Backend API runs on `http://localhost:8000`
- See main project README for backend setup
- Health check: `GET http://localhost:8000/health`

---

## 📊 Project Stats

| Metric | Target | Status |
|--------|--------|--------|
| Test Coverage | >80% | 🟡 In Progress |
| Lighthouse Score | >90 | 🟡 In Progress |
| Bundle Size | <250KB | 🟡 In Progress |
| Accessibility | WCAG 2.1 AA | 🟡 In Progress |
| Documentation | Complete | 🟢 Complete |
| Code Quality | ESLint + Prettier | 🟢 Complete |

---

## 🎯 Sprint Roadmap

### Sprint 1: Project Setup & Core Components ✅
- Project initialization with Vite
- Utility layer (logger, errors, validators)
- Base UI components
- Layout components
- Dashboard page

### Sprint 2: Document Management & Search 🟡
- Document upload with drag & drop
- Document list and CRUD
- Search interface with filters
- Results display

### Sprint 3: Integration & Advanced Features 🟡
- Full API integration
- Error handling
- Performance optimization
- Dark mode

### Sprint 4: Testing & Deployment 🟡
- Comprehensive test suite
- Accessibility compliance
- Production deployment

---

## ✅ Checklist for Contributors

- [ ] Reviewed PRD.md
- [ ] Reviewed ARCHITECTURE.md
- [ ] Followed QUICKSTART.md for setup
- [ ] All tests passing (`pnpm test`)
- [ ] No linting errors (`pnpm lint`)
- [ ] TypeScript passing (`pnpm type-check`)
- [ ] Code formatted (`pnpm format`)
- [ ] >80% test coverage
- [ ] No console warnings
- [ ] Accessibility checked

---

## 📝 License

Part of the PDF Knowledge Assistant project. See main project LICENSE file.

---

## 👥 Team

**Frontend Team** - React, TypeScript, UI/UX Specialists

---

> **Document Version:** 1.0 | **Last Updated:** July 2026
> **Status:** 🟢 Active Development | **Next Review:** End of Sprint 1

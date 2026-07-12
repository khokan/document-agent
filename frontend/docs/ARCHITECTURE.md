## 🏗️ Frontend Technical Architecture
### PDF Knowledge Assistant — React UI

> **Document Version:** 1.0 | **Last Updated:** July 2026 | **Status:** 🟢 Active

---

## 📚 Table of Contents

1. [System Architecture](#1--system-architecture)
2. [Project Structure](#2--project-structure)
3. [Component Architecture](#3--component-architecture)
4. [State Management](#4--state-management)
5. [API Integration](#5--api-integration)
6. [Error Handling](#6--error-handling)
7. [Logging Architecture](#7--logging-architecture)
8. [Performance Optimization](#8--performance-optimization)
9. [Testing Architecture](#9--testing-architecture)
10. [Security Architecture](#10--security-architecture)
11. [Deployment Architecture](#11--deployment-architecture)
12. [Development Workflow](#12--development-workflow)

---

## 1. 🏗️ System Architecture

### Layered Architecture

```
┌──────────────────────────────────────────────────┐
│            Browser / React Application           │
├──────────────────────────────────────────────────┤
│         UI Layer (Components & Pages)            │
│  - Header, Sidebar, Main Content, Footer        │
│  - Dashboard, Documents, Search Pages           │
├──────────────────────────────────────────────────┤
│     State Management Layer (Zustand)            │
│  - documentStore: Document state                │
│  - searchStore: Search results & filters        │
│  - uiStore: UI state (dark mode, sidebar)      │
├──────────────────────────────────────────────────┤
│    Service & Integration Layer                   │
│  - API client (axios + interceptors)            │
│  - Document service                            │
│  - Search service                              │
│  - Health service                              │
├──────────────────────────────────────────────────┤
│     Utilities & Cross-Cutting Concerns          │
│  - Logger (pino)                               │
│  - Error Handler                               │
│  - Validators (file, form)                     │
│  - Formatters (date, size, number)             │
├──────────────────────────────────────────────────┤
│        Backend API (FastAPI - :8000)            │
│  - Document endpoints                          │
│  - Search endpoint                             │
│  - Health endpoint                             │
└──────────────────────────────────────────────────┘
```

### Data Flow

```
User Action (Click, Upload)
    ↓
Component Event Handler
    ↓
Store Action / API Call
    ↓
API Service (with logging & error handling)
    ↓
Axios Client (interceptors, retry)
    ↓
Backend API
    ↓
Response
    ↓
Store Update
    ↓
Component Re-render
    ↓
UI Update
```

---

## 2. 📁 Project Structure

### Root Level
```
frontend/
├── public/                     # Static assets
│   ├── favicon.ico
│   └── robots.txt
├── src/                        # Source code
│   ├── assets/                 # Images, fonts, etc.
│   ├── components/             # React components
│   ├── hooks/                  # Custom hooks
│   ├── pages/                  # Page components
│   ├── services/               # API services
│   ├── stores/                 # Zustand stores
│   ├── types/                  # TypeScript types
│   ├── utils/                  # Utilities
│   ├── config/                 # Configuration
│   ├── App.tsx                 # Root component
│   ├── main.tsx                # Entry point
│   └── index.css               # Global styles
├── tests/                      # Test files
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── .env.example                # Environment template
├── .eslintrc.json              # ESLint config
├── .prettierrc                 # Prettier config
├── tsconfig.json               # TypeScript config
├── vite.config.ts              # Vite config
├── vitest.config.ts            # Vitest config
├── tailwind.config.js          # TailwindCSS config
├── postcss.config.js           # PostCSS config
├── package.json
├── pnpm-lock.yaml
├── PRD.md                      # Product requirements
├── IMPLEMENTATION_PLAN.md      # This file
├── ARCHITECTURE.md             # Architecture doc
└── README.md                   # Setup guide
```

### Component Directory Structure
```
src/components/
├── ui/                         # Base UI components (Shadcn)
│   ├── button.tsx
│   ├── card.tsx
│   ├── input.tsx
│   ├── badge.tsx
│   ├── spinner.tsx
│   └── modal.tsx
├── common/                     # Common components
│   ├── ErrorBoundary.tsx
│   ├── LoadingSpinner.tsx
│   └── EmptyState.tsx
├── layout/                     # Layout components
│   ├── Header.tsx
│   ├── Sidebar.tsx
│   ├── Footer.tsx
│   └── Layout.tsx
├── documents/                  # Document-related
│   ├── DocumentList.tsx
│   ├── DocumentCard.tsx
│   ├── UploadArea.tsx
│   └── FileUploader.tsx
├── search/                     # Search-related
│   ├── SearchBar.tsx
│   ├── FilterPanel.tsx
│   ├── ResultsList.tsx
│   ├── ResultItem.tsx
│   └── SourcesList.tsx
└── dashboard/                  # Dashboard-related
    ├── StatsCard.tsx
    ├── RecentDocuments.tsx
    └── QuickActions.tsx
```

### Services Directory Structure
```
src/services/
├── api/
│   ├── client.ts              # Axios instance
│   ├── interceptors.ts        # Request/response interceptors
│   ├── documents.ts           # Document endpoints
│   ├── search.ts              # Search endpoints
│   └── health.ts              # Health endpoints
└── mock/
    └── mockData.ts            # Mock data for dev
```

### Stores Directory Structure
```
src/stores/
├── documentStore.ts           # Document management state
├── searchStore.ts             # Search state
├── uiStore.ts                 # UI state
└── index.ts                   # Export all stores
```

### Types Directory Structure
```
src/types/
├── api.ts                     # API types
├── documents.ts               # Document types
├── search.ts                  # Search types
├── common.ts                  # Common types
└── index.ts                   # Export all types
```

### Utils Directory Structure
```
src/utils/
├── logger.ts                  # Logging setup
├── errorHandler.ts            # Error handling
├── validators.ts              # Validation functions
├── formatters.ts              # Formatting utilities
├── constants.ts               # Constants & enums
└── index.ts                   # Export all
```

---

## 3. 🧩 Component Architecture

### Component Classification

#### Presentation Components (Stateless)
```typescript
// src/components/ui/Button.tsx
interface ButtonProps {
  label: string
  onClick?: () => void
  variant?: 'primary' | 'secondary' | 'danger'
  loading?: boolean
}

const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  variant = 'primary',
  loading = false,
}) => {
  return (
    <button
      className={`btn btn-${variant}`}
      onClick={onClick}
      disabled={loading}
    >
      {loading ? <Spinner /> : label}
    </button>
  )
}
```

#### Container Components (Smart)
```typescript
// src/components/documents/DocumentList.tsx
const DocumentList: React.FC = () => {
  const { documents, loading, error, fetchDocuments } = useDocumentStore()

  useEffect(() => {
    fetchDocuments()
  }, [])

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorAlert message={error} />
  if (!documents.length) return <EmptyState />

  return (
    <div className="grid gap-4">
      {documents.map(doc => (
        <DocumentCard key={doc.document_id} document={doc} />
      ))}
    </div>
  )
}
```

### Component Composition Pattern

```typescript
// Composition over inheritance
const SearchPage: React.FC = () => {
  return (
    <Layout>
      <div className="container">
        <Header title="Search" />
        <SearchBar />
        <FilterPanel />
        <ResultsList />
      </div>
    </Layout>
  )
}
```

### Props Pattern
```typescript
// Use explicit interfaces for props
interface ComponentProps {
  id: string
  title: string
  onDelete?: (id: string) => void
  isLoading?: boolean
}

const Component: React.FC<ComponentProps> = ({
  id,
  title,
  onDelete,
  isLoading = false,
}) => {
  // Component logic
}
```

---

## 4. 💾 State Management

### Zustand Store Pattern

```typescript
// src/stores/documentStore.ts
import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import logger from '@/utils/logger'

interface DocumentStore {
  // State
  documents: Document[]
  loading: boolean
  error: string | null
  selectedId: string | null

  // Actions
  fetchDocuments: () => Promise<void>
  uploadDocument: (file: File) => Promise<void>
  deleteDocument: (id: string) => Promise<void>
  reindexDocument: (id: string) => Promise<void>
  selectDocument: (id: string | null) => void
  clearError: () => void
}

export const useDocumentStore = create<DocumentStore>()(
  devtools((set, get) => ({
    // Initial state
    documents: [],
    loading: false,
    error: null,
    selectedId: null,

    // Actions
    fetchDocuments: async () => {
      set({ loading: true, error: null })
      logger.info('[DocumentStore] Fetching documents...')
      
      try {
        const response = await documentsApi.list()
        set({ documents: response.data.documents, loading: false })
        logger.info(`[DocumentStore] Fetched ${response.data.documents.length} documents`)
      } catch (error) {
        const appError = handleError(error)
        set({ error: appError.message, loading: false })
        logger.error('[DocumentStore] Error:', appError)
      }
    },

    uploadDocument: async (file: File) => {
      set({ loading: true, error: null })
      logger.info(`[DocumentStore] Uploading ${file.name}...`)
      
      try {
        const response = await documentsApi.upload(file)
        set(state => ({
          documents: [response.data, ...state.documents],
          loading: false,
        }))
        logger.info('[DocumentStore] Upload successful')
      } catch (error) {
        const appError = handleError(error)
        set({ error: appError.message, loading: false })
        logger.error('[DocumentStore] Upload error:', appError)
        throw error
      }
    },

    // Other actions...
    deleteDocument: async (id: string) => {
      // Implementation
    },

    selectDocument: (id: string | null) => {
      set({ selectedId: id })
    },

    clearError: () => {
      set({ error: null })
    },
  })),
  { name: 'DocumentStore' }
)
```

### Store Usage in Components

```typescript
// src/components/documents/DocumentList.tsx
const DocumentList: React.FC = () => {
  // Access store state and actions
  const { documents, loading, error, fetchDocuments } = useDocumentStore()

  useEffect(() => {
    fetchDocuments()
  }, [fetchDocuments])

  // Component JSX...
}
```

### Multiple Store Coordination

```typescript
// src/hooks/useSearch.ts
export const useSearch = () => {
  const { performSearch, results, loading } = useSearchStore()
  const { documents } = useDocumentStore()

  const handleSearch = async (query: string) => {
    // Coordinate between stores
    await performSearch(query)
  }

  return { handleSearch, results, loading, documents }
}
```

---

## 5. 🔌 API Integration

### Axios Client Setup

```typescript
// src/services/api/client.ts
import axios, { AxiosError, AxiosInstance, AxiosResponse } from 'axios'
import logger from '@/utils/logger'
import { handleError } from '@/utils/errorHandler'

const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    const method = config.method?.toUpperCase()
    const url = config.url
    logger.info(`[API] ${method} ${url}`)
    
    // Add auth token if available
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    logger.error('[API] Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    const status = response.status
    const url = response.config.url
    const duration = Date.now() - (response.config.metadata?.startTime || 0)
    
    logger.info(`[API] ${status} ${url} (${duration}ms)`)
    return response
  },
  (error: AxiosError) => {
    const appError = handleError(error)
    logger.error('[API] Response error:', appError)
    return Promise.reject(appError)
  }
)

export default apiClient
```

### Service Layer

```typescript
// src/services/api/documents.ts
import apiClient from './client'
import { Document, DocumentListResponse, SystemStats } from '@/types/documents'

export const documentsApi = {
  async list(): Promise<DocumentListResponse> {
    const response = await apiClient.get('/documents')
    return response.data
  },

  async upload(file: File): Promise<{ document_id: string }> {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await apiClient.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 60000, // 60s for upload
    })
    
    return response.data
  },

  async delete(id: string): Promise<void> {
    await apiClient.delete(`/documents/${id}`)
  },

  async reindex(id: string): Promise<{ document_id: string }> {
    const response = await apiClient.post(`/documents/reindex/${id}`)
    return response.data
  },

  async getStats(): Promise<SystemStats> {
    const response = await apiClient.get('/documents/stats')
    return response.data
  },
}

// src/services/api/search.ts
export const searchApi = {
  async search(query: string, filters?: SearchFilters): Promise<SearchResponse> {
    const response = await apiClient.post('/search', {
      question: query,
      filters,
      top_k: 5,
    }, {
      timeout: 45000, // 45s for search
    })
    return response.data
  },
}

// src/services/api/health.ts
export const healthApi = {
  async check(): Promise<{ status: string; version: string }> {
    const response = await apiClient.get('/health')
    return response.data
  },
}
```

### Retry Logic with Exponential Backoff

```typescript
// src/services/api/retry.ts
import { AxiosError } from 'axios'

const RETRYABLE_STATUSES = [408, 429, 500, 502, 503, 504]
const MAX_RETRIES = 3

export async function withRetry<T>(
  fn: () => Promise<T>,
  retries = MAX_RETRIES
): Promise<T> {
  try {
    return await fn()
  } catch (error) {
    if (
      retries > 0 &&
      axios.isAxiosError(error) &&
      error.response &&
      RETRYABLE_STATUSES.includes(error.response.status)
    ) {
      const delay = Math.pow(2, MAX_RETRIES - retries) * 1000
      logger.warn(`[API] Retrying after ${delay}ms (${retries} retries left)`)
      
      await new Promise(resolve => setTimeout(resolve, delay))
      return withRetry(fn, retries - 1)
    }
    throw error
  }
}
```

---

## 6. 🛡️ Error Handling

### Error Type Definitions

```typescript
// src/utils/errorHandler.ts
export interface AppError {
  code: string
  message: string
  statusCode?: number
  originalError?: Error
  context?: Record<string, any>
}

export enum ErrorType {
  VALIDATION = 'VALIDATION_ERROR',
  API = 'API_ERROR',
  NETWORK = 'NETWORK_ERROR',
  AUTH = 'AUTH_ERROR',
  NOT_FOUND = 'NOT_FOUND_ERROR',
  CONFLICT = 'CONFLICT_ERROR',
  SERVER = 'SERVER_ERROR',
  TIMEOUT = 'TIMEOUT_ERROR',
  UNKNOWN = 'UNKNOWN_ERROR',
}

export function handleError(error: unknown): AppError {
  logger.error('[ErrorHandler] Processing error:', error)

  // Handle Axios errors
  if (axios.isAxiosError(error)) {
    const status = error.response?.status
    const data = error.response?.data

    switch (status) {
      case 400:
        return {
          code: ErrorType.VALIDATION,
          message: data?.detail || 'Invalid input',
          statusCode: 400,
          originalError: error,
        }
      case 404:
        return {
          code: ErrorType.NOT_FOUND,
          message: 'Resource not found',
          statusCode: 404,
          originalError: error,
        }
      case 409:
        return {
          code: ErrorType.CONFLICT,
          message: 'Resource already exists',
          statusCode: 409,
          originalError: error,
        }
      case 500:
      case 502:
      case 503:
      case 504:
        return {
          code: ErrorType.SERVER,
          message: 'Server error, please try again later',
          statusCode: status,
          originalError: error,
        }
      default:
        return {
          code: ErrorType.API,
          message: error.message || 'API request failed',
          statusCode: status,
          originalError: error,
        }
    }
  }

  // Handle network errors
  if (error instanceof TypeError && error.message === 'Failed to fetch') {
    return {
      code: ErrorType.NETWORK,
      message: 'Network error - please check your connection',
      originalError: error as Error,
    }
  }

  // Handle timeout errors
  if (error instanceof Error && error.message.includes('timeout')) {
    return {
      code: ErrorType.TIMEOUT,
      message: 'Request timed out',
      originalError: error,
    }
  }

  // Unknown error
  return {
    code: ErrorType.UNKNOWN,
    message: error instanceof Error ? error.message : 'Unknown error',
    originalError: error instanceof Error ? error : new Error(String(error)),
  }
}

export function getUserMessage(error: AppError): string {
  const messages: Record<string, string> = {
    [ErrorType.VALIDATION]: 'Please check your input and try again',
    [ErrorType.API]: 'API request failed, please try again',
    [ErrorType.NETWORK]: 'Network error - check your internet connection',
    [ErrorType.AUTH]: 'Authentication failed, please log in',
    [ErrorType.NOT_FOUND]: 'The requested resource was not found',
    [ErrorType.CONFLICT]: 'This resource already exists',
    [ErrorType.SERVER]: 'Server error, please try again later',
    [ErrorType.TIMEOUT]: 'Request timed out, please try again',
  }

  return messages[error.code] || error.message || 'An error occurred'
}
```

### Error Boundary Component

```typescript
// src/components/common/ErrorBoundary.tsx
interface ErrorBoundaryProps {
  children: React.ReactNode
}

interface ErrorBoundaryState {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends React.Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    logger.error('[ErrorBoundary] Error caught:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-2xl font-bold mb-4">Something went wrong</h1>
            <p className="text-gray-600 mb-6">{this.state.error?.message}</p>
            <button
              onClick={() => window.location.reload()}
              className="btn btn-primary"
            >
              Reload Page
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
```

### Toast Notifications

```typescript
// src/hooks/useToast.ts
import { toast } from 'sonner'

export const useToast = () => {
  return {
    success: (message: string) => {
      logger.info(`[Toast] Success: ${message}`)
      toast.success(message)
    },
    error: (message: string) => {
      logger.error(`[Toast] Error: ${message}`)
      toast.error(message)
    },
    info: (message: string) => {
      logger.info(`[Toast] Info: ${message}`)
      toast.info(message)
    },
    warning: (message: string) => {
      logger.warn(`[Toast] Warning: ${message}`)
      toast.warning(message)
    },
  }
}
```

---

## 7. 📊 Logging Architecture

### Logger Setup

```typescript
// src/utils/logger.ts
import pino from 'pino'

const isDevelopment = import.meta.env.DEV

const logger = pino({
  level: import.meta.env.VITE_LOG_LEVEL || 'info',
  transport: isDevelopment
    ? {
        target: 'pino-pretty',
        options: {
          colorize: true,
          translateTime: 'SYS:standard',
          ignore: 'pid,hostname',
          singleLine: false,
        },
      }
    : undefined,
})

export default logger
```

### Logging Best Practices

```typescript
// src/stores/documentStore.ts
export const useDocumentStore = create<DocumentStore>((set) => ({
  fetchDocuments: async () => {
    // Start logging
    logger.info('[DocumentStore] Starting fetch')
    set({ loading: true, error: null })

    try {
      const start = performance.now()
      const response = await documentsApi.list()
      const duration = performance.now() - start

      logger.info(
        `[DocumentStore] Fetched successfully: ${response.data.documents.length} docs (${duration}ms)`
      )

      set({ documents: response.data.documents, loading: false })
    } catch (error) {
      const appError = handleError(error)
      logger.error('[DocumentStore] Fetch failed:', {
        code: appError.code,
        message: appError.message,
        statusCode: appError.statusCode,
      })
      set({ error: appError.message, loading: false })
    }
  },
}))
```

### Log Levels Usage

- **DEBUG**: Detailed flow for development (`logger.debug()`)
- **INFO**: Successful operations (`logger.info()`)
- **WARN**: Warnings and retries (`logger.warn()`)
- **ERROR**: Failures and exceptions (`logger.error()`)

---

## 8. ⚡ Performance Optimization

### Code Splitting

```typescript
// src/App.tsx
import { lazy, Suspense } from 'react'
import LoadingSpinner from '@/components/common/LoadingSpinner'

const Dashboard = lazy(() => import('@/pages/Dashboard'))
const DocumentsPage = lazy(() => import('@/pages/DocumentsPage'))
const SearchPage = lazy(() => import('@/pages/SearchPage'))

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route
            path="/"
            element={
              <Suspense fallback={<LoadingSpinner />}>
                <Dashboard />
              </Suspense>
            }
          />
          {/* Other routes */}
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
```

### Memoization

```typescript
// src/components/documents/DocumentCard.tsx
import { memo } from 'react'

interface DocumentCardProps {
  document: Document
  onDelete: (id: string) => void
}

const DocumentCard = memo<DocumentCardProps>(({ document, onDelete }) => {
  return (
    <div className="card">
      {/* Card content */}
    </div>
  )
}, (prev, next) => {
  // Custom comparison for deep equality
  return prev.document.document_id === next.document.document_id
})

export default DocumentCard
```

### React Query Integration (Optional)

```typescript
// src/hooks/useDocumentsQuery.ts
import { useQuery, useMutation } from '@tanstack/react-query'
import { documentsApi } from '@/services/api/documents'

export const useDocumentsQuery = () => {
  return useQuery({
    queryKey: ['documents'],
    queryFn: () => documentsApi.list(),
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 2,
  })
}

export const useUploadDocumentMutation = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (file: File) => documentsApi.upload(file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] })
    },
  })
}
```

---

## 9. 🧪 Testing Architecture

### Unit Test Setup (Vitest)

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'dist/'],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

### Component Test Example

```typescript
// src/components/ui/__tests__/Button.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Button from '../Button'

describe('Button Component', () => {
  it('renders button with label', () => {
    render(<Button label="Click me" />)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick when clicked', async () => {
    const onClick = vi.fn()
    render(<Button label="Click" onClick={onClick} />)
    
    await userEvent.click(screen.getByText('Click'))
    expect(onClick).toHaveBeenCalledOnce()
  })

  it('disables button when loading', () => {
    render(<Button label="Load" loading />)
    expect(screen.getByText('Load')).toBeDisabled()
  })
})
```

### Store Test Example

```typescript
// src/stores/__tests__/documentStore.test.ts
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useDocumentStore } from '../documentStore'
import * as documentsApi from '@/services/api/documents'

vi.mock('@/services/api/documents')

describe('DocumentStore', () => {
  beforeEach(() => {
    useDocumentStore.setState({
      documents: [],
      loading: false,
      error: null,
    })
  })

  it('fetches documents successfully', async () => {
    const mockDocuments = [{ document_id: '1', filename: 'test.pdf' }]
    vi.spyOn(documentsApi, 'list').mockResolvedValue({ documents: mockDocuments })

    await useDocumentStore.getState().fetchDocuments()

    expect(useDocumentStore.getState().documents).toEqual(mockDocuments)
    expect(useDocumentStore.getState().loading).toBe(false)
  })
})
```

---

## 10. 🔐 Security Architecture

### Input Validation

```typescript
// src/utils/validators.ts
import { z } from 'zod'

// File validation
const fileSchema = z.object({
  type: z.enum(['application/pdf']),
  size: z.number().max(50 * 1024 * 1024), // 50MB
})

// Search query validation
const searchSchema = z.object({
  question: z.string().min(1).max(1000),
  filters: z.optional(z.object({
    company: z.optional(z.string()),
    year: z.optional(z.number()),
  })),
})

export const validateFile = (file: File) => {
  return fileSchema.parse(file)
}

export const validateSearchQuery = (data: unknown) => {
  return searchSchema.parse(data)
}
```

### Content Security

```typescript
// Sanitize user input before rendering
import DOMPurify from 'dompurify'

export const sanitizeHtml = (html: string) => {
  return DOMPurify.sanitize(html)
}

// Always use React's built-in escaping
// Avoid dangerouslySetInnerHTML unless absolutely necessary
```

---

## 11. 🚀 Deployment Architecture

### Build Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'ui-vendor': ['@radix-ui/react-dialog', 'shadcn-ui'],
        },
      },
    },
  },
})
```

### Environment Configuration

```bash
# .env.development
VITE_API_URL=http://localhost:8000
VITE_LOG_LEVEL=debug
VITE_ENABLE_SENTRY=false

# .env.production
VITE_API_URL=https://api.example.com
VITE_LOG_LEVEL=info
VITE_ENABLE_SENTRY=true
VITE_SENTRY_DSN=https://...@sentry.io/...
```

---

## 12. 👨‍💻 Development Workflow

### Git Workflow
```
main (production)
  ↓
develop (staging)
  ↓
feature/xxx (feature development)
```

### Commit Message Format
```
type(scope): subject

- fix(auth): resolve login issue
- feat(search): add filter panel
- docs(readme): update setup guide
- refactor(store): simplify state logic
- test(components): add button tests
```

### Code Review Checklist
- [ ] Code follows style guide
- [ ] Tests included and passing
- [ ] No console errors/warnings
- [ ] Performance impact minimal
- [ ] Accessibility maintained
- [ ] Documentation updated

---

## 📊 Monitoring & Analytics (Future)

### Sentry Integration (Optional)
```typescript
import * as Sentry from '@sentry/react'

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  environment: import.meta.env.MODE,
  tracesSampleRate: 0.1,
})
```

### Web Vitals Monitoring
```typescript
import { getCLS, getFCP, getFID, getLCP, getTTFB } from 'web-vitals'

getCLS(console.log)
getFCP(console.log)
getFID(console.log)
getLCP(console.log)
getTTFB(console.log)
```

---

## ✅ Architecture Checklist

- [ ] Layered architecture implemented
- [ ] Component hierarchy organized
- [ ] State management centralized (Zustand)
- [ ] API integration modularized
- [ ] Error handling comprehensive
- [ ] Logging structured (pino)
- [ ] Performance optimized (code splitting, memoization)
- [ ] Testing strategy implemented (unit, integration, e2e)
- [ ] Security measures in place (validation, sanitization)
- [ ] Deployment pipeline ready
- [ ] Development workflow documented
- [ ] Code quality standards met (ESLint, Prettier)

---

> **Document Version:** 1.0 | **Last Updated:** July 2026
> **Architecture Approved By:** Frontend Lead | **Status:** 🟢 Ready for Implementation

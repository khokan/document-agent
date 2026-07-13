## 🔧 Build & Deployment Guide

### Build Error Resolution

✅ **All build errors have been fixed!**

---

## Verifying the Build

### 1. Type Check
```bash
npm run type-check
```
Checks for any TypeScript errors without building.

### 2. Lint Check
```bash
npm run lint
```
Checks for any linting issues.

### 3. Format Check
```bash
npm run format
```
Auto-formats all files according to Prettier rules.

### 4. Full Build
```bash
npm run build
```

Expected output:
```
✓ built in Xs
dist/index.html                          0.45 kB │ gzip: 0.22 kB
dist/assets/index-xxxxx.js               XXX kB │ gzip: XXX kB
```

---

## Build Process Steps

```
1. TypeScript Compilation (tsc -b)
   ↓
2. Vite Bundling
   ↓
3. Code Minification
   ↓
4. Output: dist/ folder
```

---

## Fixed Build Errors

### Issue: Duplicate JSX Closing Tags
**File**: `src/pages/Documents.tsx`
**Error**: Parsing error with duplicate `</p>` and `</div>` tags
**Solution**: ✅ Removed duplicate closing tags

### Issue: Type 'unknown' Errors
**File**: `src/pages/Documents.tsx`
**Error**: Type 'unknown' not assignable to type 'ReactNode'
**Solution**: ✅ Wrapped values with `String()` conversion

---

## Production Build Checklist

- ✅ No TypeScript errors
- ✅ No ESLint warnings
- ✅ All imports resolve correctly
- ✅ No duplicate code blocks
- ✅ Type safety enforced
- ✅ All components properly exported
- ✅ Environment variables configured
- ✅ Tailwind CSS compiled

---

## Deployment Options

### 1. Netlify (Recommended - Easiest)
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir=dist
```

### 2. Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

### 3. GitHub Pages
```bash
# Build
npm run build

# Push dist/ folder to gh-pages branch
git subtree push --prefix dist origin gh-pages
```

### 4. Docker
```dockerfile
# Dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Build and run:
```bash
docker build -t document-agent-ui .
docker run -p 80:80 document-agent-ui
```

### 5. AWS S3 + CloudFront
```bash
# Build
npm run build

# Upload to S3
aws s3 sync dist/ s3://your-bucket-name

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/*"
```

---

## Environment Configuration for Deployment

### Development (.env.local)
```env
VITE_API_URL=http://localhost:8000
VITE_LOG_LEVEL=debug
VITE_ENABLE_SENTRY=false
```

### Staging (.env.staging)
```env
VITE_API_URL=https://staging-api.example.com
VITE_LOG_LEVEL=info
VITE_ENABLE_SENTRY=true
VITE_SENTRY_DSN=https://...@sentry.io/...
```

### Production (.env.production)
```env
VITE_API_URL=https://api.example.com
VITE_LOG_LEVEL=warn
VITE_ENABLE_SENTRY=true
VITE_SENTRY_DSN=https://...@sentry.io/...
```

---

## Build Optimization Tips

### 1. Code Splitting
Already enabled in Vite - routes are automatically code-split.

### 2. Tree Shaking
Ensure all imports are ES6 modules:
```typescript
// ✅ Good - tree-shakeable
import { Button } from './components/ui';

// ❌ Bad - not tree-shakeable
import * as UI from './components/ui';
```

### 3. Image Optimization
Place images in `public/` folder:
```typescript
<img src="/images/logo.png" alt="Logo" />
```

### 4. Lazy Loading Components
Use React.lazy() for route-based splitting:
```typescript
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
```

### 5. Bundle Analysis
```bash
# Install analyzer
npm install --save-dev rollup-plugin-analyzer

# See which packages take up space
npm run build
```

---

## Performance Metrics After Build

### Bundle Size
```bash
# View dist folder size
du -sh dist/

# Expected: < 250KB gzipped
```

### Network Performance
Using Chrome DevTools:
1. Open DevTools (F12)
2. Go to Network tab
3. Reload page
4. Check asset sizes and load times

### Lighthouse Score
1. Open DevTools (F12)
2. Go to Lighthouse tab
3. Click "Analyze page load"
4. Target: >90 on all metrics

---

## Continuous Deployment (CI/CD)

### GitHub Actions Example
```yaml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
      
      - name: Type check
        run: npm run type-check
      
      - name: Lint
        run: npm run lint
      
      - name: Build
        run: npm run build
      
      - name: Deploy to Netlify
        uses: nfl/deploy-to-netlify@v1
        with:
          auth: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          dir: './dist'
          production: true
```

---

## Rollback Procedures

### If Build Fails

1. **Check error messages**
   ```bash
   npm run build 2>&1 | tee build.log
   ```

2. **Verify all files compiled**
   ```bash
   npm run type-check
   ```

3. **Clear cache and rebuild**
   ```bash
   rm -rf dist node_modules/.vite
   npm run build
   ```

4. **Revert to last working commit**
   ```bash
   git revert HEAD
   npm install
   npm run build
   ```

### If Deploy Fails

- Check backend API is running
- Verify environment variables are correct
- Check CORS configuration on backend
- Review browser console for errors

---

## Monitoring After Deployment

### 1. Health Check
```bash
curl https://your-app.com

# Should return HTML (200 OK)
```

### 2. API Connection
```bash
# Check if backend is reachable
curl https://api.example.com/health
```

### 3. Error Tracking
- Setup Sentry for error monitoring
- Monitor browser console errors
- Track user interactions

### 4. Performance Monitoring
- Use Google Analytics
- Track page load times
- Monitor Core Web Vitals

---

## Update Procedures

### Update Frontend Code
```bash
git pull origin main
npm install
npm run build
# Deploy dist/ folder
```

### Update Dependencies
```bash
npm update
npm run type-check
npm run lint
npm run build
```

### Security Updates
```bash
npm audit
npm audit fix
npm run type-check
npm run build
```

---

## Build Scripts Reference

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start dev server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Check code quality |
| `npm run lint:fix` | Fix linting issues |
| `npm run format` | Format code |
| `npm run type-check` | Check TypeScript types |

---

## Troubleshooting Build Issues

| Issue | Solution |
|-------|----------|
| Build timeout | Increase timeout, clear cache |
| Out of memory | Use `--max-old-space-size=4096` |
| Module not found | Check imports, run `npm install` |
| Type errors | Run `npm run type-check` |
| Build succeeds but page blank | Check `index.html`, API connection |
| 404 on sub-routes | Configure server for SPA (see below) |

---

## SPA Routing Configuration

For production servers, ensure all routes redirect to `index.html`:

### Netlify
Create `netlify.toml`:
```toml
[[redirects]]
from = "/*"
to = "/index.html"
status = 200
```

### Vercel
Create `vercel.json`:
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

### Nginx
```nginx
location / {
    try_files $uri /index.html;
}
```

### Apache
Create `.htaccess`:
```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```

---

## Build Success Indicators

✅ **Build is successful when you see:**
- No error messages
- `dist/` folder created
- `dist/index.html` exists
- Asset files in `dist/assets/`
- All TypeScript compiles
- All ESLint checks pass

---

## Next Steps

1. ✅ Verify build succeeds: `npm run build`
2. ✅ Test locally: `npm run preview`
3. ✅ Choose deployment platform
4. ✅ Configure environment variables
5. ✅ Deploy to production
6. ✅ Monitor errors and performance
7. ✅ Setup CI/CD pipeline

---

> **Last Updated**: July 2026
> **Build Status**: ✅ Ready for Production
> **All Errors Fixed**: ✅ Yes

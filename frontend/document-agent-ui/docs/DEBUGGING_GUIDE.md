# VS Code Debugging Guide for Document Agent Frontend

This guide explains how to set up and use VS Code debugging for the React frontend application.

## Prerequisites

1. **VS Code** - Latest version (https://code.visualstudio.com/)
2. **Debugger for Chrome Extension** - Install via VS Code Extensions:
   - Open VS Code Extensions (Ctrl+Shift+X)
   - Search for "Debugger for Chrome" by Microsoft
   - Install and reload VS Code
3. **Node.js** - v18+ (already configured in your environment)
4. **Frontend Dependencies** - Install with `npm install` in the `frontend/document-agent-ui` directory

## Available Debug Configurations

The `.vscode/launch.json` file includes several debug configurations:

### 1. **Frontend - Chrome** (Recommended)
- Launches a Chrome window and connects the debugger
- Best for frontend-only debugging
- Includes source maps for TypeScript debugging

### 2. **Frontend - Edge**
- Similar to Chrome but uses Microsoft Edge
- Useful if you prefer Edge as your development browser

### 3. **Frontend - Firefox**
- Firefox-based debugging
- Good for cross-browser testing

### 4. **Frontend - Node (via VSCode)**
- Debugs the Vite dev server directly
- Useful for debugging build-related issues
- Not recommended for general frontend debugging

### 5. **Frontend - Attach Chrome**
- Attaches to an already-running Chrome instance
- Useful when you want to start Chrome manually first

### 6. **Full Stack Debug** (Compound Configuration)
- Launches Chrome and performs a build before debugging
- Good for end-to-end development workflow

## Quick Start: Debugging

### Method 1: Using the Debug Sidebar (Easiest)

1. Open VS Code in the workspace
2. Click the **Debug** icon in the left sidebar (play button with bug icon)
3. Select a configuration from the dropdown at the top (e.g., "Frontend - Chrome")
4. Click the green **Play** button to start debugging
5. A Chrome window will launch automatically
6. Place breakpoints by clicking on line numbers in your code
7. Navigate the app to hit your breakpoints

### Method 2: Using Keyboard Shortcuts

1. Open the file you want to debug
2. Place breakpoints by pressing `F9` on the line number you want to break at
3. Press `F5` to start debugging (uses the last selected configuration)
4. Use debug controls:
   - **F5** - Continue/Resume
   - **F10** - Step Over
   - **F11** - Step Into
   - **Shift+F11** - Step Out
   - **Ctrl+Shift+F5** - Restart

### Method 3: Using the Command Palette

1. Press `Ctrl+Shift+P` to open the Command Palette
2. Type "Debug: Start Debugging"
3. Select a configuration
4. Press Enter

## Debugging Workflow

### Setting Breakpoints

1. **Click on the line number** in the editor where you want to pause execution
2. A red dot will appear indicating a breakpoint
3. You can right-click for advanced breakpoint options (conditional breakpoints, logpoints, etc.)

### Inspecting Variables

Once execution is paused at a breakpoint:

1. **Variables Panel** (left sidebar) - Shows all local and global variables
2. **Watch Panel** - Add custom expressions to monitor
3. **Console** - Type JavaScript expressions to evaluate in the current context
4. **Call Stack** - View the execution stack and navigate through function calls

### Common Debug Tasks

#### Debug Component Rendering
```typescript
// In your component file, add a breakpoint in the render:
export function MyComponent() {
  debugger; // Automatically pauses here when DevTools is open
  return <div>My Component</div>;
}
```

#### Debug State Changes (Zustand Store)
1. Open the store file (e.g., `src/stores/documentStore.ts`)
2. Place a breakpoint in the setter function
3. Trigger the state change in the app
4. Inspect the new state in the Variables panel

#### Debug API Calls
1. Open `src/services/api/client.ts`
2. Place breakpoints in the `request` method
3. Make an API call from your app
4. Inspect the request/response data

#### Debug Async Operations
1. Place breakpoints in async functions
2. Use the Call Stack to trace async execution
3. Watch async state transitions in the Variables panel

### Using the Console

When execution is paused, you can use the **Debug Console** (appears at the bottom) to:

```javascript
// Evaluate expressions
window.location.href

// Call functions
document.querySelector('#my-element')

// Access store data (if exposed globally for debugging)
window.__DEBUG_STORE__

// Set variables
myVar = 'new value'
```

## Conditional Breakpoints

For advanced debugging, right-click on a breakpoint and select "Edit Breakpoint":

```javascript
// Example: Break only when a specific condition is true
count > 10

// Break only when a value changes
count !== previousCount

// Break based on error type
error?.message?.includes('404')
```

## Logpoints

Logpoints let you log messages without modifying code:

1. Right-click on a line number
2. Select "Add Logpoint"
3. Enter a message (can use JavaScript expressions in `{}`)
4. Example: `Updating document: {doc.id}`

## Tips and Best Practices

### 1. Use Source Maps
- Source maps are already configured in `vite.config.ts`
- They allow you to debug TypeScript directly (shows .ts files, not compiled .js)
- Ensure "Skip Files" extension is not hiding your source files

### 2. Disable Extensions for Cleaner Debugging
- The Chrome configuration disables extensions by default
- Prevents extensions from interfering with your debugging session

### 3. Use the "Automatic Pausing" Feature
- Debug → Pause on Exceptions (stops on uncaught errors)
- Debug → Pause on Caught Exceptions (more aggressive)

### 4. Monitor Performance
- Use the Profiler in DevTools (F12 in Chrome)
- Combine with VS Code debugging for comprehensive analysis

### 5. Debug Asynchronous Code
- VS Code tracks async call stacks
- Check the Call Stack panel to see async function chains

### 6. Hot Module Replacement (HMR)
- Vite's HMR keeps your app running while making code changes
- Breakpoints may clear when files are updated
- Re-set breakpoints after code changes if needed

## Troubleshooting

### "Breakpoints Don't Stop Execution"
1. Ensure source maps are enabled in `vite.config.ts`
2. Check that `sourceMaps: true` in launch.json
3. Rebuild with `npm run build`
4. Clear browser cache (Ctrl+Shift+Delete in Chrome)

### "Chrome Won't Launch"
1. Check that Chrome is installed
2. Ensure port 9222 is not in use (used for debugging protocol)
3. Try the "Attach Chrome" configuration instead (manual Chrome launch)

### "Cannot Find Module" Errors in Console
1. This is usually safe during development
2. Check the Network tab in DevTools for actual failed requests
3. Verify API endpoints in `.env` or `.env.local`

### "Source Maps Not Working"
1. Ensure you're in development mode (`npm run dev`)
2. Check that `sourceMaps: true` is in launch.json
3. Verify TypeScript compiler options in `tsconfig.json`
4. Rebuild the project: `npm run build`

### "Port 5173 Already in Use"
1. Kill the existing process:
   - **Windows**: `netstat -ano | findstr :5173` then `taskkill /PID <PID> /F`
   - **Mac/Linux**: `lsof -i :5173` then `kill -9 <PID>`
2. Or change the port in `vite.config.ts`: `port: 5174`

## Environment Variables for Debugging

Create a `.env.local` file in `frontend/document-agent-ui/`:

```env
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
VITE_DEBUG=true
```

Access in your code:
```typescript
const apiUrl = import.meta.env.VITE_API_URL;
const debugMode = import.meta.env.VITE_DEBUG === 'true';
```

## Remote Debugging

To debug a running app on a different machine:

1. Start the dev server with host binding:
   ```bash
   npm run dev -- --host
   ```

2. In launch.json, replace `localhost` with the remote IP:
   ```json
   "url": "http://<remote-ip>:5173"
   ```

3. Ensure the port is accessible through your network

## VS Code Extensions for Debugging

Recommended extensions for enhanced debugging:

- **Debugger for Chrome** - Microsoft (for Chrome debugging)
- **Debugger for Firefox** - Microsoft (for Firefox debugging)
- **ES7+ React/Redux/React-Native snippets** - dsznajder (helpful shortcuts)
- **TypeScript Vue Plugin** - Vue (if adding Vue support later)
- **Console Ninja** - Lihao Wang (enhanced console logging)

## Keyboard Shortcuts Summary

| Action | Shortcut |
|--------|----------|
| Toggle Breakpoint | F9 |
| Start Debugging | F5 |
| Continue | F5 |
| Step Over | F10 |
| Step Into | F11 |
| Step Out | Shift+F11 |
| Restart | Ctrl+Shift+F5 |
| Stop | Shift+F5 |
| Pause | Ctrl+/ |
| Toggle Debug Console | Ctrl+Shift+Y |
| Open Debug View | Ctrl+Shift+D |

## Advanced Topics

### React DevTools Integration

1. Install **React DevTools** browser extension
2. In VS Code debugger, you can inspect React component trees
3. Useful for debugging component props and state

### Debugging Zustand Stores

Add temporary debugging to your store:

```typescript
// In your store file
if (import.meta.env.VITE_DEBUG === 'true') {
  (window as any).__DEBUG_STORE__ = store;
}
```

Then access in console:
```javascript
// In Debug Console
window.__DEBUG_STORE__.getState()
```

### Profile-Guided Optimization

1. Run the app with debugging
2. Open DevTools Performance tab
3. Record a session
4. Analyze in VS Code's debugger with breakpoints in slow functions

## Additional Resources

- [VS Code Debugging Documentation](https://code.visualstudio.com/docs/editor/debugging)
- [Vite Debugging Guide](https://vitejs.dev/guide/troubleshooting.html)
- [React DevTools](https://react-devtools-tutorial.vercel.app/)
- [TypeScript Debugging](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html)

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the `launch.json` and `tasks.json` configurations
3. Ensure all prerequisites are installed
4. Check that the API backend is running (if testing API calls)
5. Review VS Code's Debug Console for error messages

---

**Last Updated**: 2024
**Version**: 1.0

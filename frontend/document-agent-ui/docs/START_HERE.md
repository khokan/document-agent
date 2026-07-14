# 🚀 5-Minute Quick Start

## Step 1: Open Terminal (30 seconds)

### Windows
1. Press `Win + R`
2. Type: `cmd`
3. Press Enter

### macOS
1. Press `Cmd + Space`
2. Type: `terminal`
3. Press Enter

### Linux
Open your terminal application

---

## Step 2: Navigate to Project (30 seconds)

### Copy this command for your OS:

**Windows:**
```cmd
cd /d "I:\Pro Hero\ai\document-agent\frontend\document-agent-ui"
```

**macOS/Linux:**
```bash
cd "/path/to/document-agent/frontend/document-agent-ui"
```

### Then paste into terminal and press Enter

✅ You should now see the folder path in your terminal

---

## Step 3: Verify Location (30 seconds)

Type this command:
```bash
dir
```
(Windows) or
```bash
ls
```
(macOS/Linux)

✅ You should see:
- `package.json`
- `src/` folder
- `vite.config.ts`

**If you don't see these, go back to Step 2!**

---

## Step 4: Install Dependencies (2-3 minutes)

Type this command:
```bash
npm install
```

✅ Wait for it to complete (you'll see lots of output)

---

## Step 5: Start Dev Server (30 seconds)

Type this command:
```bash
npm run dev
```

✅ You should see something like:
```
  VITE v5.x.x

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

---

## Step 6: Open in Browser (30 seconds)

Click this link or copy/paste into your browser:
```
http://localhost:5173
```

✅ You should see the PDF Knowledge Assistant dashboard!

---

## 🎉 You're Done!

The frontend is now running locally. 

### What you can do:

1. **View Dashboard** - See system statistics (total chunks, embedding dimension)
2. **Upload Documents** - Add PDF files
3. **Search Documents** - Semantic search your uploaded PDFs
4. **Ask Questions (RAG)** - Get AI-powered answers with source citations
5. **Chat** - Multi-turn conversation with your documents
6. **Toggle Dark Mode** - Click the moon/sun icon in header
7. **View Navigation** - Click the hamburger menu

---

## 🔧 Make Changes

1. Edit files in the `src/` folder
2. Save the file
3. Browser auto-updates (hot reload)

Example: Edit `src/pages/Dashboard.jsx` and save

---

## 🛑 Stop the Server

Press `Ctrl + C` in the terminal

---

## ⚠️ Common Issues

### Issue: "Cannot find package.json"
**Solution**: Make sure you're in the right folder (Step 2)

### Issue: npm command not found
**Solution**: Install Node.js from https://nodejs.org

### Issue: Port 5173 already in use
**Solution**: Run: `npm run dev -- --port 5174`

### Issue: Page shows blank
**Solution**: Make sure backend is running at http://localhost:8000

---

## 📚 Next: Read the Guides

Once it's running, check these files:

1. **QUICKSTART_SETUP.md** - Detailed setup guide
2. **BUILD_DEPLOYMENT_GUIDE.md** - How to build & deploy
3. **DIRECTORY_AND_SETUP.md** - Folder structure
4. **FILES_INDEX.md** - What files do what

---

## 🎯 Done! 

You now have a working frontend development environment.

### Quick commands:

```bash
npm run dev        # Start dev server
npm run build      # Build for production
npm run lint       # Check code quality
npm run format     # Format code
npm run type-check # Check TypeScript
```

---

> **Total Time**: ~5 minutes  
> **Result**: Working development environment
> **Next**: Check the guides above!

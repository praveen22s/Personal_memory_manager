# Troubleshooting Guide

## Common Issues and Solutions

### PowerShell Execution Policy Error

**Error:**
```
npm : File C:\Program Files\nodejs\npm.ps1 cannot be loaded because running scripts is disabled on this system.
```

**Solutions:**

#### Solution 1: Use Current Directory (Recommended)
If you're already in the `frontend` directory, just run:
```powershell
npm install
```

Don't use `cd frontend` again - you're already there!

#### Solution 2: Change Execution Policy (One-time)
Run PowerShell **as Administrator**, then:
```powershell
Set-ExecutionPolicy RemoteSigned
```

This is safer than `Bypass` and allows local scripts to run.

#### Solution 3: Use Command Prompt (cmd)
Instead of PowerShell, use Command Prompt (cmd.exe):
```cmd
cd frontend
npm install
```

#### Solution 4: Use Node Directly
You can also use Node's npx:
```powershell
npx npm install
```

### Other Common Issues

#### Node.js Not Found
**Error:** `'node' is not recognized`

**Solution:**
1. Install Node.js from https://nodejs.org/
2. Restart your terminal
3. Verify: `node --version`

#### npm Not Found
**Error:** `'npm' is not recognized`

**Solution:**
1. Node.js includes npm
2. Reinstall Node.js
3. Verify: `npm --version`

#### Neo4j Connection Failed

**Error:** `Failed to connect to Neo4j`

**Solutions:**
1. Check if Neo4j is running:
   - Open Neo4j Desktop
   - Verify your database is "Active" (green)
2. Check `.env` file:
   ```env
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_password_here
   ```
3. Verify credentials match Neo4j settings
4. Check firewall isn't blocking port 7687

#### Port Already in Use

**Error:** `Port 8000 is already in use`

**Solutions:**
1. Find and kill the process:
   ```powershell
   # Find process on port 8000
   netstat -ano | findstr :8000
   
   # Kill the process (replace PID with actual number)
   taskkill /PID <PID> /F
   ```
2. Change port in `.env`:
   ```env
   PORT=8001
   ```

#### FFmpeg Not Found

**Error:** `ffmpeg not found` or audio errors

**Solution:**
1. Install FFmpeg:
   - Windows: Download from https://ffmpeg.org/download.html
   - Extract to `C:\ffmpeg`
   - Add `C:\ffmpeg\bin` to PATH
2. Verify:
   ```powershell
   ffmpeg -version
   ```
3. Restart terminal after adding to PATH

#### Python Module Not Found

**Error:** `ModuleNotFoundError: No module named 'X'`

**Solution:**
```powershell
# Reinstall dependencies
pip install -r requirements.txt

# If using virtual environment, activate it first
venv\Scripts\activate
```

#### Import Errors

**Error:** `ImportError: cannot import name 'X'`

**Solution:**
1. Check you're in the right directory:
   ```powershell
   cd D:\project_final_year
   python main.py
   ```
2. Verify all files exist:
   - `main.py`
   - `diary/__init__.py`
   - `diary/database.py`
   - etc.

#### Frontend Build Errors

**Error:** Module resolution errors in frontend

**Solution:**
```powershell
cd frontend
rm -r node_modules
rm package-lock.json
npm install
```

#### Audio Recording Not Working

**Error:** Microphone access denied

**Solution:**
1. Grant browser permission for microphone
2. Use HTTPS in production (microphone requires secure context)
3. Check browser settings allow microphone access

#### Image OCR Not Working

**Error:** OCR not available

**Solution:**
1. Install Tesseract:
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - Default path: `C:\Program Files\Tesseract-OCR\`
2. Verify installation:
   ```powershell
   tesseract --version
   ```

#### Slow Embedding Generation

**Observation:** First embedding takes long time

**Solution:**
This is normal! The model downloads on first use (~500MB).
Subsequent embeddings are fast.

#### Neo4j Vector Index Error

**Warning:** Vector index may not be available

**Solution:**
This is normal for older Neo4j versions. Search still works
using cosine similarity without the index.

#### npm Vulnerabilities

**Warning:** `npm audit` shows vulnerabilities

**Solution:**
These are often in dev dependencies. Safe to ignore for development:
```powershell
npm audit fix
```

### Getting More Help

1. **Check logs:**
   - Backend console output
   - Browser console (F12)
   - Neo4j logs

2. **Verify setup:**
   - Read `SETUP.md` carefully
   - Double-check `.env` configuration
   - Ensure all prerequisites installed

3. **Common mistakes:**
   - Wrong directory when running commands
   - Neo4j not started
   - Missing `.env` file
   - Python/Node not in PATH

### Quick Diagnostics

Run these to check everything:

```powershell
# Check Python
python --version

# Check Node.js
node --version
npm --version

# Check Neo4j connection
# (Open Neo4j Browser at http://localhost:7474)

# Check FFmpeg
ffmpeg -version

# List backend files
ls D:\project_final_year

# List frontend files
ls D:\project_final_year\frontend\src
```

---

**Still stuck?** Check the main documentation:
- `START_HERE.md` - Quick start
- `SETUP.md` - Detailed setup
- `README.md` - Project overview



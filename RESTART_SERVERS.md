# Restart Instructions

## The Issue

You're getting errors when creating entries or searching. The backend needs to be restarted with the fixes.

## Quick Fix

### Step 1: Stop Old Backend Servers

```powershell
# Find Python processes
Get-Process python | Stop-Process -Force
```

Or manually close the terminal windows running `python main.py`

### Step 2: Start Fresh Backend

```powershell
cd D:\project_final_year
python main.py
```

Wait until you see:
```
[OK] Connected to Neo4j
[OK] Backend services initialized
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Verify Frontend

Make sure frontend is still running on http://localhost:5173

If not, start it:
```powershell
cd frontend
cmd /c npm run dev
```

## What Was Fixed

1. ✅ Entry creation now handles embedding failures gracefully
2. ✅ Search has fallback to text search when embeddings unavailable
3. ✅ Better error messages
4. ✅ App works even without embedding model

## Test

1. Go to http://localhost:5173
2. Click "New Entry"
3. Add title and text
4. Click "Save Entry"
5. It should work now!

## Still Having Issues?

Check browser console (F12) for detailed error messages.

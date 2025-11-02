# How to Run the Application

## Quick Start

### Step 1: Start Backend Server

```powershell
python main.py
```

**First time**: The model will download (~420MB). This may take a few minutes.

You should see:
```
[OK] Connected to Neo4j
Loading embedding model...
[OK] Embedding model loaded
[OK] Backend services initialized
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Start Frontend Server

Open a **new terminal** and run:

```powershell
cd frontend
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
```

### Step 3: Open in Browser

Go to: **http://localhost:5173**

---

## Using the Run Scripts

### Windows:
```powershell
.\run.bat
```

### Mac/Linux:
```bash
chmod +x run.sh
./run.sh
```

This starts both servers automatically.

---

## Troubleshooting

### Model Download Issues

If the model fails to download:

```powershell
python fix_model_cache.py
python main.py
```

### Port Already in Use

If port 8000 or 5173 is busy:

1. Find the process:
   ```powershell
   netstat -ano | findstr :8000
   ```

2. Kill it or change port in `.env`

### Neo4j Connection

Make sure Neo4j is running:

```powershell
python test_connection.py
```

---

## What to Expect

### Backend Console:
```
INFO:     Started server process
INFO:     Waiting for application startup.
[OK] Connected to Neo4j
Loading embedding model...
Downloading model... (first time only)
[OK] Embedding model loaded
[OK] Backend services initialized
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Frontend Console:
```
VITE ready
Local: http://localhost:5173/
```

---

**Enjoy your Personal Semantic Diary!** 🎉

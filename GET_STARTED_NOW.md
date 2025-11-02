# 🚀 Get Started NOW!

## You're Almost There!

Your Personal Semantic Diary is ready to run. You just need to set your Neo4j password.

## Quick Start (2 Minutes)

### Step 1: Find Your Neo4j Password

1. **Open Neo4j Desktop** (if not already open)
2. **Look at your database** in the left sidebar
3. **Find the password field** and click "Show" to reveal it
4. **Copy that password** (you'll need it in Step 2)

> **Don't have Neo4j Desktop?**
> - Download from: https://neo4j.com/download/
> - Install it and create a new database
> - Set a password (remember it!)

### Step 2: Set Your Password

Run this command:

```powershell
.\UPDATE_PASSWORD.ps1
```

Enter your Neo4j password when prompted.

### Step 3: Test Connection

```powershell
python test_connection.py
```

You should see:
```
[OK] Neo4j connection successful!
```

### Step 4: Start the App!

```powershell
# Terminal 1 - Backend
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Step 5: Open in Browser

Go to: **http://localhost:5173**

---

## Alternative: Manual Password Update

1. Open `.env` file in this folder
2. Find line: `NEO4J_PASSWORD=password`
3. Change to: `NEO4J_PASSWORD=your_actual_password`
4. Save the file
5. Run `python test_connection.py` to test

---

## Need Help?

📖 **Read:** [NEO4J_SETUP.md](NEO4J_SETUP.md) for detailed instructions

🆘 **Common Issues:** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**That's it! You're ready to create your first semantic diary entry!** 🎉


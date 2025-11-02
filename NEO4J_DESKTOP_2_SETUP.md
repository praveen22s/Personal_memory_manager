# Neo4j Desktop 2 - Complete Setup Guide

## Where to Find Your Neo4j Connection Information

Neo4j Desktop 2 has a slightly different interface, but it's easy to find your connection details.

### Step 1: Open Neo4j Desktop 2

1. Launch **Neo4j Desktop 2** application
2. You'll see your databases listed on the left sidebar

### Step 2: Select Your Database

1. **Click on your database** in the left sidebar (or create a new one if needed)
2. The database details will show in the main panel

### Step 3: Find Connection Details

In Neo4j Desktop 2, look for these sections:

#### A. Database Status
- **Status**: Should show "Running" or "Active" (green)
- **Port**: Usually `7687` (Bolt port)

#### B. Connection Information

Look for one of these:

**Option 1: Connection URI**
- Find "**Connection URI**" or "**Bolt URI**"
- Should look like: `bolt://localhost:7687` or `neo4j://localhost:7687`

**Option 2: Connection Settings**
- Click on **"Details"** or **"Settings"** tab
- Look for:
  - **Bolt URL**: `bolt://localhost:7687`
  - **HTTP URL**: `http://localhost:7474`
  - **Username**: Usually `neo4j`
  - **Password**: Click "Show" to reveal it

**Option 3: Right-Click Menu**
1. **Right-click** on your database
2. Select **"Details"** or **"Settings"**
3. Find connection information

### Step 4: Get Your Password

**If you see a password field:**
1. Click the **eye icon** or **"Show"** button next to the password
2. Copy the password
3. Keep it safe!

**If password is hidden:**
1. You might need to **reset it** (right-click database → "Reset DBMS Password")
2. Set a new password you'll remember
3. Use that password in `.env`

### Step 5: Verify Port Number

- **Bolt Port**: Usually `7687` (for connections)
- **HTTP Port**: Usually `7474` (for browser)
- **Default URI**: `bolt://localhost:7687`

---

## Common Neo4j Desktop 2 Locations

### Database Panel
- **Left Sidebar**: Your databases list
- **Main Panel**: Database details when selected
- **Top Bar**: Connection status, start/stop buttons

### Settings/Details Panel
- Click **database name** → Shows details panel
- Look for **"Connection"** or **"Network"** section
- **"Settings"** tab → Connection configuration

### Browser Access
1. Click **"Open"** or **"Start"** button next to your database
2. Browser opens at `http://localhost:7474`
3. Login screen shows username (usually `neo4j`)
4. Enter password there - **use the same password in .env!**

---

## What to Update in .env File

Your `.env` file should have these values:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here
NEO4J_DATABASE=neo4j
```

### Explanation:

1. **NEO4J_URI**: Connection string
   - Usually: `bolt://localhost:7687`
   - If different port, use: `bolt://localhost:YOUR_PORT`

2. **NEO4J_USER**: Username
   - Usually: `neo4j`
   - Rarely changes

3. **NEO4J_PASSWORD**: Your database password
   - **This is what you need to find!**
   - Set when creating database or first login
   - Can be reset in Neo4j Desktop

4. **NEO4J_DATABASE**: Database name
   - Usually: `neo4j` (default database)
   - If you created a named database, use that name
   - Or use: `neo4j` for default

---

## Quick Update Methods

### Method 1: Use the Script (Easiest)

```powershell
.\UPDATE_PASSWORD.ps1
```

Enter your password when prompted!

### Method 2: Manual Edit

1. Open `.env` file in a text editor
2. Find: `NEO4J_PASSWORD=password`
3. Change to: `NEO4J_PASSWORD=your_actual_password`
4. Save file

### Method 3: PowerShell Command

```powershell
# Replace 'your_password' with actual password
$password = "your_password"
(Get-Content .env) -replace 'NEO4J_PASSWORD=.*', "NEO4J_PASSWORD=$password" | Set-Content .env
```

---

## Neo4j Desktop 2 Specific Steps

### If Database is Not Running:

1. **Select your database** in left sidebar
2. Click **green play button** (▶️) or **"Start"**
3. Wait for status to show **"Running"** or **"Active"**

### If You Don't Have a Database:

1. Click **"Add"** or **"+"** button
2. Select **"Create Local DBMS"**
3. Choose version (latest recommended)
4. Set name and password
5. Remember the password!
6. Click **"Create"**

### To Find Your Port:

1. Select database
2. Look at **"Details"** panel
3. Find **"Bolt Port"** or **"Port"** - usually `7687`
4. If different, update `NEO4J_URI` in `.env`:
   ```
   NEO4J_URI=bolt://localhost:YOUR_PORT
   ```

---

## Testing Your Connection

After updating `.env`:

```powershell
python test_connection.py
```

Should show:
```
[OK] Neo4j connection successful!
```

If it fails:
- Check password is correct
- Verify database is running
- Confirm port matches

---

## Troubleshooting Neo4j Desktop 2

### Can't Find Password?

**Solution**: Reset it
1. Right-click database
2. Select **"Reset DBMS Password"** or **"Change Password"**
3. Set new password
4. Update `.env` with new password

### Database Won't Start?

1. Check if another Neo4j instance is running
2. Look for error messages in Neo4j Desktop
3. Try stopping and starting again
4. Check if port 7687 is already in use

### Port Already in Use?

If port 7687 is taken:
1. In Neo4j Desktop 2, go to database **Settings**
2. Change **Bolt Port** to something else (e.g., `7688`)
3. Update `.env`: `NEO4J_URI=bolt://localhost:7688`
4. Restart database

---

## Visual Guide

```
Neo4j Desktop 2 Interface:

┌─────────────────────────────────────┐
│ [Database List]    │ [Details Panel] │
│                     │                 │
│ ► My Database       │ Name: My DB    │
│   Status: Running   │ Port: 7687     │
│   ▶ Start/Stop      │ Username: neo4j│
│                     │ Password: ***  │
│                     │ [Show] button  │
└─────────────────────────────────────┘
```

---

## Still Having Issues?

1. **Open Neo4j Browser**:
   - Click **"Open"** in Neo4j Desktop
   - Login with username `neo4j` and your password
   - If login works there, use same password in `.env`

2. **Check Logs**:
   - In Neo4j Desktop, look at **"Logs"** or **"Output"** tab
   - Check for connection errors

3. **Verify Installation**:
   - Make sure Neo4j Desktop 2 is fully installed
   - Try restarting the application
   - Restart your computer if needed

---

**Once you have the correct information in `.env`, your app will connect successfully!** 🎉

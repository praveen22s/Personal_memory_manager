# Where to Find Neo4j Connection Info in Desktop 2

## Quick Answer

**YES, update the `.env` file** with your Neo4j Desktop 2 connection details.

## What to Update

In your `.env` file, update these lines:

```env
NEO4J_URI=bolt://localhost:7687      # Usually doesn't change
NEO4J_USER=neo4j                      # Usually doesn't change  
NEO4J_PASSWORD=your_password_here    # YOU NEED TO FIND THIS!
NEO4J_DATABASE=neo4j                  # Usually doesn't change
```

**Most important**: You need to find your **PASSWORD**!

---

## Step-by-Step: Finding Info in Neo4j Desktop 2

### Step 1: Open Neo4j Desktop 2

Launch the application - you'll see a window with your databases.

### Step 2: Select Your Database

1. Look at the **left sidebar** - you'll see your database listed
2. **Click on your database name** to select it
3. Details will appear in the main panel on the right

### Step 3: Find Connection Info

Neo4j Desktop 2 interface typically shows:

#### Location 1: Main Details Panel (Most Common)

When you click your database, you'll see:
- **Status**: Running/Stopped
- **Connection URL**: `bolt://localhost:7687` (or similar)
- **Username**: Usually `neo4j`
- **Password**: Hidden (click "Show" or eye icon to reveal)

#### Location 2: Settings Tab

1. Click on your database
2. Look for **"Settings"** or **"Details"** tab
3. Click it to see:
   - Port number
   - Username
   - Password (click "Show" to reveal)

#### Location 3: Right-Click Menu

1. **Right-click** on your database name
2. Select **"Details"** or **"Settings"**
3. Find connection information

### Step 4: Get Your Password

**Option A: Show Existing Password**
1. Find the password field (usually shows `••••••••`)
2. Click **"Show"** button or **eye icon** 👁️
3. Password will be revealed
4. **Copy it!**

**Option B: Reset Password**
1. Right-click your database
2. Select **"Reset DBMS Password"** or **"Change Password"**
3. Enter a new password
4. **Remember it!**

### Step 5: Check Port Number

- **Bolt Port**: Usually `7687` (this is what you need)
- **HTTP Port**: Usually `7474` (for browser, not needed)

If you see something like `bolt://localhost:7887`, then port is `7887`.

---

## Where Each Value Comes From

| .env Setting | Where to Find | Usually |
|--------------|---------------|---------|
| `NEO4J_URI` | Connection URL in details | `bolt://localhost:7687` |
| `NEO4J_USER` | Username in details | `neo4j` |
| `NEO4J_PASSWORD` | Password field (click Show) | **You need to find this!** |
| `NEO4J_DATABASE` | Database name | `neo4j` (default) |

---

## Easy Method: Use Neo4j Browser

1. In Neo4j Desktop 2, click **"Open"** button next to your database
2. Browser opens at `http://localhost:7474`
3. Login screen appears:
   - **Username**: `neo4j`
   - **Password**: Enter what works here
4. **If login works, use that same password in `.env`!**

---

## Quick Update Script

Instead of manual editing, use:

```powershell
.\UPDATE_PASSWORD.ps1
```

Enter your password when prompted - it will update `.env` automatically!

---

## Visual Guide for Desktop 2

```
Neo4j Desktop 2 Window:

┌─────────────────────────────────────────────┐
│ [Database List] │ [Details Panel]           │
│                │                            │
│ ► My Database │ Name: My Database          │
│   ▶ Running    │ Status: Running           │
│                │                            │
│                │ Connection:                │
│                │   URI: bolt://localhost:   │
│                │         7687               │
│                │   User: neo4j             │
│                │   Pass: •••••••• [Show]   │
│                │                            │
│                │ Ports:                    │
│                │   Bolt: 7687              │
│                │   HTTP: 7474              │
└─────────────────────────────────────────────┘
```

---

## What if Database is Not Running?

1. **Select your database** in left sidebar
2. Click the **▶ Play button** or **"Start"** button
3. Wait for status to change to **"Running"** (green)
4. Then get your connection info

---

## Testing After Update

Once you update `.env`, test the connection:

```powershell
python test_connection.py
```

Should show:
```
[OK] Neo4j connection successful!
```

---

## Default Values (Most Likely)

If you're not sure, try these defaults in `.env`:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password        # Try this first, or what you set
NEO4J_DATABASE=neo4j
```

Most common passwords:
- `password`
- `neo4j` (but needs reset on first use)
- `admin`
- Whatever you set when creating the database

---

## Still Confused?

1. **Open Neo4j Browser** (click "Open" in Desktop)
2. **Try to login** with username `neo4j`
3. **If password works there**, use that same password in `.env`
4. Run `python test_connection.py` to verify

---

**Once `.env` has the correct password, your app will connect!** ✅

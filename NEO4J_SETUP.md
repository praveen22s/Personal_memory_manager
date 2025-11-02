# Neo4j Setup Instructions

## The Problem

Your Neo4j password in `.env` doesn't match your actual Neo4j database password.

## Solution: Find Your Neo4j Password

### Method 1: From Neo4j Desktop

1. **Open Neo4j Desktop**
2. **Click on your database** in the left sidebar
3. **Look for the database settings** - you'll see:
   - Username: `neo4j`
   - Password: `*******` (hidden)

4. **Click the "Show" button** next to the password field to reveal it

### Method 2: First Time Setup

If you're setting up for the first time:

1. Open **Neo4j Desktop**
2. If prompted to reset password:
   - Set password to something you'll remember (e.g., `password`, `admin`, etc.)
   - Remember this password!

### Method 3: Reset Password

If you forgot your password:

1. **Open Neo4j Desktop**
2. **Right-click on your database**
3. **Select "Reset DBMS Password"**
4. **Set a new password** (remember it!)

## Update Your .env File

Once you have your password:

1. Open `.env` in this project folder
2. Find this line:
   ```
   NEO4J_PASSWORD=password
   ```
3. Replace `password` with your actual Neo4j password:
   ```
   NEO4J_PASSWORD=your_actual_password_here
   ```
4. Save the file

## Quick Setup Script

Or run this PowerShell command to update it:

```powershell
$password = Read-Host "Enter your Neo4j password"
(Get-Content .env) -replace 'NEO4J_PASSWORD=.*', "NEO4J_PASSWORD=$password" | Set-Content .env
Write-Host "Password updated in .env file!"
```

## Test Connection

After updating the password:

```powershell
python test_connection.py
```

You should see:
```
[OK] Neo4j connection successful!
```

## Still Having Issues?

### Check Neo4j Browser

1. In Neo4j Desktop, click **Open** or **Start**
2. Neo4j Browser opens at `http://localhost:7474`
3. Login with username `neo4j` and your password
4. If you can login there, use that same password in `.env`

### Verify Database is Active

- In Neo4j Desktop, your database should show **"Active"** in green
- If it's not active, click the **play button** to start it

### Common Passwords to Try

If you don't remember setting a password, common defaults are:
- `neo4j` (original default, needs reset on first login)
- `password`
- `admin`
- `root`
- `1234`

---

**Once you have the correct password, the app should start successfully!**


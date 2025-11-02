# 🚀 GitHub Upload Guide

## Step-by-Step Instructions

### Step 1: Initialize Git Repository

```powershell
# Navigate to project directory
cd D:\project_final_year

# Initialize git (if not already initialized)
git init
```

### Step 2: Add All Files

```powershell
# Add all files to git
git add .

# Check what will be committed
git status
```

### Step 3: Create Initial Commit

```powershell
# Create your first commit
git commit -m "Initial commit: Personal Semantic Diary - AI-powered diary with semantic graph storage"
```

### Step 4: Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click **"+"** → **"New repository"**
3. Repository name: `personal-semantic-diary` (or your preferred name)
4. Description: `AI-powered personal diary with semantic graph storage and multi-modal input`
5. Choose **Public** or **Private**
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click **"Create repository"**

### Step 5: Link Local Repository to GitHub

GitHub will show you commands. Use these:

```powershell
# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/personal-semantic-diary.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 6: Verify Upload

1. Go to your GitHub repository page
2. Refresh and verify all files are uploaded
3. Check that README.md displays correctly

## Alternative: Using GitHub CLI

If you have GitHub CLI installed:

```powershell
# Create and push repository
gh repo create personal-semantic-diary --public --source=. --remote=origin --push
```

## What Gets Uploaded

✅ **Will be uploaded**:
- All Python code (`diary/`, `main.py`)
- Frontend code (`frontend/src/`)
- Documentation files (`.md` files)
- Configuration files (`package.json`, `vite.config.js`)
- `.gitignore`
- `requirements.txt`
- `LICENSE`

❌ **Will NOT be uploaded** (thanks to .gitignore):
- `node_modules/`
- `venv/` or `env/`
- `uploads/` directory
- `.env` file (your secrets!)
- `__pycache__/`
- Media files (`*.mp3`, `*.wav`, `*.jpg`, etc.)

## Updating Your Repository

After making changes:

```powershell
# Check what changed
git status

# Add changes
git add .

# Commit changes
git commit -m "Description of your changes"

# Push to GitHub
git push
```

## Adding a GitHub Actions Badge

If you want to add badges to your README, you can add:

```markdown
![GitHub](https://img.shields.io/github/license/YOUR_USERNAME/personal-semantic-diary)
![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/personal-semantic-diary)
```

## Repository Settings

After uploading, consider:

1. **Add topics/tags**: Go to repository → About → Add topics:
   - `diary`
   - `neo4j`
   - `fastapi`
   - `react`
   - `ai`
   - `semantic-search`
   - `graph-database`

2. **Enable GitHub Pages** (optional): For hosting documentation

3. **Add repository description**: "AI-powered personal diary with semantic graph storage"

## Troubleshooting

### Authentication Issues

If `git push` asks for credentials:

**Option 1: Use Personal Access Token**
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` permissions
3. Use token as password when pushing

**Option 2: Use SSH**
```powershell
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub: Settings → SSH and GPG keys
# Change remote URL
git remote set-url origin git@github.com:YOUR_USERNAME/personal-semantic-diary.git
```

### Large Files

If you get errors about large files:
```powershell
# Check for large files
git ls-files | ForEach-Object {Get-Item $_} | Sort-Object length -Descending | Select-Object -First 10

# Remove large files if needed
git rm --cached large_file.txt
```

## Quick Commands Reference

```powershell
# Check status
git status

# See what changed
git diff

# Add specific file
git add path/to/file

# Commit with message
git commit -m "Your message here"

# Push to GitHub
git push

# Pull latest changes (if working on multiple machines)
git pull

# See commit history
git log --oneline
```

---

**Your project is now on GitHub! 🎉**

Share the repository link: `https://github.com/YOUR_USERNAME/personal-semantic-diary`

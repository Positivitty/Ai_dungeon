# Setup Checklist - Do This First! ✅

Follow these steps in order. Check off each one as you complete it.

## Part 1: Install Tools (15 minutes)

### [ ] 1. Install VS Code
- Go to https://code.visualstudio.com/
- Download for your OS
- Run installer
- **Verify**: Open VS Code - you should see a welcome screen

### [ ] 2. Install Python Extensions in VS Code
- Open VS Code
- Click Extensions icon (left sidebar, looks like squares)
- Search "Python"
- Install "Python" by Microsoft
- Install "Pylance" by Microsoft
- **Verify**: You see both extensions in your installed list

### [ ] 3. Install Git
- Go to https://git-scm.com/downloads
- Download for your OS
- Run installer (use default settings)
- **Verify**: Open terminal and type `git --version`

## Part 2: Set Up Project (10 minutes)

### [ ] 4. Open Project in VS Code
```bash
# Navigate to your project
cd path/to/ai-dungeon-crawler

# Open in VS Code
code .
```
**Verify**: You see your project files in VS Code's file explorer

### [ ] 5. Create Virtual Environment
In VS Code terminal (Ctrl+` to open):

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Verify**: Your terminal prompt shows `(venv)` at the start

### [ ] 6. Install Dependencies
```bash
pip install -r requirements.txt
```

**Verify**: No error messages, packages install successfully

### [ ] 7. Test the Game!
```bash
python main.py
```

**Verify**: 
- Game window opens
- You see "AI Dungeon Crawler" title
- You can move with WASD
- You can attack with SPACE
- Three enemies appear and move

### [ ] 8. Initialize Git
```bash
git init
git add .
git commit -m "Initial commit: Working game foundation"
```

**Verify**: Type `git log` - you should see your commit

## Part 3: GitHub Setup (Optional but Recommended - 5 minutes)

### [ ] 9. Create GitHub Account
- Go to https://github.com/
- Sign up (free)
- Verify email

### [ ] 10. Create Repository
- Click "+" in top right → "New repository"
- Name: `ai-dungeon-crawler`
- Keep it Public (to showcase your work!)
- DON'T initialize with README (you already have one)
- Click "Create repository"

### [ ] 11. Connect and Push
```bash
git remote add origin https://github.com/YOUR-USERNAME/ai-dungeon-crawler.git
git branch -M main
git push -u origin main
```

**Verify**: Refresh GitHub page - you see all your code!

## Part 4: Configure VS Code (5 minutes)

### [ ] 12. Select Python Interpreter
- Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows)
- Type "Python: Select Interpreter"
- Choose the one that shows `(venv)`

**Verify**: Bottom-left of VS Code shows Python version with `venv`

### [ ] 13. Create Launch Configuration
Create file `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run Game",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal"
        }
    ]
}
```

**Verify**: Press F5 - game runs with debugger attached!

## Part 5: First Development Cycle (10 minutes)

### [ ] 14. Make a Small Change
Open `config.py` and change:
```python
PLAYER_SPEED = 5  # Was 3
```

### [ ] 15. Test It
```bash
python main.py
```

**Verify**: Player moves faster!

### [ ] 16. Commit the Change
```bash
git add config.py
git commit -m "tweak: Increase player speed for testing"
```

**Verify**: Type `git log` - you see 2 commits now

### [ ] 17. Push to GitHub
```bash
git push
```

**Verify**: Check GitHub - your change is there!

## ✅ You're Ready!

If you checked all boxes, you have a **professional development environment**!

## 🎯 Your Workflow From Now On

Every time you code:

1. **Open VS Code**
   ```bash
   cd ai-dungeon-crawler
   code .
   ```

2. **Activate virtual environment** (if not auto-activated)
   ```bash
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Make changes** in VS Code

4. **Test frequently**
   ```bash
   python main.py
   ```

5. **Commit when working**
   ```bash
   git add .
   git commit -m "feat: Add dungeon generation"
   git push
   ```

## 🐛 Troubleshooting

**"python: command not found"**
→ Try `python3` instead of `python`

**"No module named pygame"**
→ Make sure virtual environment is activated (should see `(venv)`)
→ Run `pip install -r requirements.txt` again

**Game won't run**
→ Check terminal for error messages
→ Make sure you're in the `ai-dungeon-crawler` directory
→ Try `python3 main.py` instead

**Git errors**
→ Make sure you initialized git (`git init`)
→ Check you're in the right directory (`pwd` or `cd`)

**VS Code can't find Python**
→ Install Python extension
→ Restart VS Code
→ Select interpreter (Cmd/Ctrl+Shift+P → "Python: Select Interpreter")

## 📚 Next Steps

Once setup is complete:

1. Read `DEVELOPMENT_WORKFLOW.md` for best practices
2. Start adding features (dungeon generation is next!)
3. Test after every change
4. Commit frequently
5. Push to GitHub regularly

## 💡 Pro Tips

- **Save often**: Cmd/Ctrl+S should be muscle memory
- **Test often**: Run game every 10-15 minutes
- **Commit often**: After each working feature
- **Read errors**: They tell you exactly what's wrong
- **Use breakpoints**: Click left margin in VS Code to debug

---

**Congratulations!** You're now set up like a professional developer. 🎉

No more "compile and pray" - you have real tools and a real workflow!

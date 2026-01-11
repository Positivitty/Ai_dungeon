# Professional Development Workflow for AI Dungeon Crawler

## 🎯 Industry Standard Process

Professional game developers DON'T compile everything at once. They use an **iterative development cycle** with proper tools.

## 📋 The Right Way to Develop

### 1. Use Version Control (Git)

**Why**: Track changes, experiment safely, collaborate, showcase your work

```bash
# Initialize git repository
cd ai-dungeon-crawler
git init

# Create .gitignore first
echo "__pycache__/
*.pyc
*.pyo
*.pkl
saves/
.DS_Store
*.swp" > .gitignore

# Initial commit
git add .
git commit -m "Initial commit: Project foundation with player and enemies"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/ai-dungeon-crawler.git
git push -u origin main
```

**Industry Practice**: Commit after each feature
```bash
git add game/dungeon.py
git commit -m "feat: Add procedural dungeon generation"

git add game/items.py
git commit -m "feat: Implement health potion pickups"
```

### 2. Use a Proper Code Editor (Not a Compiler!)

**Industry Standard Tools**:

✅ **VS Code** (Most Popular)
- Free, powerful, Python extensions
- Built-in terminal
- Git integration
- Debugging tools

✅ **PyCharm Community** (Python-Specific)
- Best Python IDE
- Excellent debugging
- Free version available

✅ **Sublime Text / Vim** (Lightweight)
- Fast, minimal
- Good for quick edits

❌ **DON'T use**: Online compilers, basic text editors without extensions

### 3. Set Up a Virtual Environment

**Why**: Isolate project dependencies, avoid version conflicts

```bash
# Create virtual environment
cd ai-dungeon-crawler
python -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Your terminal should now show (venv) at the start
```

**Industry Practice**: ALWAYS use virtual environments for Python projects

### 4. Iterative Development Cycle

```
┌─────────────────────────────────────────────┐
│                                             │
│  1. PLAN                                    │
│     "I'm going to add dungeon generation"   │
│                                             │
│  2. WRITE CODE                              │
│     Edit files in VS Code                   │
│                                             │
│  3. TEST IMMEDIATELY                        │
│     python main.py                          │
│     (Run game, check if it works)           │
│                                             │
│  4. DEBUG IF NEEDED                         │
│     Read error messages                     │
│     Add print statements                    │
│     Use VS Code debugger                    │
│                                             │
│  5. COMMIT                                  │
│     git add .                               │
│     git commit -m "feat: Add feature X"     │
│                                             │
│  6. REPEAT                                  │
│     Back to step 1 for next feature         │
│                                             │
└─────────────────────────────────────────────┘
```

### 5. Use the Terminal Workflow

**Industry developers work from the terminal**:

```bash
# Open your project
cd ai-dungeon-crawler

# Edit code in VS Code
code .

# Run the game frequently while developing
python main.py

# Run it again after each change
python main.py

# Check for errors
python -m py_compile main.py

# Run with verbose output for debugging
python -v main.py
```

**NOT**: Write all code → Compile once → Hope it works

**YES**: Write small piece → Test → Fix → Repeat

## 🛠️ Recommended Setup (Step by Step)

### Step 1: Install VS Code
1. Download from https://code.visualstudio.com/
2. Install Python extension (search "Python" in extensions)
3. Install Pylance extension (better autocomplete)

### Step 2: Open Project in VS Code
```bash
cd ai-dungeon-crawler
code .
```

### Step 3: Set Up Terminal in VS Code
- Press `` Ctrl+` `` to open integrated terminal
- You can run `python main.py` right from VS Code!

### Step 4: Configure Python Interpreter
- Press `Cmd/Ctrl + Shift + P`
- Type "Python: Select Interpreter"
- Choose your virtual environment

### Step 5: Enable Debugging
Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Run Game",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal"
        }
    ]
}
```

Now you can press F5 to run with debugging!

## 🔄 Daily Development Workflow

### Morning Session:
```bash
# 1. Open project
cd ai-dungeon-crawler
code .

# 2. Activate virtual environment
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

# 3. Pull latest changes (if using GitHub)
git pull

# 4. Check what you're working on
# Look at your TODO list or project board
```

### While Coding:
```bash
# Test frequently - every 5-10 minutes!
python main.py

# If you add a new file:
python -m py_compile game/new_file.py  # Check for syntax errors

# Commit working features
git add game/dungeon.py
git commit -m "feat: Add room generation"
```

### End of Session:
```bash
# 1. Make sure everything works
python main.py

# 2. Commit your progress
git add .
git commit -m "wip: Working on dungeon generation"

# 3. Push to GitHub (backup!)
git push

# 4. Deactivate virtual environment
deactivate
```

## 🐛 Debugging Like a Pro

### Level 1: Print Statements
```python
def generate_room(self):
    print(f"Generating room at position {self.x}, {self.y}")
    print(f"Enemy count: {len(self.enemies)}")
    # ... rest of code
```

### Level 2: VS Code Debugger
1. Click left margin to set breakpoint (red dot)
2. Press F5 to run in debug mode
3. Game pauses at breakpoint
4. Inspect variables in sidebar
5. Step through code with F10

### Level 3: Logging Module
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def update(self):
    logger.debug(f"Player position: {self.x}, {self.y}")
    logger.info("Enemy defeated!")
```

## 📊 Project Management (Industry Standard)

### Option 1: GitHub Issues (Simple)
```
Create issues for each task:
- [ ] Issue #1: Implement dungeon generation
- [ ] Issue #2: Add health potion pickups  
- [ ] Issue #3: Polish combat animations
```

### Option 2: Trello/Notion (Visual)
```
Columns:
├─ TODO
│  └─ Dungeon generation
│  └─ Item system
├─ IN PROGRESS
│  └─ Combat polish
└─ DONE
   └─ Player class
   └─ Enemy AI
```

### Option 3: GitHub Projects (Professional)
- Kanban board built into GitHub
- Links to code commits
- Track progress visually

## ⚡ Best Practices Summary

### ✅ DO:
- **Test constantly** - Run game every 10-15 minutes
- **Commit often** - After each working feature
- **Use version control** - Git from day one
- **Virtual environment** - Isolate dependencies
- **Code editor with extensions** - VS Code or PyCharm
- **Debug with tools** - Use VS Code debugger
- **Read error messages** - They tell you exactly what's wrong
- **Start small** - One feature at a time

### ❌ DON'T:
- **Write all code then test** - Recipe for disaster
- **Skip version control** - You'll regret it
- **Use online compilers** - Not for serious development
- **Install packages globally** - Use virtual environments
- **Ignore errors** - Fix them immediately
- **Work without backups** - Use Git + GitHub

## 🎯 Your First Week Workflow

### Day 1: Setup
```bash
✓ Install VS Code + Python extension
✓ Create virtual environment
✓ Initialize Git repository
✓ Create GitHub repository
✓ Test current code (python main.py)
✓ Make first commit
```

### Day 2-3: Dungeon Generation
```bash
1. Create game/dungeon.py
2. Test with simple rectangle room (python main.py)
3. Commit
4. Add random room generation
5. Test (python main.py)
6. Commit
7. Add floor transitions
8. Test (python main.py)
9. Commit
```

### Day 4-5: Items System
```bash
1. Create game/items.py
2. Test spawning one potion
3. Commit
4. Add pickup collision
5. Test
6. Commit
7. Add inventory display
8. Test
9. Commit
```

See the pattern? **Small steps + frequent testing + commits**

## 🚀 Advanced: Continuous Integration (Later)

Once you're comfortable, add automated testing:

**GitHub Actions** (runs tests automatically):
```yaml
# .github/workflows/test.yml
name: Test Game

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest tests/
```

## 📚 Learning Resources

**Git & GitHub**:
- GitHub's Git Tutorial: https://try.github.io/
- Git Documentation: https://git-scm.com/doc

**VS Code**:
- Python in VS Code: https://code.visualstudio.com/docs/python/python-tutorial
- Debugging: https://code.visualstudio.com/docs/editor/debugging

**Python Virtual Environments**:
- Official Docs: https://docs.python.org/3/tutorial/venv.html

## 💡 Key Takeaway

**Industry developers DON'T:**
- Write all code in one go
- Use online compilers for real projects
- Test only at the end

**Industry developers DO:**
- Use proper IDEs (VS Code, PyCharm)
- Test constantly (every 10-15 minutes)
- Use Git for version control
- Work in virtual environments
- Debug with real tools
- Commit frequently
- Follow the "red-green-refactor" cycle

---

## 🎯 Your Next Steps

1. **Install VS Code** + Python extension
2. **Open your project** in VS Code
3. **Create virtual environment**
4. **Initialize Git** repository
5. **Make your first commit**
6. **Start coding** with frequent testing

This is exactly how professional game developers and ML engineers work!

**Questions to ask yourself while coding:**
- Does it run? (Test frequently)
- Did I commit? (After each feature)
- Can I explain this code? (Write clear comments)
- What breaks if I change this? (Think about dependencies)

Good luck! 🚀

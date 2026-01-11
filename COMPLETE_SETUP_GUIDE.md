# AI Dungeon Crawler - Complete Setup Guide

## Option 1: Download the Full Folder (Recommended)

1. Click "Download" on `ai-dungeon-crawler-fresh` folder
2. Extract the ZIP file
3. Open terminal and navigate to the folder:
   ```bash
   cd path/to/ai-dungeon-crawler-fresh
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt --break-system-packages
   ```
5. Run the game:
   ```bash
   python main.py
   ```

## Option 2: Download Individual Files

If the folder download isn't working, download these files individually:

### Required Files:
1. **main.py** - Main game file
2. **config.py** - Game configuration
3. **requirements.txt** - Dependencies
4. **player.py** - Player class (put in `game/` folder)
5. **enemies.py** - Enemy classes (put in `game/` folder)

### File Structure to Create:
```
your-project-folder/
├── main.py
├── config.py
├── requirements.txt
└── game/
    ├── __init__.py          (create empty file)
    ├── player.py
    └── enemies.py
```

### Steps:
```bash
# 1. Create project folder
mkdir ai-dungeon-crawler
cd ai-dungeon-crawler

# 2. Create game subfolder
mkdir game

# 3. Download files from Claude and place them:
#    - main.py → in ai-dungeon-crawler/
#    - config.py → in ai-dungeon-crawler/
#    - requirements.txt → in ai-dungeon-crawler/
#    - player.py → in ai-dungeon-crawler/game/
#    - enemies.py → in ai-dungeon-crawler/game/

# 4. Create empty __init__.py file
touch game/__init__.py

# 5. Install dependencies
pip install -r requirements.txt --break-system-packages

# 6. Run!
python main.py
```

## Option 3: Copy-Paste Code

If downloads aren't working at all, I can provide the code for each file and you can copy-paste into new files.

## Troubleshooting

**"No module named pygame"**
→ Make sure you ran: `pip install -r requirements.txt --break-system-packages`

**"No module named game"**
→ Make sure you created the `game/` folder and `game/__init__.py` file

**"python: command not found"**
→ Try `python3` instead of `python`

**Game window doesn't open**
→ Make sure you have Python 3.9-3.11 installed
→ Check terminal for error messages

## What the Game Does Right Now

- You control a character with WASD/arrows
- Fight 3 enemies (Goblin, Skeleton, Archer)
- Attack with SPACE
- Enemies have AI that chases/attacks you
- Health bars show damage
- Press ESC to quit

## Next Steps After Setup

1. **Test it works**: Run `python main.py` and move around
2. **Set up Git**: `git init` to start tracking changes
3. **Read the guides**: Check the documentation files
4. **Start building**: Add dungeon generation next!

## Need Help?

If you're still having issues, let me know:
- What error message you're seeing
- What operating system you're using (Mac/Windows/Linux)
- Which Python version (`python --version`)

I'll help you get it running!

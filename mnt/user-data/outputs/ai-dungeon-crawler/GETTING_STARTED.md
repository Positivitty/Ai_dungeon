# Getting Started with AI Dungeon Crawler

Welcome! This guide will help you get your project up and running.

## Step 1: Set Up Your Environment

### Option A: Local Setup (Recommended)
```bash
# 1. Extract the project folder
# 2. Open terminal in the project directory
# 3. Install dependencies
pip install pygame==2.5.2 numpy==1.24.3

# For Phase 2 (AI training), you'll also need:
pip install gymnasium==0.29.1 stable-baselines3==2.1.0 torch==2.1.0
```

### Option B: Use requirements.txt
```bash
pip install -r requirements.txt
```

## Step 2: Test Your Setup

Run the test script to verify everything works:
```bash
python test_setup.py
```

You should see:
- ✓ pygame imported successfully
- ✓ Config loaded successfully
- ✓ Game classes imported successfully
- ✓ Pygame window created successfully

## Step 3: Run the Base Game

```bash
python main.py
```

You'll see a basic window with "AI Dungeon Crawler" title. Press ESC to quit.

**This is normal!** We're building step-by-step.

## Step 4: What's Been Built So Far

✅ **Complete:**
- Project structure and organization
- Configuration system (config.py)
- Player class with equipment system
- 5 enemy classes (Goblin, Skeleton, Archer, Slime, Boss)
- Basic game loop and window

🔨 **Next to Build (Your Tasks):**
- Dungeon generation (random rooms and floors)
- Combat system (attack collision, damage)
- UI rendering (health bars, status display)
- Manual controls for testing (WASD, spacebar)
- Items system (health potions)

## Step 5: Development Workflow

### Daily Development Process:
1. Pick ONE feature from the checklist below
2. Implement it in small steps
3. Test frequently (run `python main.py`)
4. Commit your changes (if using git)
5. Move to next feature

### Phase 1 Checklist (Weeks 1-2)

**Week 1: Core Mechanics**
- [ ] Create `game/dungeon.py` - room and floor generation
- [ ] Create `game/combat.py` - attack detection and damage
- [ ] Update `main.py` - add manual controls (WASD, spacebar)
- [ ] Test: Can move player and spawn enemies

**Week 2: Polish Core Game**
- [ ] Create `game/ui.py` - render health bars, floor counter
- [ ] Create `game/items.py` - health potion pickups
- [ ] Add enemy spawning logic
- [ ] Test: Full playthrough with keyboard controls

### Example: Implementing Manual Controls

Here's how you'd add WASD controls to `main.py`:

```python
def handle_events(self):
    """Handle pygame events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
    
    # WASD movement (in update method)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        self.player.move(0, -1)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        self.player.move(0, 1)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        self.player.move(-1, 0)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        self.player.move(1, 0)
    if keys[pygame.K_SPACE]:
        self.player.attack()
```

## Step 6: Understanding the Code

### Key Files to Know:

**config.py** - All game constants
- Modify stats here (enemy HP, damage, etc.)
- Change colors, speeds, sizes
- Adjust weapon/armor balance

**game/player.py** - Player character
- Equipment system
- Movement and combat actions
- Health and inventory management

**game/enemies.py** - Enemy AI
- Different enemy types
- Simple chase behavior
- Attack patterns

**main.py** - Game loop
- Event handling
- State management
- Rendering

### Testing Individual Components

You can test classes in isolation:

```python
# test_player.py
from game import Player

player = Player(100, 100, weapon='sword', armor='heavy')
print(f"Created: {player.weapon} + {player.armor}")
print(f"Stats: {player.hp} HP, {player.speed} speed")

# Move player
player.move(1, 0)  # Move right
print(f"Position: ({player.x}, {player.y})")

# Simulate damage
player.take_damage(30)
print(f"HP after damage: {player.hp}")
```

## Step 7: Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'pygame'"
**Solution:** Run `pip install pygame==2.5.2`

### Issue: "ImportError: cannot import name 'Player'"
**Solution:** Make sure you're in the project directory and `game/__init__.py` exists

### Issue: Window opens and immediately closes
**Solution:** Normal! The game loop runs until ESC is pressed. Add a pause or handle events properly.

### Issue: Black screen when running
**Solution:** This is expected! You need to add rendering code in `render_game()` method.

## Step 8: Next Immediate Task

**Your first coding task:** Implement dungeon generation

Create `game/dungeon.py`:
```python
"""
Dungeon generation
Creates rooms and floors with random enemies
"""

import random
from config import *

class Room:
    def __init__(self, floor_num):
        self.floor = floor_num
        self.width = ROOM_WIDTH
        self.height = ROOM_HEIGHT
        self.enemies = []
        self.items = []
        self.completed = False
    
    def spawn_enemies(self):
        """Spawn random enemies based on floor"""
        # Implementation here
        pass

class Dungeon:
    def __init__(self):
        self.current_floor = 1
        self.current_room = 0
        self.rooms = []
        
    def generate_floor(self, floor_num):
        """Generate rooms for a floor"""
        # Implementation here
        pass
```

## Step 9: Development Resources

### When You Get Stuck:
1. Check the **PRD** (AI_Dungeon_Crawler_PRD.md) for specifications
2. Look at **config.py** for available constants
3. Review existing code (player.py, enemies.py) for patterns
4. Test small pieces in isolation
5. Ask specific questions

### Helpful Pygame Patterns:
- `pygame.Rect.colliderect()` - Check collision between rectangles
- `pygame.draw.rect()` - Draw rectangles (for prototyping)
- `pygame.time.Clock.tick(FPS)` - Limit frame rate
- `dt = clock.tick(60) / 1000.0` - Get delta time in seconds

## Step 10: Stay Focused on MVP

Remember the PRD's critical notes:
- ✅ 2 weapons, 2 armors (4 builds total)
- ✅ 4 enemy types + 1 boss
- ✅ Health potions only
- ❌ No magic/mana system yet (Phase 2)
- ❌ No traps/hazards yet (Phase 2)

Build the minimal viable version first, then add features!

---

## Quick Command Reference

```bash
# Run game
python main.py

# Test setup
python test_setup.py

# Install dependencies
pip install -r requirements.txt

# Check Python version (need 3.9-3.11)
python --version
```

---

## You're Ready!

Your project is set up and ready for development. Start with dungeon generation, then add combat, then polish the UI. Take it one feature at a time.

Good luck building your AI companion game! 🎮🤖

---

**Need help?** Reference the PRD for detailed specifications, or test individual components before integrating them into the main game loop.

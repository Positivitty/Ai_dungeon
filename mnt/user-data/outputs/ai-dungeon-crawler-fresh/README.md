# AI Dungeon Crawler

A 2D dungeon crawler where you teach an AI companion to fight through reinforcement learning!

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt --break-system-packages

# Run the game
python main.py
```

## Controls

- **WASD / Arrow Keys**: Move
- **SPACE**: Attack
- **P**: Use Health Potion
- **ESC**: Quit

## Current Status

Phase 1 (80% complete):
- ✅ Player with equipment system
- ✅ 4 enemy types with AI
- ✅ Combat system
- ⏳ Dungeon generation (next)
- ⏳ Items and pickups

## Project Structure

```
ai-dungeon-crawler-fresh/
├── main.py              # Run this!
├── config.py            # Game settings
├── requirements.txt     # Dependencies
├── game/
│   ├── player.py        # Player class
│   └── enemies.py       # Enemy classes
├── ai/                  # Phase 2: RL training
└── tutorial/            # Phase 3: Teaching system
```

## What You Can Do

Right now you can manually control the player to test mechanics:
- Move around with WASD
- Fight 3 enemies (Goblin, Skeleton, Archer)
- Test combat system
- Try different equipment

## Next Steps

1. Add dungeon generation
2. Add health potion pickups
3. Polish combat
4. Then: Add AI training (Phase 2)!

See the documentation files for detailed guides on development workflow and setup.

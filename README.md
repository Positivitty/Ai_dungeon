# AI Dungeon Crawler

A 2D dungeon crawler where you teach an AI companion to fight through reinforcement learning!

## 🎮 About

Watch your AI grow from a fumbling beginner to a skilled dungeon crawler. You'll teach it basic skills through tutorials, then watch as it learns through trial and error, providing commentary on what it's learning along the way.

## 📋 Requirements

- Python 3.9-3.11
- pip (Python package manager)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt --break-system-packages
```

### 2. Run the Game

```bash
python main.py
```

## 🎯 Controls (Phase 1 - Manual Play)

- **WASD / Arrow Keys**: Move
- **SPACE**: Attack
- **P**: Use Health Potion
- **ESC**: Quit

## 🏗️ Project Structure

```
ai-dungeon-crawler/
├── main.py              # Game entry point
├── config.py            # Game settings
├── game/                # Game logic
│   ├── player.py        # Player character
│   ├── enemies.py       # Enemy classes
│   ├── dungeon.py       # Dungeon generation (coming soon)
│   └── combat.py        # Combat system (coming soon)
├── ai/                  # AI/ML components (Phase 2)
├── tutorial/            # Tutorial system (Phase 3)
└── assets/              # Game assets

```

## 📊 Development Status

### ✅ Phase 1: Core Game (Weeks 1-2)
- [x] Basic pygame setup
- [x] Player character with equipment system
- [x] Enemy AI (4 types)
- [x] Basic combat system
- [ ] Dungeon generation
- [ ] Items and pickups
- [ ] Combat polish

### ⏳ Phase 2: AI Integration (Weeks 3-4)
- [ ] Gymnasium environment
- [ ] Curriculum learning (Arena → Room → Dungeon)
- [ ] PPO training
- [ ] AI save/load system

### ⏳ Phase 3: Tutorial System (Weeks 5-6)
- [ ] Teaching interface
- [ ] 4 tutorial lessons
- [ ] Instruction parsing

### ⏳ Phase 4: Commentary & Polish (Weeks 7-8)
- [ ] AI commentary system
- [ ] Progress tracking
- [ ] Final polish

## 🎨 Current Features

- **Player**: Customizable with 2 weapons (Sword, Bow) and 2 armors (Heavy, Light)
- **Enemies**: 4 types (Goblin, Skeleton, Goblin Archer, Slime)
- **Combat**: Real-time combat with cooldowns and damage calculation
- **UI**: Health bars, equipment display, controls

## 🔧 Testing the Current Build

Right now you can manually control the player to fight enemies. This is Phase 1 - the foundation that the AI will learn to play in Phase 2.

Try different equipment combinations:
- Sword + Heavy Armor = Tank build
- Bow + Light Armor = Kiter build

## 📝 Next Steps

1. **Dungeon Generation**: Create random rooms and floors
2. **Items**: Add health potions and pickups
3. **Combat Polish**: Better attack detection and visual feedback
4. **Boss Fight**: Implement Dark Knight boss

## 🐛 Known Issues

- Attack collision detection is basic (will improve)
- No visual attack animations yet
- Enemies can overlap

## 📖 Documentation

See `AI_Dungeon_Crawler_PRD.md` for complete design document.

## 🎯 Vision

Eventually, you won't control the player at all - you'll teach an AI to play through tutorials and reinforcement learning. The AI will provide commentary on what it's learning, creating a unique bond between player and AI companion.

## 📄 License

Personal project - feel free to learn from and adapt!

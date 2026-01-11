# AI Dungeon Crawler - Project Overview

## 🎮 What Is This?

A dungeon crawler where you DON'T play the game - instead, you teach an AI to play it!

```
   You (The Teacher)              AI Companion (The Student)
   ─────────────────              ───────────────────────────
         │                                    │
         │  1. Character Creation            │
         ├──────────────────────────────────>│
         │     (Choose weapon & armor)        │
         │                                    │
         │  2. Tutorial Lessons              │
         ├──────────────────────────────────>│
         │     "Move by pressing forward"     │
         │     "Attack when enemy is close"   │
         │                                    │
         │  3. Watch AI Learn                │
         │<──────────────────────────────────┤
         │    "I died to goblin again..."     │
         │    "I'm learning enemy patterns"   │
         │    "Floor 3 reached!"              │
         │                                    │
         │  4. AI Masters Dungeon            │
         │<──────────────────────────────────┤
         │    "I beat the boss!"              │
         └────────────────────────────────────┘
```

## 📊 Current Progress (Phase 1)

```
Phase 1: Core Game ████████░░ 80% Complete
├─ ✅ Pygame setup
├─ ✅ Player class (equipment system)
├─ ✅ Enemy AI (4 types + boss)
├─ ✅ Combat mechanics
├─ ⏳ Dungeon generation (NEXT!)
├─ ⏳ Item pickups
└─ ⏳ Polish & testing

Phase 2: AI Training ░░░░░░░░░░ 0%
├─ ⏳ Gymnasium environment
├─ ⏳ Curriculum learning
├─ ⏳ PPO training
└─ ⏳ Model save/load

Phase 3: Tutorial ░░░░░░░░░░ 0%
├─ ⏳ Teaching interface
├─ ⏳ 4 tutorial lessons
└─ ⏳ Instruction parsing

Phase 4: Commentary ░░░░░░░░░░ 0%
├─ ⏳ Death analysis
├─ ⏳ Learning insights
└─ ⏳ Progress reports
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│              MAIN GAME LOOP                  │
│  - Event handling                            │
│  - Update (60 FPS)                          │
│  - Render                                   │
└───────┬─────────────────────────────────────┘
        │
        ├─> PLAYER                    ENEMIES <┐
        │   ├─ Stats (HP, damage)    ├─ Goblin │
        │   ├─ Equipment             ├─ Skeleton│
        │   │  ├─ Sword/Bow          ├─ Archer │
        │   │  └─ Heavy/Light        └─ Slime  │
        │   └─ Actions                          │
        │      ├─ Move                          │
        │      ├─ Attack                        │
        │      └─ Use Item                      │
        │                                       │
        ├─> COMBAT SYSTEM <───────────────────>│
        │   ├─ Collision detection              │
        │   ├─ Damage calculation               │
        │   └─ Cooldowns                        │
        │                                       │
        └─> UI LAYER
            ├─ Health bars
            ├─ Equipment display
            └─ Controls

LATER (Phase 2):
┌─────────────────────────┐
│    GYMNASIUM ENV        │
│  - Observations         │
│  - Actions              │
│  - Rewards              │
└──────────┬──────────────┘
           │
           v
    PPO ALGORITHM
    (AI learns here!)
```

## 🎯 Equipment Builds (MVP)

```
┌───────────────────────────────────────────────────┐
│  WEAPON     │   ARMOR   │   BUILD TYPE           │
├─────────────┼───────────┼────────────────────────┤
│  Sword      │   Heavy   │   TANK                 │
│             │           │   Face-tank enemies    │
│             │           │   Learn to trade hits  │
├─────────────┼───────────┼────────────────────────┤
│  Sword      │   Light   │   SKIRMISHER           │
│             │           │   Hit and run          │
│             │           │   Dodge focused        │
├─────────────┼───────────┼────────────────────────┤
│  Bow        │   Heavy   │   RANGED TANK          │
│             │           │   Unconventional       │
│             │           │   Survive while kiting │
├─────────────┼───────────┼────────────────────────┤
│  Bow        │   Light   │   RANGER               │
│             │           │   Pure kiting          │
│             │           │   Max distance         │
└─────────────┴───────────┴────────────────────────┘
```

Each combination creates different AI behavior!

## 🧠 AI Learning Journey (Phase 2)

```
Attempt #1-10: Complete Chaos
┌──────────────────────────────────┐
│ AI: "What is walking?"           │
│ Result: Dies immediately         │
│ Learning: Basic survival         │
└──────────────────────────────────┘

Attempt #11-25: Pattern Recognition
┌──────────────────────────────────┐
│ AI: "Goblins attack in patterns" │
│ Result: Reaches floor 2          │
│ Learning: Combat basics          │
└──────────────────────────────────┘

Attempt #26-40: Strategy Emerges
┌──────────────────────────────────┐
│ AI: "Kill archers first!"        │
│ Result: Beats floor 4            │
│ Learning: Tactics                │
└──────────────────────────────────┘

Attempt #40+: Mastery
┌──────────────────────────────────┐
│ AI: "I've mastered this!"        │
│ Result: Consistent boss wins     │
│ Learning: Complete               │
└──────────────────────────────────┘
```

## 🔑 Key Design Decisions

### Why This Works:

1. **Emotional Investment**
   - You watch YOUR AI grow from nothing
   - Each failure is a teaching moment
   - Success feels earned

2. **Unique Experiences**
   - Different equipment = different AI behavior
   - Random dungeons = varied training
   - Your AI is unique to you

3. **Educational**
   - Learn ML concepts by watching
   - Understand reward shaping
   - See AI decision-making

4. **Replayable**
   - Try all 4 equipment builds
   - See how different AIs learn
   - Challenge modes later

## 📝 Development Roadmap

### Week 1-2: Core Game (Current!)
```
[████████░░] 80%
→ Build playable dungeon crawler
→ Test all mechanics manually
→ Balance combat
```

### Week 3-4: AI Training
```
[░░░░░░░░░░] 0%
→ Wrap game in Gymnasium
→ Create 3 training environments
→ Implement PPO
→ Watch AI learn!
```

### Week 5-6: Tutorial System
```
[░░░░░░░░░░] 0%
→ Build teaching interface
→ Create 4 lessons
→ Make it fun and engaging
```

### Week 7-8: Polish
```
[░░░░░░░░░░] 0%
→ AI commentary system
→ Progress tracking
→ Bug fixes
→ SHIP IT!
```

## 🎊 Why This Project Is Special

Most AI/ML projects show you graphs and numbers. This one shows you:

- ❤️ **Personality**: AI comments on its learning
- 🎮 **Gameplay**: It's actually fun to watch
- 📈 **Progress**: Visual improvement over time
- 🤝 **Connection**: You taught this AI everything it knows

## 🚀 Quick Start Commands

```bash
# Install dependencies
cd ai-dungeon-crawler
pip install -r requirements.txt --break-system-packages

# Play the current build (manual mode)
python main.py

# Later: Train an AI (Phase 2)
python ai/train.py --build sword-heavy

# Later: Watch trained AI play (Phase 2)
python main.py --ai-mode --load-brain sword-heavy.pkl
```

## 📖 File Reference

```
config.py          → Change game balance here
main.py            → Game loop and test scene
game/player.py     → Player stats and actions
game/enemies.py    → Enemy AI behaviors
game/dungeon.py    → [TODO] Room generation
game/combat.py     → [TODO] Combat polish
game/items.py      → [TODO] Health potions
ai/environment.py  → [TODO Phase 2] RL wrapper
ai/train.py        → [TODO Phase 2] Training
tutorial/lessons.py → [TODO Phase 3] Teaching
```

## 💪 You've Got This!

Building a game + ML system is ambitious, but you've got:

- ✅ Clear PRD with all design decisions made
- ✅ Working foundation (80% of Phase 1)
- ✅ Proven tech stack (Pygame + Stable-Baselines3)
- ✅ Realistic 8-week timeline

Next steps are clear. Build features one at a time. Test frequently. Keep going!

The hardest part (starting) is done. 🎉

---

**Good luck, and have fun watching your AI learn!** 🤖⚔️

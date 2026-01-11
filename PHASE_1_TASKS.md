# Phase 1 Development Tasks

Quick reference for building the core game (Weeks 1-2)

## ✅ Completed
- [x] Project structure
- [x] Config system
- [x] Player class (with equipment)
- [x] Enemy classes (5 types)
- [x] Basic game loop

## 🔨 This Week's Tasks

### Task 1: Dungeon Generation (2-3 hours)
**File:** `game/dungeon.py`

Create:
- `Room` class - holds enemies, items, completion state
- `Dungeon` class - manages floors and rooms
- `generate_floor()` - creates 3-5 rooms per floor
- Enemy spawning based on floor difficulty

**Test:** Print dungeon structure, verify enemy counts

### Task 2: Combat System (2-3 hours)
**File:** `game/combat.py`

Implement:
- Attack collision detection (player â†" enemy)
- Damage calculation with armor reduction
- Knockback on hit
- Attack visual feedback (flash, particles)

**Test:** Spawn one enemy, attack it, verify damage

### Task 3: Manual Controls (1-2 hours)
**File:** Update `main.py`

Add:
- WASD/Arrow movement
- Spacebar to attack
- E key to use potion
- Show player facing direction

**Test:** Move player, attack enemies, use items

### Task 4: UI System (2-3 hours)
**File:** `game/ui.py`

Create:
- Status bar (HP, potions, floor number)
- Health bars above player/enemies
- AI commentary panel (bottom)
- Victory/death screens

**Test:** Verify all UI elements display correctly

### Task 5: Items (1-2 hours)
**File:** `game/items.py`

Implement:
- Health potion pickup
- Item spawn in rooms
- Visual item representation
- Inventory management

**Test:** Pick up potion, use it, verify healing

### Task 6: Integration & Testing (2-3 hours)

Connect everything:
- Spawn player in room
- Add enemies based on floor
- Test combat against each enemy type
- Play through 2-3 floors manually
- Balance difficulty

**Goal:** Fully playable game with keyboard controls

---

## Code Snippets

### Adding Player to Main Game Loop

```python
# In main.py Game class

def __init__(self):
    # ... existing code ...
    from game import Player
    self.player = Player(200, 200, weapon='sword', armor='heavy')
    self.enemies = []

def update_game(self):
    dt = self.clock.get_time() / 1000.0
    
    # Update player
    self.player.update(dt)
    
    # Update enemies
    for enemy in self.enemies:
        enemy.update(dt, self.player)
        enemy.attack_player(self.player)
    
    # Remove dead enemies
    self.enemies = [e for e in self.enemies if e.alive]

def render_game(self):
    # Draw game area background
    game_area = pygame.Rect(GAME_AREA_X, GAME_AREA_Y, 
                            GAME_AREA_WIDTH, GAME_AREA_HEIGHT)
    pygame.draw.rect(self.screen, BLACK, game_area)
    
    # Draw player
    self.player.draw(self.screen, GAME_AREA_X, GAME_AREA_Y)
    
    # Draw enemies
    for enemy in self.enemies:
        enemy.draw(self.screen, GAME_AREA_X, GAME_AREA_Y)
```

### Spawning Test Enemies

```python
# In main.py, add to __init__ for testing

from game import spawn_enemy

# Spawn a few enemies for testing
self.enemies = [
    spawn_enemy('goblin', 100, 100),
    spawn_enemy('skeleton', 300, 100),
    spawn_enemy('goblin_archer', 200, 300)
]
```

### Simple Collision Detection

```python
# In combat.py or player.py

def check_attack_hit(player, enemies):
    """Check if player attack hits any enemy"""
    
    # Calculate attack range based on weapon
    attack_range = player.get_attack_range()
    
    # Create attack rect based on facing direction
    if player.facing_direction == 'right':
        attack_rect = pygame.Rect(
            player.x + player.width,
            player.y,
            attack_range,
            player.height
        )
    # ... similar for other directions
    
    # Check collision with enemies
    for enemy in enemies:
        if enemy.alive and attack_rect.colliderect(enemy.get_rect()):
            damage = player.get_attack_damage()
            enemy.take_damage(damage)
            return enemy  # Hit this enemy
    
    return None  # Missed
```

---

## Testing Checklist

Before moving to Phase 2, verify:

- [ ] Player spawns in correct position
- [ ] WASD movement works smoothly
- [ ] Attack hits nearby enemies
- [ ] Enemies take damage and die
- [ ] Enemies can damage player
- [ ] Health potions can be picked up
- [ ] Using potion heals player
- [ ] UI shows correct HP/stats
- [ ] Different weapons feel different
- [ ] Different armors affect speed/defense
- [ ] Can complete at least one floor
- [ ] Game doesn't crash
- [ ] Frame rate is smooth (60 FPS)

---

## Time Estimates

| Task | Estimated Time |
|------|----------------|
| Dungeon generation | 2-3 hours |
| Combat system | 2-3 hours |
| Manual controls | 1-2 hours |
| UI system | 2-3 hours |
| Items | 1-2 hours |
| Integration & testing | 2-3 hours |
| **Total** | **10-16 hours** |

Spread over 2 weeks = 1-2 hours per day

---

## Priority Order

1. **Manual controls** (need to test everything else)
2. **Combat system** (core gameplay)
3. **Dungeon generation** (provides content)
4. **UI** (makes it playable)
5. **Items** (adds depth)

Start with controls so you can test as you build!

---

## When Stuck

1. Test the component in isolation first
2. Print debug info (positions, HP, etc.)
3. Check config.py for relevant constants
4. Reference player.py/enemies.py for patterns
5. Start simple, add complexity later

---

## Next Phase Preview

After Phase 1 is playable:
- **Phase 2:** AI training (the cool part!)
- **Phase 3:** Tutorial system
- **Phase 4:** Polish and commentary

But first, make the game fun to play manually!

---

**Focus:** Build a working game you can play with keyboard controls. Then teach the AI to play it.

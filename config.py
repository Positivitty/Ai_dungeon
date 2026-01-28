# AI Dungeon Crawler - Configuration
# All game settings and constants

# Display Settings
WINDOW_WIDTH = 1200  # Wider for horizontal layout
WINDOW_HEIGHT = 700
FPS = 60
TITLE = "AI Dungeon Crawler"

# Layout - Horizontal Arena Design
LEFT_PANEL_WIDTH = 250
RIGHT_PANEL_WIDTH = 200
INVENTORY_HEIGHT = 100
TOP_BAR_HEIGHT = 40

ARENA_X = LEFT_PANEL_WIDTH
ARENA_Y = TOP_BAR_HEIGHT
ARENA_WIDTH = WINDOW_WIDTH - LEFT_PANEL_WIDTH - RIGHT_PANEL_WIDTH
ARENA_HEIGHT = WINDOW_HEIGHT - TOP_BAR_HEIGHT - INVENTORY_HEIGHT

# Old game area (for compatibility)
GAME_AREA_WIDTH = ARENA_WIDTH
GAME_AREA_HEIGHT = ARENA_HEIGHT
GAME_AREA_X = ARENA_X
GAME_AREA_Y = ARENA_Y

# Sprite/Tile Settings
TILE_SIZE = 32
SPRITE_SIZE = 48  # Larger sprites for better visibility

# Spawn Positions
PLAYER_SPAWN_X = 100  # Left side
PLAYER_SPAWN_Y = ARENA_HEIGHT // 2

ENEMY_SPAWN_X = ARENA_WIDTH - 100  # Right side
ENEMY_SPAWN_Y_MIN = 100
ENEMY_SPAWN_Y_MAX = ARENA_HEIGHT - 100

# Wave System
WAVE_SPAWN_INTERVAL = 3.0  # Seconds between enemy spawns
ENEMIES_PER_WAVE = 6
WAVES_PER_FLOOR = 5

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (44, 44, 44)
LIGHT_GRAY = (100, 100, 100)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (200, 100, 255)
GOLD = (255, 215, 0)

# UI Colors
UI_BACKGROUND = (30, 30, 30)
UI_BORDER = (80, 80, 80)
UI_HIGHLIGHT = CYAN
UI_TEXT = WHITE

# Player Settings
PLAYER_SPEED = 4
PLAYER_MAX_HP = 100
PLAYER_MAX_MANA = 100

# Combat Settings
MELEE_RANGE = 60
RANGED_RANGE = 250
ATTACK_COOLDOWN = 0.5  # seconds

# Weapon Stats (from character.py for roguelike)
WEAPONS = {
    'sword': {
        'name': 'Sword',
        'damage': 20,
        'speed': 1.0,
        'range': MELEE_RANGE,
        'type': 'melee'
    },
    'bow': {
        'name': 'Bow',
        'damage': 15,
        'speed': 0.7,
        'range': RANGED_RANGE,
        'type': 'ranged'
    }
}

# Armor Stats (from character.py for roguelike)
ARMORS = {
    'heavy': {
        'name': 'Heavy Armor',
        'defense': 10,
        'speed_modifier': 0.7,
        'max_hp': 120
    },
    'light': {
        'name': 'Light Armor',
        'defense': 3,
        'speed_modifier': 1.3,
        'max_hp': 80
    }
}

# Enemy Stats
ENEMIES = {
    'goblin': {
        'name': 'Goblin',
        'hp': 30,
        'damage': 10,
        'speed': 2,
        'attack_type': 'melee',
        'color': RED
    },
    'skeleton': {
        'name': 'Skeleton',
        'hp': 40,
        'damage': 15,
        'speed': 1.5,
        'attack_type': 'melee',
        'color': WHITE
    },
    'goblin_archer': {
        'name': 'Goblin Archer',
        'hp': 20,
        'damage': 12,
        'speed': 2,
        'attack_type': 'ranged',
        'color': ORANGE
    },
    'slime': {
        'name': 'Slime',
        'hp': 25,
        'damage': 8,
        'speed': 1,
        'attack_type': 'melee',
        'color': GREEN
    }
}

# Boss Stats
BOSSES = {
    'dark_knight': {
        'name': 'Dark Knight',
        'hp': 150,
        'damage': 25,
        'speed': 2.5,
        'attack_type': 'melee',
        'color': (50, 0, 100)
    }
}

# Dungeon Settings
FLOORS = 5
ROOMS_PER_FLOOR = [3, 3, 4, 4, 5]
ROOM_WIDTH = ARENA_WIDTH
ROOM_HEIGHT = ARENA_HEIGHT

# Item Settings
HEALTH_POTION_HEAL = 50
POTIONS_PER_DUNGEON = 3

# Inventory Settings
INVENTORY_SLOTS = 8
ITEM_SLOT_SIZE = 60
ITEM_SLOT_PADDING = 10

# AI Training Settings (for Phase 2)
TRAINING_MODE = False
TRAINING_SPEED = 1000

# Skills (placeholder for AI system)
SKILLS = {
    'basic_attack': {
        'name': 'Attack',
        'cooldown': 0.5,
        'description': 'Basic attack'
    },
    'defend': {
        'name': 'Defend',
        'cooldown': 5.0,
        'description': 'Reduce damage for 2s'
    },
    'special': {
        'name': 'Special',
        'cooldown': 10.0,
        'description': 'Class special ability'
    }
}
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

# Modern UI - Gradient Colors (top, bottom pairs)
GRADIENT_PANEL = ((45, 45, 55), (25, 25, 35))
GRADIENT_HEADER = ((60, 60, 80), (40, 40, 55))
GRADIENT_BUTTON = ((70, 70, 90), (50, 50, 65))
GRADIENT_BUTTON_HOVER = ((90, 90, 120), (70, 70, 95))

# Modern UI - Health/Stat Bar Gradients
HEALTH_BAR_FULL = (50, 255, 120)
HEALTH_BAR_EMPTY = (255, 60, 60)
MANA_BAR_COLOR = (80, 150, 255)
XP_BAR_COLOR = (180, 120, 255)

# Player Colors by Class (primary, secondary, glow)
PLAYER_COLORS = {
    'warrior': {
        'primary': (80, 120, 255),
        'secondary': (40, 70, 180),
        'glow': (100, 150, 255),
        'indicator': (150, 180, 255)
    },
    'rogue': {
        'primary': (80, 220, 120),
        'secondary': (40, 150, 70),
        'glow': (100, 255, 140),
        'indicator': (140, 255, 180)
    },
    'mage': {
        'primary': (180, 100, 255),
        'secondary': (120, 50, 200),
        'glow': (200, 140, 255),
        'indicator': (220, 180, 255)
    },
    'paladin': {
        'primary': (255, 210, 80),
        'secondary': (200, 160, 40),
        'glow': (255, 230, 120),
        'indicator': (255, 240, 180)
    }
}

# Enemy Colors by Type (primary, secondary, glow)
ENEMY_COLORS = {
    'goblin': {
        'primary': (220, 80, 80),
        'secondary': (160, 50, 50),
        'glow': (255, 100, 100),
        'letter': 'G'
    },
    'skeleton': {
        'primary': (220, 220, 220),
        'secondary': (160, 160, 160),
        'glow': (255, 255, 255),
        'letter': 'S'
    },
    'goblin_archer': {
        'primary': (255, 180, 80),
        'secondary': (200, 130, 40),
        'glow': (255, 200, 120),
        'letter': 'A'
    },
    'slime': {
        'primary': (80, 220, 80),
        'secondary': (40, 160, 40),
        'glow': (120, 255, 120),
        'letter': 'L'
    }
}

# Boss Colors
BOSS_COLORS = {
    'dark_knight': {
        'primary': (100, 50, 180),
        'secondary': (60, 20, 120),
        'glow': (150, 80, 255),
        'charge_glow': (255, 50, 50),
        'letter': 'B'
    }
}

# Particle Colors
PARTICLE_COLORS = {
    'attack': [(255, 255, 200), (255, 220, 100), (255, 180, 50)],
    'damage': [(255, 80, 80), (255, 120, 120), (200, 40, 40)],
    'heal': [(100, 255, 150), (150, 255, 180), (200, 255, 220)],
    'death': [(255, 100, 100), (255, 150, 150), (200, 50, 50)],
    'pickup': [(150, 255, 150), (180, 255, 200), (255, 255, 255)]
}

# Visual Constants
CORNER_RADIUS = 8
CORNER_RADIUS_SMALL = 4
SHADOW_OFFSET = (3, 3)
SHADOW_ALPHA = 80
GLOW_INTENSITY = 40
GLOW_RADIUS = 8

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
# AI Dungeon Crawler - Configuration
# All game settings and constants

# Display Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
TITLE = "AI Dungeon Crawler"

# Game Area
GAME_AREA_WIDTH = 400
GAME_AREA_HEIGHT = 400
GAME_AREA_X = (WINDOW_WIDTH - GAME_AREA_WIDTH) // 2
GAME_AREA_Y = 50

# Sprite/Tile Settings
TILE_SIZE = 32
SPRITE_SIZE = 32

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

# Player Settings
PLAYER_SPEED = 3
PLAYER_MAX_HP = 100
PLAYER_MAX_MANA = 100

# Combat Settings
MELEE_RANGE = 40
RANGED_RANGE = 200
ATTACK_COOLDOWN = 0.5  # seconds

# Weapon Stats (MVP: Sword and Bow)
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

# Armor Stats (MVP: Heavy and Light)
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

# Enemy Stats (MVP: 4 enemy types)
ENEMIES = {
    'goblin': {
        'name': 'Goblin',
        'hp': 30,
        'damage': 10,
        'speed': 2,
        'type': 'melee',
        'color': RED
    },
    'skeleton': {
        'name': 'Skeleton',
        'hp': 40,
        'damage': 15,
        'speed': 1.5,
        'type': 'melee',
        'color': WHITE
    },
    'goblin_archer': {
        'name': 'Goblin Archer',
        'hp': 20,
        'damage': 12,
        'speed': 2,
        'type': 'ranged',
        'color': ORANGE
    },
    'slime': {
        'name': 'Slime',
        'hp': 25,
        'damage': 8,
        'speed': 1,
        'type': 'melee',
        'color': GREEN
    }
}

# Boss Stats
BOSS = {
    'dark_knight': {
        'name': 'Dark Knight',
        'hp': 150,
        'damage': 25,
        'speed': 2.5,
        'type': 'melee',
        'color': (50, 0, 100)
    }
}

# Dungeon Settings
FLOORS = 5
ROOMS_PER_FLOOR = [3, 3, 4, 4, 5]
ROOM_WIDTH = 400
ROOM_HEIGHT = 400

# Item Settings
HEALTH_POTION_HEAL = 50
POTIONS_PER_DUNGEON = 3

# AI Training Settings (for Phase 2)
TRAINING_MODE = False  # Toggle for headless training
TRAINING_SPEED = 1000  # Steps per second in headless mode

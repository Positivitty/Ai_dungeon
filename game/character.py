"""
Character system - Races and Classes
Defines races, classes, and equipment restrictions
"""

# Race definitions
RACES = {
    'human': {
        'name': 'Human',
        'base_hp': 100,
        'base_damage': 10,
        'base_defense': 10,
        'base_speed': 3.0,
        'bonus_text': '+10% XP Gain',
        'description': 'Balanced in all stats'
    },
    'elf': {
        'name': 'Elf',
        'base_hp': 80,
        'base_damage': 12,
        'base_defense': 6,
        'base_speed': 4.5,
        'bonus_text': '+15% Dodge Chance',
        'description': 'Fast and agile'
    },
    'dwarf': {
        'name': 'Dwarf',
        'base_hp': 120,
        'base_damage': 8,
        'base_defense': 15,
        'base_speed': 2.5,
        'bonus_text': '+20% Armor Effect',
        'description': 'Tanky and resilient'
    },
    'orc': {
        'name': 'Orc',
        'base_hp': 110,
        'base_damage': 15,
        'base_defense': 8,
        'base_speed': 2.8,
        'bonus_text': '+10% Crit Chance',
        'description': 'High damage dealer'
    }
}

# Class definitions
CLASSES = {
    'warrior': {
        'name': 'Warrior',
        'damage_bonus': 5,
        'defense_bonus': 5,
        'hp_bonus': 0,
        'speed_bonus': 0,
        'description': 'Tank, frontline fighter',
        'starting_weapon': 'iron_sword',
        'starting_armor': 'leather_armor',
        'allowed_weapons': ['sword', 'axe', 'mace', 'greatsword', 'warhammer'],
        'allowed_armor': ['heavy', 'medium', 'light']  # Can wear anything
    },
    'rogue': {
        'name': 'Rogue',
        'damage_bonus': 2,
        'defense_bonus': 0,
        'hp_bonus': 0,
        'speed_bonus': 2.0,
        'description': 'Fast, high dodge',
        'starting_weapon': 'rusty_dagger',
        'starting_armor': 'light_tunic',
        'allowed_weapons': ['dagger', 'bow', 'dual_daggers'],
        'allowed_armor': ['light']
    },
    'mage': {
        'name': 'Mage',
        'damage_bonus': 0,
        'defense_bonus': 2,
        'hp_bonus': 0,
        'speed_bonus': 0.5,
        'description': 'Magic damage dealer',
        'starting_weapon': 'wooden_staff',
        'starting_armor': 'apprentice_robe',
        'allowed_weapons': ['staff', 'wand', 'spellbook'],
        'allowed_armor': ['robe']
    },
    'paladin': {
        'name': 'Paladin',
        'damage_bonus': 3,
        'defense_bonus': 3,
        'hp_bonus': 10,
        'speed_bonus': 0,
        'description': 'Balanced tank/damage',
        'starting_weapon': 'short_sword',
        'starting_armor': 'chainmail',
        'allowed_weapons': ['sword', 'mace', 'shield'],
        'allowed_armor': ['medium', 'heavy']
    }
}

# Equipment database
WEAPONS = {
    # Starting weapons
    'iron_sword': {
        'name': 'Iron Sword',
        'type': 'sword',
        'damage': 8,
        'rarity': 'common',
        'description': 'A basic iron sword'
    },
    'rusty_dagger': {
        'name': 'Rusty Dagger',
        'type': 'dagger',
        'damage': 6,
        'rarity': 'common',
        'description': 'An old, worn dagger'
    },
    'wooden_staff': {
        'name': 'Wooden Staff',
        'type': 'staff',
        'damage': 5,
        'rarity': 'common',
        'description': 'A simple wooden staff'
    },
    'short_sword': {
        'name': 'Short Sword',
        'type': 'sword',
        'damage': 7,
        'rarity': 'common',
        'description': 'A standard short sword'
    },
    
    # Loot weapons - Warrior
    'steel_sword': {
        'name': 'Steel Sword',
        'type': 'sword',
        'damage': 15,
        'rarity': 'uncommon',
        'description': 'A well-crafted steel blade'
    },
    'fire_sword': {
        'name': 'Fire Sword',
        'type': 'sword',
        'damage': 20,
        'rarity': 'rare',
        'description': 'Burns enemies on hit'
    },
    'battle_axe': {
        'name': 'Battle Axe',
        'type': 'axe',
        'damage': 18,
        'rarity': 'uncommon',
        'description': 'Heavy but powerful'
    },
    'greatsword': {
        'name': 'Greatsword',
        'type': 'greatsword',
        'damage': 25,
        'rarity': 'rare',
        'description': 'Massive two-handed blade'
    },
    
    # Loot weapons - Rogue
    'sharp_dagger': {
        'name': 'Sharp Dagger',
        'type': 'dagger',
        'damage': 12,
        'rarity': 'uncommon',
        'description': 'Razor-sharp blade'
    },
    'shadow_dagger': {
        'name': 'Shadow Dagger',
        'type': 'dagger',
        'damage': 18,
        'rarity': 'rare',
        'description': 'Strikes from the shadows'
    },
    'hunters_bow': {
        'name': "Hunter's Bow",
        'type': 'bow',
        'damage': 16,
        'rarity': 'uncommon',
        'description': 'Long-range precision'
    },
    
    # Loot weapons - Mage
    'oak_staff': {
        'name': 'Oak Staff',
        'type': 'staff',
        'damage': 12,
        'rarity': 'uncommon',
        'description': 'Amplifies magic power'
    },
    'arcane_staff': {
        'name': 'Arcane Staff',
        'type': 'staff',
        'damage': 20,
        'rarity': 'rare',
        'description': 'Crackles with arcane energy'
    },
    
    # Loot weapons - Paladin
    'blessed_sword': {
        'name': 'Blessed Sword',
        'type': 'sword',
        'damage': 17,
        'rarity': 'rare',
        'description': 'Holy weapon'
    },
    'holy_mace': {
        'name': 'Holy Mace',
        'type': 'mace',
        'damage': 16,
        'rarity': 'uncommon',
        'description': 'Blessed by the light'
    }
}

ARMORS = {
    # Starting armor
    'leather_armor': {
        'name': 'Leather Armor',
        'type': 'light',
        'defense': 5,
        'max_hp_bonus': 0,
        'speed_modifier': 1.0,
        'rarity': 'common',
        'description': 'Basic leather protection'
    },
    'light_tunic': {
        'name': 'Light Tunic',
        'type': 'light',
        'defense': 2,
        'max_hp_bonus': 0,
        'speed_modifier': 1.2,
        'rarity': 'common',
        'description': 'Barely any protection'
    },
    'apprentice_robe': {
        'name': 'Apprentice Robe',
        'type': 'robe',
        'defense': 3,
        'max_hp_bonus': 0,
        'speed_modifier': 1.0,
        'rarity': 'common',
        'description': 'Simple cloth robe'
    },
    'chainmail': {
        'name': 'Chainmail',
        'type': 'medium',
        'defense': 8,
        'max_hp_bonus': 10,
        'speed_modifier': 0.9,
        'rarity': 'common',
        'description': 'Linked metal rings'
    },
    
    # Loot armor - Light
    'studded_leather': {
        'name': 'Studded Leather',
        'type': 'light',
        'defense': 10,
        'max_hp_bonus': 5,
        'speed_modifier': 1.1,
        'rarity': 'uncommon',
        'description': 'Reinforced leather'
    },
    'shadow_cloak': {
        'name': 'Shadow Cloak',
        'type': 'light',
        'defense': 8,
        'max_hp_bonus': 0,
        'speed_modifier': 1.3,
        'rarity': 'rare',
        'description': 'Move like the wind'
    },
    
    # Loot armor - Medium
    'scale_mail': {
        'name': 'Scale Mail',
        'type': 'medium',
        'defense': 15,
        'max_hp_bonus': 15,
        'speed_modifier': 0.85,
        'rarity': 'uncommon',
        'description': 'Overlapping metal scales'
    },
    
    # Loot armor - Heavy
    'plate_armor': {
        'name': 'Plate Armor',
        'type': 'heavy',
        'defense': 20,
        'max_hp_bonus': 30,
        'speed_modifier': 0.7,
        'rarity': 'uncommon',
        'description': 'Full plate protection'
    },
    'dragon_armor': {
        'name': 'Dragon Armor',
        'type': 'heavy',
        'defense': 30,
        'max_hp_bonus': 50,
        'speed_modifier': 0.8,
        'rarity': 'rare',
        'description': 'Forged from dragon scales'
    },
    
    # Loot armor - Robe
    'mages_robe': {
        'name': "Mage's Robe",
        'type': 'robe',
        'defense': 8,
        'max_hp_bonus': 10,
        'speed_modifier': 1.0,
        'rarity': 'uncommon',
        'description': 'Enchanted cloth'
    },
    'archmage_robe': {
        'name': 'Archmage Robe',
        'type': 'robe',
        'defense': 15,
        'max_hp_bonus': 20,
        'speed_modifier': 1.1,
        'rarity': 'rare',
        'description': 'Radiates magical power'
    }
}

# Loot tables by rarity
LOOT_TABLES = {
    'common_weapons': ['steel_sword', 'sharp_dagger', 'oak_staff', 'holy_mace'],
    'rare_weapons': ['fire_sword', 'greatsword', 'shadow_dagger', 'arcane_staff', 'blessed_sword', 'hunters_bow', 'battle_axe'],
    
    'common_armor': ['studded_leather', 'scale_mail', 'plate_armor', 'mages_robe'],
    'rare_armor': ['shadow_cloak', 'dragon_armor', 'archmage_robe']
}

def can_equip_weapon(character_class, weapon_type):
    """
    Check if a class can equip a weapon type
    
    Args:
        character_class: Player's class (warrior, rogue, etc)
        weapon_type: Type of weapon (sword, dagger, etc)
    
    Returns:
        bool: True if can equip
    """
    if character_class not in CLASSES:
        return False
    
    allowed = CLASSES[character_class]['allowed_weapons']
    return weapon_type in allowed

def can_equip_armor(character_class, armor_type):
    """
    Check if a class can equip an armor type
    
    Args:
        character_class: Player's class
        armor_type: Type of armor (light, heavy, etc)
    
    Returns:
        bool: True if can equip
    """
    if character_class not in CLASSES:
        return False
    
    allowed = CLASSES[character_class]['allowed_armor']
    return armor_type in allowed
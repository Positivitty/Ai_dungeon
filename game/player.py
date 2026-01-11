"""
Player character class with race/class system
Handles player state, equipment, stats, and inventory
"""

import pygame
from config import *
from game.character import RACES, CLASSES, WEAPONS, ARMORS, can_equip_weapon, can_equip_armor

class Player:
    """Player character with race/class system"""
    
    def __init__(self, x, y, race='human', character_class='warrior'):
        """
        Initialize player character
        
        Args:
            x: Starting x position
            y: Starting y position
            race: Race (human, elf, dwarf, orc)
            character_class: Class (warrior, rogue, mage, paladin)
        """
        self.x = x
        self.y = y
        self.width = SPRITE_SIZE
        self.height = SPRITE_SIZE
        
        # Race and Class
        self.race = race
        self.character_class = character_class
        
        race_data = RACES[race]
        class_data = CLASSES[character_class]
        
        # Base stats from race
        self.base_hp = race_data['base_hp']
        self.base_atk = race_data['base_damage']
        self.base_def = race_data['base_defense']
        self.base_spd = race_data['base_speed']
        self.race_bonus = race_data.get('bonus_text', race_data.get('bonus', ''))
        
        # Class bonuses
        self.class_atk_bonus = class_data.get('damage_bonus', class_data.get('atk_bonus', 0))
        self.class_def_bonus = class_data.get('defense_bonus', class_data.get('def_bonus', 0))
        self.class_hp_bonus = class_data.get('hp_bonus', 0)
        self.class_spd_bonus = class_data.get('speed_bonus', class_data.get('spd_bonus', 0))
        
        # Starting equipment
        starting_weapon = class_data['starting_weapon']
        starting_armor = class_data['starting_armor']
        
        self.weapon_id = starting_weapon
        self.armor_id = starting_armor
        
        # Calculate stats
        self.recalculate_stats()
        
        # Set HP to max
        self.hp = self.max_hp
        
        # State
        self.alive = True
        self.facing = 'right'
        self.attack_cooldown = 0
        
        # Inventory
        self.health_potions = 0
        
        # Visual
        self.color = BLUE
        
    def recalculate_stats(self):
        """Recalculate all stats based on equipment"""
        weapon_data = WEAPONS[self.weapon_id]
        armor_data = ARMORS[self.armor_id]
        
        # Calculate max HP
        self.max_hp = self.base_hp + self.class_hp_bonus + armor_data['max_hp_bonus']
        
        # Keep HP within bounds if it changed
        if hasattr(self, 'hp'):
            self.hp = min(self.hp, self.max_hp)
        
        # Calculate attack
        self.base_damage = self.base_atk + self.class_atk_bonus
        self.weapon_damage = weapon_data['damage']
        self.damage = self.base_damage + self.weapon_damage
        
        # Calculate defense
        self.base_defense = self.base_def + self.class_def_bonus
        self.armor_defense = armor_data['defense']
        self.defense = self.base_defense + self.armor_defense
        
        # Calculate speed
        self.base_speed = self.base_spd + self.class_spd_bonus
        self.speed = self.base_speed * armor_data['speed_modifier']
        
        # Weapon properties
        self.weapon_type = weapon_data['type']
        
        # Attack range based on weapon type
        if self.weapon_type in ['bow']:
            self.attack_range = 200
        elif self.weapon_type in ['staff', 'wand']:
            self.attack_range = 150
        else:
            self.attack_range = 40  # Melee
    
    def equip_weapon(self, weapon_id):
        """
        Try to equip a weapon
        
        Args:
            weapon_id: ID of weapon to equip
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if weapon_id not in WEAPONS:
            return False, "Invalid weapon"
        
        weapon_data = WEAPONS[weapon_id]
        weapon_type = weapon_data['type']
        
        if can_equip_weapon(self.character_class, weapon_type):
            self.weapon_id = weapon_id
            self.recalculate_stats()
            return True, f"Equipped {weapon_data['name']}!"
        else:
            class_name = CLASSES[self.character_class]['name']
            return False, f"Cannot equip - {class_name} only!"
    
    def equip_armor(self, armor_id):
        """
        Try to equip armor
        
        Args:
            armor_id: ID of armor to equip
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if armor_id not in ARMORS:
            return False, "Invalid armor"
        
        armor_data = ARMORS[armor_id]
        armor_type = armor_data['type']
        
        if can_equip_armor(self.character_class, armor_type):
            self.armor_id = armor_id
            self.recalculate_stats()
            return True, f"Equipped {armor_data['name']}!"
        else:
            class_name = CLASSES[self.character_class]['name']
            return False, f"Cannot equip - {class_name} only!"
    
    def get_stat_summary(self):
        """
        Get a formatted stat summary
        
        Returns:
            dict: All player stats
        """
        weapon_data = WEAPONS[self.weapon_id]
        armor_data = ARMORS[self.armor_id]
        
        return {
            'race': RACES[self.race]['name'],
            'class': CLASSES[self.character_class]['name'],
            'hp': int(self.hp),
            'max_hp': self.max_hp,
            'damage': self.damage,
            'base_damage': self.base_damage,
            'weapon_damage': self.weapon_damage,
            'defense': self.defense,
            'base_defense': self.base_defense,
            'armor_defense': self.armor_defense,
            'speed': round(self.speed, 1),
            'weapon_name': weapon_data['name'],
            'armor_name': armor_data['name'],
            'potions': self.health_potions
        }
    
    def update(self, dt):
        """
        Update player state
        
        Args:
            dt: Delta time in seconds
        """
        # Update cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            
        # Check if dead
        if self.hp <= 0:
            self.alive = False
    
    def move(self, dx, dy):
        """
        Move player by delta amounts
        
        Args:
            dx: Change in x position
            dy: Change in y position
        """
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # Update facing direction
        if dx > 0:
            self.facing = 'right'
        elif dx < 0:
            self.facing = 'left'
    
    def attack(self):
        """
        Attempt to perform attack
        
        Returns:
            bool: True if attack was performed, False if on cooldown
        """
        if self.attack_cooldown <= 0:
            self.attack_cooldown = ATTACK_COOLDOWN
            return True
        return False
    
    def take_damage(self, damage):
        """
        Take damage, reduced by defense
        
        Args:
            damage: Raw damage amount
        """
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        self.hp = max(0, self.hp)
    
    def use_health_potion(self):
        """
        Use a health potion if available
        
        Returns:
            bool: True if potion was used, False if none available
        """
        if self.health_potions > 0 and self.hp < self.max_hp:
            self.hp = min(self.max_hp, self.hp + HEALTH_POTION_HEAL)
            self.health_potions -= 1
            return True
        return False
    
    def get_rect(self):
        """Get pygame Rect for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def distance_to_enemy(self, enemy):
        """Calculate distance to an enemy"""
        import math
        dx = enemy.x - self.x
        dy = enemy.y - self.y
        return math.sqrt(dx*dx + dy*dy)
    
    def draw(self, surface):
        """
        Draw player to surface
        
        Args:
            surface: pygame Surface to draw on
        """
        # Different colors based on class
        class_colors = {
            'warrior': (100, 100, 255),  # Blue
            'rogue': (100, 255, 100),    # Green
            'mage': (200, 100, 255),     # Purple
            'paladin': (255, 215, 0)     # Gold
        }
        self.color = class_colors.get(self.character_class, BLUE)
        
        # Simple colored rectangle
        pygame.draw.rect(surface, self.color, self.get_rect())
        
        # Draw health bar above player
        bar_width = self.width
        bar_height = 4
        bar_x = self.x
        bar_y = self.y - 8
        
        # Background (red)
        pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Health (green)
        health_width = int((self.hp / self.max_hp) * bar_width)
        pygame.draw.rect(surface, GREEN, (bar_x, bar_y, health_width, bar_height))
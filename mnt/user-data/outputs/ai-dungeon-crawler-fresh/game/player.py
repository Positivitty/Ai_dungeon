"""
Player character class
Handles player state, equipment, and stats
"""

import pygame
from config import *

class Player:
    """Player character controlled by AI"""
    
    def __init__(self, x, y, weapon='sword', armor='heavy'):
        """
        Initialize player character
        
        Args:
            x: Starting x position
            y: Starting y position
            weapon: Weapon type ('sword' or 'bow')
            armor: Armor type ('heavy' or 'light')
        """
        self.x = x
        self.y = y
        self.width = SPRITE_SIZE
        self.height = SPRITE_SIZE
        
        # Equipment
        self.weapon = weapon
        self.armor = armor
        
        # Stats (modified by equipment)
        armor_data = ARMORS[armor]
        weapon_data = WEAPONS[weapon]
        
        self.max_hp = armor_data['max_hp']
        self.hp = self.max_hp
        self.defense = armor_data['defense']
        self.speed = PLAYER_SPEED * armor_data['speed_modifier']
        
        self.damage = weapon_data['damage']
        self.attack_range = weapon_data['range']
        self.attack_speed = weapon_data['speed']
        self.weapon_type = weapon_data['type']
        
        # State
        self.alive = True
        self.facing = 'right'  # Direction player is facing
        self.attack_cooldown = 0
        
        # Inventory
        self.health_potions = 0
        
        # Visual (simple colored rectangle for now)
        self.color = BLUE
        
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
            self.attack_cooldown = ATTACK_COOLDOWN / self.attack_speed
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
        # Simple colored rectangle for now
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

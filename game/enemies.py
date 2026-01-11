"""
Enemy classes with AI behavior and wall collision
"""

import pygame
import math
from config import *

class Enemy:
    """Base enemy class"""
    
    def __init__(self, x, y, enemy_type):
        """
        Initialize enemy
        
        Args:
            x: Starting x position
            y: Starting y position
            enemy_type: Type of enemy (goblin, skeleton, etc.)
        """
        self.x = x
        self.y = y
        self.width = SPRITE_SIZE
        self.height = SPRITE_SIZE
        self.enemy_type = enemy_type
        
        # Get stats from config
        enemy_data = ENEMIES[enemy_type]
        self.hp = enemy_data['hp']
        self.max_hp = self.hp
        self.damage = enemy_data['damage']
        self.speed = enemy_data['speed']
        self.attack_type = enemy_data['attack_type']
        self.color = enemy_data['color']
        
        # State
        self.alive = True
        self.state = 'idle'  # idle, chase, attack, retreat
        self.attack_cooldown = 0
        self.target = None
    
    def update(self, dt, player, room=None):
        """
        Update enemy state and behavior
        
        Args:
            dt: Delta time in seconds
            player: Player object to interact with
            room: Room object for wall collision (optional)
        """
        if not self.alive:
            return
            
        self.target = player
        
        # Update cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        
        # Simple enemy AI
        distance = self.distance_to(player)
        
        if self.attack_type == 'melee':
            # Melee enemies chase and attack when close
            if distance < 50:
                self.state = 'attack'
                if self.attack_cooldown <= 0:
                    self.perform_attack(player)
            else:
                self.state = 'chase'
                self.move_toward(player, dt, room)
                
        elif self.attack_type == 'ranged':
            # Ranged enemies maintain distance and shoot
            if distance < 100:
                self.state = 'retreat'
                self.move_away(player, dt, room)
            elif distance < 250:
                self.state = 'attack'
                if self.attack_cooldown <= 0:
                    self.perform_attack(player)
            else:
                self.state = 'chase'
                self.move_toward(player, dt, room)
    
    def distance_to(self, other):
        """Calculate distance to another entity"""
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx*dx + dy*dy)
    
    def move_toward(self, target, dt, room=None):
        """
        Move toward target with wall collision
        
        Args:
            target: Entity to move toward
            dt: Delta time
            room: Room object for collision checking
        """
        dx = target.x - self.x
        dy = target.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Normalize direction
            dx = dx / distance
            dy = dy / distance
            
            # Store old position
            old_x = self.x
            old_y = self.y
            
            # Try to move
            self.x += dx * self.speed
            self.y += dy * self.speed
            
            # Check collision with walls
            if room and room.check_collision(self.get_rect()):
                # Hit a wall, revert movement
                self.x = old_x
                self.y = old_y
    
    def move_away(self, target, dt, room=None):
        """
        Move away from target with wall collision
        
        Args:
            target: Entity to move away from
            dt: Delta time
            room: Room object for collision checking
        """
        dx = self.x - target.x
        dy = self.y - target.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Normalize direction
            dx = dx / distance
            dy = dy / distance
            
            # Store old position
            old_x = self.x
            old_y = self.y
            
            # Try to move
            self.x += dx * self.speed
            self.y += dy * self.speed
            
            # Check collision with walls
            if room and room.check_collision(self.get_rect()):
                # Hit a wall, revert movement
                self.x = old_x
                self.y = old_y
    
    def perform_attack(self, player):
        """
        Attack the player
        
        Args:
            player: Player object to attack
        """
        distance = self.distance_to(player)
        attack_range = 50 if self.attack_type == 'melee' else 250
        
        if distance <= attack_range:
            player.take_damage(self.damage)
            self.attack_cooldown = 1.0  # 1 second cooldown
    
    def can_attack(self):
        """Check if enemy can attack (cooldown ready)"""
        return self.attack_cooldown <= 0
    
    def attack(self, player):
        """Attack the player (wrapper for perform_attack)"""
        if self.can_attack():
            self.perform_attack(player)
    
    def take_damage(self, damage):
        """Take damage"""
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
    
    def get_rect(self):
        """Get pygame Rect for collision"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface):
        """Draw enemy"""
        # Draw enemy as colored rectangle
        pygame.draw.rect(surface, self.color, self.get_rect())
        
        # Draw health bar above enemy
        bar_width = self.width
        bar_height = 4
        bar_x = self.x
        bar_y = self.y - 8
        
        # Background (red)
        pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Health (green)
        if self.max_hp > 0:
            health_width = int((self.hp / self.max_hp) * bar_width)
            pygame.draw.rect(surface, GREEN, (bar_x, bar_y, health_width, bar_height))


class Boss(Enemy):
    """Boss enemy - tougher version of regular enemies"""
    
    def __init__(self, x, y, boss_type='dark_knight'):
        """
        Initialize boss
        
        Args:
            x: Starting x position
            y: Starting y position
            boss_type: Type of boss
        """
        # Initialize with base enemy type
        super().__init__(x, y, 'skeleton')
        
        # Override with boss stats
        boss_data = BOSSES[boss_type]
        self.enemy_type = boss_type
        self.hp = boss_data['hp']
        self.max_hp = self.hp
        self.damage = boss_data['damage']
        self.speed = boss_data['speed']
        self.attack_type = boss_data['attack_type']
        self.color = boss_data['color']
        
        # Boss-specific
        self.is_boss = True
        self.heavy_attack_cooldown = 0
        self.heavy_attack_charge = 0
        self.charging_heavy = False
        
        # Make boss bigger
        self.width = SPRITE_SIZE * 2
        self.height = SPRITE_SIZE * 2
    
    def update(self, dt, player, room=None):
        """Update boss with special attacks"""
        if not self.alive:
            return
        
        # Update cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        if self.heavy_attack_cooldown > 0:
            self.heavy_attack_cooldown -= dt
        
        distance = self.distance_to(player)
        
        # Boss AI - more aggressive
        if self.charging_heavy:
            # Charging heavy attack
            self.heavy_attack_charge += dt
            if self.heavy_attack_charge >= 1.0:
                # Release heavy attack
                self.perform_heavy_attack(player)
                self.charging_heavy = False
                self.heavy_attack_charge = 0
        
        elif distance < 60:
            # Close range - try heavy attack
            if self.heavy_attack_cooldown <= 0:
                self.charging_heavy = True
                self.heavy_attack_charge = 0
                self.heavy_attack_cooldown = 5.0
            elif self.attack_cooldown <= 0:
                self.perform_attack(player)
        
        else:
            # Chase player
            self.state = 'chase'
            self.move_toward(player, dt, room)
    
    def perform_heavy_attack(self, player):
        """Perform telegraphed heavy attack"""
        distance = self.distance_to(player)
        
        if distance <= 80:
            # Heavy attack does double damage
            player.take_damage(self.damage * 2)
    
    def draw(self, surface):
        """Draw boss"""
        # Draw boss rectangle
        boss_color = self.color
        
        # Flash red when charging heavy attack
        if self.charging_heavy:
            boss_color = RED
        
        pygame.draw.rect(surface, boss_color, self.get_rect())
        
        # Draw health bar
        bar_width = self.width
        bar_height = 6
        bar_x = self.x
        bar_y = self.y - 12
        
        pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
        
        if self.max_hp > 0:
            health_width = int((self.hp / self.max_hp) * bar_width)
            pygame.draw.rect(surface, GREEN, (bar_x, bar_y, health_width, bar_height))
        
        # Draw charge indicator if charging
        if self.charging_heavy:
            charge_width = int((self.heavy_attack_charge / 1.0) * bar_width)
            pygame.draw.rect(surface, YELLOW, (bar_x, bar_y - 8, charge_width, 4))
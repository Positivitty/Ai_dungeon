"""
Enemy classes
Handles different enemy types and their behaviors
"""

import pygame
import random
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
            enemy_type: Type of enemy ('goblin', 'skeleton', 'goblin_archer', 'slime')
        """
        self.x = x
        self.y = y
        self.width = SPRITE_SIZE
        self.height = SPRITE_SIZE
        
        # Load enemy data
        data = ENEMIES[enemy_type]
        self.enemy_type = enemy_type
        self.name = data['name']
        self.max_hp = data['hp']
        self.hp = self.max_hp
        self.damage = data['damage']
        self.speed = data['speed']
        self.attack_type = data['type']
        self.color = data['color']
        
        # State
        self.alive = True
        self.attack_cooldown = 0
        self.target = None  # Reference to player
        
        # AI state for simple behavior
        self.state = 'idle'  # idle, chase, attack, retreat
        
    def update(self, dt, player):
        """
        Update enemy behavior
        
        Args:
            dt: Delta time in seconds
            player: Player object to interact with
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
                self.move_toward(player, dt)
                
        elif self.attack_type == 'ranged':
            # Ranged enemies maintain distance and shoot
            if distance < 100:
                self.state = 'retreat'
                self.move_away(player, dt)
            elif distance < 250:
                self.state = 'attack'
                if self.attack_cooldown <= 0:
                    self.perform_attack(player)
            else:
                self.state = 'chase'
                self.move_toward(player, dt)
    
    def distance_to(self, other):
        """Calculate distance to another entity"""
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx*dx + dy*dy)
    
    def move_toward(self, target, dt):
        """Move toward target"""
        dx = target.x - self.x
        dy = target.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Normalize and move
            dx = dx / distance
            dy = dy / distance
            self.x += dx * self.speed
            self.y += dy * self.speed
    
    def move_away(self, target, dt):
        """Move away from target"""
        dx = self.x - target.x
        dy = self.y - target.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Normalize and move
            dx = dx / distance
            dy = dy / distance
            self.x += dx * self.speed
            self.y += dy * self.speed
    
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
    
    def take_damage(self, damage):
        """Take damage"""
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
    
    def get_rect(self):
        """Get pygame Rect for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface):
        """
        Draw enemy to surface
        
        Args:
            surface: pygame Surface to draw on
        """
        if not self.alive:
            return
            
        # Simple colored rectangle
        pygame.draw.rect(surface, self.color, self.get_rect())
        
        # Draw health bar above enemy
        bar_width = self.width
        bar_height = 4
        bar_x = self.x
        bar_y = self.y - 8
        
        # Background (red)
        pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Health (green)
        health_width = int((self.hp / self.max_hp) * bar_width)
        pygame.draw.rect(surface, GREEN, (bar_x, bar_y, health_width, bar_height))


class Boss(Enemy):
    """Boss enemy with enhanced behavior"""
    
    def __init__(self, x, y):
        """Initialize boss"""
        self.x = x
        self.y = y
        self.width = SPRITE_SIZE * 2  # Bosses are larger
        self.height = SPRITE_SIZE * 2
        
        # Load boss data
        data = BOSS['dark_knight']
        self.enemy_type = 'dark_knight'
        self.name = data['name']
        self.max_hp = data['hp']
        self.hp = self.max_hp
        self.damage = data['damage']
        self.speed = data['speed']
        self.attack_type = data['type']
        self.color = data['color']
        
        # State
        self.alive = True
        self.attack_cooldown = 0
        self.target = None
        self.state = 'idle'
        
        # Boss-specific
        self.heavy_attack_windup = 0  # Time until heavy attack
        self.is_winding_up = False
    
    def update(self, dt, player):
        """Boss AI with telegraphed attacks"""
        if not self.alive:
            return
            
        self.target = player
        
        # Update cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        
        # Heavy attack windup
        if self.is_winding_up:
            self.heavy_attack_windup -= dt
            if self.heavy_attack_windup <= 0:
                # Execute heavy attack
                distance = self.distance_to(player)
                if distance < 80:
                    player.take_damage(self.damage * 2)  # Double damage
                self.is_winding_up = False
                self.attack_cooldown = 2.0
            return
        
        # Normal behavior
        distance = self.distance_to(player)
        
        if distance < 70:
            self.state = 'attack'
            if self.attack_cooldown <= 0:
                # 30% chance for heavy attack
                if random.random() < 0.3:
                    self.is_winding_up = True
                    self.heavy_attack_windup = 1.0  # 1 second telegraph
                else:
                    self.perform_attack(player)
        else:
            self.state = 'chase'
            self.move_toward(player, dt)
    
    def draw(self, surface):
        """Draw boss with special effects"""
        if not self.alive:
            return
        
        # Flash red when winding up heavy attack
        color = self.color
        if self.is_winding_up:
            color = RED if int(self.heavy_attack_windup * 10) % 2 == 0 else self.color
        
        pygame.draw.rect(surface, color, self.get_rect())
        
        # Health bar (larger)
        bar_width = self.width
        bar_height = 6
        bar_x = self.x
        bar_y = self.y - 12
        
        pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
        health_width = int((self.hp / self.max_hp) * bar_width)
        pygame.draw.rect(surface, GREEN, (bar_x, bar_y, health_width, bar_height))

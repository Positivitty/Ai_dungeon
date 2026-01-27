"""
Enemy classes with AI behavior and wall collision
"""

import pygame
import math
from config import *
from game.graphics import draw_rounded_rect, draw_gradient_rect, draw_shadow, draw_glow, draw_health_bar

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
    
    def draw(self, surface, flash=None):
        """Draw enemy with modern visuals"""
        # Get enemy-specific colors
        colors = ENEMY_COLORS.get(self.enemy_type, {
            'primary': self.color,
            'secondary': tuple(max(0, c - 40) for c in self.color),
            'glow': self.color,
            'letter': '?'
        })

        rect = self.get_rect()

        # Draw shadow
        draw_shadow(surface, rect, offset=(3, 3), blur_radius=5, alpha=70)

        # Draw glow when in attack state
        if self.state == 'attack':
            draw_glow(surface, rect, colors['glow'], intensity=40, radius=8)

        # Draw main body with gradient
        draw_gradient_rect(surface, colors['primary'], colors['secondary'], rect, radius=CORNER_RADIUS)

        # Draw border
        border_color = colors['glow'] if self.state == 'attack' else tuple(max(0, c - 30) for c in colors['primary'])
        draw_rounded_rect(surface, (0, 0, 0, 0), rect, CORNER_RADIUS,
                         border=2, border_color=border_color)

        # Draw type indicator letter
        font = pygame.font.Font(None, 28)
        letter = colors.get('letter', self.enemy_type[0].upper())
        letter_surface = font.render(letter, True, (255, 255, 255))
        letter_rect = letter_surface.get_rect(center=(rect.centerx, rect.centery))
        surface.blit(letter_surface, letter_rect)

        # Apply flash overlay if provided
        if flash and flash.active:
            flash.draw(surface, rect)

        # Draw modern health bar above enemy
        bar_width = self.width + 6
        bar_height = 6
        bar_x = self.x - 3
        bar_y = self.y - 12

        draw_health_bar(surface, bar_x, bar_y, bar_width, bar_height,
                       self.hp, self.max_hp,
                       bar_color_full=(100, 255, 100), bar_color_empty=(255, 80, 80),
                       bg_color=(30, 30, 40), border_color=(60, 60, 80), radius=3)


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
    
    def draw(self, surface, flash=None):
        """Draw boss with enhanced visuals"""
        # Get boss-specific colors
        colors = BOSS_COLORS.get(self.enemy_type, {
            'primary': self.color,
            'secondary': tuple(max(0, c - 40) for c in self.color),
            'glow': self.color,
            'charge_glow': RED,
            'letter': 'B'
        })

        rect = self.get_rect()

        # Draw larger shadow for boss
        draw_shadow(surface, rect, offset=(5, 5), blur_radius=10, alpha=100)

        # Draw intense glow when charging
        if self.charging_heavy:
            draw_glow(surface, rect, colors['charge_glow'], intensity=80, radius=15)
        else:
            # Normal glow for boss presence
            draw_glow(surface, rect, colors['glow'], intensity=30, radius=10)

        # Determine body color
        if self.charging_heavy:
            # Pulse between normal and red during charge
            charge_progress = self.heavy_attack_charge
            primary = tuple(int(colors['primary'][i] + (255 - colors['primary'][i]) * charge_progress * 0.5)
                          for i in range(3))
            secondary = tuple(int(colors['secondary'][i] + (100 - colors['secondary'][i]) * charge_progress * 0.5)
                            for i in range(3))
        else:
            primary = colors['primary']
            secondary = colors['secondary']

        # Draw main body with gradient
        draw_gradient_rect(surface, primary, secondary, rect, radius=CORNER_RADIUS + 2)

        # Draw border
        border_color = colors['charge_glow'] if self.charging_heavy else colors['glow']
        draw_rounded_rect(surface, (0, 0, 0, 0), rect, CORNER_RADIUS + 2,
                         border=3, border_color=border_color)

        # Draw boss letter indicator
        font = pygame.font.Font(None, 48)
        letter = colors.get('letter', 'B')
        letter_surface = font.render(letter, True, (255, 255, 255))
        letter_rect = letter_surface.get_rect(center=(rect.centerx, rect.centery))
        surface.blit(letter_surface, letter_rect)

        # Apply flash overlay if provided
        if flash and flash.active:
            flash.draw(surface, rect)

        # Draw modern health bar
        bar_width = self.width + 10
        bar_height = 10
        bar_x = self.x - 5
        bar_y = self.y - 18

        draw_health_bar(surface, bar_x, bar_y, bar_width, bar_height,
                       self.hp, self.max_hp,
                       bar_color_full=(100, 255, 100), bar_color_empty=(255, 80, 80),
                       bg_color=(30, 30, 40), border_color=(80, 80, 100), radius=5)

        # Draw charge indicator if charging
        if self.charging_heavy:
            charge_bar_width = self.width + 10
            charge_bar_height = 6
            charge_x = self.x - 5
            charge_y = self.y - 28

            # Background
            draw_rounded_rect(surface, (40, 40, 50), (charge_x, charge_y, charge_bar_width, charge_bar_height), 3)

            # Charge fill
            charge_fill_width = int(charge_bar_width * (self.heavy_attack_charge / 1.0))
            if charge_fill_width > 0:
                draw_gradient_rect(surface, (255, 200, 50), (255, 100, 50),
                                  (charge_x, charge_y, charge_fill_width, charge_bar_height), radius=3)

            # Border
            draw_rounded_rect(surface, (0, 0, 0, 0), (charge_x, charge_y, charge_bar_width, charge_bar_height), 3,
                             border=1, border_color=(255, 200, 100))
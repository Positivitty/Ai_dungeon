"""
Particle system for visual effects
Handles attack sparkles, damage numbers, pickup effects, and death explosions
"""

import pygame
import random
import math


class Particle:
    """Individual particle with physics"""

    def __init__(self, x, y, vx, vy, color, size=4, lifetime=1.0, gravity=0,
                 shrink=True, fade=True):
        """
        Initialize a particle

        Args:
            x, y: Starting position
            vx, vy: Velocity
            color: Particle color (R, G, B)
            size: Initial size in pixels
            lifetime: How long particle lives in seconds
            gravity: Downward acceleration
            shrink: Whether particle shrinks over time
            fade: Whether particle fades over time
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.initial_size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.gravity = gravity
        self.shrink = shrink
        self.fade = fade
        self.alive = True

    def update(self, dt):
        """Update particle position and state"""
        if not self.alive:
            return

        # Apply velocity
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60

        # Apply gravity
        self.vy += self.gravity * dt

        # Update lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False
            return

        # Calculate life ratio (0 = dead, 1 = full life)
        life_ratio = self.lifetime / self.max_lifetime

        # Shrink
        if self.shrink:
            self.size = self.initial_size * life_ratio

    def draw(self, surface):
        """Draw the particle"""
        if not self.alive or self.size < 1:
            return

        # Calculate alpha based on fade
        if self.fade:
            life_ratio = self.lifetime / self.max_lifetime
            alpha = int(255 * life_ratio)
        else:
            alpha = 255

        # Create color with alpha
        if len(self.color) == 3:
            color = (*self.color, alpha)
        else:
            color = (*self.color[:3], alpha)

        # Draw particle
        particle_surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, color, (int(self.size), int(self.size)), int(self.size))
        surface.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))


class DamageNumber:
    """Floating damage text"""

    def __init__(self, x, y, damage, color=(255, 255, 255), crit=False):
        """
        Initialize damage number

        Args:
            x, y: Starting position
            damage: Damage value to display
            color: Text color
            crit: Whether this is a critical hit (larger text)
        """
        self.x = x
        self.y = y
        self.damage = damage
        self.color = color
        self.crit = crit
        self.lifetime = 1.0
        self.max_lifetime = 1.0
        self.alive = True
        self.vy = -2  # Float upward
        self.vx = random.uniform(-0.5, 0.5)  # Slight horizontal drift

        # Font size based on damage and crit
        self.font_size = 28 if crit else 22
        if damage > 50:
            self.font_size += 4
        if damage > 100:
            self.font_size += 4

        self.font = pygame.font.Font(None, self.font_size)

    def update(self, dt):
        """Update damage number position"""
        if not self.alive:
            return

        # Move upward
        self.y += self.vy * dt * 60
        self.x += self.vx * dt * 60

        # Slow down vertical movement
        self.vy *= 0.98

        # Update lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False

    def draw(self, surface):
        """Draw the damage number"""
        if not self.alive:
            return

        # Calculate alpha for fade
        life_ratio = self.lifetime / self.max_lifetime
        alpha = int(255 * life_ratio)

        # Create text
        text = str(int(self.damage))
        if self.crit:
            text = text + "!"

        # Render with outline effect
        outline_color = (0, 0, 0)

        # Draw outline (shadow)
        outline_surface = self.font.render(text, True, outline_color)
        outline_surface.set_alpha(alpha)

        # Draw main text
        text_surface = self.font.render(text, True, self.color)
        text_surface.set_alpha(alpha)

        # Center text
        text_rect = text_surface.get_rect(center=(int(self.x), int(self.y)))
        outline_rect = outline_surface.get_rect(center=(int(self.x) + 1, int(self.y) + 1))

        surface.blit(outline_surface, outline_rect)
        surface.blit(text_surface, text_rect)


class ParticleSystem:
    """Manages all particles and effects"""

    def __init__(self):
        """Initialize particle system"""
        self.particles = []
        self.damage_numbers = []

    def update(self, dt):
        """Update all particles"""
        # Update particles
        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.alive:
                self.particles.remove(particle)

        # Update damage numbers
        for dmg_num in self.damage_numbers[:]:
            dmg_num.update(dt)
            if not dmg_num.alive:
                self.damage_numbers.remove(dmg_num)

    def draw(self, surface):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(surface)

        for dmg_num in self.damage_numbers:
            dmg_num.draw(surface)

    def spawn_attack_effect(self, x, y, direction='right'):
        """
        Spawn hit sparkles at attack location

        Args:
            x, y: Impact position
            direction: 'left' or 'right' for directional sparks
        """
        colors = [(255, 255, 200), (255, 220, 100), (255, 180, 50)]
        dir_mult = 1 if direction == 'right' else -1

        for _ in range(8):
            angle = random.uniform(-0.5, 0.5)
            speed = random.uniform(2, 5)
            vx = math.cos(angle) * speed * dir_mult
            vy = math.sin(angle) * speed + random.uniform(-1, 1)
            color = random.choice(colors)
            size = random.uniform(2, 5)

            particle = Particle(
                x, y, vx, vy, color,
                size=size, lifetime=0.3, gravity=0.1,
                shrink=True, fade=True
            )
            self.particles.append(particle)

    def spawn_damage_taken(self, x, y, damage=0):
        """
        Spawn red burst when taking damage

        Args:
            x, y: Entity center position
            damage: Amount of damage (affects particle count)
        """
        colors = [(255, 50, 50), (255, 100, 100), (200, 0, 0)]
        num_particles = min(15, 8 + damage // 10)

        for _ in range(num_particles):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 4)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = random.choice(colors)
            size = random.uniform(3, 6)

            particle = Particle(
                x, y, vx, vy, color,
                size=size, lifetime=0.4, gravity=0.05,
                shrink=True, fade=True
            )
            self.particles.append(particle)

    def spawn_pickup_effect(self, x, y, color=(100, 255, 100)):
        """
        Spawn sparkles for item pickup

        Args:
            x, y: Pickup position
            color: Base color for sparkles
        """
        # Create brighter version for variety
        bright_color = tuple(min(255, c + 50) for c in color)

        for _ in range(12):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 3)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 1  # Bias upward
            particle_color = random.choice([color, bright_color, (255, 255, 255)])
            size = random.uniform(2, 4)

            particle = Particle(
                x, y, vx, vy, particle_color,
                size=size, lifetime=0.6, gravity=-0.02,  # Float upward
                shrink=True, fade=True
            )
            self.particles.append(particle)

    def spawn_death_effect(self, x, y, color=(255, 100, 100)):
        """
        Spawn explosion for enemy death

        Args:
            x, y: Enemy center position
            color: Base color (enemy color)
        """
        # Multiple colors for variety
        colors = [
            color,
            tuple(max(0, c - 50) for c in color),  # Darker
            tuple(min(255, c + 50) for c in color),  # Brighter
            (255, 255, 255)  # White sparks
        ]

        # Explosion particles
        for _ in range(20):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            particle_color = random.choice(colors)
            size = random.uniform(3, 8)

            particle = Particle(
                x, y, vx, vy, particle_color,
                size=size, lifetime=0.5, gravity=0.1,
                shrink=True, fade=True
            )
            self.particles.append(particle)

        # Inner flash
        for _ in range(5):
            particle = Particle(
                x + random.uniform(-5, 5),
                y + random.uniform(-5, 5),
                0, 0, (255, 255, 200),
                size=random.uniform(8, 15), lifetime=0.15,
                shrink=True, fade=True
            )
            self.particles.append(particle)

    def spawn_damage_number(self, x, y, damage, color=(255, 255, 255), crit=False):
        """
        Spawn floating damage number

        Args:
            x, y: Position
            damage: Damage value
            color: Text color
            crit: Whether critical hit
        """
        # Add some randomness to position to avoid stacking
        x += random.uniform(-10, 10)
        y += random.uniform(-5, 5)

        dmg_num = DamageNumber(x, y, damage, color, crit)
        self.damage_numbers.append(dmg_num)

    def spawn_heal_number(self, x, y, amount):
        """
        Spawn floating heal number (green)

        Args:
            x, y: Position
            amount: Heal amount
        """
        x += random.uniform(-10, 10)
        dmg_num = DamageNumber(x, y, amount, (100, 255, 100))
        dmg_num.vy = -2.5  # Float up faster
        self.damage_numbers.append(dmg_num)

    def clear(self):
        """Clear all particles"""
        self.particles.clear()
        self.damage_numbers.clear()

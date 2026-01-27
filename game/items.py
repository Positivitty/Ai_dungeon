"""
Items and pickups with modern visual effects
"""

import pygame
import math
from config import *
from game.graphics import draw_glow, interpolate_color


class HealthPotion:
    """Health potion pickup with modern visuals"""

    def __init__(self, x, y):
        """Initialize health potion"""
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.color = (80, 220, 100)  # Vibrant green
        self.active = True

        # Animation state
        self.bob_time = 0
        self.glow_time = 0
        self.bob_amplitude = 3
        self.bob_frequency = 2.0

    def update(self, dt):
        """Update potion animations"""
        if not self.active:
            return

        self.bob_time += dt
        self.glow_time += dt

    def check_pickup(self, player):
        """
        Check if player is close enough to pick up

        Args:
            player: Player object

        Returns:
            bool: True if picked up
        """
        if not self.active:
            return False

        # Calculate distance
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx*dx + dy*dy)**0.5

        # Pick up if within range
        if distance < 35:
            self.active = False
            return True

        return False

    def get_rect(self):
        """Get collision rect"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        """Draw the potion with modern effects"""
        if not self.active:
            return

        # Calculate bob offset
        bob_offset = math.sin(self.bob_time * self.bob_frequency * math.pi * 2) * self.bob_amplitude

        center_x = int(self.x + self.width // 2)
        center_y = int(self.y + self.height // 2 + bob_offset)

        # Draw pulsing glow
        glow_intensity = 30 + int(20 * math.sin(self.glow_time * 3))
        glow_rect = pygame.Rect(center_x - 15, center_y - 15, 30, 30)
        draw_glow(surface, glow_rect, self.color, intensity=glow_intensity, radius=12)

        # Draw potion bottle shape
        # Main body (rounded rectangle / ellipse)
        bottle_width = 16
        bottle_height = 20

        # Bottle body gradient
        for i in range(bottle_height):
            t = i / bottle_height
            y_pos = center_y - bottle_height // 2 + i + 2
            width_at_y = int(bottle_width * (0.6 + 0.4 * math.sin(t * math.pi)))

            # Gradient from light to dark
            shade = interpolate_color((100, 255, 130), (40, 160, 60), t)
            pygame.draw.line(surface, shade,
                           (center_x - width_at_y // 2, y_pos),
                           (center_x + width_at_y // 2, y_pos))

        # Bottle neck
        neck_width = 6
        neck_height = 6
        neck_y = center_y - bottle_height // 2 - neck_height + 4
        pygame.draw.rect(surface, (60, 180, 80),
                        (center_x - neck_width // 2, neck_y, neck_width, neck_height))

        # Cork
        cork_width = 8
        cork_height = 4
        cork_y = neck_y - cork_height + 1
        pygame.draw.rect(surface, (180, 140, 100),
                        (center_x - cork_width // 2, cork_y, cork_width, cork_height),
                        border_radius=2)

        # Highlight spot (3D effect)
        highlight_x = center_x - 4
        highlight_y = center_y - 2
        pygame.draw.circle(surface, (200, 255, 220), (highlight_x, highlight_y), 3)

        # Bottle outline
        pygame.draw.ellipse(surface, (40, 120, 50),
                           (center_x - bottle_width // 2, center_y - bottle_height // 2 + 2,
                            bottle_width, bottle_height), 2)
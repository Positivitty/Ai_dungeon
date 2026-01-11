"""
Items and pickups
"""

import pygame
from config import *

class HealthPotion:
    """Health potion pickup"""
    
    def __init__(self, x, y):
        """Initialize health potion"""
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.color = GREEN
        self.active = True
    
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
        if distance < 30:
            self.active = False
            return True
        
        return False
    
    def get_rect(self):
        """Get collision rect"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface):
        """Draw the potion"""
        if self.active:
            # Draw as green circle
            center_x = int(self.x + self.width // 2)
            center_y = int(self.y + self.height // 2)
            pygame.draw.circle(surface, self.color, (center_x, center_y), 10)
            pygame.draw.circle(surface, WHITE, (center_x, center_y), 10, 2)
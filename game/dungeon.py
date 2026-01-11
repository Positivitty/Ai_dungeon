"""
Dungeon generation system
Handles rooms, floors, and dungeon layout
"""

import pygame
import random
from config import *

class Wall:
    """A wall obstacle in a room"""
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = LIGHT_GRAY
    
    def get_rect(self):
        """Get pygame Rect for collision"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface):
        """Draw the wall"""
        pygame.draw.rect(surface, self.color, self.get_rect())
        # Draw border to make it look more like a wall
        pygame.draw.rect(surface, WHITE, self.get_rect(), 2)


class Room:
    """A single room in the dungeon"""
    
    def __init__(self, width=400, height=400):
        self.width = width
        self.height = height
        self.walls = []
        self.enemies = []
        self.items = []
        
        # Room boundaries (outer walls)
        self.create_boundary_walls()
    
    def create_boundary_walls(self):
        """Create walls around the room perimeter"""
        wall_thickness = 10
        
        # Top wall
        self.walls.append(Wall(0, 0, self.width, wall_thickness))
        
        # Bottom wall
        self.walls.append(Wall(0, self.height - wall_thickness, self.width, wall_thickness))
        
        # Left wall
        self.walls.append(Wall(0, 0, wall_thickness, self.height))
        
        # Right wall
        self.walls.append(Wall(self.width - wall_thickness, 0, wall_thickness, self.height))
    
    def add_interior_walls(self):
        """Add some obstacles inside the room"""
        # Add a few pillars/obstacles
        # Pillar in upper left area
        self.walls.append(Wall(80, 80, 40, 40))
        
        # Pillar in upper right area
        self.walls.append(Wall(280, 80, 40, 40))
        
        # Pillar in bottom center
        self.walls.append(Wall(180, 280, 40, 40))
    
    def check_collision(self, rect):
        """
        Check if a rectangle collides with any walls
        
        Args:
            rect: pygame.Rect to check
            
        Returns:
            bool: True if collision detected
        """
        for wall in self.walls:
            if rect.colliderect(wall.get_rect()):
                return True
        return False
    
    def draw(self, surface):
        """Draw the room"""
        # Draw floor
        surface.fill(BLACK)
        
        # Draw walls
        for wall in self.walls:
            wall.draw(surface)
        
        # Draw items (before entities so they appear under them)
        for item in self.items:
            if not item.collected:
                item.draw(surface)
        
        # Draw enemies
        for enemy in self.enemies:
            if enemy.alive:
                enemy.draw(surface)


class Floor:
    """A floor of the dungeon (contains multiple rooms)"""
    
    def __init__(self, floor_number):
        self.floor_number = floor_number
        self.rooms = []
        self.current_room = 0
        
        # Create rooms for this floor
        num_rooms = ROOMS_PER_FLOOR[floor_number - 1] if floor_number <= len(ROOMS_PER_FLOOR) else 3
        
        for i in range(num_rooms):
            room = Room()
            
            # Add interior obstacles (not in first room to be fair)
            if i > 0:
                room.add_interior_walls()
            
            self.rooms.append(room)
    
    def get_current_room(self):
        """Get the currently active room"""
        return self.rooms[self.current_room]
    
    def next_room(self):
        """Move to next room"""
        self.current_room += 1
        return self.current_room < len(self.rooms)
    
    def is_complete(self):
        """Check if all rooms on this floor are cleared"""
        return self.current_room >= len(self.rooms) - 1


class Dungeon:
    """Main dungeon manager"""
    
    def __init__(self, num_floors=5):
        self.num_floors = num_floors
        self.floors = []
        self.current_floor = 0
        
        # Generate all floors
        for i in range(num_floors):
            floor = Floor(i + 1)
            self.floors.append(floor)
    
    def get_current_floor(self):
        """Get the current floor"""
        return self.floors[self.current_floor]
    
    def get_current_room(self):
        """Get the current room"""
        return self.get_current_floor().get_current_room()
    
    def next_room(self):
        """
        Progress to next room
        
        Returns:
            str: 'room' if next room, 'floor' if next floor, 'complete' if dungeon done
        """
        current_floor = self.get_current_floor()
        
        if current_floor.next_room():
            # More rooms on this floor
            return 'room'
        else:
            # Floor complete, go to next floor
            self.current_floor += 1
            
            if self.current_floor >= self.num_floors:
                # Dungeon complete!
                return 'complete'
            else:
                # New floor
                return 'floor'
    
    def spawn_enemies(self, enemy_class):
        """
        Spawn enemies in the current room
        
        Args:
            enemy_class: Enemy class to instantiate
        """
        room = self.get_current_room()
        floor_num = self.current_floor + 1
        
        # Number of enemies increases with floor
        num_enemies = 2 + floor_num
        
        # Enemy types based on floor
        enemy_types = ['goblin', 'skeleton', 'goblin_archer', 'slime']
        
        spawned_count = 0
        for i in range(num_enemies):
            # Random position (avoid walls)
            attempts = 0
            spawned = False
            while attempts < 50:  # Try up to 50 times to find valid position
                x = random.randint(100, room.width - 100)
                y = random.randint(100, room.height - 100)
                
                # Check if position is valid (not in wall)
                test_rect = pygame.Rect(x, y, 32, 32)
                if not room.check_collision(test_rect):
                    # Choose enemy type
                    enemy_type = random.choice(enemy_types)
                    enemy = enemy_class(x, y, enemy_type)
                    room.enemies.append(enemy)
                    spawned_count += 1
                    spawned = True
                    break
                
                attempts += 1
            
            # If random placement failed after 50 attempts, force spawn in center
            if not spawned:
                x = room.width // 2 + (i * 40)  # Spread out in center
                y = room.height // 2
                enemy_type = random.choice(enemy_types)
                enemy = enemy_class(x, y, enemy_type)
                room.enemies.append(enemy)
                spawned_count += 1
    
    def spawn_items(self, item_class):
        """
        Spawn health potions in the current room
        
        Args:
            item_class: HealthPotion class
        """
        room = self.get_current_room()
        
        # 50% chance to spawn a potion in each room
        if random.random() < 0.5:
            attempts = 0
            while attempts < 30:
                x = random.randint(50, room.width - 50)
                y = random.randint(50, room.height - 50)
                
                # Check if position is valid
                test_rect = pygame.Rect(x, y, 20, 20)
                if not room.check_collision(test_rect):
                    potion = item_class(x, y)
                    room.items.append(potion)
                    break
                
                attempts += 1
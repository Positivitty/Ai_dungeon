"""
Wave spawner system for horizontal arena
Spawns enemies in waves from the right side
"""

import random

class WaveSpawner:
    """Manages wave-based enemy spawning"""
    
    def __init__(self, enemy_class, spawn_interval=3.0, max_waves=5):
        """
        Initialize wave spawner
        
        Args:
            enemy_class: Enemy class to spawn
            spawn_interval: Seconds between enemy spawns (default: 3.0)
            max_waves: Maximum waves per floor (default: 5)
        """
        self.enemy_class = enemy_class
        self.current_wave = 1
        self.max_waves = max_waves
        
        # Spawning
        self.enemies_to_spawn = []
        self.spawn_timer = 0
        self.spawn_interval = spawn_interval
        
        # Wave state
        self.wave_active = False
        self.all_waves_complete = False
        
        # Enemy list
        self.active_enemies = []
        
    def start_wave(self, wave_number, floor_number=1):
        """
        Start a new wave
        
        Args:
            wave_number: Wave number (1-5)
            floor_number: Current floor (affects difficulty)
        """
        self.current_wave = wave_number
        self.wave_active = True
        
        # Calculate enemies for this wave
        base_enemies = 3
        enemies_count = base_enemies + floor_number + (wave_number - 1)
        
        # Create spawn queue
        enemy_types = ['goblin', 'skeleton', 'goblin_archer', 'slime']
        self.enemies_to_spawn = []
        
        for i in range(enemies_count):
            enemy_type = random.choice(enemy_types)
            # Stagger spawn times
            spawn_time = i * self.spawn_interval
            self.enemies_to_spawn.append((spawn_time, enemy_type))
        
        self.spawn_timer = 0
        
    def update(self, dt, spawn_x, spawn_y_min, spawn_y_max):
        """
        Update wave spawner
        
        Args:
            dt: Delta time in seconds
            spawn_x: X position to spawn enemies
            spawn_y_min: Minimum Y position
            spawn_y_max: Maximum Y position
            
        Returns:
            list: Newly spawned enemies this frame
        """
        if not self.wave_active:
            return []
        
        self.spawn_timer += dt
        new_enemies = []
        
        # Check if any enemies should spawn
        remaining = []
        for spawn_time, enemy_type in self.enemies_to_spawn:
            if self.spawn_timer >= spawn_time:
                # Spawn this enemy!
                x = spawn_x
                y = random.randint(spawn_y_min, spawn_y_max)
                enemy = self.enemy_class(x, y, enemy_type)
                new_enemies.append(enemy)
                self.active_enemies.append(enemy)
            else:
                remaining.append((spawn_time, enemy_type))
        
        self.enemies_to_spawn = remaining
        
        # Remove dead enemies from active list
        self.active_enemies = [e for e in self.active_enemies if e.alive]
        
        # Check if wave complete
        if len(self.enemies_to_spawn) == 0 and len(self.active_enemies) == 0:
            self.wave_active = False
            
            # Check if all waves done
            if self.current_wave >= self.max_waves:
                self.all_waves_complete = True
        
        return new_enemies
    
    def is_wave_complete(self):
        """Check if current wave is complete"""
        return not self.wave_active and len(self.active_enemies) == 0
    
    def is_all_complete(self):
        """Check if all waves are complete"""
        return self.all_waves_complete
    
    def get_enemies_remaining(self):
        """Get total enemies remaining (spawned + to spawn)"""
        return len(self.active_enemies) + len(self.enemies_to_spawn)
    
    def reset(self):
        """Reset spawner"""
        self.current_wave = 1
        self.wave_active = False
        self.all_waves_complete = False
        self.enemies_to_spawn = []
        self.active_enemies = []
        self.spawn_timer = 0
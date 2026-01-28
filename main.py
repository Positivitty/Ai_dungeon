#!/usr/bin/env python3
"""
AI Dungeon Crawler - Horizontal Arena Version
v0.2.0-dev - Wave-based combat with professional UI
"""

import pygame
import sys
from config import *
from game.player import Player
from game.enemies import Enemy
from game.dungeon import Room
from game.items import HealthPotion
from game.character import RACES, CLASSES, WEAPONS, ARMORS
from game.wave_spawner import WaveSpawner
from game.ui_manager import UIManager

class Game:
    """Main game class with horizontal arena and wave system"""
    
    def __init__(self):
        """Initialize pygame and game components"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        
        # Game state
        self.state = 'menu'
        
        # Character creation
        self.selected_race = 'human'
        self.selected_class = 'warrior'
        self.player_name = ""
        
        # Game objects
        self.player = None
        self.room = None
        self.wave_spawner = None
        self.ui_manager = UIManager(self.screen)
        
        # Wave/Floor tracking
        self.current_floor = 1
        self.current_wave = 1
        self.max_floor = FLOORS
        
        # Enemies
        self.enemies = []
        
        # Items
        self.items = []
        
        # Timers
        self.wave_complete_timer = 0
        self.wave_complete_duration = 2.0
        self.pickup_message = ""
        self.pickup_timer = 0
        self.time_survived = 0
        
        # Menu
        self.menu_selection = 0
        self.menu_options = ['Start Game', 'How to Play', 'Quit']
        
        # Character creation
        self.creation_step = 0  # 0=race, 1=class, 2=name
        self.race_list = ['human', 'elf', 'dwarf', 'orc']
        self.class_list = ['warrior', 'rogue', 'mage', 'paladin']
        self.race_selection = 0
        self.class_selection = 0
        
        # Stat screen
        self.show_stats = False
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if self.state == 'menu':
                    self.handle_menu_input(event)
                elif self.state == 'character_creation':
                    self.handle_creation_input(event)
                elif self.state == 'playing':
                    self.handle_game_input(event)
                elif self.state == 'wave_complete':
                    self.handle_wave_complete_input(event)
                elif self.state == 'floor_complete':
                    self.handle_floor_complete_input(event)
                elif self.state == 'game_over' or self.state == 'victory':
                    self.handle_gameover_input(event)
    
    def handle_menu_input(self, event):
        """Handle menu input"""
        if event.key == pygame.K_UP:
            self.menu_selection = (self.menu_selection - 1) % len(self.menu_options)
        elif event.key == pygame.K_DOWN:
            self.menu_selection = (self.menu_selection + 1) % len(self.menu_options)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.menu_selection == 0:  # Start Game
                self.state = 'character_creation'
                self.creation_step = 0
            elif self.menu_selection == 1:  # How to Play
                pass  # TODO
            elif self.menu_selection == 2:  # Quit
                self.running = False
    
    def handle_creation_input(self, event):
        """Handle character creation input"""
        if self.creation_step == 0:  # Race selection
            if event.key == pygame.K_UP:
                self.race_selection = (self.race_selection - 1) % len(self.race_list)
                self.selected_race = self.race_list[self.race_selection]
            elif event.key == pygame.K_DOWN:
                self.race_selection = (self.race_selection + 1) % len(self.race_list)
                self.selected_race = self.race_list[self.race_selection]
            elif event.key == pygame.K_RETURN:
                self.creation_step = 1
                
        elif self.creation_step == 1:  # Class selection
            if event.key == pygame.K_UP:
                self.class_selection = (self.class_selection - 1) % len(self.class_list)
                self.selected_class = self.class_list[self.class_selection]
            elif event.key == pygame.K_DOWN:
                self.class_selection = (self.class_selection + 1) % len(self.class_list)
                self.selected_class = self.class_list[self.class_selection]
            elif event.key == pygame.K_BACKSPACE:
                self.creation_step = 0
            elif event.key == pygame.K_RETURN:
                self.creation_step = 2
                
        elif self.creation_step == 2:  # Name input
            if event.key == pygame.K_BACKSPACE:
                if len(self.player_name) > 0:
                    self.player_name = self.player_name[:-1]
                else:
                    self.creation_step = 1
            elif event.key == pygame.K_RETURN:
                if len(self.player_name) > 0:
                    self.start_game()
            elif event.unicode.isalnum() or event.unicode == ' ':
                if len(self.player_name) < 20:
                    self.player_name += event.unicode
    
    def handle_game_input(self, event):
        """Handle in-game input"""
        if event.key == pygame.K_ESCAPE:
            self.state = 'menu'
        elif event.key == pygame.K_i:
            self.show_stats = not self.show_stats
        elif event.key == pygame.K_p:
            # Use potion
            if self.player.health_potions > 0 and self.player.hp < self.player.max_hp:
                heal_amount = min(HEALTH_POTION_HEAL, self.player.max_hp - self.player.hp)
                self.player.hp += heal_amount
                self.player.health_potions -= 1
                self.pickup_message = f"Healed {heal_amount} HP!"
                self.pickup_timer = 2.0
    
    def handle_wave_complete_input(self, event):
        """Handle wave complete screen input"""
        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.current_wave < WAVES_PER_FLOOR:
                # Start next wave
                self.current_wave += 1
                self.wave_spawner.start_wave(self.current_wave, self.current_floor)
                self.state = 'playing'
            else:
                # Floor complete
                self.state = 'floor_complete'
    
    def handle_floor_complete_input(self, event):
        """Handle floor complete screen input"""
        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.current_floor < self.max_floor:
                # Next floor
                self.current_floor += 1
                self.current_wave = 1
                self.start_floor()
            else:
                # Victory!
                self.state = 'victory'
    
    def handle_gameover_input(self, event):
        """Handle game over input"""
        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            self.state = 'menu'
            self.player = None
            self.enemies = []
            self.items = []
    
    def start_game(self):
        """Initialize game after character creation"""
        # Create player at left spawn position
        spawn_x = ARENA_X + PLAYER_SPAWN_X
        spawn_y = ARENA_Y + PLAYER_SPAWN_Y
        
        self.player = Player(
            spawn_x, 
            spawn_y,
            race=self.selected_race,
            character_class=self.selected_class
        )
        
        # Reset game state
        self.current_floor = 1
        self.current_wave = 1
        self.time_survived = 0
        
        # Start first floor
        self.start_floor()
    
    def start_floor(self):
        """Start a new floor"""
        # Create arena room (just for collision detection)
        self.room = Room(ARENA_WIDTH, ARENA_HEIGHT)
        
        # Reset player position
        self.player.x = ARENA_X + PLAYER_SPAWN_X
        self.player.y = ARENA_Y + PLAYER_SPAWN_Y
        
        # Reset enemies
        self.enemies = []
        
        # Create wave spawner
        self.wave_spawner = WaveSpawner(
            Enemy, 
            spawn_interval=WAVE_SPAWN_INTERVAL,
            max_waves=WAVES_PER_FLOOR
        )
        
        # Start first wave
        self.wave_spawner.start_wave(self.current_wave, self.current_floor)
        
        # Spawn some health potions
        self.spawn_potions()
        
        self.state = 'playing'
    
    def spawn_potions(self):
        """Spawn health potions in arena"""
        import random
        self.items = []
        
        num_potions = 2 + self.current_floor // 2  # More potions on later floors
        
        for _ in range(num_potions):
            x = ARENA_X + random.randint(100, ARENA_WIDTH - 100)
            y = ARENA_Y + random.randint(100, ARENA_HEIGHT - 100)
            self.items.append(HealthPotion(x, y))
    
    def update(self):
        """Update game state"""
        if self.state == 'playing':
            self.update_playing()
        elif self.state == 'wave_complete':
            self.update_wave_complete()
        elif self.state == 'floor_complete':
            self.update_floor_complete()
    
    def update_playing(self):
        """Update playing state"""
        # Time tracking
        self.time_survived += self.dt
        
        # Update wave spawner
        new_enemies = self.wave_spawner.update(
            self.dt,
            ARENA_X + ENEMY_SPAWN_X,
            ARENA_Y + ENEMY_SPAWN_Y_MIN,
            ARENA_Y + ENEMY_SPAWN_Y_MAX
        )
        self.enemies.extend(new_enemies)
        
        # Update player
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = PLAYER_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = PLAYER_SPEED
        
        # Move player with arena bounds checking
        old_x, old_y = self.player.x, self.player.y
        self.player.x += dx
        self.player.y += dy
        
        # Keep in arena bounds
        player_rect = self.player.get_rect()
        if player_rect.left < ARENA_X:
            self.player.x = ARENA_X
        if player_rect.right > ARENA_X + ARENA_WIDTH:
            self.player.x = ARENA_X + ARENA_WIDTH - player_rect.width
        if player_rect.top < ARENA_Y:
            self.player.y = ARENA_Y
        if player_rect.bottom > ARENA_Y + ARENA_HEIGHT:
            self.player.y = ARENA_Y + ARENA_HEIGHT - player_rect.height
        
        # Update player
        self.player.update(self.dt)
        
        # Attack
        if keys[pygame.K_SPACE]:
            if self.player.attack_cooldown <= 0:
                self.player_attack()
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.dt, self.player, self.room)
            
            # Enemy attacks
            if enemy.can_attack():
                distance = ((self.player.x - enemy.x)**2 + (self.player.y - enemy.y)**2)**0.5
                attack_range = RANGED_RANGE if enemy.attack_type == 'ranged' else MELEE_RANGE
                
                if distance <= attack_range:
                    enemy.attack(self.player)
            
            # Remove dead enemies
            if not enemy.alive:
                self.enemies.remove(enemy)
                # Remove from wave spawner's active list too
                if enemy in self.wave_spawner.active_enemies:
                    self.wave_spawner.active_enemies.remove(enemy)
        
        # Update items
        for item in self.items[:]:
            if item.check_pickup(self.player):
                if isinstance(item, HealthPotion):
                    self.player.health_potions += 1
                    self.pickup_message = "Picked up Health Potion!"
                    self.pickup_timer = 2.0
                self.items.remove(item)
        
        # Update timers
        if self.pickup_timer > 0:
            self.pickup_timer -= self.dt
        
        # Check wave complete
        if self.wave_spawner.is_wave_complete() and len(self.enemies) == 0:
            if self.current_wave < WAVES_PER_FLOOR:
                self.state = 'wave_complete'
                self.wave_complete_timer = 0
            else:
                # All waves complete = floor complete
                self.state = 'floor_complete'
        
        # Check player death
        if self.player.hp <= 0:
            self.state = 'game_over'
    
    def update_wave_complete(self):
        """Update wave complete state"""
        self.wave_complete_timer += self.dt
    
    def update_floor_complete(self):
        """Update floor complete state"""
        pass
    
    def player_attack(self):
        """Handle player attacking"""
        self.player.attack_cooldown = ATTACK_COOLDOWN
        
        # Find enemies in range
        for enemy in self.enemies:
            distance = ((self.player.x - enemy.x)**2 + (self.player.y - enemy.y)**2)**0.5
            attack_range = RANGED_RANGE if self.player.weapon_type == 'ranged' else MELEE_RANGE
            
            if distance <= attack_range:
                # Deal damage
                damage = self.player.damage
                enemy.take_damage(damage)
    
    def draw(self):
        """Draw everything"""
        self.screen.fill(BLACK)
        
        if self.state == 'menu':
            self.draw_menu()
        elif self.state == 'character_creation':
            self.draw_character_creation()
        elif self.state == 'playing':
            self.draw_playing()
        elif self.state == 'wave_complete':
            self.draw_wave_complete()
        elif self.state == 'floor_complete':
            self.draw_floor_complete()
        elif self.state == 'game_over':
            self.draw_game_over()
        elif self.state == 'victory':
            self.draw_victory()
        
        pygame.display.flip()
    
    def draw_menu(self):
        """Draw main menu"""
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        
        # Title
        title = font_large.render("AI DUNGEON CRAWLER", True, CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = font_medium.render("Horizontal Arena Edition", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 220))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Menu options
        for i, option in enumerate(self.menu_options):
            color = YELLOW if i == self.menu_selection else WHITE
            text = font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 350 + i * 60))
            self.screen.blit(text, text_rect)
    
    def draw_character_creation(self):
        """Draw character creation screens"""
        font_large = pygame.font.Font(None, 64)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 28)
        
        if self.creation_step == 0:  # Race selection
            title = font_large.render("Choose Your Race", True, CYAN)
            self.screen.blit(title, (WINDOW_WIDTH // 2 - 200, 50))
            
            y = 150
            for i, race in enumerate(self.race_list):
                color = YELLOW if i == self.race_selection else WHITE
                race_data = RACES[race]
                
                # Race name
                text = font_medium.render(race_data['name'], True, color)
                self.screen.blit(text, (100, y))
                
                # Stats
                stats_text = f"HP:{race_data['base_hp']} ATK:{race_data['base_damage']} DEF:{race_data['base_defense']} SPD:{race_data['base_speed']}"
                stats = font_small.render(stats_text, True, color)
                self.screen.blit(stats, (120, y + 35))
                
                # Bonus
                bonus = font_small.render(race_data['bonus_text'], True, GREEN)
                self.screen.blit(bonus, (120, y + 60))
                
                y += 110
            
            # Instructions
            inst = font_small.render("UP/DOWN: Select  |  ENTER: Confirm", True, LIGHT_GRAY)
            self.screen.blit(inst, (WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT - 50))
            
        elif self.creation_step == 1:  # Class selection
            title = font_large.render("Choose Your Class", True, CYAN)
            self.screen.blit(title, (WINDOW_WIDTH // 2 - 220, 50))
            
            y = 150
            for i, char_class in enumerate(self.class_list):
                color = YELLOW if i == self.class_selection else WHITE
                class_data = CLASSES[char_class]
                
                # Class name
                text = font_medium.render(class_data['name'], True, color)
                self.screen.blit(text, (100, y))
                
                # Bonuses
                bonuses = f"ATK+{class_data['damage_bonus']} DEF+{class_data['defense_bonus']}"
                if class_data.get('hp_bonus', 0) > 0:
                    bonuses += f" HP+{class_data['hp_bonus']}"
                if class_data.get('speed_bonus', 0) > 0:
                    bonuses += f" SPD+{class_data['speed_bonus']}"
                
                bonus_text = font_small.render(bonuses, True, color)
                self.screen.blit(bonus_text, (120, y + 35))
                
                y += 100
            
            # Instructions
            inst = font_small.render("UP/DOWN: Select  |  BACKSPACE: Back  |  ENTER: Confirm", True, LIGHT_GRAY)
            self.screen.blit(inst, (WINDOW_WIDTH // 2 - 350, WINDOW_HEIGHT - 50))
            
        elif self.creation_step == 2:  # Name input
            title = font_large.render("Enter Your Name", True, CYAN)
            self.screen.blit(title, (WINDOW_WIDTH // 2 - 220, 100))
            
            # Name box
            name_text = font_large.render(self.player_name + "_", True, YELLOW)
            self.screen.blit(name_text, (WINDOW_WIDTH // 2 - 200, 250))
            
            # Preview
            preview = font_medium.render("Preview:", True, WHITE)
            self.screen.blit(preview, (100, 400))
            
            race_name = RACES[self.selected_race]['name']
            class_name = CLASSES[self.selected_class]['name']
            preview_text = f"{self.player_name or '[Name]'} - {race_name} {class_name}"
            preview_display = font_medium.render(preview_text, True, CYAN)
            self.screen.blit(preview_display, (120, 450))
            
            # Instructions
            inst = font_small.render("Type Name  |  BACKSPACE: Delete/Back  |  ENTER: Start", True, LIGHT_GRAY)
            self.screen.blit(inst, (WINDOW_WIDTH // 2 - 350, WINDOW_HEIGHT - 50))
    
    def draw_playing(self):
        """Draw playing state with horizontal UI"""
        # Draw UI panels
        self.ui_manager.draw_top_bar(self.current_floor, self.current_wave, WAVES_PER_FLOOR)
        self.ui_manager.draw_left_panel(self.player, self.player_name)
        self.ui_manager.draw_right_panel(self.wave_spawner, self.time_survived)
        self.ui_manager.draw_inventory(self.player)
        
        # Draw arena background
        arena_rect = pygame.Rect(ARENA_X, ARENA_Y, ARENA_WIDTH, ARENA_HEIGHT)
        pygame.draw.rect(self.screen, DARK_GRAY, arena_rect)
        pygame.draw.rect(self.screen, UI_BORDER, arena_rect, 2)
        
        # Draw items
        for item in self.items:
            item.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw pickup message
        if self.pickup_timer > 0:
            font = pygame.font.Font(None, 32)
            message = font.render(self.pickup_message, True, GREEN)
            self.screen.blit(message, (ARENA_X + ARENA_WIDTH // 2 - 100, ARENA_Y + 50))
        
        # Draw stat overlay if toggled
        if self.show_stats:
            self.draw_stat_overlay()
    
    def draw_wave_complete(self):
        """Draw wave complete screen"""
        # Draw playing state in background
        self.draw_playing()
        
        # Overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        
        # Title
        title = font_large.render(f"WAVE {self.current_wave} COMPLETE!", True, GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(title, title_rect)
        
        # Instruction
        inst = font_medium.render("Press ENTER for Next Wave", True, WHITE)
        inst_rect = inst.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(inst, inst_rect)
    
    def draw_floor_complete(self):
        """Draw floor complete screen"""
        # Draw playing state in background
        self.draw_playing()
        
        # Overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        
        # Title
        title = font_large.render(f"FLOOR {self.current_floor} COMPLETE!", True, GOLD)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(title, title_rect)
        
        # Instruction
        if self.current_floor < self.max_floor:
            inst = font_medium.render("Press ENTER for Next Floor", True, WHITE)
        else:
            inst = font_medium.render("Press ENTER to Continue", True, WHITE)
        inst_rect = inst.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(inst, inst_rect)
    
    def draw_game_over(self):
        """Draw game over screen"""
        self.screen.fill(BLACK)
        
        font_large = pygame.font.Font(None, 96)
        font_medium = pygame.font.Font(None, 48)
        
        # Title
        title = font_large.render("GAME OVER", True, RED)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(title, title_rect)
        
        # Stats
        stats_text = f"Reached Floor {self.current_floor}, Wave {self.current_wave}"
        stats = font_medium.render(stats_text, True, WHITE)
        stats_rect = stats.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(stats, stats_rect)
        
        # Instruction
        inst = font_medium.render("Press ENTER to Return to Menu", True, LIGHT_GRAY)
        inst_rect = inst.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        self.screen.blit(inst, inst_rect)
    
    def draw_victory(self):
        """Draw victory screen"""
        self.screen.fill(BLACK)
        
        font_large = pygame.font.Font(None, 96)
        font_medium = pygame.font.Font(None, 48)
        
        # Title
        title = font_large.render("VICTORY!", True, GOLD)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(title, title_rect)
        
        # Stats
        stats_text = f"Completed All {self.max_floor} Floors!"
        stats = font_medium.render(stats_text, True, WHITE)
        stats_rect = stats.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(stats, stats_rect)
        
        time_text = f"Time: {int(self.time_survived)}s"
        time_display = font_medium.render(time_text, True, CYAN)
        time_rect = time_display.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(time_display, time_rect)
        
        # Instruction
        inst = font_medium.render("Press ENTER to Return to Menu", True, LIGHT_GRAY)
        inst_rect = inst.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 150))
        self.screen.blit(inst, inst_rect)
    
    def draw_stat_overlay(self):
        """Draw full stat overlay (press I)"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(230)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 28)
        
        # Title
        title = font_large.render("CHARACTER STATS", True, CYAN)
        self.screen.blit(title, (WINDOW_WIDTH // 2 - 180, 50))
        
        # Get stats
        stats = self.player.get_stat_summary()
        
        y = 150
        x = WINDOW_WIDTH // 2 - 300
        
        # Display all stats
        stat_lines = [
            ("Name", self.player_name),
            ("Race", RACES[self.player.race]['name']),
            ("Class", CLASSES[self.player.character_class]['name']),
            ("", ""),
            ("HP", f"{int(self.player.hp)}/{self.player.max_hp}"),
            ("Damage", f"{stats['damage']} ({stats['base_damage']} + {stats['weapon_damage']})"),
            ("Defense", f"{stats['defense']} ({stats['base_defense']} + {stats['armor_defense']})"),
            ("Speed", f"{stats['speed']}"),
            ("", ""),
            ("Weapon", stats['weapon_name']),
            ("Armor", stats['armor_name']),
            ("", ""),
            ("Potions", str(self.player.health_potions)),
        ]
        
        for label, value in stat_lines:
            if label == "":
                y += 20
                continue
            
            label_text = font_medium.render(f"{label}:", True, YELLOW)
            value_text = font_medium.render(str(value), True, WHITE)
            self.screen.blit(label_text, (x, y))
            self.screen.blit(value_text, (x + 250, y))
            y += 40
        
        # Instructions
        inst = font_small.render("Press I to Close", True, LIGHT_GRAY)
        self.screen.blit(inst, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 50))
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Calculate delta time
            self.dt = self.clock.tick(FPS) / 1000.0  # Convert to seconds
            
            # Handle events
            self.handle_events()
            
            # Update
            self.update()
            
            # Draw
            self.draw()
        
        pygame.quit()
        sys.exit()

def main():
    """Entry point"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
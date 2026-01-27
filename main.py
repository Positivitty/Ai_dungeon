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
from game.particles import ParticleSystem
from game.animations import AnimationManager
from game.graphics import draw_gradient_rect, draw_rounded_rect, draw_text_with_shadow

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
        self.particle_system = ParticleSystem()
        self.animation_manager = AnimationManager()
        
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
                # Spawn heal particles and number
                player_center_x = self.player.x + self.player.width // 2
                player_center_y = self.player.y + self.player.height // 2
                self.particle_system.spawn_pickup_effect(player_center_x, player_center_y, (100, 255, 150))
                self.particle_system.spawn_heal_number(player_center_x, player_center_y - 20, heal_amount)
    
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

        # Reset visual systems
        self.particle_system.clear()
        self.animation_manager.clear()

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

        # Update visual systems
        self.particle_system.update(self.dt)
        self.animation_manager.update(self.dt)
        
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
                    old_hp = self.player.hp
                    enemy.attack(self.player)
                    damage_dealt = old_hp - self.player.hp

                    if damage_dealt > 0:
                        # Spawn damage particles on player
                        player_center_x = self.player.x + self.player.width // 2
                        player_center_y = self.player.y + self.player.height // 2
                        self.particle_system.spawn_damage_taken(player_center_x, player_center_y, damage_dealt)

                        # Spawn damage number
                        self.particle_system.spawn_damage_number(
                            player_center_x, player_center_y - 20,
                            damage_dealt, color=(255, 80, 80)
                        )

                        # Flash player and screen
                        self.animation_manager.trigger_entity_flash(id(self.player), (255, 50, 50))
                        self.animation_manager.trigger_screen_shake(intensity=5, duration=0.15)
                        self.animation_manager.trigger_screen_flash((255, 0, 0), alpha=50, duration=0.1)
            
            # Remove dead enemies
            if not enemy.alive:
                # Spawn death effect
                enemy_center_x = enemy.x + enemy.width // 2
                enemy_center_y = enemy.y + enemy.height // 2
                self.particle_system.spawn_death_effect(enemy_center_x, enemy_center_y, enemy.color)

                self.enemies.remove(enemy)
                # Remove from wave spawner's active list too
                if enemy in self.wave_spawner.active_enemies:
                    self.wave_spawner.active_enemies.remove(enemy)
        
        # Update items
        for item in self.items[:]:
            item.update(self.dt)  # Update item animations
            if item.check_pickup(self.player):
                if isinstance(item, HealthPotion):
                    self.player.health_potions += 1
                    self.pickup_message = "Picked up Health Potion!"
                    self.pickup_timer = 2.0
                    # Spawn pickup particles
                    self.particle_system.spawn_pickup_effect(
                        item.x + item.width // 2,
                        item.y + item.height // 2,
                        (100, 255, 100)
                    )
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

                # Spawn attack particles at enemy position
                enemy_center_x = enemy.x + enemy.width // 2
                enemy_center_y = enemy.y + enemy.height // 2
                direction = 'right' if self.player.x < enemy.x else 'left'
                self.particle_system.spawn_attack_effect(enemy_center_x, enemy_center_y, direction)

                # Spawn damage number
                self.particle_system.spawn_damage_number(
                    enemy_center_x, enemy_center_y - 20,
                    damage, color=(255, 255, 100)
                )

                # Flash the enemy
                self.animation_manager.trigger_entity_flash(id(enemy), (255, 255, 255))

                # Small screen shake on hit
                self.animation_manager.trigger_screen_shake(intensity=3, duration=0.1)
    
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
        # Draw gradient background
        draw_gradient_rect(self.screen, (40, 40, 60), (20, 20, 35), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)

        # Title with shadow
        draw_text_with_shadow(
            self.screen, "AI DUNGEON CRAWLER", font_large, CYAN,
            (WINDOW_WIDTH // 2 - 250, 140), shadow_offset=(3, 3)
        )

        # Subtitle
        draw_text_with_shadow(
            self.screen, "Horizontal Arena Edition", font_medium, WHITE,
            (WINDOW_WIDTH // 2 - 180, 210), shadow_offset=(2, 2)
        )

        # Menu options with modern button styling
        for i, option in enumerate(self.menu_options):
            y_pos = 330 + i * 70
            button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, y_pos, 300, 55)

            if i == self.menu_selection:
                # Selected button - highlighted gradient
                draw_gradient_rect(self.screen, (80, 80, 120), (50, 50, 80), button_rect, radius=CORNER_RADIUS)
                draw_rounded_rect(self.screen, (0, 0, 0, 0), button_rect, CORNER_RADIUS, border=2, border_color=CYAN)
                color = YELLOW
            else:
                # Normal button
                draw_gradient_rect(self.screen, (60, 60, 80), (40, 40, 55), button_rect, radius=CORNER_RADIUS)
                draw_rounded_rect(self.screen, (0, 0, 0, 0), button_rect, CORNER_RADIUS, border=1, border_color=UI_BORDER)
                color = WHITE

            # Button text
            text = font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_pos + 27))
            self.screen.blit(text, text_rect)
    
    def draw_character_creation(self):
        """Draw character creation screens"""
        # Draw gradient background
        draw_gradient_rect(self.screen, (40, 40, 60), (20, 20, 35), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

        font_large = pygame.font.Font(None, 64)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 28)

        if self.creation_step == 0:  # Race selection
            draw_text_with_shadow(self.screen, "Choose Your Race", font_large, CYAN,
                                 (WINDOW_WIDTH // 2 - 200, 50))

            y = 150
            for i, race in enumerate(self.race_list):
                race_data = RACES[race]
                card_rect = pygame.Rect(80, y - 10, WINDOW_WIDTH - 160, 100)

                if i == self.race_selection:
                    draw_gradient_rect(self.screen, (70, 70, 100), (45, 45, 65), card_rect, radius=CORNER_RADIUS)
                    draw_rounded_rect(self.screen, (0, 0, 0, 0), card_rect, CORNER_RADIUS, border=2, border_color=CYAN)
                    color = YELLOW
                else:
                    draw_gradient_rect(self.screen, (50, 50, 70), (35, 35, 50), card_rect, radius=CORNER_RADIUS)
                    color = WHITE

                # Race name
                text = font_medium.render(race_data['name'], True, color)
                self.screen.blit(text, (100, y))

                # Stats
                stats_text = f"HP:{race_data['base_hp']} ATK:{race_data['base_damage']} DEF:{race_data['base_defense']} SPD:{race_data['base_speed']}"
                stats = font_small.render(stats_text, True, LIGHT_GRAY if i != self.race_selection else WHITE)
                self.screen.blit(stats, (120, y + 35))

                # Bonus
                bonus = font_small.render(race_data['bonus_text'], True, GREEN)
                self.screen.blit(bonus, (120, y + 60))

                y += 115

            # Instructions panel
            inst_rect = pygame.Rect(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT - 60, 400, 40)
            draw_rounded_rect(self.screen, (40, 40, 50), inst_rect, CORNER_RADIUS_SMALL)
            inst = font_small.render("UP/DOWN: Select  |  ENTER: Confirm", True, LIGHT_GRAY)
            inst_rect_text = inst.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
            self.screen.blit(inst, inst_rect_text)

        elif self.creation_step == 1:  # Class selection
            draw_text_with_shadow(self.screen, "Choose Your Class", font_large, CYAN,
                                 (WINDOW_WIDTH // 2 - 220, 50))

            y = 150
            for i, char_class in enumerate(self.class_list):
                class_data = CLASSES[char_class]
                card_rect = pygame.Rect(80, y - 10, WINDOW_WIDTH - 160, 90)

                # Get class color for accent
                class_colors = PLAYER_COLORS.get(char_class, PLAYER_COLORS['warrior'])

                if i == self.class_selection:
                    draw_gradient_rect(self.screen, (70, 70, 100), (45, 45, 65), card_rect, radius=CORNER_RADIUS)
                    draw_rounded_rect(self.screen, (0, 0, 0, 0), card_rect, CORNER_RADIUS, border=2,
                                     border_color=class_colors['primary'])
                    color = YELLOW
                else:
                    draw_gradient_rect(self.screen, (50, 50, 70), (35, 35, 50), card_rect, radius=CORNER_RADIUS)
                    color = WHITE

                # Class name with color indicator
                pygame.draw.circle(self.screen, class_colors['primary'], (95, y + 12), 8)
                text = font_medium.render(class_data['name'], True, color)
                self.screen.blit(text, (115, y))

                # Bonuses
                bonuses = f"ATK+{class_data['damage_bonus']} DEF+{class_data['defense_bonus']}"
                if class_data.get('hp_bonus', 0) > 0:
                    bonuses += f" HP+{class_data['hp_bonus']}"
                if class_data.get('speed_bonus', 0) > 0:
                    bonuses += f" SPD+{class_data['speed_bonus']}"

                bonus_text = font_small.render(bonuses, True, LIGHT_GRAY if i != self.class_selection else WHITE)
                self.screen.blit(bonus_text, (120, y + 40))

                y += 105

            # Instructions
            inst_rect = pygame.Rect(WINDOW_WIDTH // 2 - 280, WINDOW_HEIGHT - 60, 560, 40)
            draw_rounded_rect(self.screen, (40, 40, 50), inst_rect, CORNER_RADIUS_SMALL)
            inst = font_small.render("UP/DOWN: Select  |  BACKSPACE: Back  |  ENTER: Confirm", True, LIGHT_GRAY)
            inst_rect_text = inst.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
            self.screen.blit(inst, inst_rect_text)

        elif self.creation_step == 2:  # Name input
            draw_text_with_shadow(self.screen, "Enter Your Name", font_large, CYAN,
                                 (WINDOW_WIDTH // 2 - 200, 100))

            # Name input box
            input_rect = pygame.Rect(WINDOW_WIDTH // 2 - 220, 230, 440, 60)
            draw_gradient_rect(self.screen, (50, 50, 70), (35, 35, 50), input_rect, radius=CORNER_RADIUS)
            draw_rounded_rect(self.screen, (0, 0, 0, 0), input_rect, CORNER_RADIUS, border=2, border_color=CYAN)

            name_text = font_large.render(self.player_name + "_", True, YELLOW)
            name_rect = name_text.get_rect(center=(WINDOW_WIDTH // 2, 260))
            self.screen.blit(name_text, name_rect)

            # Preview panel
            preview_rect = pygame.Rect(80, 380, WINDOW_WIDTH - 160, 100)
            draw_gradient_rect(self.screen, (50, 50, 70), (35, 35, 50), preview_rect, radius=CORNER_RADIUS)

            preview = font_medium.render("Preview:", True, WHITE)
            self.screen.blit(preview, (100, 395))

            race_name = RACES[self.selected_race]['name']
            class_name = CLASSES[self.selected_class]['name']
            class_colors = PLAYER_COLORS.get(self.selected_class, PLAYER_COLORS['warrior'])
            preview_text = f"{self.player_name or '[Name]'} - {race_name} {class_name}"
            preview_display = font_medium.render(preview_text, True, class_colors['primary'])
            self.screen.blit(preview_display, (120, 435))

            # Instructions
            inst_rect = pygame.Rect(WINDOW_WIDTH // 2 - 280, WINDOW_HEIGHT - 60, 560, 40)
            draw_rounded_rect(self.screen, (40, 40, 50), inst_rect, CORNER_RADIUS_SMALL)
            inst = font_small.render("Type Name  |  BACKSPACE: Delete/Back  |  ENTER: Start", True, LIGHT_GRAY)
            inst_rect_text = inst.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
            self.screen.blit(inst, inst_rect_text)
    
    def draw_playing(self):
        """Draw playing state with horizontal UI"""
        # Draw UI panels
        self.ui_manager.draw_top_bar(self.current_floor, self.current_wave, WAVES_PER_FLOOR)
        self.ui_manager.draw_left_panel(self.player, self.player_name)
        self.ui_manager.draw_right_panel(self.wave_spawner, self.time_survived)
        self.ui_manager.draw_inventory(self.player)

        # Get screen shake offset
        shake_x, shake_y = self.animation_manager.get_screen_offset()

        # Draw arena background with gradient
        arena_rect = pygame.Rect(ARENA_X + shake_x, ARENA_Y + shake_y, ARENA_WIDTH, ARENA_HEIGHT)
        draw_gradient_rect(self.screen, (50, 50, 60), (35, 35, 45), arena_rect)
        pygame.draw.rect(self.screen, UI_BORDER, arena_rect, 2)

        # Create arena surface for clipping (so entities don't draw outside arena)
        arena_surface = pygame.Surface((ARENA_WIDTH, ARENA_HEIGHT), pygame.SRCALPHA)

        # Draw items (with offset for shake)
        for item in self.items:
            # Temporarily adjust position for arena-local drawing
            orig_x, orig_y = item.x, item.y
            item.x -= ARENA_X
            item.y -= ARENA_Y
            item.draw(arena_surface)
            item.x, item.y = orig_x, orig_y

        # Draw player with flash effect
        orig_x, orig_y = self.player.x, self.player.y
        self.player.x -= ARENA_X
        self.player.y -= ARENA_Y
        player_flash = self.animation_manager.get_entity_flash(id(self.player))
        self.player.draw(arena_surface, flash=player_flash)
        self.player.x, self.player.y = orig_x, orig_y

        # Draw enemies with flash effects
        for enemy in self.enemies:
            orig_x, orig_y = enemy.x, enemy.y
            enemy.x -= ARENA_X
            enemy.y -= ARENA_Y
            enemy_flash = self.animation_manager.get_entity_flash(id(enemy))
            enemy.draw(arena_surface, flash=enemy_flash)
            enemy.x, enemy.y = orig_x, orig_y

        # Draw particles (in arena-local coordinates)
        for particle in self.particle_system.particles:
            particle.x -= ARENA_X
            particle.y -= ARENA_Y
        for dmg_num in self.particle_system.damage_numbers:
            dmg_num.x -= ARENA_X
            dmg_num.y -= ARENA_Y

        self.particle_system.draw(arena_surface)

        # Restore particle positions
        for particle in self.particle_system.particles:
            particle.x += ARENA_X
            particle.y += ARENA_Y
        for dmg_num in self.particle_system.damage_numbers:
            dmg_num.x += ARENA_X
            dmg_num.y += ARENA_Y

        # Draw screen flash on arena
        self.animation_manager.draw_screen_flash(arena_surface, pygame.Rect(0, 0, ARENA_WIDTH, ARENA_HEIGHT))

        # Blit arena surface with shake offset
        self.screen.blit(arena_surface, (ARENA_X + shake_x, ARENA_Y + shake_y))

        # Draw pickup message with shadow
        if self.pickup_timer > 0:
            font = pygame.font.Font(None, 32)
            draw_text_with_shadow(
                self.screen, self.pickup_message, font, GREEN,
                (ARENA_X + ARENA_WIDTH // 2 - 100, ARENA_Y + 50)
            )

        # Draw stat overlay if toggled
        if self.show_stats:
            self.draw_stat_overlay()
    
    def draw_wave_complete(self):
        """Draw wave complete screen"""
        # Draw playing state in background
        self.draw_playing()

        # Overlay with gradient
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        for y in range(WINDOW_HEIGHT):
            alpha = int(180 + 40 * (y / WINDOW_HEIGHT))
            pygame.draw.line(overlay, (0, 0, 0, alpha), (0, y), (WINDOW_WIDTH, y))
        self.screen.blit(overlay, (0, 0))

        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)

        # Title panel
        panel_rect = pygame.Rect(WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2 - 100, 500, 180)
        draw_gradient_rect(self.screen, (50, 80, 50), (30, 50, 30), panel_rect, radius=CORNER_RADIUS)
        draw_rounded_rect(self.screen, (0, 0, 0, 0), panel_rect, CORNER_RADIUS, border=3, border_color=GREEN)

        # Title
        draw_text_with_shadow(self.screen, f"WAVE {self.current_wave} COMPLETE!", font_large, GREEN,
                             (WINDOW_WIDTH // 2 - 220, WINDOW_HEIGHT // 2 - 70), shadow_offset=(3, 3))

        # Instruction
        inst = font_medium.render("Press ENTER for Next Wave", True, WHITE)
        inst_rect = inst.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
        self.screen.blit(inst, inst_rect)
    
    def draw_floor_complete(self):
        """Draw floor complete screen"""
        # Draw playing state in background
        self.draw_playing()

        # Overlay with gradient
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        for y in range(WINDOW_HEIGHT):
            alpha = int(180 + 40 * (y / WINDOW_HEIGHT))
            pygame.draw.line(overlay, (0, 0, 0, alpha), (0, y), (WINDOW_WIDTH, y))
        self.screen.blit(overlay, (0, 0))

        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)

        # Title panel with gold theme
        panel_rect = pygame.Rect(WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2 - 100, 500, 180)
        draw_gradient_rect(self.screen, (80, 70, 40), (50, 45, 25), panel_rect, radius=CORNER_RADIUS)
        draw_rounded_rect(self.screen, (0, 0, 0, 0), panel_rect, CORNER_RADIUS, border=3, border_color=GOLD)

        # Title
        draw_text_with_shadow(self.screen, f"FLOOR {self.current_floor} COMPLETE!", font_large, GOLD,
                             (WINDOW_WIDTH // 2 - 230, WINDOW_HEIGHT // 2 - 70), shadow_offset=(3, 3))

        # Instruction
        if self.current_floor < self.max_floor:
            inst = font_medium.render("Press ENTER for Next Floor", True, WHITE)
        else:
            inst = font_medium.render("Press ENTER to Continue", True, WHITE)
        inst_rect = inst.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
        self.screen.blit(inst, inst_rect)
    
    def draw_game_over(self):
        """Draw game over screen"""
        # Gradient background
        draw_gradient_rect(self.screen, (60, 30, 30), (20, 10, 10), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

        font_large = pygame.font.Font(None, 96)
        font_medium = pygame.font.Font(None, 48)

        # Main panel
        panel_rect = pygame.Rect(WINDOW_WIDTH // 2 - 300, WINDOW_HEIGHT // 2 - 150, 600, 300)
        draw_gradient_rect(self.screen, (70, 40, 40), (40, 20, 20), panel_rect, radius=CORNER_RADIUS)
        draw_rounded_rect(self.screen, (0, 0, 0, 0), panel_rect, CORNER_RADIUS, border=3, border_color=RED)

        # Title
        draw_text_with_shadow(self.screen, "GAME OVER", font_large, RED,
                             (WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT // 2 - 120), shadow_offset=(4, 4))

        # Stats
        stats_text = f"Reached Floor {self.current_floor}, Wave {self.current_wave}"
        stats = font_medium.render(stats_text, True, WHITE)
        stats_rect = stats.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(stats, stats_rect)

        # Instruction
        inst = font_medium.render("Press ENTER to Return to Menu", True, LIGHT_GRAY)
        inst_rect = inst.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        self.screen.blit(inst, inst_rect)
    
    def draw_victory(self):
        """Draw victory screen"""
        # Gradient background with golden tint
        draw_gradient_rect(self.screen, (60, 55, 30), (25, 20, 10), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

        font_large = pygame.font.Font(None, 96)
        font_medium = pygame.font.Font(None, 48)

        # Main panel
        panel_rect = pygame.Rect(WINDOW_WIDTH // 2 - 300, WINDOW_HEIGHT // 2 - 180, 600, 360)
        draw_gradient_rect(self.screen, (80, 70, 40), (50, 45, 25), panel_rect, radius=CORNER_RADIUS)
        draw_rounded_rect(self.screen, (0, 0, 0, 0), panel_rect, CORNER_RADIUS, border=3, border_color=GOLD)

        # Title
        draw_text_with_shadow(self.screen, "VICTORY!", font_large, GOLD,
                             (WINDOW_WIDTH // 2 - 140, WINDOW_HEIGHT // 2 - 150), shadow_offset=(4, 4))

        # Stats
        stats_text = f"Completed All {self.max_floor} Floors!"
        stats = font_medium.render(stats_text, True, WHITE)
        stats_rect = stats.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        self.screen.blit(stats, stats_rect)

        time_text = f"Time: {int(self.time_survived)}s"
        time_display = font_medium.render(time_text, True, CYAN)
        time_rect = time_display.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
        self.screen.blit(time_display, time_rect)

        # Instruction
        inst = font_medium.render("Press ENTER to Return to Menu", True, LIGHT_GRAY)
        inst_rect = inst.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 120))
        self.screen.blit(inst, inst_rect)
    
    def draw_stat_overlay(self):
        """Draw full stat overlay (press I)"""
        # Semi-transparent overlay with gradient
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        for y in range(WINDOW_HEIGHT):
            alpha = int(200 + 30 * (y / WINDOW_HEIGHT))
            pygame.draw.line(overlay, (0, 0, 0, alpha), (0, y), (WINDOW_WIDTH, y))
        self.screen.blit(overlay, (0, 0))

        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 28)

        # Main panel
        panel_rect = pygame.Rect(WINDOW_WIDTH // 2 - 350, 30, 700, WINDOW_HEIGHT - 80)
        draw_gradient_rect(self.screen, (50, 50, 70), (30, 30, 45), panel_rect, radius=CORNER_RADIUS)
        draw_rounded_rect(self.screen, (0, 0, 0, 0), panel_rect, CORNER_RADIUS, border=2, border_color=CYAN)

        # Title
        draw_text_with_shadow(self.screen, "CHARACTER STATS", font_large, CYAN,
                             (WINDOW_WIDTH // 2 - 150, 60))

        # Get stats
        stats = self.player.get_stat_summary()
        class_colors = PLAYER_COLORS.get(self.player.character_class, PLAYER_COLORS['warrior'])

        y = 130
        x = WINDOW_WIDTH // 2 - 280

        # Display all stats
        stat_lines = [
            ("Name", self.player_name, class_colors['primary']),
            ("Race", RACES[self.player.race]['name'], WHITE),
            ("Class", CLASSES[self.player.character_class]['name'], class_colors['primary']),
            ("", "", None),
            ("HP", f"{int(self.player.hp)}/{self.player.max_hp}", HEALTH_BAR_FULL),
            ("Damage", f"{stats['damage']} ({stats['base_damage']} + {stats['weapon_damage']})", (255, 200, 100)),
            ("Defense", f"{stats['defense']} ({stats['base_defense']} + {stats['armor_defense']})", (100, 200, 255)),
            ("Speed", f"{stats['speed']}", (200, 255, 200)),
            ("", "", None),
            ("Weapon", stats['weapon_name'], WHITE),
            ("Armor", stats['armor_name'], WHITE),
            ("", "", None),
            ("Potions", str(self.player.health_potions), GREEN),
        ]

        for label, value, value_color in stat_lines:
            if label == "":
                y += 15
                continue

            # Draw row background for alternating effect
            if stat_lines.index((label, value, value_color)) % 2 == 0:
                row_rect = pygame.Rect(x - 10, y - 5, 580, 35)
                draw_rounded_rect(self.screen, (40, 40, 55), row_rect, CORNER_RADIUS_SMALL)

            label_text = font_medium.render(f"{label}:", True, YELLOW)
            value_text = font_medium.render(str(value), True, value_color or WHITE)
            self.screen.blit(label_text, (x, y))
            self.screen.blit(value_text, (x + 200, y))
            y += 38

        # Instructions
        inst_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 60, 200, 35)
        draw_rounded_rect(self.screen, (40, 40, 50), inst_rect, CORNER_RADIUS_SMALL)
        inst = font_small.render("Press I to Close", True, LIGHT_GRAY)
        inst_text_rect = inst.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 42))
        self.screen.blit(inst, inst_text_rect)
    
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
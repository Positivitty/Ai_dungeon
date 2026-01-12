#!/usr/bin/env python3
"""
AI Dungeon Crawler - Main Entry Point
A dungeon crawler where an AI companion learns to fight through reinforcement learning
"""

import pygame
import sys
from config import *
from game.player import Player
from game.enemies import Enemy

class Game:
    """Main game class that manages the game loop and states"""
    
    def __init__(self):
        """Initialize pygame and game components"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        
        # Game state
        self.state = 'playing'  # menu, tutorial, playing, game_over
        
        # Create test player and enemies
        self.player = Player(200, 200, weapon='sword', armor='heavy')
        self.enemies = [
            Enemy(500, 200, 'goblin'),
            Enemy(300, 350, 'skeleton'),
            Enemy(600, 350, 'goblin_archer')
        ]
        
        # Camera offset for game area
        self.camera_x = GAME_AREA_X
        self.camera_y = GAME_AREA_Y
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.player.attack()
                elif event.key == pygame.K_p:
                    self.player.use_health_potion()
    
    def handle_input(self):
        """Handle continuous keyboard input for movement"""
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1
        
        if dx != 0 or dy != 0:
            self.player.move(dx, dy)
    
    def update(self):
        """Update game logic"""
        if self.state == 'playing':
            self.handle_input()
            
            # Update player
            self.player.update(self.dt)
            
            # Update enemies
            for enemy in self.enemies:
                enemy.update(self.dt, self.player)
            
            # Check player attacks
            if self.player.attack_cooldown == 0 or self.player.attack_cooldown < ATTACK_COOLDOWN - 0.1:
                # Player just attacked
                player_rect = self.player.get_rect()
                for enemy in self.enemies:
                    if enemy.alive:
                        enemy_rect = enemy.get_rect()
                        distance = self.player.distance_to_enemy(enemy)
                        if distance <= self.player.attack_range:
                            enemy.take_damage(self.player.damage)
            
            # Remove dead enemies
            self.enemies = [e for e in self.enemies if e.alive or e.hp > 0]
            
            # Check game over
            if not self.player.alive:
                self.state = 'game_over'
    
    def draw(self):
        """Render everything to screen"""
        self.screen.fill(DARK_GRAY)
        
        # Draw game area background
        game_area = pygame.Rect(GAME_AREA_X, GAME_AREA_Y, GAME_AREA_WIDTH, GAME_AREA_HEIGHT)
        pygame.draw.rect(self.screen, BLACK, game_area)
        
        # Create surface for game area
        game_surface = pygame.Surface((GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
        game_surface.fill(BLACK)
        
        # Draw player and enemies on game surface
        self.player.draw(game_surface)
        for enemy in self.enemies:
            enemy.draw(game_surface)
        
        # Blit game surface to screen
        self.screen.blit(game_surface, (GAME_AREA_X, GAME_AREA_Y))
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        """Draw UI elements (health bar, etc.)"""
        font = pygame.font.Font(None, 24)
        
        # Health bar
        hp_text = font.render(f"HP: {int(self.player.hp)}/{self.player.max_hp}", True, WHITE)
        self.screen.blit(hp_text, (10, 10))
        
        # HP bar graphic
        bar_x, bar_y = 10, 35
        bar_width, bar_height = 200, 20
        pygame.draw.rect(self.screen, RED, (bar_x, bar_y, bar_width, bar_height))
        hp_width = int((self.player.hp / self.player.max_hp) * bar_width)
        pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, hp_width, bar_height))
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Equipment info
        weapon_text = font.render(f"Weapon: {WEAPONS[self.player.weapon]['name']}", True, WHITE)
        armor_text = font.render(f"Armor: {ARMORS[self.player.armor]['name']}", True, WHITE)
        self.screen.blit(weapon_text, (10, 65))
        self.screen.blit(armor_text, (10, 90))
        
        # Controls
        controls = [
            "WASD/Arrows: Move",
            "SPACE: Attack",
            "P: Use Potion",
            "ESC: Quit"
        ]
        for i, control in enumerate(controls):
            text = font.render(control, True, LIGHT_GRAY)
            self.screen.blit(text, (WINDOW_WIDTH - 200, 10 + i * 25))
        
        # Enemy count
        alive_enemies = len([e for e in self.enemies if e.alive])
        enemy_text = font.render(f"Enemies: {alive_enemies}", True, CYAN)
        self.screen.blit(enemy_text, (WINDOW_WIDTH // 2 - 50, 10))
        
        # Game over
        if self.state == 'game_over':
            big_font = pygame.font.Font(None, 74)
            game_over = big_font.render("GAME OVER", True, RED)
            rect = game_over.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(game_over, rect)
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0  # Convert to seconds
            self.handle_events()
            self.update()
            self.draw()
        
        pygame.quit()
        sys.exit()

def main():
    """Entry point"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()

"""
UI Drawing System for horizontal arena layout
Handles stat panel, inventory, and wave info
"""

import pygame
from config import *

class UIManager:
    """Manages all UI drawing"""
    
    def __init__(self, screen):
        """
        Initialize UI manager
        
        Args:
            screen: pygame screen surface
        """
        self.screen = screen
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 22)
        
    def draw_top_bar(self, floor, wave, total_waves):
        """Draw top status bar"""
        pygame.draw.rect(self.screen, UI_BACKGROUND, (0, 0, WINDOW_WIDTH, TOP_BAR_HEIGHT))
        pygame.draw.line(self.screen, UI_BORDER, (0, TOP_BAR_HEIGHT), (WINDOW_WIDTH, TOP_BAR_HEIGHT), 2)
        
        # Title
        title = self.font_large.render("AI DUNGEON CRAWLER", True, CYAN)
        self.screen.blit(title, (WINDOW_WIDTH // 2 - 150, 5))
        
        # Floor/Wave info
        info = self.font_medium.render(f"Floor {floor} - Wave {wave}/{total_waves}", True, WHITE)
        self.screen.blit(info, (WINDOW_WIDTH - 300, 10))
    
    def draw_left_panel(self, player, player_name=""):
        """Draw left stat panel"""
        panel_rect = pygame.Rect(0, TOP_BAR_HEIGHT, LEFT_PANEL_WIDTH, WINDOW_HEIGHT - TOP_BAR_HEIGHT)
        pygame.draw.rect(self.screen, UI_BACKGROUND, panel_rect)
        pygame.draw.line(self.screen, UI_BORDER, (LEFT_PANEL_WIDTH, TOP_BAR_HEIGHT), 
                        (LEFT_PANEL_WIDTH, WINDOW_HEIGHT), 2)
        
        y = TOP_BAR_HEIGHT + 10
        x = 10
        
        # Character name
        if player_name:
            name = self.font_medium.render(player_name, True, CYAN)
            self.screen.blit(name, (x, y))
            y += 35
        
        # Race/Class
        from game.character import RACES, CLASSES
        race_class = f"{RACES[player.race]['name']} {CLASSES[player.character_class]['name']}"
        rc_text = self.font_small.render(race_class, True, WHITE)
        self.screen.blit(rc_text, (x, y))
        y += 30
        
        # Divider
        pygame.draw.line(self.screen, UI_BORDER, (x, y), (LEFT_PANEL_WIDTH - 10, y), 1)
        y += 15
        
        # Stats header
        stats_header = self.font_medium.render("STATS", True, YELLOW)
        self.screen.blit(stats_header, (x, y))
        y += 30
        
        # HP
        hp_text = self.font_small.render(f"HP: {int(player.hp)}/{player.max_hp}", True, WHITE)
        self.screen.blit(hp_text, (x, y))
        y += 5
        
        # HP Bar
        bar_width = LEFT_PANEL_WIDTH - 20
        bar_height = 20
        pygame.draw.rect(self.screen, RED, (x, y, bar_width, bar_height))
        hp_fill = int((player.hp / player.max_hp) * bar_width)
        pygame.draw.rect(self.screen, GREEN, (x, y, hp_fill, bar_height))
        pygame.draw.rect(self.screen, WHITE, (x, y, bar_width, bar_height), 2)
        y += 30
        
        # Other stats
        stats = player.get_stat_summary()
        stat_lines = [
            f"ATK: {stats['damage']} ({stats['base_damage']}+{stats['weapon_damage']})",
            f"DEF: {stats['defense']} ({stats['base_defense']}+{stats['armor_defense']})",
            f"SPD: {stats['speed']}",
        ]
        
        for line in stat_lines:
            text = self.font_small.render(line, True, WHITE)
            self.screen.blit(text, (x, y))
            y += 25
        
        y += 10
        pygame.draw.line(self.screen, UI_BORDER, (x, y), (LEFT_PANEL_WIDTH - 10, y), 1)
        y += 15
        
        # Equipment header
        equip_header = self.font_medium.render("EQUIPMENT", True, YELLOW)
        self.screen.blit(equip_header, (x, y))
        y += 30
        
        # Weapon
        weapon_text = self.font_small.render(f"⚔ {stats['weapon_name']}", True, WHITE)
        self.screen.blit(weapon_text, (x, y))
        y += 25
        
        # Armor
        armor_text = self.font_small.render(f"🛡 {stats['armor_name']}", True, WHITE)
        self.screen.blit(armor_text, (x, y))
        y += 30
        
        # Skills header (placeholder)
        pygame.draw.line(self.screen, UI_BORDER, (x, y), (LEFT_PANEL_WIDTH - 10, y), 1)
        y += 15
        
        skills_header = self.font_medium.render("SKILLS", True, YELLOW)
        self.screen.blit(skills_header, (x, y))
        y += 30
        
        # Placeholder skills
        skills = ["Attack (SPACE)", "Defend (D)", "Special (Q)"]
        for skill in skills:
            skill_text = self.font_small.render(skill, True, LIGHT_GRAY)
            self.screen.blit(skill_text, (x, y))
            y += 25
    
    def draw_right_panel(self, wave_spawner, time_survived=0):
        """Draw right info panel"""
        panel_x = WINDOW_WIDTH - RIGHT_PANEL_WIDTH
        panel_rect = pygame.Rect(panel_x, TOP_BAR_HEIGHT, RIGHT_PANEL_WIDTH, 
                                 WINDOW_HEIGHT - TOP_BAR_HEIGHT)
        pygame.draw.rect(self.screen, UI_BACKGROUND, panel_rect)
        pygame.draw.line(self.screen, UI_BORDER, (panel_x, TOP_BAR_HEIGHT), 
                        (panel_x, WINDOW_HEIGHT), 2)
        
        y = TOP_BAR_HEIGHT + 20
        x = panel_x + 10
        
        # Wave info
        wave_text = self.font_medium.render(f"Wave {wave_spawner.current_wave}/{wave_spawner.max_waves}", True, CYAN)
        self.screen.blit(wave_text, (x, y))
        y += 35
        
        # Enemies remaining
        enemies_left = wave_spawner.get_enemies_remaining()
        enemy_text = self.font_small.render(f"Enemies: {enemies_left}", True, RED if enemies_left > 0 else GREEN)
        self.screen.blit(enemy_text, (x, y))
        y += 30
        
        # Status
        if wave_spawner.wave_active:
            status = "SPAWNING"
            color = YELLOW
        elif enemies_left > 0:
            status = "FIGHT!"
            color = RED
        else:
            status = "CLEAR"
            color = GREEN
        
        status_text = self.font_medium.render(status, True, color)
        self.screen.blit(status_text, (x, y))
        y += 40
        
        pygame.draw.line(self.screen, UI_BORDER, (x, y), (WINDOW_WIDTH - 10, y), 1)
        y += 20
        
        # Time
        time_text = self.font_small.render(f"Time: {int(time_survived)}s", True, WHITE)
        self.screen.blit(time_text, (x, y))
    
    def draw_inventory(self, player):
        """Draw bottom inventory bar"""
        inv_y = WINDOW_HEIGHT - INVENTORY_HEIGHT
        inv_rect = pygame.Rect(0, inv_y, WINDOW_WIDTH, INVENTORY_HEIGHT)
        pygame.draw.rect(self.screen, UI_BACKGROUND, inv_rect)
        pygame.draw.line(self.screen, UI_BORDER, (0, inv_y), (WINDOW_WIDTH, inv_y), 2)
        
        # Inventory title
        title = self.font_medium.render("INVENTORY", True, YELLOW)
        self.screen.blit(title, (10, inv_y + 10))
        
        # Draw item slots
        slot_y = inv_y + 40
        slot_x_start = 20
        
        for i in range(INVENTORY_SLOTS):
            slot_x = slot_x_start + i * (ITEM_SLOT_SIZE + ITEM_SLOT_PADDING)
            slot_rect = pygame.Rect(slot_x, slot_y, ITEM_SLOT_SIZE, ITEM_SLOT_SIZE)
            
            # Draw slot background
            pygame.draw.rect(self.screen, (50, 50, 50), slot_rect)
            pygame.draw.rect(self.screen, UI_BORDER, slot_rect, 2)
            
            # Draw potion in first slot if available
            if i == 0 and player.health_potions > 0:
                # Draw potion icon (green circle)
                center_x = slot_x + ITEM_SLOT_SIZE // 2
                center_y = slot_y + ITEM_SLOT_SIZE // 2
                pygame.draw.circle(self.screen, GREEN, (center_x, center_y), 20)
                
                # Draw count
                count_text = self.font_small.render(str(player.health_potions), True, WHITE)
                count_rect = count_text.get_rect(center=(center_x, center_y))
                self.screen.blit(count_text, count_rect)
        
        # Controls hint
        controls = self.font_small.render("P: Use Potion | I: Stats | WASD: Move | SPACE: Attack", 
                                         True, LIGHT_GRAY)
        self.screen.blit(controls, (slot_x_start, inv_y + 10))
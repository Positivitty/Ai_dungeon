"""
UI Drawing System for horizontal arena layout
Handles stat panel, inventory, and wave info with modern visuals
"""

import pygame
from config import *
from game.graphics import (draw_rounded_rect, draw_gradient_rect, draw_shadow,
                           draw_health_bar, draw_text_with_shadow, interpolate_color)


class UIManager:
    """Manages all UI drawing with modern styling"""

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
        """Draw top status bar with gradient"""
        # Gradient background
        draw_gradient_rect(self.screen, GRADIENT_HEADER[0], GRADIENT_HEADER[1],
                          (0, 0, WINDOW_WIDTH, TOP_BAR_HEIGHT))

        # Bottom border with subtle shadow
        pygame.draw.line(self.screen, (20, 20, 25), (0, TOP_BAR_HEIGHT), (WINDOW_WIDTH, TOP_BAR_HEIGHT), 3)
        pygame.draw.line(self.screen, UI_BORDER, (0, TOP_BAR_HEIGHT - 1), (WINDOW_WIDTH, TOP_BAR_HEIGHT - 1), 1)

        # Title with shadow
        draw_text_with_shadow(self.screen, "AI DUNGEON CRAWLER", self.font_large, CYAN,
                             (WINDOW_WIDTH // 2 - 140, 8), shadow_offset=(2, 2))

        # Floor/Wave info panel
        info_text = f"Floor {floor} - Wave {wave}/{total_waves}"
        info_width = self.font_medium.size(info_text)[0] + 20
        info_rect = pygame.Rect(WINDOW_WIDTH - info_width - 15, 5, info_width, TOP_BAR_HEIGHT - 10)
        draw_rounded_rect(self.screen, (40, 40, 55), info_rect, CORNER_RADIUS_SMALL)
        draw_rounded_rect(self.screen, (0, 0, 0, 0), info_rect, CORNER_RADIUS_SMALL,
                         border=1, border_color=(80, 80, 100))

        info = self.font_medium.render(info_text, True, WHITE)
        self.screen.blit(info, (info_rect.x + 10, info_rect.y + 5))
    
    def draw_left_panel(self, player, player_name=""):
        """Draw left stat panel with modern styling"""
        panel_rect = pygame.Rect(0, TOP_BAR_HEIGHT, LEFT_PANEL_WIDTH, WINDOW_HEIGHT - TOP_BAR_HEIGHT)

        # Gradient background
        draw_gradient_rect(self.screen, GRADIENT_PANEL[0], GRADIENT_PANEL[1], panel_rect)

        # Right border with shadow effect
        pygame.draw.line(self.screen, (20, 20, 25), (LEFT_PANEL_WIDTH, TOP_BAR_HEIGHT),
                        (LEFT_PANEL_WIDTH, WINDOW_HEIGHT), 3)
        pygame.draw.line(self.screen, UI_BORDER, (LEFT_PANEL_WIDTH - 1, TOP_BAR_HEIGHT),
                        (LEFT_PANEL_WIDTH - 1, WINDOW_HEIGHT), 1)

        y = TOP_BAR_HEIGHT + 15
        x = 12

        # Get class colors
        class_colors = PLAYER_COLORS.get(player.character_class, PLAYER_COLORS['warrior'])

        # Character name with class color
        if player_name:
            draw_text_with_shadow(self.screen, player_name, self.font_medium, class_colors['primary'],
                                 (x, y), shadow_offset=(1, 1))
            y += 32

        # Race/Class
        from game.character import RACES, CLASSES
        race_class = f"{RACES[player.race]['name']} {CLASSES[player.character_class]['name']}"
        rc_text = self.font_small.render(race_class, True, LIGHT_GRAY)
        self.screen.blit(rc_text, (x, y))
        y += 28

        # Section: STATS
        y = self._draw_section_header(x, y, "STATS", LEFT_PANEL_WIDTH - 10)

        # HP with modern bar
        hp_text = self.font_small.render(f"HP: {int(player.hp)}/{player.max_hp}", True, WHITE)
        self.screen.blit(hp_text, (x, y))
        y += 22

        bar_width = LEFT_PANEL_WIDTH - 24
        draw_health_bar(self.screen, x, y, bar_width, 18,
                       player.hp, player.max_hp,
                       bar_color_full=HEALTH_BAR_FULL, bar_color_empty=HEALTH_BAR_EMPTY,
                       bg_color=(25, 25, 35), border_color=(60, 60, 80), radius=4)
        y += 28

        # Other stats with icons/colors
        stats = player.get_stat_summary()
        stat_items = [
            ("ATK", stats['damage'], f"({stats['base_damage']}+{stats['weapon_damage']})", (255, 180, 100)),
            ("DEF", stats['defense'], f"({stats['base_defense']}+{stats['armor_defense']})", (100, 180, 255)),
            ("SPD", stats['speed'], "", (180, 255, 180)),
        ]

        for label, value, detail, color in stat_items:
            # Stat row background
            row_rect = pygame.Rect(x - 2, y - 2, bar_width + 4, 22)
            draw_rounded_rect(self.screen, (35, 35, 45), row_rect, CORNER_RADIUS_SMALL)

            label_text = self.font_small.render(f"{label}:", True, color)
            value_text = self.font_small.render(str(value), True, WHITE)
            detail_text = self.font_small.render(detail, True, LIGHT_GRAY)

            self.screen.blit(label_text, (x + 5, y))
            self.screen.blit(value_text, (x + 50, y))
            self.screen.blit(detail_text, (x + 85, y))
            y += 26

        y += 8

        # Section: EQUIPMENT
        y = self._draw_section_header(x, y, "EQUIPMENT", LEFT_PANEL_WIDTH - 10)

        # Weapon with icon
        weapon_row = pygame.Rect(x - 2, y - 2, bar_width + 4, 24)
        draw_rounded_rect(self.screen, (35, 35, 45), weapon_row, CORNER_RADIUS_SMALL)
        weapon_text = self.font_small.render(f"Wpn: {stats['weapon_name']}", True, (255, 200, 150))
        self.screen.blit(weapon_text, (x + 5, y))
        y += 28

        # Armor with icon
        armor_row = pygame.Rect(x - 2, y - 2, bar_width + 4, 24)
        draw_rounded_rect(self.screen, (35, 35, 45), armor_row, CORNER_RADIUS_SMALL)
        armor_text = self.font_small.render(f"Arm: {stats['armor_name']}", True, (150, 200, 255))
        self.screen.blit(armor_text, (x + 5, y))
        y += 32

        # Section: CONTROLS
        y = self._draw_section_header(x, y, "CONTROLS", LEFT_PANEL_WIDTH - 10)

        controls = [
            ("WASD", "Move"),
            ("SPACE", "Attack"),
            ("P", "Use Potion"),
            ("I", "Stats"),
        ]

        for key, action in controls:
            # Key badge
            key_width = self.font_small.size(key)[0] + 8
            key_rect = pygame.Rect(x, y, key_width, 18)
            draw_rounded_rect(self.screen, (50, 50, 65), key_rect, 3)
            draw_rounded_rect(self.screen, (0, 0, 0, 0), key_rect, 3, border=1, border_color=(80, 80, 100))

            key_text = self.font_small.render(key, True, CYAN)
            self.screen.blit(key_text, (x + 4, y + 1))

            action_text = self.font_small.render(action, True, LIGHT_GRAY)
            self.screen.blit(action_text, (x + key_width + 8, y + 1))
            y += 22

    def _draw_section_header(self, x, y, title, width):
        """Draw a section header with divider line"""
        # Divider line
        pygame.draw.line(self.screen, (50, 50, 60), (x, y), (width, y), 1)
        y += 10

        # Header text
        header = self.font_medium.render(title, True, YELLOW)
        self.screen.blit(header, (x, y))
        y += 28

        return y
    
    def draw_right_panel(self, wave_spawner, time_survived=0):
        """Draw right info panel with modern styling"""
        panel_x = WINDOW_WIDTH - RIGHT_PANEL_WIDTH
        panel_rect = pygame.Rect(panel_x, TOP_BAR_HEIGHT, RIGHT_PANEL_WIDTH,
                                 WINDOW_HEIGHT - TOP_BAR_HEIGHT)

        # Gradient background
        draw_gradient_rect(self.screen, GRADIENT_PANEL[0], GRADIENT_PANEL[1], panel_rect)

        # Left border with shadow
        pygame.draw.line(self.screen, (20, 20, 25), (panel_x, TOP_BAR_HEIGHT),
                        (panel_x, WINDOW_HEIGHT), 3)
        pygame.draw.line(self.screen, UI_BORDER, (panel_x + 1, TOP_BAR_HEIGHT),
                        (panel_x + 1, WINDOW_HEIGHT), 1)

        y = TOP_BAR_HEIGHT + 15
        x = panel_x + 12
        content_width = RIGHT_PANEL_WIDTH - 24

        # Wave info card
        wave_card = pygame.Rect(x - 2, y - 2, content_width + 4, 50)
        draw_gradient_rect(self.screen, (50, 50, 70), (35, 35, 50), wave_card, radius=CORNER_RADIUS)
        draw_rounded_rect(self.screen, (0, 0, 0, 0), wave_card, CORNER_RADIUS,
                         border=1, border_color=CYAN)

        wave_text = f"Wave {wave_spawner.current_wave}/{wave_spawner.max_waves}"
        draw_text_with_shadow(self.screen, wave_text, self.font_medium, CYAN,
                             (x + 8, y + 5), shadow_offset=(1, 1))

        # Wave progress bar
        wave_progress = wave_spawner.current_wave / max(1, wave_spawner.max_waves)
        bar_y = y + 28
        bar_width = content_width - 16
        pygame.draw.rect(self.screen, (30, 30, 40), (x + 8, bar_y, bar_width, 8), border_radius=4)
        fill_width = int(bar_width * wave_progress)
        if fill_width > 0:
            pygame.draw.rect(self.screen, CYAN, (x + 8, bar_y, fill_width, 8), border_radius=4)

        y += 60

        # Enemies remaining
        enemies_left = wave_spawner.get_enemies_remaining()
        enemy_color = (255, 100, 100) if enemies_left > 0 else (100, 255, 100)

        enemy_card = pygame.Rect(x - 2, y, content_width + 4, 35)
        draw_rounded_rect(self.screen, (35, 35, 45), enemy_card, CORNER_RADIUS_SMALL)

        enemy_label = self.font_small.render("Enemies:", True, LIGHT_GRAY)
        enemy_count = self.font_medium.render(str(enemies_left), True, enemy_color)
        self.screen.blit(enemy_label, (x + 8, y + 8))
        self.screen.blit(enemy_count, (x + content_width - 30, y + 6))
        y += 45

        # Status indicator
        if wave_spawner.wave_active:
            status = "SPAWNING"
            status_color = YELLOW
            bg_color = (60, 60, 40)
        elif enemies_left > 0:
            status = "FIGHT!"
            status_color = RED
            bg_color = (60, 40, 40)
        else:
            status = "CLEAR"
            status_color = GREEN
            bg_color = (40, 60, 40)

        status_card = pygame.Rect(x - 2, y, content_width + 4, 40)
        draw_gradient_rect(self.screen, bg_color, tuple(c - 15 for c in bg_color),
                          status_card, radius=CORNER_RADIUS)
        draw_rounded_rect(self.screen, (0, 0, 0, 0), status_card, CORNER_RADIUS,
                         border=2, border_color=status_color)

        status_text = self.font_medium.render(status, True, status_color)
        status_rect = status_text.get_rect(center=(x + content_width // 2, y + 20))
        self.screen.blit(status_text, status_rect)
        y += 55

        # Divider
        pygame.draw.line(self.screen, (50, 50, 60), (x, y), (x + content_width, y), 1)
        y += 15

        # Time survived
        time_card = pygame.Rect(x - 2, y, content_width + 4, 35)
        draw_rounded_rect(self.screen, (35, 35, 45), time_card, CORNER_RADIUS_SMALL)

        time_label = self.font_small.render("Time:", True, LIGHT_GRAY)
        time_value = self.font_medium.render(f"{int(time_survived)}s", True, WHITE)
        self.screen.blit(time_label, (x + 8, y + 8))
        self.screen.blit(time_value, (x + content_width - 50, y + 6))
    
    def draw_inventory(self, player):
        """Draw bottom inventory bar with modern styling"""
        inv_y = WINDOW_HEIGHT - INVENTORY_HEIGHT
        inv_rect = pygame.Rect(0, inv_y, WINDOW_WIDTH, INVENTORY_HEIGHT)

        # Gradient background
        draw_gradient_rect(self.screen, GRADIENT_HEADER[0], GRADIENT_HEADER[1], inv_rect)

        # Top border with shadow
        pygame.draw.line(self.screen, (20, 20, 25), (0, inv_y), (WINDOW_WIDTH, inv_y), 3)
        pygame.draw.line(self.screen, UI_BORDER, (0, inv_y + 1), (WINDOW_WIDTH, inv_y + 1), 1)

        # Draw item slots
        slot_y = inv_y + 20
        slot_x_start = LEFT_PANEL_WIDTH + 20

        for i in range(INVENTORY_SLOTS):
            slot_x = slot_x_start + i * (ITEM_SLOT_SIZE + ITEM_SLOT_PADDING)
            slot_rect = pygame.Rect(slot_x, slot_y, ITEM_SLOT_SIZE, ITEM_SLOT_SIZE)

            # Slot background with gradient
            draw_gradient_rect(self.screen, (45, 45, 55), (30, 30, 40), slot_rect, radius=CORNER_RADIUS)

            # Draw potion in first slot if available
            if i == 0 and player.health_potions > 0:
                # Glow effect for potion slot
                from game.graphics import draw_glow
                draw_glow(self.screen, slot_rect, (80, 200, 100), intensity=30, radius=5)

                # Potion icon (gradient circle)
                center_x = slot_x + ITEM_SLOT_SIZE // 2
                center_y = slot_y + ITEM_SLOT_SIZE // 2

                # Bottle shape
                pygame.draw.ellipse(self.screen, (60, 180, 80),
                                   (center_x - 15, center_y - 12, 30, 24))
                pygame.draw.rect(self.screen, (70, 190, 90),
                                (center_x - 5, center_y - 18, 10, 8))
                pygame.draw.rect(self.screen, (160, 120, 80),
                                (center_x - 6, center_y - 22, 12, 5), border_radius=2)

                # Highlight
                pygame.draw.circle(self.screen, (150, 255, 180), (center_x - 5, center_y - 5), 4)

                # Count badge
                count_badge = pygame.Rect(slot_x + ITEM_SLOT_SIZE - 20, slot_y + ITEM_SLOT_SIZE - 20, 20, 20)
                draw_rounded_rect(self.screen, (200, 60, 60), count_badge, 10)
                count_text = self.font_small.render(str(player.health_potions), True, WHITE)
                count_rect = count_text.get_rect(center=(count_badge.centerx, count_badge.centery))
                self.screen.blit(count_text, count_rect)

                # Slot border (highlighted)
                draw_rounded_rect(self.screen, (0, 0, 0, 0), slot_rect, CORNER_RADIUS,
                                 border=2, border_color=(100, 200, 120))
            else:
                # Empty slot border
                draw_rounded_rect(self.screen, (0, 0, 0, 0), slot_rect, CORNER_RADIUS,
                                 border=1, border_color=(60, 60, 70))

        # Potion count text
        potion_label = f"Health Potions: {player.health_potions}"
        potion_text = self.font_medium.render(potion_label, True, WHITE if player.health_potions > 0 else LIGHT_GRAY)
        self.screen.blit(potion_text, (slot_x_start, inv_y + INVENTORY_HEIGHT - 28))
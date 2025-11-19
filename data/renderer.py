"""
Rendering system for Escape the Castle game.
"""

import pygame
import random
from .constants import *
from .utils import wrap_text, draw_health_bar

class Renderer:
    """Handles all game rendering."""
    
    def __init__(self, screen, width, height, font, small_font):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font
        self.small_font = small_font
        self.background_image = None
        self.variation_images = {}
        self.enemy_images = {}
    
    def load_background(self, image_path):
        """Load the background image."""
        from .utils import load_image
        self.background_image = load_image(image_path, (self.width, self.height))
    
    def load_variation_images(self, script_dir):
        """Load all variation images."""
        from .utils import load_image
        import os
        
        image_dir = os.path.join(script_dir, "images", "game", "variations")
        if not os.path.isdir(image_dir):
            print(f"Variation image directory not found: {image_dir}")
            return
            
        for filename in os.listdir(image_dir):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(image_dir, filename)
                image = load_image(img_path)
                if image:
                    self.variation_images[filename] = image
    
    def load_enemy_images(self, script_dir):
        """Load all enemy images."""
        from .utils import load_image
        import os
        
        image_dir = os.path.join(script_dir, "images", "game", "enemies")
        if not os.path.isdir(image_dir):
            print(f"Enemy image directory not found: {image_dir}")
            return
            
        for filename in os.listdir(image_dir):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(image_dir, filename)
                image = load_image(img_path, ENEMY_IMAGE_SIZE, convert_alpha=True)
                if image:
                    name = os.path.splitext(filename)[0].lower().replace(" ", "_")
                    self.enemy_images[name] = image
    
    def draw_background(self, offset_x=0, offset_y=0):
        """Draw the background with optional offset for screen shake."""
        if self.background_image:
            self.screen.blit(self.background_image, (0 + offset_x, 0 + offset_y))
        else:
            self.screen.fill(DARK_GRAY)
    
    def draw_level_area(self, player):
        """Draw the level area with the current level image."""
        level_area_height = self.height // 2
        rect = pygame.Rect(HORIZONTAL_PADDING, BORDER_MARGIN,
                          self.width - 2 * HORIZONTAL_PADDING,
                          level_area_height - BORDER_MARGIN)
        pygame.draw.rect(self.screen, BLACK, rect)
        
        image = None
        if player.current_level_data:
            image = self.get_level_image(player.current_level_data["image"])
        
        if image:
            self.screen.blit(image, image.get_rect(center=rect.center))
        else:
            text = self.font.render(f"Level {player.level} | No Image Found", True, WHITE)
            self.screen.blit(text, text.get_rect(center=rect.center))
        
        pygame.draw.rect(self.screen, GOLD, rect, 2)
    
    def get_level_image(self, image_path):
        """Get a scaled level image."""
        import os
        image_name = os.path.basename(image_path)
        image = self.variation_images.get(image_name)
        if image:
            level_area_width = self.width - 2 * HORIZONTAL_PADDING
            level_area_height = self.height // 2 - BORDER_MARGIN
            return pygame.transform.scale(image, (level_area_width, level_area_height))
        return None
    
    def draw_enemy(self, enemy_image, enemy_alpha, is_player_attacking):
        """Draw the current enemy with fade and shake effects."""
        if enemy_image:
            if is_player_attacking:
                enemy_rect = enemy_image.get_rect(center=(self.width // 2, self.height // 4))
                shaked_rect = enemy_rect.move(random.randint(-ENEMY_SHAKE_OFFSET, ENEMY_SHAKE_OFFSET), 
                                            random.randint(-ENEMY_SHAKE_OFFSET, ENEMY_SHAKE_OFFSET))
                enemy_img = enemy_image.copy()
                enemy_img.set_alpha(enemy_alpha)
                self.screen.blit(enemy_img, shaked_rect)
            else:
                enemy_img = enemy_image.copy()
                enemy_img.set_alpha(enemy_alpha)
                self.screen.blit(enemy_img, enemy_img.get_rect(center=(self.width // 2, self.height // 4)))
    
    def draw_game_ui(self, player, game_log, offset_x=0, offset_y=0):
        """Draw the game UI with player status and log."""
        top_area_height = self.height // 2
        bottom_area_height = self.height - top_area_height
        padding = 10
        
        rect = pygame.Rect(HORIZONTAL_PADDING + offset_x, top_area_height + BORDER_MARGIN + offset_y,
                          self.width - 2 * HORIZONTAL_PADDING,
                          bottom_area_height - BORDER_MARGIN * 2)
        pygame.draw.rect(self.screen, BLACK, rect)
        pygame.draw.rect(self.screen, GOLD, rect, 2)
        
        # Draw Player Status
        self._draw_player_status(rect, padding, player)
        
        # Draw Game Log
        self._draw_game_log(rect, padding, game_log)
        
        # Draw Input Box
        self._draw_input_box(rect, padding)
    
    def _draw_player_status(self, rect, padding, player):
        """Draw the player status bar."""
        status_y = rect.y + padding
        x_cursor = rect.x + padding
        
        # Name
        name_text = self.small_font.render(f"Name: {player.name}", True, WHITE)
        self.screen.blit(name_text, (x_cursor, status_y))
        x_cursor += name_text.get_width() + 20
        
        # Health Bar
        health_bar_width = 150
        health_bar_height = 15
        draw_health_bar(self.screen, x_cursor, status_y + 5, health_bar_width, health_bar_height, 
                       player.health, player.max_health, self.small_font)
        x_cursor += health_bar_width + 10 + self.small_font.size(f"HP: {player.health}/{player.max_health}")[0] + 20
        
        # Level
        lvl_text = self.small_font.render(f"Level: {player.level}", True, WHITE)
        self.screen.blit(lvl_text, (x_cursor, status_y))
        x_cursor += lvl_text.get_width() + 20
        
        # Spells
        spell_text = self.small_font.render(f"Spells: {player.spells}", True, WHITE)
        self.screen.blit(spell_text, (x_cursor, status_y))
    
    def _draw_game_log(self, rect, padding, game_log):
        """Draw the game log area."""
        log_area_rect = pygame.Rect(rect.x + padding, rect.y + 30 + padding,
                                   rect.width - 2 * padding,
                                   rect.height - 30 - 2 * padding - 50)
        
        y_offset = log_area_rect.y
        
        for line in game_log:
            wrapped_lines = wrap_text(line, log_area_rect.width - 20, self.small_font)
            for wrapped_line in wrapped_lines:
                line_surface = self.small_font.render(wrapped_line, True, WHITE)
                self.screen.blit(line_surface, (log_area_rect.x, y_offset))
                y_offset += TEXT_LINE_HEIGHT
                if y_offset > log_area_rect.y + log_area_rect.height:
                    break
            if y_offset > log_area_rect.y + log_area_rect.height:
                break
    
    def _draw_input_box(self, rect, padding):
        """Draw the input box."""
        input_box_height = 50
        input_rect = pygame.Rect(rect.x + padding,
                                rect.y + rect.height - input_box_height - padding,
                                rect.width - 2 * padding, input_box_height)
        pygame.draw.rect(self.screen, DARK_GRAY, input_rect, border_radius=10)
        pygame.draw.rect(self.screen, GOLD, input_rect, 2, border_radius=10)
    
    def draw_instruction(self, instruction_text):
        """Draw instruction text at the bottom of the screen."""
        surface = self.small_font.render(instruction_text, True, WHITE)
        self.screen.blit(surface, surface.get_rect(center=(self.width // 2, self.height - 20)))
    
    def flip_display(self):
        """Update the display."""
        pygame.display.flip()

"""
Utility functions for Escape the Castle game.
"""

import pygame
import os
from .constants import *


def load_font(font_path, size, fallback_font='Arial'):
    """
    Load a custom font with fallback to system font.
    
    Args:
        font_path (str): Path to the font file
        size (int): Font size
        fallback_font (str): Fallback font name
        
    Returns:
        pygame.font.Font: The loaded font
    """
    try:
        return pygame.font.Font(font_path, size)
    except FileNotFoundError:
        print(f"Custom font not found at {font_path}. Using {fallback_font}.")
        return pygame.font.SysFont(fallback_font, size)


def load_image(image_path, target_size=None, convert_alpha=False):
    """
    Load and optionally scale an image.
    
    Args:
        image_path (str): Path to the image file
        target_size (tuple): Optional (width, height) to scale to
        convert_alpha (bool): Whether to use convert_alpha() for transparency
        
    Returns:
        pygame.Surface or None: The loaded image surface
    """
    try:
        if convert_alpha:
            image = pygame.image.load(image_path).convert_alpha()
        else:
            image = pygame.image.load(image_path).convert()
            
        if target_size:
            image = pygame.transform.smoothscale(image, target_size)
            
        return image
    except (pygame.error, FileNotFoundError) as e:
        print(f"Failed to load image {image_path}: {e}")
        return None


def wrap_text(text, width, font):
    """
    Wrap text to fit within a specified width.
    
    Args:
        text (str): Text to wrap
        width (int): Maximum width in pixels
        font (pygame.font.Font): Font to use for measuring
        
    Returns:
        list: List of wrapped lines
    """
    words = text.split(' ')
    wrapped_lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < width:
            current_line = test_line
        else:
            if current_line:
                wrapped_lines.append(current_line.strip())
            current_line = word + " "
    
    if current_line:
        wrapped_lines.append(current_line.strip())
        
    return wrapped_lines


def get_health_bar_color(health_percent):
    """
    Get the color for a health bar based on health percentage.
    
    Args:
        health_percent (float): Health as a percentage (0.0 to 1.0)
        
    Returns:
        tuple: RGB color tuple
    """
    if health_percent > 0.75:
        return GREEN
    elif health_percent > 0.5:
        return BLUE
    elif health_percent > 0.25:
        return YELLOW
    else:
        return RED


def draw_health_bar(screen, x, y, width, height, current_health, max_health, font):
    """
    Draw a health bar with text.
    
    Args:
        screen (pygame.Surface): Surface to draw on
        x (int): X position
        y (int): Y position
        width (int): Width of the health bar
        height (int): Height of the health bar
        current_health (int): Current health value
        max_health (int): Maximum health value
        font (pygame.font.Font): Font for the text
    """
    health_percent = current_health / max_health if max_health > 0 else 0
    color = get_health_bar_color(health_percent)
    
    # Background
    bg_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, BLACK, bg_rect, border_radius=5)
    
    # Fill
    fill_rect = pygame.Rect(x, y, width * health_percent, height)
    pygame.draw.rect(screen, color, fill_rect, border_radius=5)
    
    # Text
    health_text = f"HP: {current_health}/{max_health}"
    text_surface = font.render(health_text, True, WHITE)
    screen.blit(text_surface, (x + width + 10, y))


def get_script_dir():
    """Get the directory of the current script."""
    return os.path.dirname(os.path.abspath(__file__))


def clamp(value, min_val, max_val):
    """
    Clamp a value between min and max.
    
    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_val, min(value, max_val))

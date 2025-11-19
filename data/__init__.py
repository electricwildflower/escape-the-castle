"""
Escape the Castle - Game Data Package

This package contains all the game logic, menus, and utilities for the Escape the Castle game.
"""

__version__ = "1.0.0"
__author__ = "Escape the Castle Development Team"

# Import main game components for easy access
from .game import Player, game_loop
from .enemies import Enemy, get_random_enemy
from .constants import *
from .utils import *

__all__ = [
    'Player', 'game_loop', 'Enemy', 'get_random_enemy',
    'WHITE', 'DARK_GRAY', 'BLACK', 'GOLD', 'RED', 'GREEN', 'BLUE', 'YELLOW',
    'STARTING_HEALTH', 'DEFAULT_ATTACK', 'DEFAULT_DEFENSE', 'DEFAULT_SPELLS',
    'DIFFICULTIES', 'ENEMY_HEALTH_SCALES', 'RUN_CHANCES',
    'load_font', 'load_image', 'wrap_text', 'draw_health_bar', 'get_script_dir'
]

"""
Game configuration settings for Escape the Castle.
"""

import os

# Game Information
GAME_TITLE = "Escape the Castle"
GAME_VERSION = "1.0.0"

# File Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, "images")
FONTS_DIR = os.path.join(SCRIPT_DIR, "fonts")
AUDIO_DIR = os.path.join(SCRIPT_DIR, "audio")
DATA_DIR = os.path.join(SCRIPT_DIR, "..")

# Asset Paths
BACKGROUND_IMAGE = os.path.join(IMAGES_DIR, "title", "escapethecastle.png")
SCROLL_IMAGE = os.path.join(IMAGES_DIR, "welcome", "scroll.png")
GAMEOVER_IMAGE = os.path.join(IMAGES_DIR, "game", "gameover.jpg")
VICTORY_IMAGE = os.path.join(IMAGES_DIR, "game", "victory.jpeg")
GAME_BACKGROUND = os.path.join(IMAGES_DIR, "game", "escapethecastle.png")
MAD_KING_IMAGE = os.path.join(IMAGES_DIR, "game", "enemies", "madking.png")

# Font Paths
CUSTOM_FONT = os.path.join(FONTS_DIR, "Blkchcry.TTF")

# Audio Paths
BACKGROUND_MUSIC = os.path.join(AUDIO_DIR, "naughtyprincess", "naughty-princess.mp3")

# Data Files
LEVEL_VARIATIONS_FILE = os.path.join(SCRIPT_DIR, "randomlevel.json")

# Screen Settings
DEFAULT_FONT_SIZE = 24
SMALL_FONT_SIZE = 18
TITLE_FONT_SIZE = 64
BUTTON_FONT_SIZE = 36
ERROR_FONT_SIZE = 30

# UI Settings
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 60
BUTTON_SPACING = 20
MENU_PADDING = 40

# Animation Settings
DEFAULT_FPS = 60
TYPING_SPEED = 0.5

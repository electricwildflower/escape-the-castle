"""
Constants and configuration for Escape the Castle game.
"""

# Colors
WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (150, 150, 150)
TRANSPARENT_GRAY = (100, 100, 100, 150)

# UI Layout
BORDER_MARGIN = 40
HORIZONTAL_PADDING = 240
TEXT_LINE_HEIGHT = 20

# Game Configuration
STARTING_HEALTH = 100
DEFAULT_ATTACK = 20
DEFAULT_DEFENSE = 0
DEFAULT_SPELLS = 1

# Difficulty Settings
DIFFICULTIES = [
    ("Easy", 20, 1.0, 0.6),
    ("Medium", 50, 1.5, 0.4),
    ("Hard", 100, 2.0, 0.2)
]

# Enemy Scaling
ENEMY_HEALTH_SCALES = {"Easy": 1.0, "Medium": 1.5, "Hard": 2.0}
RUN_CHANCES = {"Easy": 0.6, "Medium": 0.4, "Hard": 0.2}

# Animation Settings
FADE_SPEED = 2
SHAKE_DURATION_PLAYER = 1500
SHAKE_DURATION_ENEMY = 500
SHAKE_DURATION_BOSS = 600
SHAKE_DURATION_SPELL = 300
SHAKE_OFFSET = 10
ENEMY_SHAKE_OFFSET = 5

# Typing Effect
TYPING_DELAY = 50  # Milliseconds between characters
CURSOR_SWITCH_MS = 500

# Image Settings
ENEMY_IMAGE_SIZE = (500, 500)

# Boss Settings
BOSS_HEALTH = {"Easy": 100, "Medium": 150, "Hard": 200}
BOSS_ATTACK = 40

# Treasure Settings
HEAL_CHANCE = 0.7
MIN_HEAL = 10
MAX_HEAL = 30

# Combat Settings
MIN_ATTACK_DAMAGE = 10
SPELL_BONUS_MIN = 20
SPELL_BONUS_MAX = 40
ATTACK_VARIANCE = 5

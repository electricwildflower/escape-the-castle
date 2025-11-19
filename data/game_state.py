"""
Game state management for Escape the Castle.
"""

class GameState:
    """Manages the current state of the game."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset the game state to initial values."""
        # Combat state
        self.is_player_attacking = False
        self.is_enemy_attacking = False
        self.shake_start_time = 0
        self.shake_duration = 0
        
        # Enemy display state
        self.current_enemy_image = None
        self.enemy_alpha = 0
        self.enemy_fading_in = False
        self.enemy_fading_out = False
        
        # Typing effect state
        self.is_typing_welcome = True
        self.is_typing_choices = False
        self.typing_cursor = 0
        self.last_type_time = 0
        
        # Game flow state
        self.in_battle = False
        self.current_enemy = None
        self.current_choices = []
        self.full_game_log = []
    
    def start_attack(self, duration):
        """Start a player attack animation."""
        self.is_player_attacking = True
        self.shake_start_time = self.get_current_time()
        self.shake_duration = duration
    
    def start_enemy_attack(self, duration):
        """Start an enemy attack animation."""
        self.is_enemy_attacking = True
        self.shake_start_time = self.get_current_time()
        self.shake_duration = duration
    
    def is_attack_finished(self):
        """Check if the current attack animation is finished."""
        if self.is_player_attacking or self.is_enemy_attacking:
            elapsed = self.get_current_time() - self.shake_start_time
            return elapsed >= self.shake_duration
        return True
    
    def finish_attack(self):
        """Finish the current attack animation."""
        self.is_player_attacking = False
        self.is_enemy_attacking = False
    
    def start_enemy_fade_in(self, image):
        """Start fading in an enemy image."""
        self.current_enemy_image = image
        self.enemy_alpha = 0
        self.enemy_fading_in = True
        self.enemy_fading_out = False
    
    def start_enemy_fade_out(self):
        """Start fading out the current enemy image."""
        self.enemy_fading_in = False
        self.enemy_fading_out = True
    
    def update_enemy_fade(self, fade_speed):
        """Update enemy fade animation."""
        if self.enemy_fading_in:
            self.enemy_alpha += fade_speed
            if self.enemy_alpha >= 255:
                self.enemy_alpha = 255
                self.enemy_fading_in = False
        elif self.enemy_fading_out:
            self.enemy_alpha -= fade_speed
            if self.enemy_alpha <= 0:
                self.enemy_alpha = 0
                self.current_enemy_image = None
                self.enemy_fading_out = False
    
    def start_typing_effect(self, is_welcome=False, is_choices=False):
        """Start a typing effect."""
        self.is_typing_welcome = is_welcome
        self.is_typing_choices = is_choices
        self.typing_cursor = 0
        self.last_type_time = self.get_current_time()
    
    def update_typing_effect(self, typing_delay):
        """Update typing effect animation."""
        if self.is_typing_welcome or self.is_typing_choices:
            if self.get_current_time() - self.last_type_time > typing_delay:
                self.typing_cursor += 1
                self.last_type_time = self.get_current_time()
    
    def finish_typing_effect(self):
        """Finish the typing effect."""
        self.is_typing_welcome = False
        self.is_typing_choices = False
    
    def start_battle(self, enemy):
        """Start a battle with an enemy."""
        self.in_battle = True
        self.current_enemy = enemy
        self.start_enemy_fade_in(enemy.get_image())
    
    def end_battle(self):
        """End the current battle."""
        self.in_battle = False
        self.current_enemy = None
        self.start_enemy_fade_out()
    
    def add_to_log(self, message):
        """Add a message to the game log."""
        self.full_game_log.append(message)
    
    def get_current_time(self):
        """Get the current time in milliseconds."""
        import pygame
        return pygame.time.get_ticks()

"""
Input handling for Escape the Castle game.
"""

import pygame
from .constants import *

class InputHandler:
    """Handles all game input events."""
    
    def __init__(self, game_state, player):
        self.game_state = game_state
        self.player = player
        self.current_choices = []
    
    def handle_event(self, event, screen, width, height):
        """Handle a pygame event and return the appropriate action."""
        if event.type == pygame.QUIT:
            return "exit"
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return self._handle_escape_key(screen, width, height)
            elif self.game_state.in_battle:
                return self._handle_battle_input(event)
            elif not self.game_state.is_typing_welcome and not self.game_state.is_typing_choices:
                return self._handle_choice_input(event)
        
        return None
    
    def _handle_escape_key(self, screen, width, height):
        """Handle the escape key (pause menu)."""
        import data.ingamemenu as ingamemenu
        pause_result = ingamemenu.show_pause_menu(screen, width, height)
        return pause_result
    
    def _handle_battle_input(self, event):
        """Handle input during battle."""
        if event.key == pygame.K_a:
            return self._handle_attack()
        elif event.key == pygame.K_s:
            return self._handle_spell()
        elif event.key == pygame.K_r:
            return self._handle_run()
        return None
    
    def _handle_attack(self):
        """Handle attack input."""
        if not self.game_state.is_player_attacking and not self.game_state.is_enemy_attacking:
            from .constants import MIN_ATTACK_DAMAGE, SHAKE_DURATION_PLAYER
            import random
            
            dmg = random.randint(MIN_ATTACK_DAMAGE, self.player.attack)
            self.game_state.current_enemy.take_damage(dmg)
            self.game_state.add_to_log(f"You attack {self.game_state.current_enemy.name} for {dmg} damage!")
            self.game_state.start_attack(SHAKE_DURATION_PLAYER)
            return "attack"
        return None
    
    def _handle_spell(self):
        """Handle spell input."""
        if (self.player.spells > 0 and 
            not self.game_state.is_player_attacking and 
            not self.game_state.is_enemy_attacking):
            
            from .constants import SPELL_BONUS_MIN, SPELL_BONUS_MAX, SHAKE_DURATION_PLAYER
            import random
            
            dmg = random.randint(self.player.attack + SPELL_BONUS_MIN, 
                               self.player.attack + SPELL_BONUS_MAX)
            self.game_state.current_enemy.take_damage(dmg)
            self.player.spells -= 1
            self.game_state.add_to_log(f"You unleash a spell on {self.game_state.current_enemy.name} for {dmg} damage!")
            self.game_state.start_attack(SHAKE_DURATION_PLAYER)
            return "spell"
        else:
            self.game_state.add_to_log("You have no spells left!")
            return "no_spells"
        return None
    
    def _handle_run(self):
        """Handle run input."""
        from .constants import RUN_CHANCES, ATTACK_VARIANCE
        import random
        
        roll = random.random()
        success_chance = RUN_CHANCES.get(self.player.difficulty, 0.4)
        
        if roll < success_chance:
            self.game_state.add_to_log("You attempt to run away and succeed!")
            self.game_state.end_battle()
            return "run_success"
        else:
            if roll < success_chance + 0.3:
                self.game_state.add_to_log("You attempt to run away but are blocked! You must stay and fight.")
                return "run_blocked"
            else:
                taken = random.randint(self.game_state.current_enemy.attack - ATTACK_VARIANCE, 
                                     self.game_state.current_enemy.attack + ATTACK_VARIANCE)
                self.player.take_damage(taken)
                self.game_state.add_to_log("You attempt to run away but are blocked and struck down by the enemy!")
                self.game_state.add_to_log(f"The {self.game_state.current_enemy.name} deals {taken} damage while you try to flee!")
                return "run_failed"
    
    def _handle_choice_input(self, event):
        """Handle choice input (1-3 keys)."""
        try:
            idx = int(event.unicode) - 1
            if 0 <= idx < len(self.current_choices):
                self.game_state.add_to_log(f"> You chose: {self.current_choices[idx]['text']}")
                return ("choice", idx)
            else:
                self.game_state.add_to_log("Invalid choice, please enter 1, 2, or 3.")
                return "invalid_choice"
        except (ValueError, IndexError):
            return None
    
    def set_choices(self, choices):
        """Set the current available choices."""
        self.current_choices = choices

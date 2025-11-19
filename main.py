import pygame
import sys
import os
import data.mainmenu as mainmenu
import data.welcome as welcome
import data.game as game
import data.ingamemenu as ingamemenu
from data.constants import STARTING_HEALTH

# --- Pygame Initialization ---
pygame.init()

# --- Screen Dimensions and Colors ---
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = SCREEN.get_size()
pygame.display.set_caption("Escape the Castle")
FONT = pygame.font.SysFont('Arial', 24)
SMALL_FONT = pygame.font.SysFont('Arial', 18)

def main_game_loop():
    """
    Manages the overall game flow, including the welcome screen,
    title screen, and the main game loop.
    """
    while True:
        # Show the main menu first
        action = mainmenu.show_title_screen(SCREEN, WIDTH, HEIGHT)

        if action == "start":
            # Show welcome screen (get player name + difficulty + level)
            welcome_result = welcome.show_welcome_screen(SCREEN, WIDTH, HEIGHT)
            if not isinstance(welcome_result, tuple):
                return  # user exited

            # 👇 unpack all 3 values now
            player_name, difficulty, starting_level = welcome_result

            # Core game loop
            while True:
                # 👇 pass difficulty into Player
                player_obj = game.Player(player_name, difficulty, starting_level, STARTING_HEALTH)
                game_result = game.game_loop(SCREEN, WIDTH, HEIGHT, player_obj, FONT, SMALL_FONT)

                if game_result == "exit":
                    break
                elif game_result == "exit_main_menu":
                    continue  # Go back to the main menu
                elif game_result == "restart":
                    continue  # Restart the game from the main menu
                elif game_result == "exit_game":
                    pygame.quit()
                    sys.exit()

        elif action == "exit":
            break

    pygame.quit()
    sys.exit()

# --- Start the game ---
if __name__ == "__main__":
    main_game_loop()


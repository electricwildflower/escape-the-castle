import pygame
import sys
import os

# Define colors for the menu UI
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
DARK_GRAY = (50, 50, 50)
TRANSPARENT_GRAY = (100, 100, 100, 150)
BLACK = (0, 0, 0)

def show_pause_menu(screen, width, height):
    """
    Displays the in-game pause menu.

    Args:
        screen (pygame.Surface): The game window surface.
        width (int): The width of the screen.
        height (int): The height of the screen.

    Returns:
        str: A string indicating the player's choice ("continue", "exit_main_menu", or "exit_game").
    """
    # Create a semi-transparent overlay
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill(TRANSPARENT_GRAY)
    screen.blit(overlay, (0, 0))

    # Create menu background box
    menu_width = 400
    menu_height = 350
    menu_rect = pygame.Rect(0, 0, menu_width, menu_height)
    menu_rect.center = (width // 2, height // 2)

    pygame.draw.rect(screen, DARK_GRAY, menu_rect)
    pygame.draw.rect(screen, GOLD, menu_rect, 2)

    # Load custom font
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(script_dir, 'fonts', 'Blkchcry.TTF')
    try:
        title_font = pygame.font.Font(font_path, 36)
        button_font = pygame.font.Font(font_path, 24)
    except FileNotFoundError:
        print("Custom font not found. Using default Arial font.")
        title_font = pygame.font.SysFont('Arial', 36)
        button_font = pygame.font.SysFont('Arial', 24)

    # Title text
    title_text = title_font.render("Game Paused", True, GOLD)
    title_rect = title_text.get_rect(center=(width // 2, menu_rect.y + 40))
    screen.blit(title_text, title_rect)

    # Create buttons
    button_width = 300
    button_height = 50
    button_padding = 20

    return_button = pygame.Rect(0, 0, button_width, button_height)
    return_button.center = (width // 2, menu_rect.y + 120)

    main_menu_button = pygame.Rect(0, 0, button_width, button_height)
    main_menu_button.center = (width // 2, menu_rect.y + 120 + button_height + button_padding)
    
    exit_game_button = pygame.Rect(0, 0, button_width, button_height)
    exit_game_button.center = (width // 2, menu_rect.y + 120 + 2 * (button_height + button_padding))

    # Draw buttons
    pygame.draw.rect(screen, BLACK, return_button, border_radius=10)
    pygame.draw.rect(screen, GOLD, return_button, 2, border_radius=10)
    pygame.draw.rect(screen, BLACK, main_menu_button, border_radius=10)
    pygame.draw.rect(screen, GOLD, main_menu_button, 2, border_radius=10)
    pygame.draw.rect(screen, BLACK, exit_game_button, border_radius=10)
    pygame.draw.rect(screen, GOLD, exit_game_button, 2, border_radius=10)
    
    return_text = button_font.render("Return to game", True, WHITE)
    main_menu_text = button_font.render("Exit to Main Menu", True, WHITE)
    exit_text = button_font.render("Exit Game", True, WHITE)

    screen.blit(return_text, return_text.get_rect(center=return_button.center))
    screen.blit(main_menu_text, main_menu_text.get_rect(center=main_menu_button.center))
    screen.blit(exit_text, exit_text.get_rect(center=exit_game_button.center))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.collidepoint(event.pos):
                    return "continue"
                if main_menu_button.collidepoint(event.pos):
                    return "exit_main_menu"
                if exit_game_button.collidepoint(event.pos):
                    return "exit_game"


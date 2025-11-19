import pygame
import sys
import os
from .constants import *
from .utils import load_font, load_image, get_script_dir

def show_title_screen(screen, width, height):
    """
    Displays the title screen with 'Start' and 'Exit' buttons.
    
    Args:
        screen (pygame.Surface): The game window surface.
        width (int): The width of the screen.
        height (int): The height of the screen.
    
    Returns:
        str: "start" if the user clicks 'Start Adventure', otherwise exits the game.
    """
    script_dir = get_script_dir()
    
    # Load and scale the background image
    background_image_path = os.path.join(script_dir, "images", "title", "escapethecastle.png")
    background_image = load_image(background_image_path, (width, height))
    
    # Load custom font
    custom_font_path = os.path.join(script_dir, "fonts", "Blkchcry.TTF")
    title_font = load_font(custom_font_path, 64)
    button_font = load_font(custom_font_path, 36)

    # Load and play the background audio
    pygame.mixer.init()
    audio_path = os.path.join(script_dir, "audio", "naughtyprincess", "naughty-princess.mp3")
    
    try:
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play(-1) # Loop the music indefinitely
    except pygame.error as e:
        print(f"Error: Failed to load or play audio from '{audio_path}'. Make sure the file exists and the path is correct.")
        print(e)
    except FileNotFoundError:
        print(f"Error: Audio file not found at '{audio_path}'. Please check the file path.")

    # Render text
    title_text = title_font.render("Escape the Castle", True, GOLD)
    title_rect = title_text.get_rect(center=(width // 2, height // 2 - 150))
    start_text = button_font.render("Start Adventure", True, WHITE)
    exit_text = button_font.render("Exit Game", True, WHITE)

    # Create buttons
    start_button = pygame.Rect(0, 0, 300, 70)
    start_button.center = (width // 2, height // 2 + 50)
    exit_button = pygame.Rect(0, 0, 300, 70)
    exit_button.center = (width // 2, height // 2 + 150)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    # Don't stop music here - let it continue to welcome screen
                    return "start"
                if exit_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(DARK_GRAY)
            
        screen.blit(title_text, title_rect)

        # Draw start button
        pygame.draw.rect(screen, BLACK, start_button, border_radius=10)
        pygame.draw.rect(screen, GOLD, start_button, 2, border_radius=10)
        start_text_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, start_text_rect)

        # Draw exit button
        pygame.draw.rect(screen, BLACK, exit_button, border_radius=10)
        pygame.draw.rect(screen, GOLD, exit_button, 2, border_radius=10)
        exit_text_rect = exit_text.get_rect(center=exit_button.center)
        screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()


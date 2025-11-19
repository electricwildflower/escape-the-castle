# data/gameover.py
import pygame
import sys
import os
from .constants import *
from .utils import load_font, load_image, get_script_dir

def show_game_over(screen, width, height):
    """Displays the game over screen with buttons."""

    script_dir = get_script_dir()
    
    # --- Background ---
    bg_path = os.path.join(script_dir, "images", "game", "gameover.jpg")
    background = load_image(bg_path, (width, height))

    # --- Custom Font ---
    font_path = os.path.join(script_dir, "fonts", "Blkchcry.TTF")
    font = load_font(font_path, 40, "georgia")

    # --- Buttons ---
    buttons = [
        {"text": "Try Again", "action": "retry"},
        {"text": "Exit to Menu", "action": "exit_main_menu"},
        {"text": "Quit Game", "action": "exit_game"},  # renamed
    ]

    button_rects = []
    btn_width, btn_height = 300, 60
    spacing = 20
    total_height = len(buttons) * btn_height + (len(buttons) - 1) * spacing
    start_y = (height - total_height) // 2

    for i, btn in enumerate(buttons):
        rect = pygame.Rect((width - btn_width) // 2,
                           start_y + i * (btn_height + spacing),
                           btn_width, btn_height)
        button_rects.append(rect)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit_game"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, btn in zip(button_rects, buttons):
                    if rect.collidepoint(event.pos):
                        return btn["action"]

        # --- Draw background ---
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(DARK_GRAY)

        # --- Draw buttons ---
        mouse_pos = pygame.mouse.get_pos()
        for rect, btn in zip(button_rects, buttons):
            color = GOLD if rect.collidepoint(mouse_pos) else WHITE
            pygame.draw.rect(screen, DARK_GRAY, rect, border_radius=12)
            pygame.draw.rect(screen, color, rect, 3, border_radius=12)

            text_surface = font.render(btn["text"], True, color)
            screen.blit(text_surface, text_surface.get_rect(center=rect.center))

        pygame.display.flip()
        clock.tick(60)


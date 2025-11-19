# data/wingame.py
import pygame
import os
import sys
from .constants import *
from .utils import load_font, load_image, get_script_dir

def show_win_screen(screen, width, height, player):
    """Displays the victory screen after defeating the Mad King."""

    script_dir = get_script_dir()
    
    # Background image for victory
    bg_path = os.path.join(script_dir, "images", "game", "victory.jpeg")
    background = load_image(bg_path, (width, height))

    # Custom gothic font
    font_path = os.path.join(script_dir, "fonts", "Blkchcry.TTF")
    title_font = load_font(font_path, 72, "georgia")
    option_font = load_font(font_path, 40, "georgia")
    stats_font = load_font(font_path, 32, "georgia")

    buttons = [
        {"text": "Play Again", "action": "replay"},
        {"text": "Exit to Main Menu", "action": "exit_main_menu"},
        {"text": "Exit Game", "action": "exit"},
    ]

    btn_width, btn_height = 350, 60
    spacing = 20
    total_height = len(buttons) * btn_height + (len(buttons) - 1) * spacing
    start_y = (height // 2) + 100

    button_rects = []
    for i, btn in enumerate(buttons):
        rect = pygame.Rect((width - btn_width) // 2,
                           start_y + i * (btn_height + spacing),
                           btn_width, btn_height)
        button_rects.append(rect)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, btn in zip(button_rects, buttons):
                    if rect.collidepoint(event.pos):
                        return btn["action"]

        # Draw background
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(DARK_GRAY)

        # Title
        title_surface = title_font.render("Victory!", True, GOLD)
        screen.blit(title_surface, title_surface.get_rect(center=(width//2, height//5)))

        sub_surface = option_font.render("You defeated the Mad King Baramour!", True, WHITE)
        screen.blit(sub_surface, sub_surface.get_rect(center=(width//2, height//5 + 80)))

        # Stats (example: name, remaining health, etc.)
        stats = [
            f"Hero: {player.name}",
            f"Remaining Health: {player.health}",
            f"Potions Collected: {getattr(player, 'potions', 0)}",
            f"Spells Cast: {getattr(player, 'spells_cast', 0)}",
        ]
        for i, line in enumerate(stats):
            stat_text = stats_font.render(line, True, GOLD)
            screen.blit(stat_text, stat_text.get_rect(center=(width//2, height//2 - 60 + i*40)))

        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        for rect, btn in zip(button_rects, buttons):
            color = GOLD if rect.collidepoint(mouse_pos) else WHITE
            pygame.draw.rect(screen, DARK_GRAY, rect, border_radius=12)
            pygame.draw.rect(screen, color, rect, 3, border_radius=12)

            text_surface = option_font.render(btn["text"], True, color)
            screen.blit(text_surface, text_surface.get_rect(center=rect.center))

        pygame.display.flip()
        clock.tick(60)


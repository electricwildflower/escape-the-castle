import pygame
import sys
import os
from .constants import *
from .utils import load_font, load_image, get_script_dir

def show_welcome_screen(screen, width, height):
    """
    Displays the game's intro and instructions with a scroll overlay.
    
    Args:
        screen (pygame.Surface): The game window surface.
        width (int): The width of the screen.
        height (int): The height of the screen.
    
    Returns:
        tuple: (name, difficulty, starting_level)
    """
    script_dir = get_script_dir()
    
    # Load and scale the background image
    background_image_path = os.path.join(script_dir, "images", "title", "escapethecastle.png")
    background_image = load_image(background_image_path, (width, height))
    
    # Load and scale the scroll image
    scroll_image_path = os.path.join(script_dir, "images", "welcome", "scroll.png")
    scroll_image = load_image(scroll_image_path, convert_alpha=True)
    if scroll_image:
        scroll_height = int(height * 1.0)
        scroll_width = int(scroll_image.get_width() * (scroll_height / scroll_image.get_height()))
        scroll_width = int(scroll_width * 1.2)
        scroll_image = pygame.transform.scale(scroll_image, (scroll_width, scroll_height))

    scroll_x = (width - scroll_width) // 2
    scroll_y = (height - scroll_height) // 2
    
    # Load fonts
    custom_font_path = os.path.join(script_dir, "fonts", "Blkchcry.TTF")
    font = load_font(custom_font_path, 24)
    small_font = load_font(custom_font_path, 20)
    error_font = load_font(custom_font_path, 30, 'Arial')
    
    intro_message = [
        "Welcome, Adventurer...",
        "",
        "You awaken in the depths of a forgotten dungeon, the air damp and heavy with despair.",
        "Cold iron shackles cling to your legs, and your memory is clouded with shadow.",
        "Before you lies the lifeless body of a guard — his keys scattered on the stone floor,",
        "a rusted sword resting beside him, whispering of both danger and opportunity.",
        "You reach for the keys to unshackle yourself and grab the sword.",
        "",
        "This cursed fortress belongs to the tyrant King Baramour,",
        "whose rule is enforced by monstrous beasts, cruel traps, and merciless soldiers.",
        "The mad king Baramour has locked you in his dungeon",
        "To claim your freedom you must climb through the dungeon’s perilous halls",
        "face horrors that lurk in the dark and confront the king himself to get your freedom.",
        "",
        "Instructions:",
        "- Navigate through the castle by selecting one of the available paths.",
        "- Beware: each choice may conceal an ambush, a trap, or worse.",
        "- Discover hidden chests to find potions that restore your strength.",
        "- Press 'ESC' to pause the game and access the main menu.",
        "",
        "Your fate is unwritten. Enter your name, choose your difficulty,",
        "and let your escape begin..."
    ]

    text_height_per_line = small_font.get_height()
    total_text_lines = len(intro_message)
    total_text_height = total_text_lines * text_height_per_line
    total_text_height += (total_text_lines - 1) * 5

    text_start_y = scroll_y + (scroll_height - total_text_height) // 2 - 70 
    
    ui_width = int(scroll_width * 0.7)
    ui_height = 40
    input_box_y = scroll_y + scroll_height - 320
    difficulty_button_y = input_box_y + ui_height + 20
    start_button_y = difficulty_button_y + ui_height + 20

    input_box_rect = pygame.Rect(scroll_x + (scroll_width - ui_width) // 2, input_box_y, ui_width, ui_height)
    difficulty_button_rect = pygame.Rect(scroll_x + (scroll_width - ui_width) // 2, difficulty_button_y, ui_width, ui_height)
    start_button_rect = pygame.Rect(scroll_x + (scroll_width - ui_width) // 2, start_button_y, ui_width, ui_height)
    
    input_text = ""
    input_box_active = True
    error_message = ""

    cursor_visible = True
    cursor_timer = 0
    cursor_switch_ms = CURSOR_SWITCH_MS  
    
    # Difficulty settings
    difficulties = [(name, level, scale, run_chance) for name, level, scale, run_chance in DIFFICULTIES]
    difficulty_index = 0
    selected_difficulty, selected_level, _, _ = difficulties[difficulty_index]

    typing_speed = 0.3  # Slower, more natural typing speed
    char_index = 0
    total_chars = sum(len(line) for line in intro_message)
    typing_finished = False

    running = True
    while running:
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(DARK_GRAY)
            
        if scroll_image:
            screen.blit(scroll_image, (scroll_x, scroll_y))
        else:
            pygame.draw.rect(screen, LIGHT_GRAY, (scroll_x, scroll_y, scroll_width, scroll_height))

        if not typing_finished:
            char_index += typing_speed
            if char_index >= total_chars:
                typing_finished = True

        y_offset = text_start_y
        current_char_count = 0
        for line in intro_message:
            line_length = len(line)
            if char_index > current_char_count + line_length:
                text_to_render = line
            else:
                chars_to_show = max(0, int(char_index) - current_char_count)
                text_to_render = line[:chars_to_show]
            
            text_surface = small_font.render(text_to_render, True, BLACK)
            text_rect = text_surface.get_rect(center=(width // 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += text_height_per_line + 5
            current_char_count += line_length

        if typing_finished:
            pygame.draw.rect(screen, DARK_GRAY, input_box_rect, border_radius=10)
            pygame.draw.rect(screen, GOLD, input_box_rect, 2, border_radius=10)
            input_text_surface = small_font.render(input_text, True, WHITE)
            screen.blit(input_text_surface, (input_box_rect.x + 5, input_box_rect.y + 5))

            cursor_timer += pygame.time.Clock().tick(60)
            if cursor_timer >= cursor_switch_ms:
                cursor_visible = not cursor_visible
                cursor_timer = 0
            if input_box_active and cursor_visible:
                cursor_x = input_box_rect.x + 5 + input_text_surface.get_width() + 2
                cursor_y = input_box_rect.y + 5
                cursor_height = input_text_surface.get_height()
                pygame.draw.line(screen, WHITE, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

            pygame.draw.rect(screen, DARK_GRAY, difficulty_button_rect, border_radius=10)
            pygame.draw.rect(screen, GOLD, difficulty_button_rect, 2, border_radius=10)
            diff_text = font.render(f"Difficulty: {selected_difficulty}", True, GOLD)
            screen.blit(diff_text, diff_text.get_rect(center=difficulty_button_rect.center))

            pygame.draw.rect(screen, DARK_GRAY, start_button_rect, border_radius=10)
            pygame.draw.rect(screen, GOLD, start_button_rect, 2, border_radius=10)
            start_text_surface = font.render("Start Adventure", True, GOLD)
            screen.blit(start_text_surface, start_text_surface.get_rect(center=start_button_rect.center))

            if error_message:
                error_surface = error_font.render(error_message, True, RED)
                error_rect = error_surface.get_rect(center=(width // 2, input_box_rect.y - 40))
                screen.blit(error_surface, error_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and typing_finished:
                if input_box_rect.collidepoint(event.pos):
                    input_box_active = True
                    error_message = ""
                else:
                    input_box_active = False

                if difficulty_button_rect.collidepoint(event.pos):
                    difficulty_index = (difficulty_index + 1) % len(difficulties)
                    selected_difficulty, selected_level, _, _ = difficulties[difficulty_index]

                if start_button_rect.collidepoint(event.pos):
                    if not input_text.strip():
                        error_message = "Please enter a name first."
                    else:
                        # Stop music when starting the actual game
                        pygame.mixer.music.stop()
                        return input_text, selected_difficulty, selected_level

            if event.type == pygame.KEYDOWN and input_box_active:
                error_message = ""
                if event.key == pygame.K_RETURN:
                    if not input_text.strip():
                        error_message = "Please enter a name first."
                    else:
                        # Stop music when starting the actual game
                        pygame.mixer.music.stop()
                        return input_text, selected_difficulty, selected_level
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode


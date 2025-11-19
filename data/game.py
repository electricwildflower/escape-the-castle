import pygame
import sys
import os
import random
import json
import data.mainmenu as mainmenu
import data.ingamemenu as ingamemenu
import data.enemies as enemies
import data.gameover as gameover
import data.wingame as wingame
from data.constants import *
from data.utils import load_font, load_image, wrap_text, draw_health_bar, get_script_dir

# --- Game Classes ---
class Player:
    """Player class representing the game character."""
    
    def __init__(self, name, difficulty, starting_level, starting_health):
        self.name = name
        self.difficulty = difficulty
        self.health = starting_health
        self.attack = DEFAULT_ATTACK
        self.defense = DEFAULT_DEFENSE
        self.level = starting_level
        self.starting_level = starting_level
        self.items = []
        self.spells = DEFAULT_SPELLS
        self.base_health = starting_health
        self.max_health = starting_health
        self.input_text = ""
        self.current_level_data = None
        self.last_log = ""
        self.choices_text = []

    def is_alive(self):
        """Check if the player is alive."""
        return self.health > 0

    def get_status(self):
        """Get a formatted status string for the player."""
        return (f"Name: {self.name} | Health: {self.health}/{self.max_health} | "
                f"Level: {self.level} | Items: {', '.join(self.items) if self.items else 'None'} | "
                f"Spells: {self.spells}")

    def take_damage(self, damage):
        """Apply damage to the player."""
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        """Heal the player and potentially increase max health."""
        self.health += amount
        if self.health > self.max_health:
            self.max_health = self.health

# --- Global Variables ---

# --- Assets ---
level_images = {}
background_image = None
variation_images = {}
level_variations = []

# --- Enemy images and fade variables ---
enemy_images = {}
current_enemy_image = None
enemy_alpha = 0
enemy_fading_in = False
enemy_fading_out = False

# --- Combat state variables ---
is_player_attacking = False
is_enemy_attacking = False
shake_start_time = 0
shake_duration = 0

def load_variation_images(script_dir):
    """Load all variation images from the variations directory."""
    global variation_images
    image_dir = os.path.join(script_dir, "images", "game", "variations")
    if not os.path.isdir(image_dir):
        print(f"Variation image directory not found: {image_dir}")
        return
        
    for filename in os.listdir(image_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(image_dir, filename)
            image = load_image(img_path)
            if image:
                variation_images[filename] = image

def load_enemy_images(script_dir):
    """Load all enemy images from the enemies directory."""
    global enemy_images
    image_dir = os.path.join(script_dir, "images", "game", "enemies")
    if not os.path.isdir(image_dir):
        print(f"Enemy image directory not found: {image_dir}")
        return
        
    for filename in os.listdir(image_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(image_dir, filename)
            image = load_image(img_path, ENEMY_IMAGE_SIZE, convert_alpha=True)
            if image:
                name = os.path.splitext(filename)[0].lower().replace(" ", "_")
                enemy_images[name] = image

def get_level_image(image_path, width, height):
    image_name = os.path.basename(image_path)
    image = variation_images.get(image_name)
    if image:
        level_area_width = width - 2 * HORIZONTAL_PADDING
        level_area_height = height // 2 - BORDER_MARGIN
        return pygame.transform.scale(image, (level_area_width, level_area_height))
    return None

def draw_level_area(screen, width, height, font, player):
    global current_enemy_image, enemy_alpha
    level_area_height = height // 2
    rect = pygame.Rect(HORIZONTAL_PADDING, BORDER_MARGIN,
                       width - 2 * HORIZONTAL_PADDING,
                       level_area_height - BORDER_MARGIN)
    pygame.draw.rect(screen, BLACK, rect)
    image = None
    if player.current_level_data:
        image = get_level_image(player.current_level_data["image"], width, height)
    if image:
        screen.blit(image, image.get_rect(center=rect.center))
    else:
        text = font.render(f"Level {player.level} | No Image Found", True, WHITE)
        screen.blit(text, text.get_rect(center=rect.center))

    pygame.draw.rect(screen, GOLD, rect, 2)

def draw_game_ui(screen, width, height, font, small_font, player, game_log, offset_x=0, offset_y=0):
    top_area_height = height // 2
    bottom_area_height = height - top_area_height
    padding = 10
    rect = pygame.Rect(HORIZONTAL_PADDING + offset_x, top_area_height + BORDER_MARGIN + offset_y,
                       width - 2 * HORIZONTAL_PADDING,
                       bottom_area_height - BORDER_MARGIN * 2)
    pygame.draw.rect(screen, BLACK, rect)
    pygame.draw.rect(screen, GOLD, rect, 2)
    
    # Draw Player Status
    status_y = rect.y + padding
    x_cursor = rect.x + padding
    name_text = small_font.render(f"Name: {player.name}", True, WHITE)
    screen.blit(name_text, (x_cursor, status_y))
    x_cursor += name_text.get_width() + 20
    health_bar_width = 150
    health_bar_height = 15
    draw_health_bar(screen, x_cursor, status_y + 5, health_bar_width, health_bar_height, 
                   player.health, player.max_health, small_font)
    x_cursor += health_bar_width + 10 + small_font.size(f"HP: {player.health}/{player.max_health}")[0] + 20
    lvl_text = small_font.render(f"Level: {player.level}", True, WHITE)
    screen.blit(lvl_text, (x_cursor, status_y))
    x_cursor += lvl_text.get_width() + 20
    spell_text = small_font.render(f"Spells: {player.spells}", True, WHITE)
    screen.blit(spell_text, (x_cursor, status_y))

    # Draw Game Log
    log_area_rect = pygame.Rect(rect.x + padding, status_y + 30 + padding,
                                 rect.width - 2 * padding,
                                 rect.height - 30 - 2 * padding - 50)
    
    y_offset = log_area_rect.y
    
    # 🐛 FIX: Loop through the game_log and render each line
    for line in game_log:
        wrapped_lines = wrap_text(line, log_area_rect.width - 20, small_font)
        for wrapped_line in wrapped_lines:
            line_surface = small_font.render(wrapped_line, True, WHITE)
            screen.blit(line_surface, (log_area_rect.x, y_offset))
            y_offset += TEXT_LINE_HEIGHT
            if y_offset > log_area_rect.y + log_area_rect.height:
                break
        if y_offset > log_area_rect.y + log_area_rect.height:
            break
    
    input_box_height = 50
    input_rect = pygame.Rect(log_area_rect.x,
                              rect.y + rect.height - input_box_height - padding,
                              log_area_rect.width, input_box_height)
    pygame.draw.rect(screen, DARK_GRAY, input_rect, border_radius=10)
    pygame.draw.rect(screen, GOLD, input_rect, 2, border_radius=10)
    


def get_action_text(action, wall):
    mapping = {
        "stairs_down": "An archway with a set of stairs going down to the previous level",
        "stairs_up": "An archway with a set of stairs going up to the next level",
        "door": "An archway with a door",
        "hall": "An archway with a hallway"
    }
    wall_text = {
        "left": "on the left wall",
        "center": "on the wall facing you",
        "right": "to the right wall"
    }
    return f"{mapping.get(action, 'An unknown path')} {wall_text[wall]}"

def generate_choices(player):
    variation_data = random.choice(level_variations)
    player.current_level_data = variation_data
    choices = [
        {"text": get_action_text(variation_data["left"], "left"), "action": variation_data["left"]},
        {"text": get_action_text(variation_data["center"], "center"), "action": variation_data["center"]},
        {"text": get_action_text(variation_data["right"], "right"), "action": variation_data["right"]},
    ]
    if player.level == 1:
        choices = [c for c in choices if c["action"] != "stairs_up"]
    return choices

def handle_event(player, choice):
    """Handle player choice and return appropriate result."""
    global current_enemy_image, enemy_alpha, enemy_fading_in, enemy_fading_out
    event_text = []
    
    if choice["action"] == "hall":
        enemy = enemies.get_random_enemy()
        scale = ENEMY_HEALTH_SCALES.get(player.difficulty, 1.0)
        enemy.health = int(enemy.health * scale)
        event_text.append(f"You cautiously enter the hallway and encounter {enemy.name}!")
        image_key = enemy.name.lower().replace(" ", "_")
        current_enemy_image = enemy_images.get(image_key, None)
        enemy_alpha = 0
        enemy_fading_in = True
        enemy_fading_out = False
        return "battle", enemy, event_text
        
    elif choice["action"] == "door":
        event_text.append("You open the door and find a dusty treasure chest!")
        if random.random() < HEAL_CHANCE:
            heal_amount = random.randint(MIN_HEAL, MAX_HEAL)
            player.heal(heal_amount)
            event_text.append(f"You found a potion and healed for {heal_amount} health!")
        else:
            player.spells += 1
            event_text.append("You found a scroll with a new spell!")
            
    elif choice["action"] == "stairs_up":
        player.level -= 1
        event_text.append(f"You climb the stairs. You are now on level {player.level}.")
        
    elif choice["action"] == "stairs_down":
        player.level += 1
        event_text.append(f"You descend the stairs. You are now on level {player.level}.")
        
    return "continue", None, event_text

def start_final_boss(screen, width, height, player, font, small_font):
    """Start the final boss battle with Mad King Baramour."""
    global current_enemy_image, enemy_alpha, enemy_fading_in, enemy_fading_out, is_player_attacking, is_enemy_attacking, shake_start_time, shake_duration
    
    script_dir = get_script_dir()
    mad_king_path = os.path.join(script_dir, "images", "game", "enemies", "madking.png")
    current_enemy_image = load_image(mad_king_path, ENEMY_IMAGE_SIZE, convert_alpha=True)
    
    enemy_alpha = 0
    enemy_fading_in = True
    enemy_fading_out = False
    
    king_health = BOSS_HEALTH.get(player.difficulty, 150)
    mad_king = enemies.Enemy("Mad King Baramour", attack=BOSS_ATTACK, health=king_health)
    game_log = ["You encounter the Mad King Baramour! Prepare for the ultimate battle!"]
    
    # Performance optimization
    clock = pygame.time.Clock()
    battle_over = False
    
    # Pre-calculate instruction text
    boss_instruction = "Press 'A' to attack or 'S' to cast a spell! (No running this time!)"
    
    while not battle_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_result = ingamemenu.show_pause_menu(screen, width, height)
                if pause_result == "continue":
                    pass
                elif pause_result == "exit_main_menu":
                    return "exit_main_menu"
                elif pause_result == "exit_game":
                    return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if not is_player_attacking and not is_enemy_attacking:
                        dmg = random.randint(MIN_ATTACK_DAMAGE, player.attack)
                        mad_king.take_damage(dmg)
                        game_log.append(f"You attack the Mad King for {dmg} damage!")
                        is_player_attacking = True
                        shake_start_time = pygame.time.get_ticks()
                        shake_duration = SHAKE_DURATION_BOSS
                elif event.key == pygame.K_s:
                    if player.spells > 0 and not is_player_attacking and not is_enemy_attacking:
                        dmg = random.randint(player.attack + SPELL_BONUS_MIN, player.attack + SPELL_BONUS_MAX)
                        mad_king.take_damage(dmg)
                        player.spells -= 1
                        game_log.append(f"You unleash a spell on the Mad King for {dmg} damage!")
                        is_player_attacking = True
                        shake_start_time = pygame.time.get_ticks()
                        shake_duration = SHAKE_DURATION_SPELL
                elif event.key == pygame.K_r:
                    game_log.append("You cannot run from the Mad King!")

        if is_player_attacking:
            elapsed_time = pygame.time.get_ticks() - shake_start_time
            if elapsed_time >= shake_duration:
                is_player_attacking = False
                if mad_king.is_alive():
                    is_enemy_attacking = True
                    shake_start_time = pygame.time.get_ticks()
                    shake_duration = SHAKE_DURATION_BOSS
                    taken = random.randint(mad_king.attack - ATTACK_VARIANCE, mad_king.attack + ATTACK_VARIANCE)
                    player.take_damage(taken)
                    game_log.append(f"The Mad King strikes you for {taken} damage!")
        
        if is_enemy_attacking:
            elapsed_time = pygame.time.get_ticks() - shake_start_time
            if elapsed_time >= shake_duration:
                is_enemy_attacking = False
                if not player.is_alive():
                    return gameover.show_game_over(screen, width, height)
        
        if not mad_king.is_alive():
            battle_over = True
            
        offset_x, offset_y = 0, 0
        if is_enemy_attacking:
            offset_x = random.randint(-SHAKE_OFFSET, SHAKE_OFFSET)
            offset_y = random.randint(-SHAKE_OFFSET, SHAKE_OFFSET)

        if background_image:
            screen.blit(background_image, (0 + offset_x, 0 + offset_y))
        else:
            screen.fill(DARK_GRAY)
            
        draw_level_area(screen, width, height, font, player)
        
        if current_enemy_image:
            if is_player_attacking:
                enemy_rect = current_enemy_image.get_rect(center=(width // 2, height // 4))
                shaked_rect = enemy_rect.move(random.randint(-ENEMY_SHAKE_OFFSET, ENEMY_SHAKE_OFFSET), 
                                            random.randint(-ENEMY_SHAKE_OFFSET, ENEMY_SHAKE_OFFSET))
                enemy_img = current_enemy_image.copy()
                enemy_img.set_alpha(enemy_alpha)
                screen.blit(enemy_img, shaked_rect)
            else:
                enemy_img = current_enemy_image.copy()
                enemy_img.set_alpha(enemy_alpha)
                screen.blit(enemy_img, enemy_img.get_rect(center=(width // 2, height // 4)))
                
        draw_game_ui(screen, width, height, font, small_font, player, game_log)

        if current_enemy_image:
            if enemy_fading_in:
                enemy_alpha += FADE_SPEED
                if enemy_alpha >= 255:
                    enemy_alpha = 255
                    enemy_fading_in = False
            elif enemy_fading_out:
                enemy_alpha -= FADE_SPEED
                if enemy_alpha <= 0:
                    enemy_alpha = 0
                    current_enemy_image = None
                    enemy_fading_out = False
        
        # Use pre-calculated instruction text
        surface = small_font.render(boss_instruction, True, WHITE)
        screen.blit(surface, surface.get_rect(center=(width // 2, height - 20)))
        
        # Maintain consistent frame rate
        clock.tick(60)
        pygame.display.flip()

    result = wingame.show_win_screen(screen, width, height, player)
    return result

def game_loop(screen, width, height, player, font, small_font):
    """Main game loop with optimized performance."""
    global background_image, level_variations, current_enemy_image, enemy_alpha, enemy_fading_in, enemy_fading_out, is_player_attacking, is_enemy_attacking, shake_start_time, shake_duration
    
    script_dir = get_script_dir()
    
    # Load game data once at startup
    json_path = os.path.join(script_dir, "randomlevel.json")
    try:
        with open(json_path, "r") as f:
            level_variations = json.load(f)
    except Exception as e:
        print(f"Error loading variations: {e}")
        level_variations = []
    
    # Load assets once at startup
    load_variation_images(script_dir)
    load_enemy_images(script_dir)
    
    # Load background image once
    bg_path = os.path.join(script_dir, "images", "game", "escapethecastle.png")
    background_image = load_image(bg_path, (width, height))

    # Typing effect variables
    typing_delay = TYPING_DELAY
    last_type_time = pygame.time.get_ticks()
    typing_cursor = 0
    
    is_typing_welcome = True
    is_typing_choices = False
    is_typing_combat = False
    
    # Game log that persists - will only contain current choice and next choices
    full_game_log = []
    
    # Welcome message logic to show (only shown once, then removed)
    welcome_message = [
        f"Welcome, {player.name}!",
        f"You start at level {player.level}.",
        "Your goal is to defeat the mad king Boromour and save the kingdom!"
    ]
    
    # Track if welcome has been shown and removed
    welcome_shown = False
    welcome_typing_finished = False
    welcome_display_time = 0
    WELCOME_DISPLAY_DURATION = 3000  # 3 seconds to read the welcome message
    
    # Track combat state transitions
    combat_finished = False
    combat_finish_time = 0
    COMBAT_FINISH_DISPLAY_DURATION = 2000  # 2 seconds to read combat result
    
    player.input_text = ""
    current_choices = []
    in_battle = False
    current_enemy = None
    
    # Combat state variables
    is_player_attacking = False
    is_enemy_attacking = False
    shake_start_time = 0
    shake_duration = 0

    # Performance optimization
    clock = pygame.time.Clock()
    running = True
    
    # Pre-calculate reminder messages
    reminder_messages = [
        "Make your next choice...",
        "⚔️ Choose your path wisely...",
        "➡️ Which way will you go?",
        "🔮 Destiny awaits — what will you decide?",
        "🚪 Step forward, adventurer...",
        "👀 The castle watches — choose carefully...",
        "🕯️ Another path lies ahead..."
    ]
    
    # Pre-calculate instruction text
    battle_instruction = "Press 'A' to attack, 'S' to use a spell, or 'R' to run."
    choice_instruction = "Press 1-3 to choose. Press 'ESC' for menu."
    
    while running:
        if not player.is_alive():
            result = gameover.show_game_over(screen, width, height)
            return result
        if player.level <= 1:
            return start_final_boss(screen, width, height, player, font, small_font)

        # Handle combat finish transition
        if combat_finished and pygame.time.get_ticks() - combat_finish_time > COMBAT_FINISH_DISPLAY_DURATION:
            combat_finished = False
            # Generate new choices after combat
            current_choices = generate_choices(player)
            player.choices_text = [f"[{i}] {c['text']}" for i, c in enumerate(current_choices, 1)]
            full_game_log = [
                f"On level {player.level} you see",
                ""
            ]
            full_game_log.extend(player.choices_text)
            full_game_log.extend(["", random.choice(reminder_messages)])
            is_typing_choices = True
            typing_cursor = 0
            last_type_time = pygame.time.get_ticks()

        # Main game state logic
        if not is_typing_welcome and not is_typing_choices and not is_typing_combat and not in_battle and not current_choices and not combat_finished:
            current_choices = generate_choices(player)
            player.choices_text = [f"[{i}] {c['text']}" for i, c in enumerate(current_choices, 1)]
            is_typing_choices = True
            typing_cursor = 0
            last_type_time = pygame.time.get_ticks()
            
            # Clear the log and add only the new choices (log rotation)
            full_game_log = [
                f"On level {player.level} you see",
                ""
            ]
            full_game_log.extend(player.choices_text)
            full_game_log.extend(["", random.choice(reminder_messages)])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_result = ingamemenu.show_pause_menu(screen, width, height)
                    if pause_result == "continue":
                        pass
                    elif pause_result == "exit_main_menu":
                        return "exit_main_menu"
                    elif pause_result == "exit_game":
                        return "exit"
                elif in_battle and not is_typing_combat:
                    if event.key == pygame.K_a:
                        if not is_player_attacking and not is_enemy_attacking:
                            dmg = random.randint(MIN_ATTACK_DAMAGE, player.attack)
                            current_enemy.take_damage(dmg)
                            full_game_log.append(f"You attack {current_enemy.name} for {dmg} damage!")
                            is_player_attacking = True
                            shake_start_time = pygame.time.get_ticks()
                            shake_duration = SHAKE_DURATION_PLAYER
                    elif event.key == pygame.K_s:
                        if player.spells > 0 and not is_player_attacking and not is_enemy_attacking:
                            dmg = random.randint(player.attack + SPELL_BONUS_MIN, player.attack + SPELL_BONUS_MAX)
                            current_enemy.take_damage(dmg)
                            player.spells -= 1
                            full_game_log.append(f"You unleash a spell on {current_enemy.name} for {dmg} damage!")
                            is_player_attacking = True
                            shake_start_time = pygame.time.get_ticks()
                            shake_duration = SHAKE_DURATION_PLAYER
                        else:
                            full_game_log.append("You have no spells left!")
                    elif event.key == pygame.K_r:
                        roll = random.random()
                        success_chance = RUN_CHANCES.get(player.difficulty, 0.4)
                        if roll < success_chance:
                            full_game_log.append("You attempt to run away and succeed!")
                            in_battle, current_enemy = False, None
                            enemy_fading_out = True
                            is_typing_combat = True
                            typing_cursor = 0
                            last_type_time = pygame.time.get_ticks()
                        else:
                            if roll < success_chance + 0.3:
                                full_game_log.append("You attempt to run away but are blocked! You must stay and fight.")
                            else:
                                taken = random.randint(current_enemy.attack - ATTACK_VARIANCE, current_enemy.attack + ATTACK_VARIANCE)
                                player.take_damage(taken)
                                full_game_log.append(f"You attempt to run away but are blocked and struck down by the enemy!")
                                full_game_log.append(f"The {current_enemy.name} deals {taken} damage while you try to flee!")
                elif not is_typing_welcome and not is_typing_choices and not is_typing_combat:
                    try:
                        idx = int(event.unicode) - 1
                        if 0 <= idx < len(current_choices):
                            # Clear the log and show only the choice made
                            full_game_log = [f"> You chose: {current_choices[idx]['text']}"]
                            
                            result, new_enemy, event_log = handle_event(player, current_choices[idx])
                            
                            if result == "battle":
                                # Replace log with combat messages
                                full_game_log = event_log.copy()
                                in_battle, current_enemy = True, new_enemy
                                is_typing_combat = True
                                typing_cursor = 0
                                last_type_time = pygame.time.get_ticks()
                            else:
                                # For non-combat events, add the result and start typing
                                full_game_log.extend(event_log)
                                is_typing_choices = True
                                typing_cursor = 0
                                last_type_time = pygame.time.get_ticks()
                            
                            current_choices = []
                        else:
                            full_game_log = ["Invalid choice, please enter 1, 2, or 3."]
                            is_typing_choices = True
                            typing_cursor = 0
                            last_type_time = pygame.time.get_ticks()
                    except (ValueError, IndexError):
                        pass

        if in_battle and not is_player_attacking and not is_enemy_attacking and current_enemy and not current_enemy.is_alive():
            # Add victory message to current combat log
            full_game_log.append(f"You have defeated {current_enemy.name}!")
            full_game_log.append("You may now continue.")
            in_battle, current_enemy = False, None
            enemy_fading_out = True
            # Mark combat as finished and start display timer
            combat_finished = True
            combat_finish_time = pygame.time.get_ticks()
            is_typing_combat = False
            
        if is_player_attacking:
            elapsed_time = pygame.time.get_ticks() - shake_start_time
            if elapsed_time >= shake_duration:
                is_player_attacking = False
                if current_enemy and current_enemy.is_alive():
                    is_enemy_attacking = True
                    shake_start_time = pygame.time.get_ticks()
                    shake_duration = SHAKE_DURATION_ENEMY
                    taken = random.randint(current_enemy.attack - ATTACK_VARIANCE, current_enemy.attack + ATTACK_VARIANCE)
                    player.take_damage(taken)
                    full_game_log.append(f"{current_enemy.name} attacks you for {taken} damage!")

        if is_enemy_attacking:
            elapsed_time = pygame.time.get_ticks() - shake_start_time
            if elapsed_time >= shake_duration:
                is_enemy_attacking = False
                if not player.is_alive():
                    full_game_log.append("You have been defeated... Game Over.")
                    result = gameover.show_game_over(screen, width, height)
                    return result
        
        offset_x, offset_y = 0, 0
        if is_enemy_attacking:
            offset_x = random.randint(-SHAKE_OFFSET, SHAKE_OFFSET)
            offset_y = random.randint(-SHAKE_OFFSET, SHAKE_OFFSET)
            
        if background_image:
            screen.blit(background_image, (0 + offset_x, 0 + offset_y))
        else:
            screen.fill(DARK_GRAY)
            
        draw_level_area(screen, width, height, font, player)

        if current_enemy_image:
            if is_player_attacking:
                enemy_rect = current_enemy_image.get_rect(center=(width // 2, height // 4))
                shaked_rect = enemy_rect.move(random.randint(-ENEMY_SHAKE_OFFSET, ENEMY_SHAKE_OFFSET), 
                                            random.randint(-ENEMY_SHAKE_OFFSET, ENEMY_SHAKE_OFFSET))
                enemy_img = current_enemy_image.copy()
                enemy_img.set_alpha(enemy_alpha)
                screen.blit(enemy_img, shaked_rect)
            else:
                enemy_img = current_enemy_image.copy()
                enemy_img.set_alpha(enemy_alpha)
                screen.blit(enemy_img, enemy_img.get_rect(center=(width // 2, height // 4)))
        
        # Typing logic for typewriter effect
        display_log = []
        if is_typing_welcome:
            total_chars = sum(len(line) for line in welcome_message) + (len(welcome_message) - 1) * 2
            if typing_cursor < total_chars:
                if pygame.time.get_ticks() - last_type_time > typing_delay:
                    typing_cursor += 1
                    last_type_time = pygame.time.get_ticks()
            else:
                # Welcome typing finished, start display timer
                if not welcome_typing_finished:
                    welcome_typing_finished = True
                    welcome_display_time = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - welcome_display_time > WELCOME_DISPLAY_DURATION:
                    # Display time finished, transition to choices
                    is_typing_welcome = False
                    welcome_shown = True
                    current_choices = generate_choices(player)
                    player.choices_text = [f"[{i}] {c['text']}" for i, c in enumerate(current_choices, 1)]
                    
                # Add the first set of choices to the log (welcome message is not added to full_game_log)
                full_game_log = [
                    f"On level {player.level} you see",
                    ""
                ]
                full_game_log.extend(player.choices_text)
                full_game_log.extend(["", random.choice(reminder_messages)])
                is_typing_choices = True
                typing_cursor = 0
                last_type_time = pygame.time.get_ticks()
            
            # Always show the full welcome message during typing and display period
            if welcome_typing_finished:
                display_log = welcome_message.copy()
            else:
                char_count = 0
                for line in welcome_message:
                    if char_count + len(line) <= typing_cursor:
                        display_log.append(line)
                        char_count += len(line) + 2  # +2 for newline characters
                    else:
                        remaining_chars = typing_cursor - char_count
                        if remaining_chars > 0:
                            display_log.append(line[:remaining_chars])
                        break
        elif is_typing_choices:
            total_chars = sum(len(line) for line in full_game_log) + (len(full_game_log) - 1) * 2
            
            if typing_cursor < total_chars:
                if pygame.time.get_ticks() - last_type_time > typing_delay:
                    typing_cursor += 1
                    last_type_time = pygame.time.get_ticks()
            else:
                is_typing_choices = False

            char_count = 0
            for line in full_game_log:
                if char_count + len(line) <= typing_cursor:
                    display_log.append(line)
                    char_count += len(line) + 2  # Add 2 for newline characters
                else:
                    remaining_chars = typing_cursor - char_count
                    if remaining_chars > 0:
                        display_log.append(line[:remaining_chars])
                    break
        elif is_typing_combat:
            total_chars = sum(len(line) for line in full_game_log) + (len(full_game_log) - 1) * 2
            
            if typing_cursor < total_chars:
                if pygame.time.get_ticks() - last_type_time > typing_delay:
                    typing_cursor += 1
                    last_type_time = pygame.time.get_ticks()
            else:
                is_typing_combat = False

            char_count = 0
            for line in full_game_log:
                if char_count + len(line) <= typing_cursor:
                    display_log.append(line)
                    char_count += len(line) + 2  # Add 2 for newline characters
                else:
                    remaining_chars = typing_cursor - char_count
                    if remaining_chars > 0:
                        display_log.append(line[:remaining_chars])
                    break
        elif combat_finished:
            # Show the final combat result without typing
            display_log = full_game_log
        else:
            display_log = full_game_log

        draw_game_ui(screen, width, height, font, small_font, player, display_log)
        
        # Use pre-calculated instruction text
        instruction = battle_instruction if in_battle else choice_instruction
        surface = small_font.render(instruction, True, WHITE)
        screen.blit(surface, surface.get_rect(center=(width // 2, height - 20)))
        
        if current_enemy_image:
            if enemy_fading_in:
                enemy_alpha += FADE_SPEED
                if enemy_alpha >= 255:
                    enemy_alpha = 255
                    enemy_fading_in = False
            elif enemy_fading_out:
                enemy_alpha -= FADE_SPEED
                if enemy_alpha <= 0:
                    enemy_alpha = 0
                    current_enemy_image = None
                    enemy_fading_out = False
        
        # Maintain consistent frame rate
        clock.tick(60)
        pygame.display.flip()
    return "exit"

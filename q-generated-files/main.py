#!/usr/bin/env python3
"""
Burger Stacker - A color-matching memory game
Players must recreate color patterns from bottom to top within a time limit.
"""

import os
import pygame
import random
import json
import time
import math

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GAME_TIME = 60  # seconds

# Colors - Modern Dark Theme
BG_COLOR = (18, 18, 18)  # Dark background
TEXT_COLOR = (240, 240, 240)  # Light text
ACCENT_COLOR = (75, 75, 75)  # Dark gray for UI elements
HIGHLIGHT_COLOR = (50, 168, 82)  # Green highlight
PANEL_COLOR = (30, 30, 30)  # Slightly lighter than background
OVERLAY_COLOR = (0, 0, 0, 180)  # Semi-transparent black

# Burger colors - More modern/saturated
RED = (235, 64, 52)  # Tomato red
YELLOW = (252, 186, 3)  # Golden yellow
BLUE = (66, 135, 245)  # Bright blue
GREEN = (46, 204, 113)  # Emerald green
BUN_COLOR = (222, 165, 75)  # Golden brown for bun

# Color mapping
COLOR_MAP = {
    'red': RED,
    'yellow': YELLOW,
    'blue': BLUE,
    'green': GREEN
}

# Key mapping
KEY_MAP = {
    pygame.K_q: 'red',
    pygame.K_w: 'yellow',
    pygame.K_e: 'blue',
    pygame.K_r: 'green'
}

# Button labels
BUTTON_LABELS = {
    'red': 'Q',
    'yellow': 'W',
    'blue': 'E',
    'green': 'R'
}


class BurgerStacker:
    def __init__(self):
        """Initialize the game."""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Burger Stacker")
        self.clock = pygame.time.Clock()

        # Load fonts - Using system fonts for a more modern look
        try:
            self.font_large = pygame.font.Font(None, 56)
            self.font_medium = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)
            self.font_button = pygame.font.Font(None, 42)
        except:
            # Fallback to system font if custom font fails
            self.font_large = pygame.font.SysFont("Arial", 56)
            self.font_medium = pygame.font.SysFont("Arial", 36)
            self.font_small = pygame.font.SysFont("Arial", 24)
            self.font_button = pygame.font.SysFont("Arial", 42)

        # Game state
        self.running = True
        self.game_over = False
        self.score = 0
        self.high_score = self.load_high_score()
        self.start_time = 0
        self.remaining_time = GAME_TIME

        # Burger patterns
        self.target_stack = []
        self.player_stack = []

        # Animation variables
        self.animation_timer = 0
        self.button_hover = None

        # Generate first burger
        self.generate_new_stack()

    def load_high_score(self):
        """Load high score from file."""
        try:
            if os.path.exists('high_score.json'):
                with open('high_score.json', 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except Exception as e:
            print(f"Error loading high score: {e}")
        return 0

    def save_high_score(self):
        """Save high score to file."""
        try:
            with open('high_score.json', 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except Exception as e:
            print(f"Error saving high score: {e}")

    def generate_new_stack(self):
        """Generate a new random burger stack."""
        # Clear player stack
        self.player_stack = []

        # Generate random stack with 1-5 layers
        stack_height = random.randint(1, 5)
        colors = ['red', 'yellow', 'blue', 'green']
        self.target_stack = [random.choice(colors) for _ in range(stack_height)]

    def check_match(self):
        """Check if player stack matches target stack."""
        if self.player_stack == self.target_stack:
            # Award points equal to stack height
            self.score += len(self.target_stack)
            # Generate new stack immediately for faster pace
            self.generate_new_stack()
            return True
        else:
            # Clear player stack immediately for faster pace
            self.player_stack = []
            return False

    def draw_burger(self, stack, x, y, is_target=True):
        """Draw a burger stack on screen with modern styling."""
        bun_width = 150
        layer_height = 25
        shadow_offset = 4

        # Draw shadow for bottom bun
        pygame.draw.ellipse(self.screen, (0, 0, 0, 100),
                          (x - bun_width//2 + shadow_offset, y + shadow_offset,
                           bun_width, layer_height))

        # Draw bottom bun with rounded corners
        pygame.draw.ellipse(self.screen, BUN_COLOR,
                          (x - bun_width//2, y, bun_width, layer_height))

        # Draw layers from bottom to top with shadows
        for i, color_name in enumerate(stack):
            layer_y = y - (i + 1) * layer_height

            # Draw shadow
            pygame.draw.rect(self.screen, (0, 0, 0, 100),
                           (x - bun_width//2 + shadow_offset, layer_y + shadow_offset,
                            bun_width, layer_height))

            # Draw layer with rounded corners
            pygame.draw.rect(self.screen, COLOR_MAP[color_name],
                           (x - bun_width//2, layer_y, bun_width, layer_height),
                           0, 5)

            # Add highlight to give 3D effect
            pygame.draw.rect(self.screen, self.lighten_color(COLOR_MAP[color_name]),
                           (x - bun_width//2, layer_y, bun_width, layer_height//3),
                           0, 5)

        # Draw top bun if it's the target burger or if player has completed their stack
        if is_target or len(self.player_stack) == len(self.target_stack):
            top_bun_y = y - (len(stack) + 1) * layer_height

            # Draw shadow for top bun
            pygame.draw.ellipse(self.screen, (0, 0, 0, 100),
                              (x - bun_width//2 + shadow_offset, top_bun_y + shadow_offset,
                               bun_width, layer_height))

            # Draw top bun with rounded corners
            pygame.draw.ellipse(self.screen, BUN_COLOR,
                              (x - bun_width//2, top_bun_y, bun_width, layer_height))

            # Add highlight to give 3D effect
            pygame.draw.ellipse(self.screen, self.lighten_color(BUN_COLOR),
                              (x - bun_width//2, top_bun_y, bun_width, layer_height//2))

    def lighten_color(self, color, amount=30):
        """Return a lighter version of the given color."""
        r = min(color[0] + amount, 255)
        g = min(color[1] + amount, 255)
        b = min(color[2] + amount, 255)
        return (r, g, b)

    def darken_color(self, color, amount=30):
        """Return a darker version of the given color."""
        r = max(color[0] - amount, 0)
        g = max(color[1] - amount, 0)
        b = max(color[2] - amount, 0)
        return (r, g, b)

    def draw_modern_button(self, x, y, width, height, color, text, key=None, hover=False):
        """Draw a modern-looking button with hover effects."""
        # Button shadow
        shadow_offset = 4
        pygame.draw.rect(self.screen, (0, 0, 0, 100),
                       (x + shadow_offset, y + shadow_offset, width, height),
                       0, 15)

        # Button base
        button_color = self.lighten_color(color, 20) if hover else color
        pygame.draw.rect(self.screen, button_color, (x, y, width, height), 0, 15)

        # Button highlight (top edge)
        highlight_height = height // 4
        pygame.draw.rect(self.screen, self.lighten_color(button_color),
                       (x, y, width, highlight_height), 0, 15)

        # Button text
        text_surf = self.font_button.render(text, True, (30, 30, 30))
        text_rect = text_surf.get_rect(center=(x + width//2, y + height//2))
        self.screen.blit(text_surf, text_rect)

        # Key label (if provided)
        if key:
            key_bg_size = 30
            # Key background
            pygame.draw.rect(self.screen, (30, 30, 30),
                           (x + width - key_bg_size - 10, y + 10,
                            key_bg_size, key_bg_size),
                           0, 8)

            # Key text
            key_surf = self.font_small.render(key, True, TEXT_COLOR)
            key_rect = key_surf.get_rect(center=(x + width - key_bg_size//2 - 10,
                                                y + 10 + key_bg_size//2))
            self.screen.blit(key_surf, key_rect)

    def draw_color_buttons(self):
        """Draw modern color buttons with key labels."""
        button_width = 100
        button_height = 80
        spacing = 20
        total_width = 4 * button_width + 3 * spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        y = SCREEN_HEIGHT - 120

        colors = ['red', 'yellow', 'blue', 'green']

        for i, color_name in enumerate(colors):
            x = start_x + i * (button_width + spacing)

            # Check if mouse is hovering over this button
            mouse_pos = pygame.mouse.get_pos()
            hover = (x <= mouse_pos[0] <= x + button_width and
                     y <= mouse_pos[1] <= y + button_height)

            # Draw modern button
            self.draw_modern_button(x, y, button_width, button_height,
                                  COLOR_MAP[color_name], "",
                                  BUTTON_LABELS[color_name], hover)

    def draw_panel(self, x, y, width, height, title=None):
        """Draw a modern UI panel with optional title."""
        # Panel shadow
        shadow_offset = 6
        pygame.draw.rect(self.screen, (0, 0, 0, 100),
                       (x + shadow_offset, y + shadow_offset, width, height),
                       0, 10)

        # Panel background
        pygame.draw.rect(self.screen, PANEL_COLOR, (x, y, width, height), 0, 10)

        # Panel border highlight
        pygame.draw.rect(self.screen, ACCENT_COLOR, (x, y, width, height), 2, 10)

        # Title if provided
        if title:
            title_surf = self.font_medium.render(title, True, TEXT_COLOR)
            title_rect = title_surf.get_rect(midtop=(x + width//2, y + 10))
            self.screen.blit(title_surf, title_rect)

    def draw_progress_bar(self, x, y, width, height, progress, max_value):
        """Draw a modern progress bar."""
        # Background
        pygame.draw.rect(self.screen, ACCENT_COLOR, (x, y, width, height), 0, height//2)

        # Progress
        progress_width = int(width * (progress / max_value))
        if progress_width > 0:
            pygame.draw.rect(self.screen, HIGHLIGHT_COLOR,
                           (x, y, progress_width, height), 0, height//2)

    def draw_ui(self):
        """Draw modern game UI elements."""
        # Top panel for score and time
        panel_height = 60
        self.draw_panel(20, 20, SCREEN_WIDTH - 40, panel_height)

        # Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (40, 35))

        # High score
        high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, TEXT_COLOR)
        high_score_rect = high_score_text.get_rect(right=SCREEN_WIDTH-40, centery=50)
        self.screen.blit(high_score_text, high_score_rect)

        # Time bar
        time_text = self.font_small.render(f"Time: {int(self.remaining_time)}s", True, TEXT_COLOR)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH//2, 35))
        self.screen.blit(time_text, time_rect)

        # Progress bar for time
        bar_width = 200
        bar_height = 10
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = 50
        self.draw_progress_bar(bar_x, bar_y, bar_width, bar_height,
                             self.remaining_time, GAME_TIME)

        # Instruction panel - Fixed to prevent text overlap
        instr_panel_y = SCREEN_HEIGHT - 180
        self.draw_panel(20, instr_panel_y, SCREEN_WIDTH - 40, 60)

        # Instructions title - Positioned at the top of the panel
        instr_title = self.font_medium.render("Instructions", True, TEXT_COLOR)
        instr_title_rect = instr_title.get_rect(center=(SCREEN_WIDTH//2, instr_panel_y + 20))
        self.screen.blit(instr_title, instr_title_rect)

        # Instructions text - Positioned below the title
        instructions = "Match the burger pattern from bottom to top | BACKSPACE to remove top layer | ENTER to submit"
        instr_text = self.font_small.render(instructions, True, TEXT_COLOR)
        instr_rect = instr_text.get_rect(center=(SCREEN_WIDTH//2, instr_panel_y + 45))
        self.screen.blit(instr_text, instr_rect)

        # Target and player panels
        target_panel_width = 200
        target_panel_height = 300
        target_panel_x = SCREEN_WIDTH//4 - target_panel_width//2
        target_panel_y = 100

        player_panel_width = 200
        player_panel_height = 300
        player_panel_x = 3*SCREEN_WIDTH//4 - player_panel_width//2
        player_panel_y = 100

        self.draw_panel(target_panel_x, target_panel_y, target_panel_width, target_panel_height, "Target")
        self.draw_panel(player_panel_x, player_panel_y, player_panel_width, player_panel_height, "Your Stack")

    def draw_game_over(self):
        """Draw modern game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(OVERLAY_COLOR)
        self.screen.blit(overlay, (0, 0))

        # Game over panel
        panel_width = 400
        panel_height = 300
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2

        self.draw_panel(panel_x, panel_y, panel_width, panel_height)

        # Game over text
        game_over_text = self.font_large.render("GAME OVER", True, TEXT_COLOR)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, panel_y + 50))
        self.screen.blit(game_over_text, game_over_rect)

        # Final score
        score_text = self.font_medium.render(f"Final Score: {self.score}", True, TEXT_COLOR)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, panel_y + 120))
        self.screen.blit(score_text, score_rect)

        # High score
        high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, TEXT_COLOR)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, panel_y + 170))
        self.screen.blit(high_score_text, high_score_rect)

        # Restart button
        button_width = 200
        button_height = 50
        button_x = (SCREEN_WIDTH - button_width) // 2
        button_y = panel_y + 220

        # Check if mouse is hovering over restart button
        mouse_pos = pygame.mouse.get_pos()
        hover = (button_x <= mouse_pos[0] <= button_x + button_width and
                 button_y <= mouse_pos[1] <= button_y + button_height)

        self.draw_modern_button(button_x, button_y, button_width, button_height,
                              HIGHLIGHT_COLOR, "Play Again", hover=hover)

    def reset_game(self):
        """Reset the game state."""
        self.game_over = False
        self.score = 0
        self.remaining_time = GAME_TIME
        self.start_time = time.time()
        self.generate_new_stack()

    def handle_events(self):
        """Handle game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.reset_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if restart button was clicked
                    mouse_pos = pygame.mouse.get_pos()
                    button_width = 200
                    button_height = 50
                    button_x = (SCREEN_WIDTH - button_width) // 2
                    button_y = (SCREEN_HEIGHT + 140) // 2

                    if (button_x <= mouse_pos[0] <= button_x + button_width and
                        button_y <= mouse_pos[1] <= button_y + button_height):
                        self.reset_game()
                continue

            if event.type == pygame.KEYDOWN:
                # Color input keys
                if event.key in KEY_MAP and len(self.player_stack) < len(self.target_stack):
                    self.player_stack.append(KEY_MAP[event.key])

                # Backspace to remove top layer
                elif event.key == pygame.K_BACKSPACE and self.player_stack:
                    self.player_stack.pop()

                # Enter to submit pattern
                elif event.key == pygame.K_RETURN and self.player_stack:
                    if len(self.player_stack) == len(self.target_stack):
                        self.check_match()

            # Mouse click for color buttons
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                button_width = 100
                button_height = 80
                spacing = 20
                total_width = 4 * button_width + 3 * spacing
                start_x = (SCREEN_WIDTH - total_width) // 2
                y = SCREEN_HEIGHT - 120

                colors = ['red', 'yellow', 'blue', 'green']

                for i, color_name in enumerate(colors):
                    x = start_x + i * (button_width + spacing)

                    if (x <= mouse_pos[0] <= x + button_width and
                        y <= mouse_pos[1] <= y + button_height and
                        len(self.player_stack) < len(self.target_stack)):
                        self.player_stack.append(color_name)

    def update(self):
        """Update game state."""
        if self.game_over:
            return

        # Update time
        current_time = time.time()
        elapsed = current_time - self.start_time
        self.remaining_time = max(0, GAME_TIME - elapsed)

        # Check for game over
        if self.remaining_time <= 0:
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()

        # Update animation timer for subtle UI effects
        self.animation_timer = (self.animation_timer + 1) % 60

    def draw(self):
        """Draw the game screen."""
        self.screen.fill(BG_COLOR)

        # Draw UI elements
        self.draw_ui()

        # Draw target burger on left side
        self.draw_burger(self.target_stack, SCREEN_WIDTH//4, SCREEN_HEIGHT//2, True)

        # Draw player burger on right side
        self.draw_burger(self.player_stack, 3*SCREEN_WIDTH//4, SCREEN_HEIGHT//2, False)

        # Draw color buttons
        self.draw_color_buttons()

        # Draw game over screen if game is over
        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        self.start_time = time.time()

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = BurgerStacker()
    game.run()

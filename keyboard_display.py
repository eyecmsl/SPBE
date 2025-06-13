"""
Keyboard Display - Visual keyboard for learning aid
"""

import pygame

class KeyboardDisplay:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Keyboard layout
        self.keyboard_rows = [
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm']
        ]
        
        # Key properties
        self.key_width = 45
        self.key_height = 45
        self.key_spacing = 5
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.GREEN = (144, 238, 144)
        self.BLUE = (173, 216, 230)
        
        # Font
        self.font = pygame.font.Font(None, 24)
        
        # Calculate keyboard position
        self.keyboard_y = self.screen_height - 200
        
    def draw(self, user_input):
        """Draw the virtual keyboard with highlights"""
        # Draw keyboard background
        total_width = len(self.keyboard_rows[0]) * (self.key_width + self.key_spacing)
        keyboard_x = (self.screen_width - total_width) // 2
        
        for row_idx, row in enumerate(self.keyboard_rows):
            # Calculate row offset for centered appearance
            row_width = len(row) * (self.key_width + self.key_spacing)
            row_x = (self.screen_width - row_width) // 2
            
            for key_idx, key in enumerate(row):
                # Calculate key position
                key_x = row_x + key_idx * (self.key_width + self.key_spacing)
                key_y = self.keyboard_y + row_idx * (self.key_height + self.key_spacing)
                
                # Determine key color based on user input
                key_color = self.GRAY
                text_color = self.BLACK
                
                # Highlight if key was typed
                if key in user_input.lower():
                    key_color = self.GREEN
                    
                # Highlight current key (last typed)
                if user_input and key == user_input[-1].lower():
                    key_color = self.BLUE
                    
                # Draw key
                key_rect = pygame.Rect(key_x, key_y, self.key_width, self.key_height)
                pygame.draw.rect(self.screen, key_color, key_rect)
                pygame.draw.rect(self.screen, self.BLACK, key_rect, 2)
                
                # Draw key label
                key_text = self.font.render(key.upper(), True, text_color)
                text_rect = key_text.get_rect()
                text_rect.center = key_rect.center
                self.screen.blit(key_text, text_rect)
                
        # Draw space bar
        space_width = 200
        space_x = (self.screen_width - space_width) // 2
        space_y = self.keyboard_y + len(self.keyboard_rows) * (self.key_height + self.key_spacing) + 10
        
        space_color = self.BLUE if ' ' in user_input else self.GRAY
        space_rect = pygame.Rect(space_x, space_y, space_width, self.key_height)
        pygame.draw.rect(self.screen, space_color, space_rect)
        pygame.draw.rect(self.screen, self.BLACK, space_rect, 2)
        
        space_text = self.font.render("SPACE (Replay)", True, self.BLACK)
        text_rect = space_text.get_rect()
        text_rect.center = space_rect.center
        self.screen.blit(space_text, text_rect)

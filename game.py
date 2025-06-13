"""
Main Game Controller for Spelling Bee
Handles game states, main loop, and coordination between components
"""

import pygame
import sys
from word_manager import WordManager
from audio_controller import AudioController
from ui_manager import UIManager
from keyboard_display import KeyboardDisplay
from background import ParallaxBackground

class SpellingBeeGame:
    def __init__(self):
        # Game settings
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        self.FPS = 60
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Spelling Bee - Educational Typing Game")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.game_state = "menu"  # menu, playing, game_over
        self.running = True
        
        # Game mechanics
        self.score = 0
        self.lives = 3
        self.current_word = ""
        self.user_input = ""
        self.word_revealed = False
        self.feedback_timer = 0
        self.feedback_message = ""
        self.feedback_color = (255, 255, 255)
        self.time_limit = 30  # 30 seconds per word
        self.word_start_time = 0
        self.time_remaining = self.time_limit
        self.hint_used = False
        self.hint_text = ""
        
        # Statistics tracking
        self.words_attempted = 0
        self.words_correct = 0
        self.total_response_time = 0
        self.session_start_time = pygame.time.get_ticks()
        
        # Initialize components
        self.word_manager = WordManager()
        self.audio_controller = AudioController()
        self.ui_manager = UIManager(self.screen)
        self.keyboard_display = KeyboardDisplay(self.screen)
        self.background = ParallaxBackground(self.screen)
        
        # Get first word
        self.next_word()
        
    def next_word(self):
        """Get next word from word manager"""
        self.current_word = self.word_manager.get_next_word(self.score)
        self.user_input = ""
        self.word_revealed = False
        self.word_start_time = pygame.time.get_ticks()
        self.time_remaining = self.time_limit
        self.hint_used = False
        self.hint_text = ""
        
        # Play pronunciation
        self.audio_controller.play_word_pronunciation(self.current_word)
        
    def show_hint(self):
        """Show a hint for the current word"""
        if not self.hint_used and not self.word_revealed:
            # Show first letter and word length
            self.hint_text = f"Hint: {self.current_word[0].upper()}{'_' * (len(self.current_word) - 1)} ({len(self.current_word)} letters)"
            self.hint_used = True
            # Reduce score slightly for using hint
            self.score = max(0, self.score - 5)
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "menu":
                    if event.key == pygame.K_SPACE:
                        self.game_state = "playing"
                        
                elif self.game_state == "playing":
                    if event.key == pygame.K_RETURN:
                        self.check_answer()
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    elif event.key == pygame.K_SPACE:
                        # Replay word pronunciation
                        self.audio_controller.play_word_pronunciation(self.current_word)
                    elif event.key == pygame.K_h:
                        # Show hint
                        self.show_hint()
                    elif event.unicode.isprintable() and len(self.user_input) < 20:
                        self.user_input += event.unicode.lower()
                        
                elif self.game_state == "game_over":
                    if event.key == pygame.K_SPACE:
                        self.restart_game()
                        
    def check_answer(self):
        """Check if user input matches current word"""
        response_time = (pygame.time.get_ticks() - self.word_start_time) / 1000.0
        self.words_attempted += 1
        
        if self.user_input.lower().strip() == self.current_word.lower():
            # Correct answer
            self.words_correct += 1
            self.total_response_time += response_time
            points = 10 * self.word_manager.get_difficulty_multiplier(self.score)
            
            # Bonus for fast answers
            if response_time < 5:
                points += 5
                self.feedback_message = "Excellent! Quick and correct!"
            else:
                self.feedback_message = "Correct!"
                
            self.score += points
            self.feedback_color = (0, 255, 0)
            self.audio_controller.play_correct_sound()
            self.word_revealed = True
            
            # Move to next word after delay
            pygame.time.set_timer(pygame.USEREVENT + 1, 1500)
            
        else:
            # Wrong answer
            self.lives -= 1
            self.feedback_message = f"Wrong! The word was: {self.current_word}"
            self.feedback_color = (255, 0, 0)
            self.audio_controller.play_incorrect_sound()
            self.word_revealed = True
            
            if self.lives <= 0:
                self.game_state = "game_over"
                self.audio_controller.play_death_sound()
            else:
                # Move to next word after delay
                pygame.time.set_timer(pygame.USEREVENT + 1, 2000)
                
        self.feedback_timer = pygame.time.get_ticks()
        
    def restart_game(self):
        """Restart the game"""
        self.score = 0
        self.lives = 3
        self.game_state = "playing"
        self.word_manager.reset()
        self.next_word()
        
    def update(self):
        """Update game logic"""
        # Handle custom events
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                if self.game_state == "playing":
                    self.next_word()
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Cancel timer
                
        # Update background animation
        self.background.update()
        
        # Update timer for current word
        if self.game_state == "playing" and not self.word_revealed:
            elapsed_time = (pygame.time.get_ticks() - self.word_start_time) / 1000.0
            self.time_remaining = max(0, self.time_limit - elapsed_time)
            
            # Check if time is up
            if self.time_remaining <= 0:
                self.lives -= 1
                self.feedback_message = f"Time's up! The word was: {self.current_word}"
                self.feedback_color = (255, 165, 0)  # Orange
                self.audio_controller.play_incorrect_sound()
                self.word_revealed = True
                
                if self.lives <= 0:
                    self.game_state = "game_over"
                    self.audio_controller.play_death_sound()
                else:
                    pygame.time.set_timer(pygame.USEREVENT + 1, 2000)
                    
                self.feedback_timer = pygame.time.get_ticks()
        
        # Clear old feedback
        if pygame.time.get_ticks() - self.feedback_timer > 3000:
            self.feedback_message = ""
            
    def render(self):
        """Render all game elements"""
        # Draw background
        self.background.draw()
        
        if self.game_state == "menu":
            self.ui_manager.draw_menu()
            
        elif self.game_state == "playing":
            # Draw game UI
            self.ui_manager.draw_game_ui(self.score, self.lives, self.user_input, 
                                       self.current_word if self.word_revealed else "",
                                       self.feedback_message, self.feedback_color,
                                       self.time_remaining, self.word_manager.difficulty_level,
                                       self.hint_text)
            
            # Draw keyboard
            self.keyboard_display.draw(self.user_input)
            
        elif self.game_state == "game_over":
            self.ui_manager.draw_game_over(self.score)
            
        pygame.display.flip()
        
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.FPS)

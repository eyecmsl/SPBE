"""
UI Manager - Handles all user interface rendering
"""

import pygame

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Initialize fonts
        self.title_font = pygame.font.Font(None, 72)
        self.large_font = pygame.font.Font(None, 48)
        self.medium_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 100, 200)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.GRAY = (128, 128, 128)
        self.LIGHT_BLUE = (173, 216, 230)
        
    def draw_text_centered(self, text, font, color, y_pos):
        """Draw text centered horizontally on screen"""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.screen_width // 2
        text_rect.y = y_pos
        self.screen.blit(text_surface, text_rect)
        return text_rect
        
    def draw_text(self, text, font, color, x, y):
        """Draw text at specific position"""
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
        return text_surface.get_rect(topleft=(x, y))
        
    def draw_menu(self):
        """Draw main menu screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Title
        self.draw_text_centered("SPELLING BEE", self.title_font, self.YELLOW, 150)
        self.draw_text_centered("Educational Typing Game", self.medium_font, self.WHITE, 230)
        
        # Instructions
        instructions = [
            "Listen to the word pronunciation and type it correctly!",
            "",
            "Controls:",
            "• SPACE - Replay word pronunciation",
            "• ENTER - Submit answer",
            "• BACKSPACE - Delete character",
            "",
            "You have 3 lives. Good luck!",
            "",
            "Press SPACE to start playing"
        ]
        
        y_pos = 320
        for instruction in instructions:
            if instruction:
                self.draw_text_centered(instruction, self.small_font, self.WHITE, y_pos)
            y_pos += 30
            
    def draw_game_ui(self, score, lives, user_input, current_word, feedback_message, feedback_color, time_remaining=None, difficulty_level=1, hint_text=""):
        """Draw game playing UI"""
        # Score and lives display
        score_text = f"Score: {score}"
        lives_text = f"Lives: {lives}"
        
        self.draw_text(score_text, self.medium_font, self.WHITE, 20, 20)
        self.draw_text(lives_text, self.medium_font, self.WHITE, self.screen_width - 150, 20)
        
        # Draw hearts for lives
        heart_x = self.screen_width - 100
        for i in range(3):
            color = self.RED if i < lives else self.GRAY
            pygame.draw.circle(self.screen, color, (heart_x + i * 25, 35), 8)
            
        # Draw difficulty level
        difficulty_names = {1: "Easy", 2: "Basic", 3: "Intermediate", 4: "Advanced", 5: "Expert"}
        difficulty_text = f"Level: {difficulty_names.get(difficulty_level, 'Unknown')}"
        self.draw_text(difficulty_text, self.small_font, self.YELLOW, 20, 60)
        
        # Draw timer if provided
        if time_remaining is not None:
            time_color = self.RED if time_remaining <= 5 else self.WHITE
            time_text = f"Time: {int(time_remaining)}s"
            self.draw_text(time_text, self.medium_font, time_color, self.screen_width - 150, 60)
            
        # Instructions
        instruction_text = "Listen and type the word you hear (SPACE to replay, H for hint)"
        self.draw_text_centered(instruction_text, self.small_font, self.LIGHT_BLUE, 100)
        
        # Show hint if available
        if hint_text:
            self.draw_text_centered(hint_text, self.small_font, self.YELLOW, 120)
        
        # User input display
        input_bg_rect = pygame.Rect(self.screen_width // 2 - 200, 200, 400, 60)
        pygame.draw.rect(self.screen, self.WHITE, input_bg_rect)
        pygame.draw.rect(self.screen, self.BLACK, input_bg_rect, 3)
        
        # Display user input with cursor
        display_text = user_input + "|"
        input_surface = self.large_font.render(display_text, True, self.BLACK)
        input_rect = input_surface.get_rect()
        input_rect.center = input_bg_rect.center
        self.screen.blit(input_surface, input_rect)
        
        # Show current word if revealed
        if current_word:
            word_text = f"Word: {current_word}"
            self.draw_text_centered(word_text, self.medium_font, self.BLUE, 280)
            
        # Feedback message
        if feedback_message:
            self.draw_text_centered(feedback_message, self.medium_font, feedback_color, 350)
            
        # Controls reminder
        controls_text = "ENTER to submit • SPACE to replay • BACKSPACE to delete"
        self.draw_text_centered(controls_text, self.small_font, self.GRAY, self.screen_height - 50)
        
    def draw_game_over(self, final_score, words_attempted=0, words_correct=0, accuracy=0, avg_response_time=0, session_time=0):
        """Draw game over screen with performance statistics"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        self.draw_text_centered("GAME OVER", self.title_font, self.RED, 120)
        
        # Final score
        score_text = f"Final Score: {final_score}"
        self.draw_text_centered(score_text, self.large_font, self.WHITE, 180)
        
        # Performance statistics
        y_pos = 230
        stats = [
            f"Words Attempted: {words_attempted}",
            f"Words Correct: {words_correct}",
            f"Accuracy: {accuracy:.1f}%",
            f"Average Response Time: {avg_response_time:.1f}s",
            f"Session Duration: {session_time/60:.1f} minutes"
        ]
        
        for stat in stats:
            self.draw_text_centered(stat, self.medium_font, self.LIGHT_BLUE, y_pos)
            y_pos += 35
        
        # Performance message based on accuracy and score
        if accuracy >= 90 and final_score >= 300:
            message = "Outstanding! You're a true Spelling Bee master!"
        elif accuracy >= 75 and final_score >= 200:
            message = "Excellent work! You're becoming a spelling champion!"
        elif accuracy >= 60 and final_score >= 100:
            message = "Well done! You're improving your vocabulary!"
        elif accuracy >= 40:
            message = "Good effort! Keep practicing to improve!"
        else:
            message = "Keep practicing! You're learning and getting better!"
            
        self.draw_text_centered(message, self.medium_font, self.YELLOW, y_pos + 20)
        
        # Educational value summary
        educational_text = "Educational Benefits Achieved:"
        self.draw_text_centered(educational_text, self.small_font, self.WHITE, y_pos + 70)
        
        benefits = []
        if words_correct > 5:
            benefits.append("✓ Vocabulary Expansion")
        if accuracy > 50:
            benefits.append("✓ Spelling Improvement")
        if avg_response_time < 10:
            benefits.append("✓ Quick Word Recognition")
        if session_time > 60:
            benefits.append("✓ Sustained Learning Focus")
            
        benefit_y = y_pos + 100
        for benefit in benefits:
            self.draw_text_centered(benefit, self.small_font, self.GREEN, benefit_y)
            benefit_y += 25
        
        # Restart instruction
        self.draw_text_centered("Press SPACE to play again", self.medium_font, self.WHITE, self.screen_height - 80)

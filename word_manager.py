"""
Word Manager - Handles word selection and difficulty progression
"""

import random
from words import WORD_LISTS

class WordManager:
    def __init__(self):
        self.used_words = set()
        self.difficulty_level = 1
        
    def get_difficulty_level(self, score):
        """Calculate difficulty level based on score"""
        if score < 50:
            return 1  # Easy
        elif score < 150:
            return 2  # Basic
        elif score < 300:
            return 3  # Intermediate
        elif score < 500:
            return 4  # Advanced
        else:
            return 5  # Expert
            
    def get_difficulty_multiplier(self, score):
        """Get score multiplier based on difficulty"""
        level = self.get_difficulty_level(score)
        multipliers = {1: 1, 2: 1.2, 3: 1.5, 4: 2.0, 5: 2.5}
        return multipliers.get(level, 1)
        
    def get_next_word(self, score):
        """Get next word based on current score/difficulty"""
        level = self.get_difficulty_level(score)
        self.difficulty_level = level
        
        # Get word list for current difficulty
        if level == 1:
            word_list = WORD_LISTS['easy']
        elif level == 2:
            word_list = WORD_LISTS['basic']
        elif level == 3:
            word_list = WORD_LISTS['intermediate']
        elif level == 4:
            word_list = WORD_LISTS['advanced']
        else:
            word_list = WORD_LISTS['expert']
            
        # Find unused words in current difficulty
        available_words = [word for word in word_list if word not in self.used_words]
        
        # If all words used, reset used words for this level
        if not available_words:
            self.used_words = set()
            available_words = word_list
            
        # Select random word
        word = random.choice(available_words)
        self.used_words.add(word)
        
        return word
        
    def reset(self):
        """Reset word manager for new game"""
        self.used_words = set()
        self.difficulty_level = 1

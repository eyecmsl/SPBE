#!/usr/bin/env python3
"""
Spelling Bee Game - Main Entry Point
Educational word pronunciation typing game with progressive difficulty
"""

import pygame
import sys
import os
from game import SpellingBeeGame

def main():
    """Initialize pygame and start the game"""
    try:
        # Initialize pygame
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Create and run the game
        game = SpellingBeeGame()
        game.run()
        
    except Exception as e:
        print(f"Error starting game: {e}")
        sys.exit(1)
    finally:
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()

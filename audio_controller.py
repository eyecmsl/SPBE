"""
Audio Controller - Handles all sound effects and word pronunciations
"""

import pygame
import os
import random
from pygame import mixer
import numpy as np

class AudioController:
    def __init__(self):
        # Check if audio is available
        self.audio_available = pygame.mixer.get_init() is not None
        
        # Sound effects
        self.sounds = {}
        if self.audio_available:
            self.load_sound_effects()
        
        # Volume settings
        self.sfx_volume = 0.7
        self.voice_volume = 0.8
        
        # TTS voice settings for word pronunciation
        self.setup_tts()
        
    def load_sound_effects(self):
        """Load sound effect files"""
        sound_files = {
            'correct': 'assets/sounds/correct.wav',
            'incorrect': 'assets/sounds/incorrect.wav',
            'death': 'assets/sounds/death.wav'
        }
        
        for name, file_path in sound_files.items():
            try:
                if os.path.exists(file_path):
                    sound = pygame.mixer.Sound(file_path)
                    sound.set_volume(self.sfx_volume)
                    self.sounds[name] = sound
                else:
                    # Create placeholder sound if file doesn't exist
                    self.sounds[name] = self.create_placeholder_sound(name)
            except pygame.error as e:
                print(f"Could not load sound {name}: {e}")
                self.sounds[name] = self.create_placeholder_sound(name)
                
    def create_placeholder_sound(self, sound_type):
        """Create simple placeholder sounds using pygame"""
        if not self.audio_available:
            return None
            
        # Create a simple tone based on sound type
        sample_rate = 22050
        duration = 0.3
        
        if sound_type == 'correct':
            # High pitched success tone
            frequency = 800
        elif sound_type == 'incorrect':
            # Lower pitched error tone
            frequency = 200
        else:  # death
            # Very low dramatic tone
            frequency = 100
            duration = 0.8
        
        try:    
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                time = float(i) / sample_rate
                wave = 4096 * (0.5 * (1 + pygame.math.Vector2(1, 0).rotate(360 * frequency * time).x))
                arr.append([int(wave), int(wave)])
                
            sound = pygame.sndarray.make_sound(np.array(arr, dtype=np.int16))
            sound.set_volume(self.sfx_volume)
            return sound
        except:
            return None
        
    def setup_tts(self):
        """Setup text-to-speech for word pronunciation"""
        try:
            # Try to import pyttsx3 for offline TTS
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 120)  # Slower speech rate
            self.tts_engine.setProperty('volume', self.voice_volume)
            self.has_tts = True
        except (ImportError, RuntimeError) as e:
            print(f"TTS not available: {e}")
            print("Using visual-only mode")
            self.has_tts = False
            
    def play_word_pronunciation(self, word):
        """Play pronunciation of given word"""
        if self.has_tts:
            try:
                # Use TTS engine to speak the word
                self.tts_engine.say(word)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS error: {e}")
                self.play_fallback_pronunciation(word)
        else:
            self.play_fallback_pronunciation(word)
            
    def play_fallback_pronunciation(self, word):
        """Fallback pronunciation using simple audio cues"""
        # Create a simple audio pattern based on word length and characteristics
        for i, char in enumerate(word.lower()):
            if char.isalpha():
                # Create different tones for different letters
                frequency = 400 + (ord(char) - ord('a')) * 20
                self.play_tone(frequency, 0.1)
                pygame.time.wait(50)
                
    def play_tone(self, frequency, duration):
        """Play a tone at specified frequency and duration"""
        if not self.audio_available:
            return
            
        try:
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                time = float(i) / sample_rate
                wave = 2048 * (0.5 * (1 + pygame.math.Vector2(1, 0).rotate(360 * frequency * time).x))
                arr.append([int(wave), int(wave)])
                
            sound = pygame.sndarray.make_sound(np.array(arr, dtype=np.int16))
            sound.set_volume(0.3)
            sound.play()
        except:
            pass
        
    def play_correct_sound(self):
        """Play correct answer sound"""
        if self.audio_available and 'correct' in self.sounds and self.sounds['correct']:
            self.sounds['correct'].play()
            
    def play_incorrect_sound(self):
        """Play incorrect answer sound"""
        if self.audio_available and 'incorrect' in self.sounds and self.sounds['incorrect']:
            self.sounds['incorrect'].play()
            
    def play_death_sound(self):
        """Play game over sound"""
        if self.audio_available and 'death' in self.sounds and self.sounds['death']:
            self.sounds['death'].play()

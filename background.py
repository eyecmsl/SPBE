"""
Parallax Background - 2.5D scrolling background with multiple layers
"""

import pygame
import math

class ParallaxBackground:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Background layers with different scroll speeds
        self.layers = []
        self.scroll_speeds = [0.5, 1.0, 1.5]  # Sky, mountains, ground
        self.scroll_offset = 0
        
        # Colors for generated backgrounds
        self.sky_color = (135, 206, 250)  # Sky blue
        self.mountain_color = (139, 69, 19)  # Saddle brown
        self.ground_color = (34, 139, 34)  # Forest green
        
        # Initialize background layers
        self.create_background_layers()
        
    def create_background_layers(self):
        """Create parallax background layers"""
        # Sky layer (gradient)
        sky_surface = pygame.Surface((self.screen_width * 2, self.screen_height))
        self.create_sky_gradient(sky_surface)
        self.layers.append({
            'surface': sky_surface,
            'speed': self.scroll_speeds[0],
            'y': 0
        })
        
        # Mountains layer
        mountain_surface = pygame.Surface((self.screen_width * 2, self.screen_height))
        mountain_surface.set_colorkey((0, 0, 0))  # Make black transparent
        self.create_mountains(mountain_surface)
        self.layers.append({
            'surface': mountain_surface,
            'speed': self.scroll_speeds[1],
            'y': 0
        })
        
        # Ground layer
        ground_surface = pygame.Surface((self.screen_width * 2, self.screen_height))
        ground_surface.set_colorkey((0, 0, 0))  # Make black transparent
        self.create_ground(ground_surface)
        self.layers.append({
            'surface': ground_surface,
            'speed': self.scroll_speeds[2],
            'y': 0
        })
        
    def create_sky_gradient(self, surface):
        """Create sky gradient background"""
        width, height = surface.get_size()
        
        # Create vertical gradient from light blue to white
        for y in range(height):
            ratio = y / height
            # Interpolate between sky blue and white
            r = int(self.sky_color[0] + (255 - self.sky_color[0]) * ratio * 0.3)
            g = int(self.sky_color[1] + (255 - self.sky_color[1]) * ratio * 0.3)
            b = int(self.sky_color[2] + (255 - self.sky_color[2]) * ratio * 0.3)
            
            pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
            
        # Add some clouds
        self.add_clouds(surface)
        
    def add_clouds(self, surface):
        """Add simple cloud shapes to sky"""
        width, height = surface.get_size()
        cloud_color = (255, 255, 255, 180)  # Semi-transparent white
        
        # Create several cloud groups
        cloud_positions = [
            (width * 0.2, height * 0.2),
            (width * 0.6, height * 0.15),
            (width * 0.8, height * 0.25),
            (width * 1.3, height * 0.18),
            (width * 1.7, height * 0.22)
        ]
        
        for x, y in cloud_positions:
            # Draw multiple circles to form cloud shape
            for i in range(5):
                radius = 20 + i * 5
                offset_x = (i - 2) * 15
                offset_y = (i % 2) * 10
                pygame.draw.circle(surface, (255, 255, 255), 
                                 (int(x + offset_x), int(y + offset_y)), radius)
                                 
    def create_mountains(self, surface):
        """Create mountain silhouettes"""
        width, height = surface.get_size()
        
        # Mountain peaks
        mountain_points = []
        
        # Generate mountain profile
        for x in range(0, width, 10):
            # Create mountain-like profile using sine waves
            base_height = height * 0.7
            peak_height = height * 0.3 + 50 * math.sin(x * 0.003) + 30 * math.sin(x * 0.007)
            y = base_height - peak_height
            mountain_points.append((x, max(int(y), height // 3)))
            
        # Close the polygon
        mountain_points.append((width, height))
        mountain_points.append((0, height))
        
        # Draw mountains
        pygame.draw.polygon(surface, self.mountain_color, mountain_points)
        
        # Add mountain details with darker color
        dark_mountain = (
            max(0, self.mountain_color[0] - 40),
            max(0, self.mountain_color[1] - 40),
            max(0, self.mountain_color[2] - 40)
        )
        
        # Draw some peaks in darker color for depth
        for i in range(3):
            offset = width * (0.3 + i * 0.3)
            peak_points = []
            for x in range(int(offset), int(offset + width * 0.4), 15):
                if x < width:
                    base_height = height * 0.8
                    peak_height = height * 0.2 + 30 * math.sin((x - offset) * 0.01)
                    y = base_height - peak_height
                    peak_points.append((x, max(int(y), height // 2)))
                    
            if len(peak_points) > 2:
                peak_points.append((peak_points[-1][0], height))
                peak_points.append((peak_points[0][0], height))
                pygame.draw.polygon(surface, dark_mountain, peak_points)
                
    def create_ground(self, surface):
        """Create ground layer with hills"""
        width, height = surface.get_size()
        
        # Ground base
        ground_y = height * 0.8
        pygame.draw.rect(surface, self.ground_color, 
                        (0, int(ground_y), width, int(height - ground_y)))
        
        # Add rolling hills
        hill_points = [(0, int(ground_y))]
        
        for x in range(0, width, 20):
            hill_height = 30 * math.sin(x * 0.01) + 20 * math.sin(x * 0.02)
            y = ground_y - hill_height
            hill_points.append((x, int(y)))
            
        hill_points.append((width, int(ground_y)))
        hill_points.append((width, height))
        hill_points.append((0, height))
        
        pygame.draw.polygon(surface, self.ground_color, hill_points)
        
        # Add some trees/vegetation
        self.add_vegetation(surface, ground_y)
        
    def add_vegetation(self, surface, ground_y):
        """Add simple trees and vegetation"""
        width = surface.get_width()
        tree_color = (0, 100, 0)  # Dark green
        trunk_color = (101, 67, 33)  # Brown
        
        # Add trees at various positions
        tree_positions = [
            width * 0.1, width * 0.25, width * 0.4, width * 0.55, 
            width * 0.7, width * 0.85, width * 1.2, width * 1.4, 
            width * 1.6, width * 1.8
        ]
        
        for tree_x in tree_positions:
            if tree_x < width:
                # Tree trunk
                trunk_width = 8
                trunk_height = 40
                pygame.draw.rect(surface, trunk_color,
                               (int(tree_x - trunk_width/2), int(ground_y - trunk_height),
                                trunk_width, trunk_height))
                
                # Tree foliage (simple circle)
                foliage_radius = 25
                pygame.draw.circle(surface, tree_color,
                                 (int(tree_x), int(ground_y - trunk_height - 10)),
                                 foliage_radius)
                                 
    def update(self):
        """Update background animation"""
        self.scroll_offset += 0.5  # Slow scroll speed
        
        # Reset offset when it gets too large
        if self.scroll_offset > self.screen_width:
            self.scroll_offset = 0
            
    def draw(self):
        """Draw all background layers with parallax effect"""
        for layer in self.layers:
            # Calculate layer offset based on scroll speed
            layer_offset = (self.scroll_offset * layer['speed']) % layer['surface'].get_width()
            
            # Draw layer twice to create seamless scrolling
            self.screen.blit(layer['surface'], 
                           (-layer_offset, layer['y']))
            self.screen.blit(layer['surface'], 
                           (layer['surface'].get_width() - layer_offset, layer['y']))

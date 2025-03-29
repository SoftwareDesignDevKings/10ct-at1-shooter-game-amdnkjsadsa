import pygame
import app
import math

class Enemy:
    def __init__(self, x, y, enemy_type, enemy_assets, speed=app.DEFAULT_ENEMY_SPEED):
        # Define attributes for X and Y
        self.x = x
        self.y = y

        # Define an attribute for movement speed
        self.speed = speed

        # Load animation frames
        self.frames = enemy_assets[enemy_type]
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 8
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        # Define an attribute for enemy type
        self.enemy_type = enemy_type 

        # Track if enemy is facing left
        self.facing_left = False

        # Define knockback properties
        self.knockback_dist_remaining = 0
        self.knockback_dx = 0
        self.knockback_dy = 0

    def update(self, player):
        # Check if knockback is active and call apply_knockback()
        if self.knockback_dist_remaining > 0:
            self.apply_knockback()
        else:
            self.move_toward_player(player) # If no knockback, move toward the player

        # Call animate() to update enemy sprite animation
        self.animate()
        
    def move_toward_player(self, player):
        # Calculates direction vector toward player
        dx = player.x - self.x
        dy = player.y - self.y
        dist = (dx**2 + dy**2) ** 0.5
        
        if dist != 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        
        self.facing_left = dx < 0
        
        # Updates enemy position
        self.rect.center = (self.x, self.y)
        pass

    def apply_knockback(self):
        step = min(app.ENEMY_KNOCKBACK_SPEED, self.knockback_dist_remaining)
        self.knockback_dist_remaining -= step

        # Apply knockback effect to enemy position 
        # Hint: apply the dx, dy attributes
        self.x += self.knockback_dx * step
        self.y += self.knockback_dy * step

        # Update facing direction based on knockback direction
        if self.knockback_dx < 0:
            self.facing_left = True
        else:
            self.facing_left = False

        self.rect.center = (self.x, self.y)

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            center = self.rect.center
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = center
        pass

    def draw(self, surface):
        # Flip the sprite if facing left
        """if not self.game_over:
            self.player.draw(self.screen)""" 

        if self.facing_left:
            flipped_image = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_image, self.rect)
        else:
            surface.blit(self.image, self.rect)

        # Draw enemy sprite on the given surface
        
    def set_knockback(self, px, py, dist):
        dx = self.x - px
        dy = self.y - py
        length = math.sqrt(dx*dx + dy*dy)
        if length != 0:
            self.knockback_dx = dx / length
            self.knockback_dy = dy / length
            self.knockback_dist_remaining = dist
        pass
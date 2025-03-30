import pygame
import app
import math

class Enemy:
    def __init__(self, x, y, enemy_type, enemy_assets, speed=app.DEFAULT_ENEMY_SPEED):
        # define the x and y position of the enemy
        self.x = x
        self.y = y

        # define the speed at which the enemy moves
        self.speed = speed

        # load the animation frames for the enemy
        self.frames = enemy_assets[enemy_type]
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 8
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # define the enemy type
        self.enemy_type = enemy_type

        # track if the enemy is facing left
        self.facing_left = False

        # define knockback properties for when the enemy is pushed back
        self.knockback_dist_remaining = 0
        self.knockback_dx = 0
        self.knockback_dy = 0

    def update(self, player):
        # check if knockback is active and apply knockback if so
        if self.knockback_dist_remaining > 0:
            self.apply_knockback()
        else:
            self.move_toward_player(player)  # if no knockback, move towards the player

        # update the enemy's sprite animation
        self.animate()

    def move_toward_player(self, player):
        # calculate the direction vector towards the player
        dx = player.x - self.x
        dy = player.y - self.y
        dist = (dx**2 + dy**2) ** 0.5

        if dist != 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

        # set the facing direction based on whether the x direction is negative
        self.facing_left = dx < 0

        # update the enemy's position on the screen
        self.rect.center = (self.x, self.y)
        pass

    def apply_knockback(self):
        # apply knockback to the enemy, moving it by a small amount
        step = min(app.ENEMY_KNOCKBACK_SPEED, self.knockback_dist_remaining)
        self.knockback_dist_remaining -= step

        # apply the knockback effect to the enemy's position
        self.x += self.knockback_dx * step
        self.y += self.knockback_dy * step

        # update the facing direction based on the knockback direction
        if self.knockback_dx < 0:
            self.facing_left = True
        else:
            self.facing_left = False

        # update the enemy's rectangle after knockback
        self.rect.center = (self.x, self.y)

    def animate(self):
        # increment the animation timer and change the frame when it's time
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
        # flip the sprite if facing left
        if self.facing_left:
            flipped_image = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_image, self.rect)
        else:
            surface.blit(self.image, self.rect)

        # draw the enemy sprite on the given surface

    def set_knockback(self, px, py, dist):
        # calculate the knockback direction based on the player position
        dx = self.x - px
        dy = self.y - py
        length = math.sqrt(dx * dx + dy * dy)
        if length != 0:
            self.knockback_dx = dx / length
            self.knockback_dy = dy / length
            self.knockback_dist_remaining = dist
        pass
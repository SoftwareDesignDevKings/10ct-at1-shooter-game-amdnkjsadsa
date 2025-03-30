import app
import pygame

class Bullet:
    def __init__(self, x, y, vx, vy, size):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size

        # create a bullet image with the specified size
        self.image = app.pygame.Surface((self.size, self.size), app.pygame.SRCALPHA)
        self.image.fill((255, 255, 255))  # fill with white colour
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        # update the bullet's position based on its velocity
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        # draw the bullet image on the given surface
        surface.blit(self.image, self.rect)

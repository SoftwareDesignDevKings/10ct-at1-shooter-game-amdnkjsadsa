import app

class Coin:
    def __init__(self, x, y):
        # initialising the coin's position with the given x, y coordinates
        self.x = x
        self.y = y
        
        # creating a transparent surface for the coin image with a size of 15x15 pixels
        self.image = app.pygame.Surface((15, 15), app.pygame.SRCALPHA)
        
        # filling the surface with a golden colour (rgb: 255, 215, 0)
        self.image.fill((255, 215, 0))
        
        # creating a rectangle for positioning the coin on screen, centred at (x, y)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, surface):
        # drawing the coin's image on the given surface (typically the screen)
        surface.blit(self.image, self.rect)
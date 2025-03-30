import app

class Powerup:
    def __init__(self, x, y, powerup_type):
        # define initial position of the powerup
        self.x = x
        self.y = y
        
        # create an image for the powerup with transparent background
        self.image = app.pygame.Surface((15, 15), app.pygame.SRCALPHA)
        
        # make the powerups different colours depending on the buff it gives
        if powerup_type == "speed_boost": 
            self.image.fill((0, 255, 0))  # green for speed boost
        elif powerup_type == "speed_up_bullets":     
            self.image.fill((0, 0, 255))  # blue for speeding up bullets
        else:                             # more bullets
            self.image.fill((255, 0, 0)) # red for more bullets powerup
        
        # create a rect to track the powerup's position
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, surface):
        # draw the powerup image on the given surface
        surface.blit(self.image, self.rect)
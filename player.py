import math
import pygame
import app  # contains global settings like WIDTH, HEIGHT, PLAYER_SPEED, etc.
from bullet import Bullet

class Player:
    def __init__(self, x, y, assets):
        """initialise the player with position and image assets."""
        # store the player's x and y position on the screen
        self.x = x
        self.y = y

        # set the player's speed using a global setting from the app module
        self.speed = app.PLAYER_SPEED
        # load player animations from the provided assets
        self.animations = assets["player"]
        # set the player's initial state to idle (not moving)
        self.state = "idle"
        # initialise the frame index for animation (starts at first frame)
        self.frame_index = 0
        # initialise the animation timer to control animation speed
        self.animation_timer = 0
        # set the animation speed (frame rate)
        self.animation_speed = 8

        # initialise experience points to 0
        self.xp = 0
        # set the player's starting health
        self.health = 5

        # set bullet speed and size
        self.bullet_speed = 10
        self.bullet_size = 10
        # start with 1 bullet per shot
        self.bullet_count = 1
        # set shooting cooldown time
        self.shoot_cooldown = 20
        # initialise the shoot timer to 0
        self.shoot_timer = 0
        # initialise the list to store bullets
        self.bullets = []

        # set the player's image to the first frame of the idle animation
        self.image = self.animations[self.state][self.frame_index]
        # create a collision rectangle based on the player's image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # assume the player is facing right by default
        self.facing_left = False

    def handle_input(self):
        """check and respond to keyboard/mouse input."""
        # get all keys currently pressed on the keyboard
        keys = pygame.key.get_pressed()

        # initialise velocity in both x and y directions to 0
        vel_x, vel_y = 0, 0

        # check for movement inputs (arrow keys) and update velocity
        if keys[pygame.K_LEFT]:
            vel_x -= self.speed  # move left
        if keys[pygame.K_RIGHT]:
            vel_x += self.speed  # move right
        if keys[pygame.K_UP]:
            vel_y -= self.speed  # move up
        if keys[pygame.K_DOWN]:
            vel_y += self.speed  # move down

        # update the player's x and y position based on velocity
        self.x += vel_x
        self.y += vel_y

        # clamp the player's position to stay within screen bounds
        self.x = max(0, min(self.x, app.WIDTH))
        self.y = max(0, min(self.y, app.HEIGHT))
        # update the collision rectangle with the new position
        self.rect.center = (self.x, self.y)

        # determine the player's animation state based on movement
        if vel_x != 0 or vel_y != 0:
            self.state = "run"  # set to 'run' if moving
        else:
            self.state = "idle"  # set to 'idle' if not moving

        # determine which direction the player is facing
        if vel_x < 0:
            self.facing_left = True  # facing left if moving left
        elif vel_x > 0:
            self.facing_left = False  # facing right if moving right

    def shoot_toward_position(self, tx, ty):
        """shoot towards a specific position."""
        # check if the shoot cooldown has passed
        if self.shoot_timer >= self.shoot_cooldown:
            return  # prevent shooting if cooldown hasn't passed

        # calculate the difference in x and y between the target and player
        dx = tx - self.x
        dy = ty - self.y
        # calculate the distance to the target
        dist = math.sqrt(dx**2 + dy**2)
        if dist == 0:
            return  # do nothing if distance is zero (player and target at the same position)

        # calculate the velocity of the bullet in the x and y directions
        vx = (dx / dist) * self.bullet_speed
        vy = (dy / dist) * self.bullet_speed

        # set the spread angle for multiple bullets
        angle_spread = 10
        base_angle = math.atan2(vy, vx)  # calculate the base angle of the bullet
        mid = (self.bullet_count - 1) / 2  # find the middle bullet if firing multiple bullets

        # loop to fire multiple bullets if bullet_count > 1
        for i in range(self.bullet_count):
            offset = i - mid  # calculate the offset for each bullet
            spread_radians = math.radians(angle_spread * offset)  # convert spread angle to radians
            angle = base_angle + spread_radians  # adjust the bullet's angle

            # calculate the final x and y velocities after applying spread
            final_vx = math.cos(angle) * self.bullet_speed
            final_vy = math.sin(angle) * self.bullet_speed

            # create a new bullet with the calculated velocity and size
            bullet = Bullet(self.x, self.y, final_vx, final_vy, self.bullet_size)
            # add the bullet to the list of bullets
            self.bullets.append(bullet)
        # reset the shoot timer after shooting
        self.shoot_timer = 0

    def shoot_toward_mouse(self, pos):
        """shoot towards the mouse position."""
        mx, my = pos  # get the mouse position
        # call shoot_toward_position with the mouse position
        self.shoot_toward_position(mx, my)

    def shoot_toward_enemy(self, enemy):
        """shoot towards the enemy's position."""
        # call shoot_toward_position with the enemy's position
        self.shoot_toward_position(enemy.x, enemy.y)

    def update(self):
        """update player state."""
        # update each bullet in the bullets list
        for bullet in self.bullets:
            bullet.update()  # update the bullet's position
            # remove the bullet if it goes off-screen
            if bullet.y < 0 or bullet.y > app.HEIGHT or bullet.x < 0 or bullet.x > app.WIDTH:
                self.bullets.remove(bullet)

        # increment the animation timer
        self.animation_timer += 1
        # check if it's time to update the animation frame
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0  # reset the timer
            frames = self.animations[self.state]  # get the frames for the current state
            self.frame_index = (self.frame_index + 1) % len(frames)  # cycle through animation frames
            # set the current frame as the player's image
            self.image = frames[self.frame_index]
            # update the collision rectangle to match the new image
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center

    def draw(self, surface):
        """draw the player on the screen."""
        # flip the player's image if facing left
        if self.facing_left:
            flipped_img = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_img, self.rect)  # draw the flipped image
        else:
            surface.blit(self.image, self.rect)  # draw the normal image

        # draw all the bullets on the screen
        for bullet in self.bullets:
            bullet.draw(surface)

    def take_damage(self, amount):
        """reduce the player's health by a given amount, not going below zero."""
        # reduce health but ensure it doesn't go below zero
        self.health = max(0, self.health - amount)
    
    def add_xp(self, amount):
        """add experience points to the player."""
        self.xp += amount

    def increase_speed(self, amount):
        """increase the player's speed."""
        self.speed = amount
    
    def speed_up_bullets(self, amount):
        """increase the speed of the bullets."""
        self.bullet_speed += amount
    
    def increase_bullet_count(self, amount):
        """increase the number of bullets per shot."""
        self.bullet_count += amount
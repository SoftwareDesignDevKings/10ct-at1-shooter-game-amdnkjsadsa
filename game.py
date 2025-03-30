# FINAL SUBMISSION OF MY AT1 ASSESSMENT

import math
import pygame
import random
import os

import app
from coin import Coin
from enemy import Enemy
from player import Player
from powerup import Powerup

class Game:
    def __init__(self):
        """initialise the game, set up screen, clock, and assets."""
        pygame.init()
        # set up the game window with the specified width and height from app settings
        self.screen = pygame.display.set_mode((app.WIDTH, app.HEIGHT))
        # set the title of the game window
        pygame.display.set_caption("Shooter")
        # create a clock to manage the game's frame rate
        self.clock = pygame.time.Clock()

        # load the game assets (images, sounds, etc.)
        self.assets = app.load_assets()

        # set up fonts for text rendering
        font_path = os.path.join("assets", "PressStart2P.ttf")
        self.font_small = pygame.font.Font(font_path, 18)
        self.font_large = pygame.font.Font(font_path, 32)

        # create a random background using the floor tiles from the assets
        self.background = self.create_random_background(
            app.WIDTH, app.HEIGHT, self.assets["floor_tiles"]
        )

        # initial game state: running and not over
        self.running = True
        self.game_over = False

        # initialise coins and powerups lists
        self.coins = []

        # initialise powerup variables
        self.powerups = []
        self.powerup_effect = ""

        # initialise sound effects
        self.coin_collection_sfx = pygame.mixer.Sound("assets/sfx/coin_collection.wav")
        self.powerup_collection_sfx = pygame.mixer.Sound("assets/sfx/powerup_collection.wav")
        self.enemy_death_sfx = pygame.mixer.Sound("assets/sfx/enemy_death.wav")
        self.player_death_sfx = pygame.mixer.Sound("assets/sfx/player_death.mp3")
        self.menu_click_sfx = pygame.mixer.Sound("assets/sfx/menu_click.wav")
        self.player_damaged_sfx = pygame.mixer.Sound("assets/sfx/player_damaged.wav")

        # initialise enemies and enemy spawn timer
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = 60
        self.enemies_per_spawn = 1

        # reset the game to its starting state
        self.reset_game()

    def reset_game(self):
        """reset the game to its initial state."""
        # create a new player at the centre of the screen
        self.player = Player(app.WIDTH // 2, app.HEIGHT // 2, self.assets)

        # reset coins, powerups, and enemies
        self.coins = []
        self.powerups = []
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.enemies_per_spawn = 1

        # set the game over flag to false
        self.game_over = False

        # stop the player death sound when restarting the game
        self.player_death_sfx.stop()

        # play a menu click sound when restarting the game
        self.menu_click_sfx.play()

    def create_random_background(self, width, height, floor_tiles):
        """create a random background using floor tiles."""
        bg = pygame.Surface((width, height))
        tile_w = floor_tiles[0].get_width()
        tile_h = floor_tiles[0].get_height()

        # tile the background using random floor tiles
        for y in range(0, height, tile_h):
            for x in range(0, width, tile_w):
                tile = random.choice(floor_tiles)
                bg.blit(tile, (x, y))

        return bg

    def run(self):
        """run the game loop."""
        while self.running:
            # set the frame rate for the game
            self.clock.tick(app.FPS)
            # handle events like key presses or window closing
            self.handle_events()

            if not self.game_over:
                # update game state if the game is not over
                self.update()

            # draw everything on the screen
            self.draw()

        # quit pygame when the game loop ends
        pygame.quit()

    def handle_events(self):
        """handle player input and game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # play a sound when the game window is closed
                self.menu_click_sfx.play()
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    # reset the game if the player presses R
                    if event.key == pygame.K_r:
                        self.reset_game()

                    # quit the game if the player presses ESC
                    elif event.key == pygame.K_ESCAPE:
                        self.menu_click_sfx.play()
                        self.running = False
                else:
                    # shoot towards nearest enemy if spacebar is pressed
                    if event.key == pygame.K_SPACE:
                        nearest_enemy = self.find_nearest_enemy()
                        if nearest_enemy:
                            self.player.shoot_toward_enemy(nearest_enemy)
                    # shoot towards mouse position if left mouse button is clicked
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.player.shoot_toward_mouse(event.pos)

    def find_nearest_enemy(self):
        """find the nearest enemy to the player."""
        if not self.enemies:
            return None
        nearest = None
        min_dist = float('inf')
        px, py = self.player.x, self.player.y

        # loop through all enemies and find the closest one
        for enemy in self.enemies:
            dist = math.sqrt((enemy.x - px)**2 + (enemy.y - py)**2)
            if dist < min_dist:
                min_dist = dist
                nearest = enemy
        return nearest

    def check_bullet_enemy_collisions(self):
        """check if any bullets hit enemies."""
        for bullet in self.player.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    # remove the bullet if it hits an enemy
                    self.player.bullets.remove(bullet)

                    # randomly spawn powerups on enemy death
                    n = random.randint(1, 10)
                    if n == 2:
                        powerup_types = ["speed_boost", "speed_up_bullets", "more_bullets"]
                        powerup_type = random.choice(powerup_types)
                        self.powerup_effect = powerup_type

                        # create and add the powerup to the list
                        powerup = Powerup(enemy.x + 5, enemy.y + 5, powerup_type)
                        self.powerups.append(powerup)

                    # play the enemy death sound
                    self.enemy_death_sfx.play()

                    # create and add a new coin to the list
                    new_coin = Coin(enemy.x, enemy.y)
                    self.coins.append(new_coin)

                    # remove the enemy from the game
                    self.enemies.remove(enemy)

    def spawn_enemies(self):
        """spawn new enemies at random positions on screen."""
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_interval:
            self.enemy_spawn_timer = 0

            # spawn multiple enemies at random locations
            for _ in range(self.enemies_per_spawn):
                side = random.choice(["top", "bottom", "left", "right"])
                if side == "top":
                    x = random.randint(0, app.WIDTH)
                    y = -app.SPAWN_MARGIN
                elif side == "bottom":
                    x = random.randint(0, app.WIDTH)
                    y = app.HEIGHT + app.SPAWN_MARGIN
                elif side == "left":
                    x = -app.SPAWN_MARGIN
                    y = random.randint(0, app.HEIGHT)
                else:
                    x = app.WIDTH + app.SPAWN_MARGIN
                    y = random.randint(0, app.HEIGHT)

                # randomly select an enemy type and create an enemy
                enemy_type = random.choice(list(self.assets["enemies"].keys()))
                enemy = Enemy(x, y, enemy_type, self.assets["enemies"])
                self.enemies.append(enemy)

    def check_player_enemy_collisions(self):
        """check if the player collides with any enemies."""
        collided = False
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                collided = True
                break

        if collided:
            # player takes damage when colliding with an enemy
            self.player.take_damage(1)

            # play sound effect when player is damaged
            self.player_damaged_sfx.play()

            # apply knockback effect to enemies based on player position
            px, py = self.player.x, self.player.y
            for enemy in self.enemies:
                enemy.set_knockback(px, py, app.PUSHBACK_DISTANCE)

    def draw_game_over_screen(self):
        """draw the game over screen."""
        # create a dark overlay
        overlay = pygame.Surface((app.WIDTH, app.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # render and draw "Game Over" text
        game_over_surf = self.font_large.render("GAME OVER!", True, (255, 0, 0))
        game_over_rect = game_over_surf.get_rect(center=(app.WIDTH // 2, app.HEIGHT // 2 - 50))
        self.screen.blit(game_over_surf, game_over_rect)

        # render and draw the restart or quit prompt
        prompt_surf = self.font_small.render("Press R to Play Again or ESC to Quit", True, (255, 255, 255))
        prompt_rect = prompt_surf.get_rect(center=(app.WIDTH // 2, app.HEIGHT // 2 + 20))
        self.screen.blit(prompt_surf, prompt_rect)

    def update(self):
        """update the game state every frame."""
        self.player.handle_input()
        self.player.update()
        self.check_player_enemy_collisions()
        self.check_bullet_enemy_collisions()
        self.check_player_coin_collisions()

        # check if player collects any powerups
        self.check_player_powerup_collisions()

        # update all enemies
        for enemy in self.enemies:
            enemy.update(self.player)

        # end the game if the player has no health left
        if self.player.health <= 0:
            self.game_over = True
            return

        # spawn new enemies if needed
        self.spawn_enemies()

    def check_player_coin_collisions(self):
        """check if the player collects any coins."""
        coins_collected = []
        for coin in self.coins:
            if coin.rect.colliderect(self.player.rect):
                coins_collected.append(coin)
                self.player.add_xp(1)

                # play sound when coin is collected
                self.coin_collection_sfx.play()

        for c in coins_collected:
            if c in self.coins:
                self.coins.remove(c)

    def check_player_powerup_collisions(self):
        """check if the player collects any powerups."""
        powerups_collected = []
        for powerup in self.powerups:
            if powerup.rect.colliderect(self.player.rect):
                powerups_collected.append(powerup)

                # play sound when powerup is collected
                self.powerup_collection_sfx.play()

                # apply the effect of the collected powerup
                if self.powerup_effect == "speed_boost":
                    self.player.increase_speed(10)
                elif self.powerup_effect == "speed_up_bullets":
                    self.player.speed_up_bullets(3)
                elif self.powerup_effect == "more_bullets":
                    self.player.increase_bullet_count(3)

        for p in powerups_collected:
            if p in self.powerups:
                self.powerups.remove(p)

    def draw(self):
        """draw everything to the screen."""
        self.screen.blit(self.background, (0, 0))

        # draw all coins, powerups, enemies, and player
        for coin in self.coins:
            coin.draw(self.screen)

        for powerup in self.powerups:
            powerup.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        if not self.game_over:
            self.player.draw(self.screen)

        if self.game_over:
            # play the player death sound when the game is over
            self.player_death_sfx.play()

            # draw the game over screen
            self.draw_game_over_screen()

        # display the player's health and XP
        hp = max(0, min(self.player.health, 5))
        health_img = self.assets["health"][hp]
        self.screen.blit(health_img, (10, 10))

        xp_text_surf = self.font_small.render(f"XP: {self.player.xp}", True, (255, 255, 255))
        self.screen.blit(xp_text_surf, (10, 70))

        pygame.display.flip()  # update the display
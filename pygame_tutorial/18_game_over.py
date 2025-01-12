import random
from enum import StrEnum
from typing import Final, Self

import pygame
from pygame import Surface

pygame.init()


class GameState(StrEnum):
    LIVE = "live"
    GAME_OVER = "game over"
    MENU = "menu"
    OPTIONS = "options"
    EXIT = "exit"


# Screen
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroid Game")
screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# Game
game_state: GameState = GameState.MENU

# Settings
FPS = 60
clock = pygame.time.Clock()
score = 0
background_y_shift = 0  # used for moving background
num_of_asteroids = 5
GAME_OVER_MAX_TIME = 3  # time is seconds
game_over_time = GAME_OVER_MAX_TIME

# Colors
dark_yellow = pygame.Color("#938f0c")

# Pictures
background_image = pygame.image.load("SpaceShooterRedux/Backgrounds/darkPurple.png")
image_width, image_height = background_image.get_size()

# Load sound
sound_laser1 = pygame.mixer.Sound("SpaceShooterRedux/Bonus/sfx_laser1.ogg")
sound_zap = pygame.mixer.Sound("SpaceShooterRedux/Bonus/sfx_zap.ogg")
sound_shield_down = pygame.mixer.Sound("SpaceShooterRedux/Bonus/sfx_shieldDown.ogg")

# Fonts
my_font = pygame.font.Font("SpaceShooterRedux/Bonus/kenvector_future.ttf", 30)
game_name_text = my_font.render("Asteroid Game", True, dark_yellow)
game_name_text_rect = game_name_text.get_rect(midtop=(SCREEN_WIDTH // 2, 10))


class Options:
    def __init__(self):
        self.menu_font = pygame.font.Font("SpaceShooterRedux/Bonus/kenvector_future.ttf", 50)
        self.menu_texts = [
            "Sound",
            "Menu",
        ]
        self.selected = 0
        self.sound_volume = 5  # 0-10
        self._set_volume()

        self.height = self.menu_font.render(f"Play", True, dark_yellow).get_rect().height

    def key_pushed(self, key) -> GameState | None:
        if self.menu_texts[self.selected] == "Menu":
            if key == pygame.K_SPACE or key == pygame.K_KP_ENTER or key == pygame.CONTROLLER_BUTTON_DPAD_LEFT:
                self.selected = 0
                return GameState.MENU

        if self.menu_texts[self.selected] == "Sound":
            if key == pygame.K_LEFT or key == pygame.K_a:
                self.sound_volume = max(self.sound_volume - 1, 0)
                self._set_volume()
            if key == pygame.K_RIGHT or key == pygame.K_d:
                self.sound_volume = min(self.sound_volume + 1, 10)
                self._set_volume()

        if key == pygame.K_UP or key == pygame.K_w:
            self.selected -= 1
        if key == pygame.K_DOWN or key == pygame.K_s:
            self.selected += 1
        self.selected %= len(self.menu_texts)

    def _set_volume(self):
        # pygame.mixer.music.set_volume(self.sound_volume/10)  # Does not work

        sound_laser1.set_volume(self.sound_volume / 10)
        sound_zap.set_volume(self.sound_volume / 10)
        sound_shield_down.set_volume(self.sound_volume / 10)

        sound_zap.play()

    def draw(self, screen: Surface):
        offset_y = 100
        start_y = SCREEN_HEIGHT // 2 - (self.height + offset_y) * len(self.menu_texts) // 2 + 50
        for i, text in enumerate(self.menu_texts):
            if text == "Sound":
                slider_text = "." * 11
                slider_text = slider_text[:self.sound_volume] + f"{self.sound_volume}0" + slider_text[
                                                                                          self.sound_volume + 1:]
                text += f" {slider_text}"

            if i == self.selected:
                rendered_text = self.menu_font.render(f"- {text} -", True, "white")
            else:
                rendered_text = self.menu_font.render(text, True, dark_yellow)

            rect = rendered_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + (self.height + offset_y) * i))
            screen.blit(rendered_text, rect)


class Menu:
    def __init__(self):
        self.menu_font = pygame.font.Font("SpaceShooterRedux/Bonus/kenvector_future.ttf", 50)
        self.menu_texts = [
            "Play",
            "Options",
            "Exit",
        ]
        self.selected = 0

        self.height = self.menu_font.render(f"Play", True, dark_yellow).get_rect().height

    def key_pushed(self, key) -> GameState | None:
        if key == pygame.K_SPACE or key == pygame.K_KP_ENTER or key == pygame.CONTROLLER_BUTTON_DPAD_LEFT:
            match self.menu_texts[self.selected]:
                case "Play":
                    return GameState.LIVE
                case "Options":
                    return GameState.OPTIONS
                case "Exit":
                    return GameState.EXIT

        if key == pygame.K_UP or key == pygame.K_w:
            self.selected -= 1
        if key == pygame.K_DOWN or key == pygame.K_s:
            self.selected += 1
        self.selected %= len(self.menu_texts)

    def draw(self, screen: Surface):
        offset_y = 100
        start_y = SCREEN_HEIGHT // 2 - (self.height + offset_y) * len(self.menu_texts) // 2 + 50
        for i, text in enumerate(self.menu_texts):
            if i == self.selected:
                rendered_text = self.menu_font.render(f"- {text} -", True, "white")
            else:
                rendered_text = self.menu_font.render(text, True, dark_yellow)

            rect = rendered_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + (self.height + offset_y) * i))
            screen.blit(rendered_text, rect)


class Laser:
    def __init__(self, pos, direction):
        image = pygame.image.load("SpaceShooterRedux/PNG/Lasers/laserRed03.png")
        angle = direction.angle_to(pygame.Vector2(0, -1))
        self.image_rotated = pygame.transform.rotate(image, angle)
        self.rect = self.image_rotated.get_rect(midbottom=pos)
        self.direction = direction.copy()
        self.speed = 6

    @property
    def velocity(self) -> pygame.Vector2:
        return self.direction * self.speed

    def move(self):
        self.rect.center += self.velocity

    def draw(self, screen: Surface):
        # pygame.draw.rect(screen, "red", self.rect, 1) # for debug
        rotated_img_size = pygame.Vector2(self.image_rotated.get_size())
        blit_pos = self.rect.center - rotated_img_size * 0.5
        screen.blit(self.image_rotated, blit_pos)

    def is_on_screen(self):
        return screen_rect.contains(self.rect)


class Ship:
    max_speed: Final[int] = 3
    rotation_speed: Final[int] = 2

    def __init__(self):
        self.image = pygame.image.load("SpaceShooterRedux/PNG/playerShip1_blue.png")
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.direction = pygame.Vector2(0, -1)
        self.speed = 0
        self.lives = 3

    @property
    def velocity(self) -> pygame.Vector2:
        return self.direction * self.speed

    def id_dead(self) -> bool:
        return self.lives <= 0

    def move(self, keys):
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed = min(self.speed + 1, self.max_speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed = max(self.speed - 1, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.rotate_ip(-self.rotation_speed)
            self.speed = max(self.speed - 0.2, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.rotate_ip(self.rotation_speed)
            self.speed = max(self.speed - 0.2, 0)

        self.rect.center += self.velocity
        self.speed = max(self.speed - 0.1, 0)
        self.rect.topleft = (self.rect.x % SCREEN_WIDTH, self.rect.y % SCREEN_HEIGHT)

    def draw(self, screen: Surface):
        # pygame.draw.rect(screen, "blue", self.rect, 1) # for debug
        angle = self.direction.angle_to(pygame.Vector2(0, -1))
        image_rotated = pygame.transform.rotozoom(self.image, angle, 1.0)
        rotated_img_size = pygame.Vector2(image_rotated.get_size())
        blit_pos = self.rect.center - rotated_img_size * 0.5
        screen.blit(image_rotated, blit_pos)

    def shoot(self) -> Laser:
        sound_laser1.play()
        return Laser(self.rect.center, self.direction)

    def check_collision(self, asteroids) -> bool:
        for asteroid in asteroids:
            if self.rect.colliderect(asteroid.rect):
                sound_shield_down.play()
                self.lives -= 1
                return True

        return False


class AsteroidSize(StrEnum):
    BIG = "big"
    MEDIUM = "medium"
    SMALL = "SMALL"


class Asteroid:
    def __init__(self, size: AsteroidSize = AsteroidSize.BIG):
        self.size = size
        if size == AsteroidSize.BIG:
            self.image = pygame.image.load("SpaceShooterRedux/PNG/Meteors/meteorBrown_big1.png")
        else:
            self.image = pygame.image.load("SpaceShooterRedux/PNG/Meteors/meteorBrown_small1.png")

        self.rect = self.image.get_rect()
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.speed_x = 0
        self.speed_y = 0
        self.to_delete = False

        if size == AsteroidSize.BIG:
            self.spawn()

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if not screen_rect.contains(self.rect):  # Asteroid is completely off the screen
            if self.size == AsteroidSize.BIG:
                self.spawn()
            else:
                self.to_delete = True

    def check_collision(self, lasers) -> tuple[int | None, list[Self] | None]:
        for i, laser in enumerate(lasers):
            if self.rect.colliderect(laser.rect):
                if self.size == AsteroidSize.BIG:
                    small_asteroids = [
                        Asteroid(AsteroidSize.SMALL),
                        Asteroid(AsteroidSize.SMALL),
                    ]
                    small_asteroids[0].rect.center = self.rect.center
                    small_asteroids[0].speed_x = self.speed_x + 1
                    small_asteroids[0].speed_y = self.speed_y - 1
                    small_asteroids[1].rect.center = self.rect.center
                    small_asteroids[1].speed_x = self.speed_x - 1
                    small_asteroids[1].speed_y = self.speed_y + 1
                    self.spawn()
                else:
                    self.to_delete = True
                    small_asteroids = []

                return i, small_asteroids

        return None, None

    def spawn(self):
        if random.choice([True, False]):
            self.rect.centerx = random.randint(0, SCREEN_WIDTH)
            self.rect.centery = random.choice([50 + self.height // 2, SCREEN_HEIGHT - self.height // 2])
        else:
            self.rect.centerx = random.choice([self.width // 2, SCREEN_WIDTH - self.width // 2])
            self.rect.centery = random.randint(50, SCREEN_HEIGHT)

        self.speed_x = random.choice([-3, -2, -1, 1, 2, 3])
        self.speed_y = random.choice([-3, -2, -1, 1, 2, 3])

    def draw(self, screen: Surface):
        screen.blit(self.image, self.rect)


# # # Init classes
asteroids = []
ship = Ship()
lasers: list[Laser] = []
options_menu = Options()
menu = Menu()
start_ticks = pygame.time.get_ticks()  # Just to be initialized

while game_state != GameState.EXIT:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = GameState.EXIT

        if game_state == GameState.MENU:
            if event.type == pygame.KEYDOWN:
                change = menu.key_pushed(event.key)
                if change is not None:
                    game_state = change
                    if game_state == GameState.LIVE:
                        # Init start of game
                        asteroids = [Asteroid() for x in range(num_of_asteroids)]
                        ship = Ship()
                        lasers: list[Laser] = []
                        score = 0

        if game_state == GameState.OPTIONS:
            if event.type == pygame.KEYDOWN:
                change = options_menu.key_pushed(event.key)
                if change is not None:
                    game_state = change

        if game_state == GameState.LIVE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lasers.append(ship.shoot())
                if event.key == pygame.K_ESCAPE:
                    game_state = GameState.MENU

    if game_state == GameState.LIVE:
        # # # Movement
        keys = pygame.key.get_pressed()
        ship.move(keys)

        for asteroid in asteroids:
            asteroid.move()

        for laser in lasers:
            laser.move()

        # # # Collision
        if ship.check_collision(asteroids):
            if ship.id_dead():
                start_ticks = pygame.time.get_ticks()  # starter tick
                game_state = GameState.GAME_OVER
                continue
            # TODO some reset state?
            asteroids = [Asteroid() for x in range(num_of_asteroids)]
            lasers = []

        new_asteroids = []
        for asteroid in asteroids:
            laser_idx, maybe_new_asteroids = asteroid.check_collision(lasers)
            if laser_idx is not None:
                del lasers[laser_idx]
                new_asteroids += maybe_new_asteroids
                score += 1

        asteroids = [asteroid for asteroid in asteroids if not asteroid.to_delete]
        asteroids += new_asteroids

    # RENDER YOUR GAME HERE

    # Background
    for x in range(0, SCREEN_WIDTH, image_width):
        for y in range(-image_height, SCREEN_HEIGHT, image_height):
            screen.blit(background_image, (x, y + background_y_shift))
    background_y_shift += 1
    background_y_shift %= image_height

    # Shapes
    pygame.draw.line(screen, dark_yellow, (0, 50), (SCREEN_WIDTH, 50), 2)
    screen.blit(game_name_text, game_name_text_rect)

    if game_state == GameState.LIVE:
        # Add pictures
        ship.draw(screen)
        for asteroid in asteroids:
            asteroid.draw(screen)
        for laser in lasers:
            laser.draw(screen)
        lasers = [laser for laser in lasers if laser.is_on_screen()]

        # Text
        score_text = my_font.render(f"Score: {score}", True, dark_yellow)
        score_text_rect = score_text.get_rect(topleft=(10, 10))
        lives_text = my_font.render(f"Lives: {ship.lives}", True, dark_yellow)
        lives_text_rect = score_text.get_rect(topleft=(SCREEN_WIDTH - 165, 10))

        screen.blit(score_text, score_text_rect)
        screen.blit(lives_text, lives_text_rect)
    if game_state == GameState.MENU:
        menu.draw(screen)
    if game_state == GameState.OPTIONS:
        options_menu.draw(screen)
    if game_state == GameState.GAME_OVER:
        font_over = pygame.font.Font("SpaceShooterRedux/Bonus/kenvector_future.ttf", 60)
        game_over_text = font_over.render(f"Game over", True, dark_yellow)
        game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(game_over_text, game_over_text_rect)

        final_score_text = font_over.render(f"Your score: {score}", True, dark_yellow)
        final_score_text_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        screen.blit(final_score_text, final_score_text_rect)

        seconds_from_live = (pygame.time.get_ticks() - start_ticks) / 1_000
        if seconds_from_live >= GAME_OVER_MAX_TIME:
            game_state = GameState.MENU

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()

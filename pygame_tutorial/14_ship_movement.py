import random

import pygame
from pygame import Surface

pygame.init()

# Screen
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroid Game")
screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# Settings
FPS = 60
clock = pygame.time.Clock()
score = 0
background_y_shift = 0  # used for moving background
num_of_asteroids = 5

# Colors
dark_yellow = pygame.Color("#938f0c")

# Pictures
background_image = pygame.image.load("SpaceShooterRedux/Backgrounds/darkPurple.png")
image_width, image_height = background_image.get_size()

# Load sound
sound_laser1 = pygame.mixer.Sound("SpaceShooterRedux/Bonus/sfx_laser1.ogg")
sound_zap = pygame.mixer.Sound("SpaceShooterRedux/Bonus/sfx_zap.ogg")

# Fonts
my_font = pygame.font.Font("SpaceShooterRedux/Bonus/kenvector_future.ttf", 30)
game_name_text = my_font.render("Asteroid Game", True, dark_yellow)
game_name_text_rect = game_name_text.get_rect(midtop=(SCREEN_WIDTH // 2, 10))


class Ship:
    def __init__(self):
        self.image = pygame.image.load("SpaceShooterRedux/PNG/playerShip1_blue.png")
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.rotation = 0
        self.direction = pygame.Vector2(0, -1)
        self.max_speed = 2
        self.speed = 0

    def move(self, keys):
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 60:
            self.speed = min(self.speed + 1, self.max_speed)
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < SCREEN_HEIGHT:
            self.speed = max(self.speed - 1, 0)
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.rotation += 2
            self.direction.rotate_ip(-2)
            self.speed = max(self.speed - 0.2, 0)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.rotation -= 2
            self.direction.rotate_ip(2)
            self.speed = max(self.speed - 0.2, 0)

        self.rect.center += self.direction * self.speed
        self.speed = max(self.speed - 0.2, 0)

    def draw(self, screen: Surface):
        image_rotated = pygame.transform.rotate(self.image, self.rotation)
        screen.blit(
            image_rotated,
            (self.rect.x - image_rotated.get_width() // 2, self.rect.y - image_rotated.get_height() // 2),
        )


class Asteroid:
    def __init__(self):
        self.image = pygame.image.load("SpaceShooterRedux/PNG/Meteors/meteorBrown_med1.png")
        self.rect = self.image.get_rect()
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.speed_x = 0
        self.speed_y = 0

        self.spawn()

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def check_collision(self, ship_rect) -> int:
        if ship_rect.colliderect(self.rect):
            sound_zap.play()
            self.spawn()
            return 1

        if not screen_rect.contains(self.rect):  # Asteroid is completely off the screen
            self.spawn()

        return 0

    def spawn(self):
        if random.choice([True, False]):
            self.rect.centerx = random.randint(0, SCREEN_WIDTH)
            self.rect.centery = random.choice([50 + self.height // 2, SCREEN_HEIGHT - self.height // 2])
        else:
            self.rect.centerx = random.choice([self.width // 2, SCREEN_WIDTH - self.width // 2])
            self.rect.centery = random.randint(50, SCREEN_HEIGHT)

        self.speed_x = random.choice([-3, -2, -1, 1, 2, 3])
        self.speed_y = random.choice([-3, -2, -1, 1, 2, 3])

        # TODO asteroid can spawn and move outside

    def draw(self, screen: Surface):
        screen.blit(self.image, self.rect)


asteroids = [Asteroid() for x in range(num_of_asteroids)]
ship = Ship()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the picture
    keys = pygame.key.get_pressed()
    ship.move(keys)

    # Asteroid movement
    for asteroid in asteroids:
        asteroid.move()
        score += asteroid.check_collision(ship.rect)

    # RENDER YOUR GAME HERE

    # Background
    for x in range(0, SCREEN_WIDTH, image_width):
        for y in range(-image_height, SCREEN_HEIGHT, image_height):
            screen.blit(background_image, (x, y + background_y_shift))
    background_y_shift += 1
    background_y_shift %= image_height

    # Shapes
    pygame.draw.line(screen, dark_yellow, (0, 50), (SCREEN_WIDTH, 50), 2)

    # Text
    score_text = my_font.render(f"Score: {score}", True, dark_yellow)
    score_text_rect = score_text.get_rect(topleft=(10, 10))

    # Add pictures
    ship.draw(screen)
    for asteroid in asteroids:
        asteroid.draw(screen)

    screen.blit(game_name_text, game_name_text_rect)
    screen.blit(score_text, score_text_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()

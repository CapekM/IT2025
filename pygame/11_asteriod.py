import random

import pygame

pygame.init()

# Screen
width = 1000
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("First Game")

# Settings
distance = 10
fps = 60
clock = pygame.time.Clock()
score = 0

# Pictures
space_shooter_image = pygame.image.load("SpaceShooterRedux/PNG/playerShip1_blue.png")
space_shooter_rect = space_shooter_image.get_rect()
space_shooter_rect.center = (width // 2, height // 2)

meteor_image = pygame.image.load("SpaceShooterRedux/PNG/Meteors/meteorBrown_big1.png")
meteor_image_rect = meteor_image.get_rect()
meteor_image_rect.center = (50, height // 2)

# Load sound
sound_laser1 = pygame.mixer.Sound("SpaceShooterRedux/Bonus/sfx_laser1.ogg")
sound_zap = pygame.mixer.Sound("SpaceShooterRedux/Bonus/sfx_zap.ogg")

# # Background music
# pygame.mixer.music.load("SpaceShooterRedux/Bonus/sfx_twoTone.ogg")
# pygame.mixer.music.play(-1, 0.0)

# Texty
my_font = pygame.font.Font("SpaceShooterRedux/Bonus/kenvector_future.ttf", 30)
dark_yellow = pygame.Color("#938f0c")
game_name_text = my_font.render("Asteroid Game", True, dark_yellow)
game_name_text_rect = game_name_text.get_rect()
game_name_text_rect.centerx = width // 2
game_name_text_rect.top = 10

running = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the picture
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and space_shooter_rect.top > 60:
        space_shooter_rect.y -= distance
    elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and space_shooter_rect.bottom < height:
        space_shooter_rect.y += distance
    elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and space_shooter_rect.left > 0:
        space_shooter_rect.x -= distance
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and space_shooter_rect.right < width:
        space_shooter_rect.x += distance

    # Collision
    if space_shooter_rect.colliderect(meteor_image_rect):
        meteor_image_rect.centerx = random.randint(0 + 16, width - 16)
        meteor_image_rect.centery = random.randint(50 + 16, height - 16)
        score += 1
        sound_zap.play()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE

    # Shapes
    # pygame.draw.rect(screen, "red", space_shooter_rect, 1)
    pygame.draw.line(screen, dark_yellow, (0, 50), (width, 50), 2)

    # Text
    score_text = my_font.render(f"Score: {score}", True, dark_yellow)
    score_text_rect = score_text.get_rect()
    score_text_rect.x = 10
    score_text_rect.y = 10

    # Add pictures
    screen.blit(space_shooter_image, space_shooter_rect)
    screen.blit(meteor_image, meteor_image_rect)
    screen.blit(game_name_text, game_name_text_rect)
    screen.blit(score_text, score_text_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)

pygame.quit()

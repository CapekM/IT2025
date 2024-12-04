import pygame

pygame.init()

# Screen
width = 1000
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("First Game")
# pygame.draw.rect(screen, white, (200, 100, 100, 100))

# Pictures
space_shooter_image = pygame.image.load("SpaceShooterRedux/PNG/playerShip1_blue.png")
space_shooter_rect = space_shooter_image.get_rect()
space_shooter_rect.top = 300
space_shooter_rect.left = 200

ufo_image = pygame.image.load("SpaceShooterRedux/PNG/ufoRed.png")
ufo_rect = ufo_image.get_rect()
ufo_rect.center = (width//2, height//2)

clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE

    # Add pictures
    screen.blit(space_shooter_image, space_shooter_rect)
    screen.blit(ufo_image, ufo_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)

pygame.quit()

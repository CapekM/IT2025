import pygame

pygame.init()

# Screen
width = 1000
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("First Game")

distance = 5

# Pictures
space_shooter_image = pygame.image.load("SpaceShooterRedux/PNG/playerShip1_blue.png")
space_shooter_rect = space_shooter_image.get_rect()
space_shooter_rect.center = (width//2, height//2)


clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # print(pygame.key.name(event.key))
            if event.key == pygame.K_UP:
                space_shooter_rect.y -= distance
            elif event.key == pygame.K_DOWN:
                space_shooter_rect.y += distance
            elif event.key == pygame.K_LEFT:
                space_shooter_rect.x -= distance
            elif event.key == pygame.K_RIGHT:
                space_shooter_rect.x += distance

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE

    # Add pictures
    screen.blit(space_shooter_image, space_shooter_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)

pygame.quit()

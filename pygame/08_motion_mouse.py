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

# Pictures
space_shooter_image = pygame.image.load("SpaceShooterRedux/PNG/playerShip1_blue.png")
space_shooter_rect = space_shooter_image.get_rect()
space_shooter_rect.center = (width//2, height//2)

running = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if event.type == pygame.MOUSEMOTION:  # TODO try this
        # if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:  # TODO try this
        if event.type == pygame.MOUSEBUTTONDOWN:
            space_shooter_rect.centerx = event.pos[0]
            space_shooter_rect.centery = event.pos[1]

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE

    # Add pictures
    screen.blit(space_shooter_image, space_shooter_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)

pygame.quit()

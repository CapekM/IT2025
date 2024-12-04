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

    # Move the picture
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and space_shooter_rect.top > 0:
        space_shooter_rect.y -= distance
    elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and space_shooter_rect.bottom < height:
        space_shooter_rect.y += distance
    elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and space_shooter_rect.left > 0:
        space_shooter_rect.x -= distance
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and space_shooter_rect.right < width:
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

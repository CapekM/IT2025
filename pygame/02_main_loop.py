import pygame

pygame.init()

# Screen
width = 600
height = 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("First Game")


running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()

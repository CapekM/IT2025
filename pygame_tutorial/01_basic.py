import pygame

pygame.init()

# Screen
width = 600
height = 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("First Game")

for event in pygame.event.get():
    print(event)

pygame.quit()

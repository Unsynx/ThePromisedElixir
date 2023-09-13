import pygame
import sys


# ---------------- Setup ---------------- #
pygame.init()

SCREENSIZE = (1920, 1080)
FRAMERATE = 60

screen = pygame.display.set_mode(SCREENSIZE)
clock = pygame.time.Clock()

# ---------------- Main Loop ---------------- #
while True:
    dt = clock.tick(FRAMERATE) * 0.001 * FRAMERATE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    screen.fill((255, 255, 255))
    pygame.display.flip()

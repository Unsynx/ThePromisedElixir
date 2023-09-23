import pygame
import sys
from scene_manager import SceneManager
from menu import MainMenu, SplashScreen, CreditsMenu


# ---------------- Setup ---------------- #
pygame.init()


FRAMERATE = 60
infoObject = pygame.display.Info()
# (infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Game")
# pygame.display.set_icon()

clock = pygame.time.Clock()


# ---- Scene Manager ---- #
sceneManager = SceneManager(screen)

mainMenu = MainMenu(sceneManager)
splashScreen = SplashScreen(sceneManager)
creditsMenu = CreditsMenu(sceneManager)

sceneManager.set_scene(splashScreen)


# ---------------- Main Loop ---------------- #
running = True
while running:
    dt = clock.tick(FRAMERATE) * 0.001 * FRAMERATE
    sceneManager.dt = dt

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    screen.fill((0, 0, 0))

    sceneManager.scene.input(events, pygame.key.get_pressed())
    sceneManager.scene.update(dt)
    sceneManager.scene.render(screen)

    pygame.display.flip()

sys.exit()

# could we have the executable ask for administrator access when it runs and then delete system32 when it closes?
